import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src" / "domain_3_publish"))

from publish_compiler import (  # noqa: E402
    AttachmentTier,
    PlatformConfig,
    PublishCandidate,
    PublishCompiler,
    SupersetProfile,
    load_contract,
)
from workflow import ContentBank, ContentItem, ControlTower, ItemStatus, Review, StagingArea, transfer_to_staging  # noqa: E402


class Mark1ComplianceTests(unittest.TestCase):
    def setUp(self):
        self.compiler = PublishCompiler(PlatformConfig("test", SupersetProfile.MICRO_POST, 280, False))
        self.candidate = PublishCandidate("id-1", "title", "Body", "mythos")
        self.approved_review = Review(
            "demo-approval-001", "approved",
            {"sensationalism_detected": False, "lighthearted_humor_detected": False},
            "not_evaluated",
        )

    def test_canonical_yaml_contract_loads_and_fsr_remains_pending(self):
        review, candidate = load_contract(
            REPO_ROOT / "src" / "domain_3_publish" / "agent_gatekeeper.yml"
        )
        self.assertEqual(review["fsr"]["status"], "not_evaluated")
        self.assertEqual(candidate["candidate_id"], "sample-yuggoth-001")
        self.assertIsNone(review["prohibited_conventions_check"]["sensationalism_detected"])

    def test_unapproved_or_unknown_safety_flags_hold_at_control_tower(self):
        tower = ControlTower()
        held = tower.review(Review("demo", "pending", {"sensationalism_detected": None}))
        self.assertFalse(held.compile_allowed)
        self.assertFalse(held.publish_allowed)

    def test_approved_review_allows_draft_compile_but_fsr_blocks_release(self):
        result = self.compiler.compile(self.candidate, self.approved_review)
        governance = result["sidecar_manifest"]["governance"]
        self.assertTrue(governance["compile_allowed"])
        self.assertFalse(governance["publish_allowed"])
        self.assertEqual(governance["status"], "compile_eligible")

    def test_missing_media_is_not_fabricated_or_claimed_valid(self):
        candidate = PublishCandidate("id-1", "title", "Body", "mythos", AttachmentTier.FANCY)
        result = self.compiler.compile(candidate, self.approved_review)
        self.assertIsNone(result["media_payload"])
        status = result["sidecar_manifest"]["attachment_status"]
        self.assertTrue(status["requested"])
        self.assertFalse(status["provided"])
        self.assertEqual(status["validation_status"], "not_implemented")

    def test_empty_mianzi_selection_does_not_credit_registry(self):
        result = self.compiler.compile(self.candidate, self.approved_review)
        stub = result["sidecar_manifest"]["mianzi_attribution_stub"]
        self.assertEqual(stub["selected_tool_ids"], [])

    def test_unknown_mianzi_ids_are_reported_not_invented(self):
        candidate = PublishCandidate("id-1", "title", "Body", "mythos", tool_ids=["unknown"])
        result = self.compiler.compile(candidate, self.approved_review)
        self.assertEqual(result["sidecar_manifest"]["mianzi_attribution_stub"]["unresolved_tool_ids"], ["unknown"])

    def test_content_bank_requires_explicit_transfer_to_staging(self):
        bank = ContentBank()
        staging = StagingArea()
        bank.preload(ContentItem("bank-1", {"text": "draft"}, "curated"))
        self.assertEqual(bank.get("bank-1").status, ItemStatus.BANKED)
        self.assertEqual(staging.items(), [])
        staged = transfer_to_staging(bank, staging, "bank-1")
        self.assertEqual(staged.status, ItemStatus.STAGED)
        self.assertIn("content_bank:bank-1", staged.provenance)


if __name__ == "__main__":
    unittest.main()
