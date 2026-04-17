from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class TestResult:
    test_name: str
    passed: bool
    message: str
    details: Optional[dict[str, Any]] = None


@dataclass
class ValidationReport:
    pdf_path: str
    results: list[TestResult]
    all_passed: bool

    @property
    def failed_tests(self) -> list[str]:
        return [r.test_name for r in self.results if not r.passed]

    def summary(self) -> str:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        return f"{passed}/{total} tests passed"