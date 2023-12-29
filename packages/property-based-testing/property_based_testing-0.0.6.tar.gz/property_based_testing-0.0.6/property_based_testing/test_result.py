from dataclasses import dataclass


@dataclass(frozen=True)
class Failure:
    message: str | None = None


@dataclass(frozen=True)
class Success:
    pass


@dataclass(frozen=True)
class PropertyTestResult:
    result: Failure | Success
