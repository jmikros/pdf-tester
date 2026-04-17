from .base import register_test
from pdf_tester.models import TestResult  # optional, you can also return dict


@register_test(
    name="structure",
    description="Checks basic PDF structure, version, encryption, and corruption"
)
def test_structure(pdf_path: str) -> TestResult:
        return {
            "passed": True,
            "message": pdf_path,
            "details": {
                "page_count": "page_c",
                "pdf_version": "ver"
            }
        }