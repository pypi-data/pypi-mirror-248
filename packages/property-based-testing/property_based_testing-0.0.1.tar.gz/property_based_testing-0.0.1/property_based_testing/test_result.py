from dataclasses import dataclass


@dataclass(frozen=True)
class Failure:
    message: str | None = None


@dataclass(frozen=True)
class Success:
    pass


PropertyTestResult = Failure | Success
