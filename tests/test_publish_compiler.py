import subprocess
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


class PublishCompilerTests(unittest.TestCase):
    def setUp(self):
        self.compiler = PublishCompiler(
            PlatformConfig("test", SupersetProfile.MICRO_POST, 280, include_domain_link=False)
        )
        self.review = Review(
            approval_id="demo-approval-test",
            status="approved",
            prohibited_conventions_check={
                "sensationalism_detected": False,
                "lighthearted_humor_detected": False,
            },
            fsr_status="not_evaluated",
        )

    def compile_candidate(self, max_chars: int, **candidate_fields):
        compiler = PublishCompiler(
            PlatformConfig("test", SupersetProfile.MICRO_POST, max_chars, include_domain_link=False)
        )
        candidate = PublishCandidate(
            candidate_id="test-1",
            title="Test",
            body_text="Body",
            domain_category="mythos",
            **candidate_fields,
        )
        return compiler.compile(candidate, self.review)

    def test_exact_cap_includes_footer_and_tag_separators(self):
        result = self.compile_candidate(
            52,
            partner_tags=["partner"],
            primary_hashtags=["one", "two"],
        )
        payload = result["atomic_text_base"]
        self.assertLessEqual(len(payload), 52)
        self.assertEqual(
            result["sidecar_manifest"]["budget_interface"]["total_payload_chars"],
            len(payload),
        )

    def test_omits_partner_footer_when_footer_alone_wont_fit(self):
        result = self.compile_candidate(10, partner_tags=["a-very-long-partner-tag"])
        self.assertEqual(result["atomic_text_base"], "Body")
        self.assertEqual(
            result["sidecar_manifest"]["execution_status"]["quota_status"],
            "body_only",
        )

    def test_reports_body_over_cap_without_truncating_it(self):
        result = self.compile_candidate(2)
        self.assertEqual(result["atomic_text_base"], "Body")
        self.assertEqual(
            result["sidecar_manifest"]["execution_status"]["quota_status"],
            "body_exceeds_cap",
        )

    def test_missing_attachment_is_not_reported_as_provided_or_validated(self):
        result = self.compile_candidate(100, attachment_tier=AttachmentTier.FANCY)
        status = result["sidecar_manifest"]["attachment_status"]
        self.assertFalse(status["provided"])
        self.assertEqual(status["validation_status"], "not_implemented")

    def test_command_line_module_imports_and_honestly_holds_pending_fixture(self):
        result = subprocess.run(
            [sys.executable, "-m", "src.domain_3_publish.publish_compiler"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("candidate held by Control Tower", result.stdout)


class Mark1WorkflowTests(unittest.TestCase):
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
        decision = ControlTower().review(self_review())
        self.assertTrue(decision.compile_allowed)
        self.assertFalse(decision.publish_allowed)
        self.assertEqual(decision.status, "compile_eligible")

    def test_empty_mianzi_selection_does_not_credit_registry(self):
        result = self._compile()
        stub = result["sidecar_manifest"]["mianzi_attribution_stub"]
        self.assertEqual(stub["selected_tool_ids"], [])

    def test_unknown_mianzi_ids_are_reported_not_invented(self):
        result = self._compile(tool_ids=["unknown"])
        self.assertEqual(
            result["sidecar_manifest"]["mianzi_attribution_stub"]["unresolved_tool_ids"],
            ["unknown"],
        )

    def test_content_bank_requires_explicit_transfer_to_staging(self):
        bank = ContentBank()
        staging = StagingArea()
        bank.preload(ContentItem("bank-1", {"text": "draft"}, "curated"))
        self.assertEqual(bank.get("bank-1").status, ItemStatus.BANKED)
        self.assertEqual(staging.items(), [])
        staged = transfer_to_staging(bank, staging, "bank-1")
        self.assertEqual(staged.status, ItemStatus.STAGED)
        self.assertIn("content_bank:bank-1", staged.provenance)

    def _compile(self, **candidate_fields):
        compiler = PublishCompiler(
            PlatformConfig("test", SupersetProfile.MICRO_POST, 280, include_domain_link=False)
        )
        candidate = PublishCandidate("id-1", "title", "Body", "mythos", **candidate_fields)
        return compiler.compile(candidate, self_review())


def self_review():
    return Review(
        "demo-approval-001",
        "approved",
        {"sensationalism_detected": False, "lighthearted_humor_detected": False},
        "not_evaluated",
    )


if __name__ == "__main__":
    unittest.main()
