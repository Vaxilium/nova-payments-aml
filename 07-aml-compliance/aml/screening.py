"""Screening difuso contra listas ficticias de sanciones, PEP e internas."""

from __future__ import annotations

import sqlite3
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from difflib import SequenceMatcher
from typing import Iterable

from . import config


@dataclass(frozen=True)
class WatchlistEntry:
    list_type: str
    list_id: str
    name: str
    aliases: tuple[str, ...] = ()
    country_code: str | None = None
    program: str | None = None


@dataclass(frozen=True)
class ScreeningMatch:
    list_type: str
    list_id: str
    matched_name: str
    score: float
    program: str | None = None


@dataclass(frozen=True)
class ScreeningOutcome:
    subject_name: str
    normalized_name: str
    decision: str
    score: float
    matches: list[ScreeningMatch] = field(default_factory=list)

    @property
    def best_match(self) -> ScreeningMatch | None:
        return self.matches[0] if self.matches else None


def normalize_name(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.upper()
    cleaned = []
    for char in text:
        cleaned.append(char if char.isalnum() else " ")
    tokens = [token for token in "".join(cleaned).split() if token]
    suffixes = {"SA", "S", "A", "LTDA", "SRL", "SOCIEDAD", "ANONIMA"}
    while tokens and tokens[-1] in suffixes and len(tokens) > 1:
        tokens.pop()
    return " ".join(tokens)


def _jaro(left: str, right: str) -> float:
    if left == right:
        return 1.0
    if not left or not right:
        return 0.0
    window = max(len(left), len(right)) // 2 - 1
    window = max(0, window)
    left_matches = [False] * len(left)
    right_matches = [False] * len(right)
    matches = 0
    for index, char in enumerate(left):
        start = max(0, index - window)
        end = min(index + window + 1, len(right))
        for other in range(start, end):
            if right_matches[other] or char != right[other]:
                continue
            left_matches[index] = True
            right_matches[other] = True
            matches += 1
            break
    if matches == 0:
        return 0.0
    left_sequence = [left[i] for i in range(len(left)) if left_matches[i]]
    right_sequence = [right[i] for i in range(len(right)) if right_matches[i]]
    transpositions = sum(1 for a, b in zip(left_sequence, right_sequence) if a != b) / 2
    return (
        matches / len(left)
        + matches / len(right)
        + (matches - transpositions) / matches
    ) / 3


def jaro_winkler(left: str, right: str) -> float:
    score = _jaro(left, right)
    prefix = 0
    for a, b in zip(left[:4], right[:4]):
        if a != b:
            break
        prefix += 1
    return min(1.0, score + prefix * 0.1 * (1 - score))


def _token_sort(value: str) -> str:
    return " ".join(sorted(value.split()))


def name_similarity(left: str, right: str) -> float:
    a = normalize_name(left)
    b = normalize_name(right)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    jw = jaro_winkler(a, b)
    token = SequenceMatcher(None, _token_sort(a), _token_sort(b)).ratio()
    return max(jw, token)


def load_watchlist(conn: sqlite3.Connection, list_type: str | None = None) -> list[WatchlistEntry]:
    query = """
        SELECT list_type, list_id, name, aliases, country_code, program
        FROM aml_watchlist
        WHERE is_active = 1
    """
    params: tuple[object, ...] = ()
    if list_type:
        query += " AND list_type = ?"
        params = (list_type.upper(),)
    query += " ORDER BY list_type, list_id"
    entries = []
    for row in conn.execute(query, params):
        aliases = tuple(part.strip() for part in (row["aliases"] or "").split("|") if part.strip())
        entries.append(
            WatchlistEntry(
                list_type=row["list_type"],
                list_id=row["list_id"],
                name=row["name"],
                aliases=aliases,
                country_code=row["country_code"],
                program=row["program"],
            )
        )
    return entries


def decision_for_score(score: float) -> str:
    if score >= config.SCREENING_AUTO_BLOCK:
        return "BLOCK"
    if score >= config.SCREENING_MANUAL_REVIEW:
        return "REVIEW"
    return "NO_MATCH"


def screen_name(
    name: str,
    entries: Iterable[WatchlistEntry],
    *,
    minimum: float = config.SCREENING_MINIMUM,
) -> ScreeningOutcome:
    normalized = normalize_name(name)
    matches: list[ScreeningMatch] = []
    for entry in entries:
        candidates = (entry.name, *entry.aliases)
        best_name = entry.name
        best_score = 0.0
        for candidate in candidates:
            score = name_similarity(name, candidate)
            if score > best_score:
                best_score = score
                best_name = candidate
        if best_score >= minimum:
            matches.append(
                ScreeningMatch(
                    list_type=entry.list_type,
                    list_id=entry.list_id,
                    matched_name=best_name,
                    score=round(best_score, 4),
                    program=entry.program,
                )
            )
    matches.sort(key=lambda item: (-item.score, item.list_type, item.list_id))
    best = matches[0].score if matches else 0.0
    return ScreeningOutcome(
        subject_name=name,
        normalized_name=normalized,
        decision=decision_for_score(best),
        score=round(best, 4),
        matches=matches,
    )


def screen_name_in_db(
    conn: sqlite3.Connection,
    name: str,
    *,
    list_type: str | None = None,
    minimum: float = config.SCREENING_MINIMUM,
) -> ScreeningOutcome:
    return screen_name(name, load_watchlist(conn, list_type), minimum=minimum)


def record_screening(
    conn: sqlite3.Connection,
    outcome: ScreeningOutcome,
    *,
    payment_ref: str | None = None,
    threshold: float = config.SCREENING_AUTO_BLOCK,
    created_at: str | None = None,
) -> int:
    best = outcome.best_match
    timestamp = created_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    cursor = conn.execute(
        """
        INSERT INTO aml_screening_results
            (subject_name, normalized_name, list_type, list_id, matched_name,
             score, threshold, decision, payment_ref, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            outcome.subject_name,
            outcome.normalized_name,
            best.list_type if best else None,
            best.list_id if best else None,
            best.matched_name if best else None,
            outcome.score,
            threshold,
            outcome.decision,
            payment_ref,
            timestamp,
        ),
    )
    conn.commit()
    return int(cursor.lastrowid)


__all__ = [
    "ScreeningMatch",
    "ScreeningOutcome",
    "WatchlistEntry",
    "decision_for_score",
    "jaro_winkler",
    "load_watchlist",
    "name_similarity",
    "normalize_name",
    "record_screening",
    "screen_name",
    "screen_name_in_db",
]
