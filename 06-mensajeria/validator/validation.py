"""Resultados de validación reutilizables por validador y simuladores."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ValidationIssue:
    """Un hallazgo concreto de validación."""

    code: str
    field: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "field": self.field, "message": self.message}


@dataclass
class ValidationResult:
    """Acumula hallazgos sin lanzar excepciones hasta que el llamador lo pida."""

    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.issues

    @property
    def is_valid(self) -> bool:
        return self.valid

    def add(self, code: str, field: str, message: str) -> None:
        self.issues.append(ValidationIssue(code=code, field=field, message=message))

    def merge(self, other: "ValidationResult") -> None:
        self.issues.extend(other.issues)

    def raise_if_invalid(self) -> None:
        if self.issues:
            raise MessageValidationError(self.issues)

    def as_dict(self) -> dict[str, object]:
        return {"valid": self.valid, "issues": [issue.as_dict() for issue in self.issues]}


class MessageValidationError(ValueError):
    """Error de validación con la lista completa de hallazgos."""

    def __init__(self, issues: list[ValidationIssue]) -> None:
        self.issues = list(issues)
        summary = "; ".join(f"{issue.field}: {issue.message}" for issue in self.issues[:5])
        if len(self.issues) > 5:
            summary += f"; ... ({len(self.issues)} hallazgos)"
        super().__init__(summary or "Mensaje inválido")
