import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src" / "domain_3_publish"))

from publish_compiler import load_contract  # noqa: E402


class ContractValidationTests(unittest.TestCase):
    def load_text(self, text: str):
        with tempfile.TemporaryDirectory() as directory:
            contract_path = Path(directory) / "contract.yml"
            contract_path.write_text(text, encoding="utf-8")
            return load_contract(contract_path)

    def test_rejects_non_mapping_root(self):
        with self.assertRaisesRegex(ValueError, "root must be a mapping"):
            self.load_text("- not-a-mapping\n")

    def test_rejects_missing_candidate_fields(self):
        with self.assertRaisesRegex(ValueError, "candidate_payload missing required keys"):
            self.load_text(
                "gatekeeper_review:\n"
                "  prohibited_conventions_check: {}\n"
                "  fsr:\n"
                "    status: not_evaluated\n"
                "candidate_payload: {}\n"
            )

    def test_rejects_unknown_fsr_status(self):
        with self.assertRaisesRegex(ValueError, "fsr.status must be"):
            self.load_text(
                "gatekeeper_review:\n"
                "  prohibited_conventions_check: {}\n"
                "  fsr:\n"
                "    status: probably-fine\n"
                "candidate_payload:\n"
                "  candidate_id: id\n"
                "  title: title\n"
                "  body_text: body\n"
                "  domain_category: mythos\n"
                "  attachment_tier: atomic_text\n"
            )


if __name__ == "__main__":
    unittest.main()
