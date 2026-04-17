from pathlib import Path
from typing import Optional
from .models import TestResult, ValidationReport
from .tests.base import TESTS, get_test_func, get_all_test_names


def parse_requested_tests(tests_str: Optional[str]) -> list[str]:
    """Parse --tests 'structure,fonts' into list of test names"""
    if not tests_str:
        return get_all_test_names()  # run all by default

    requested = [t.strip().lower() for t in tests_str.split(",")]
    selected = []

    for req in requested:
        match = get_test_func(req)
        if match:
            selected.append(match[0])
        else:
            print(f"Warning: Test '{req}' not found. Skipping.")

    return selected if selected else get_all_test_names()


def run_tests_on_pdf(
    pdf_path: str | Path,
    tests_str: Optional[str] = None,
) -> ValidationReport:
    """Run selected (or all) tests on a single PDF"""
    pdf_path = Path(pdf_path)
    selected_names = parse_requested_tests(tests_str)
    results: list[TestResult] = []

    for name, _, func in TESTS:
        if name in selected_names:
            try:
                raw_result = func(str(pdf_path))
                # Support both old and new TestResult style
                if isinstance(raw_result, dict):
                    result = TestResult(test_name=name, **raw_result)
                else:
                    result = TestResult(test_name=name, **raw_result.__dict__)
            except Exception as e:
                result = TestResult(
                    test_name=name,
                    passed=False,
                    message=f"Test crashed: {e}"
                )
            results.append(result)

    return ValidationReport(
        pdf_path=str(pdf_path),
        results=results,
        all_passed=all(r.passed for r in results)
    )


def run_batch(directory: str | Path, tests_str: Optional[str] = None):
    """Run on multiple PDFs (can be extended later)"""
    directory = Path(directory)
    pdf_files = list(directory.glob("**/*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF(s) in {directory}")
    reports = []
    
    for pdf in pdf_files:
        report = run_tests_on_pdf(pdf, tests_str)
        reports.append(report)
        print(f"✓ {pdf.name} → {report.summary()}")
    
    return reports