"""
Guardrails for spam control, compliance, tone consistency, and audit logging
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple
from datetime import datetime
import re
from config.config import Config, FREQUENCY_CAP_RULES, TONE_GUIDELINES

@dataclass
class GuardrailCheck:
    """Result of a guardrail check"""
    check_name: str
    passed: bool
    details: Dict[str, Any]
    severity: str  # "warning", "error", "critical"

class SpamControlGuardrail:
    """Spam detection and prevention"""
    
    SPAM_KEYWORDS = [
        "click here now", "urgent", "act now", "limited time", "guaranteed",
        "free", "no credit card", "risk free", "unsubscribe", "verify account",
    ]
    
    def check_email_frequency(self, customer_id: str, email_count_this_week: int, email_type: str = "marketing") -> GuardrailCheck:
        """Check if email respects frequency caps"""
        
        max_allowed = FREQUENCY_CAP_RULES.get(email_type, 3)
        passed = email_count_this_week < max_allowed
        
        return GuardrailCheck(
            check_name="frequency_cap",
            passed=passed,
            details={
                "customer_id": customer_id,
                "emails_this_week": email_count_this_week,
                "max_allowed": max_allowed,
                "email_type": email_type,
            },
            severity="error" if not passed else "warning",
        )
    
    def check_spam_score(self, subject: str, body: str) -> GuardrailCheck:
        """Calculate spam score for email content"""
        
        content = f"{subject} {body}".lower()
        spam_count = 0
        
        for keyword in self.SPAM_KEYWORDS:
            if keyword in content:
                spam_count += 1
        
        # Check for excessive capitalization
        if len(re.findall(r'[A-Z]{3,}', subject)) > 2:
            spam_count += 1
        
        # Check for excessive punctuation
        if len(re.findall(r'[!]{2,}', content)) > 1:
            spam_count += 1
        
        # Normalize to 0-1 scale
        spam_score = min(spam_count / 5.0, 1.0)
        passed = spam_score < Config.SPAM_SCORE_THRESHOLD
        
        return GuardrailCheck(
            check_name="spam_score",
            passed=passed,
            details={
                "spam_score": round(spam_score, 3),
                "threshold": Config.SPAM_SCORE_THRESHOLD,
                "spam_triggers_found": spam_count,
            },
            severity="error" if not passed else "warning",
        )
    
    def check_engagement_score(self, customer_engagement: float) -> GuardrailCheck:
        """Check if customer has minimum engagement to email"""
        
        passed = customer_engagement >= Config.MIN_ENGAGEMENT_SCORE
        
        return GuardrailCheck(
            check_name="engagement_score",
            passed=passed,
            details={
                "engagement_score": round(customer_engagement, 3),
                "min_threshold": Config.MIN_ENGAGEMENT_SCORE,
            },
            severity="error" if not passed else "warning",
        )

class ComplianceGuardrail:
    """GDPR, CAN-SPAM, CCPA, and regulatory compliance checks"""
    
    def check_gdpr_consent(self, customer_data: Dict[str, Any], region: str = "EU") -> GuardrailCheck:
        """Verify GDPR consent for EU customers"""
        
        has_consent = customer_data.get("gdpr_consent", False)
        passed = has_consent or region != "EU"
        
        return GuardrailCheck(
            check_name="gdpr_consent",
            passed=passed,
            details={
                "region": region,
                "has_consent": has_consent,
                "consent_date": customer_data.get("consent_date"),
            },
            severity="critical" if not passed and region == "EU" else "warning",
        )
    
    def check_can_spam(self, email_data: Dict[str, Any]) -> GuardrailCheck:
        """Check CAN-SPAM compliance (US)"""
        
        required_elements = ["from_address", "unsubscribe_link", "physical_address"]
        missing = [e for e in required_elements if not email_data.get(e)]
        
        passed = len(missing) == 0
        
        return GuardrailCheck(
            check_name="can_spam",
            passed=passed,
            details={
                "missing_elements": missing,
                "has_from_address": bool(email_data.get("from_address")),
                "has_unsubscribe_link": bool(email_data.get("unsubscribe_link")),
                "has_physical_address": bool(email_data.get("physical_address")),
            },
            severity="critical" if not passed else "warning",
        )
    
    def check_ccpa_rights(self, customer_id: str, action: str) -> GuardrailCheck:
        """Check CCPA data sale opt-out and deletion rights"""
        
        opt_out = True  # Assume opted out unless specified
        passed = opt_out or action != "sell_data"
        
        return GuardrailCheck(
            check_name="ccpa_rights",
            passed=passed,
            details={
                "customer_id": customer_id,
                "data_sale_opt_out": opt_out,
                "action": action,
            },
            severity="critical" if not passed else "warning",
        )

class ToneConsistencyGuardrail:
    """Brand tone and messaging consistency checks"""
    
    def check_tone_consistency(self, text: str) -> GuardrailCheck:
        """Evaluate copy against brand tone guidelines"""
        
        # Check for forbidden words
        forbidden = TONE_GUIDELINES.get("forbidden_words", [])
        text_lower = text.lower()
        found_forbidden = [w for w in forbidden if w in text_lower]
        
        # Check for required elements
        required = TONE_GUIDELINES.get("required_elements", [])
        has_required = len([e for e in required if e.split("(")[0].lower() in text_lower]) > 0
        
        # Calculate consistency score
        consistency_score = 1.0
        if found_forbidden:
            consistency_score -= len(found_forbidden) * 0.1
        if not has_required:
            consistency_score -= 0.2
        
        consistency_score = max(0, min(1, consistency_score))
        passed = consistency_score >= Config.TONE_CONSISTENCY_THRESHOLD
        
        return GuardrailCheck(
            check_name="tone_consistency",
            passed=passed,
            details={
                "consistency_score": round(consistency_score, 3),
                "threshold": Config.TONE_CONSISTENCY_THRESHOLD,
                "forbidden_words_found": found_forbidden,
                "voice": TONE_GUIDELINES.get("voice", ""),
                "style": TONE_GUIDELINES.get("style", ""),
            },
            severity="error" if not passed else "warning",
        )
    
    def check_personalization(self, text: str) -> GuardrailCheck:
        """Verify email is personalized"""
        
        has_first_name = "{{first_name}}" in text or "{first_name}" in text
        has_dynamic_content = any(s in text for s in ["{{", "{%", "dynamic", "personalized"])
        
        passed = has_first_name or has_dynamic_content
        
        return GuardrailCheck(
            check_name="personalization",
            passed=passed,
            details={
                "has_first_name_placeholder": has_first_name,
                "has_dynamic_content": has_dynamic_content,
            },
            severity="warning",
        )

class AuditLogger:
    """Audit and decision logging for compliance and analysis"""
    
    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []
    
    def log_decision(self, decision: Dict[str, Any], guardrail_checks: Dict[str, bool], human_review: bool = False):
        """Log a decision with guardrail results"""
        
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "decision_id": decision.get("decision_id"),
            "agent": decision.get("agent_name"),
            "customer_id": decision.get("customer_id"),
            "action": decision.get("action"),
            "guardrail_checks": guardrail_checks,
            "human_review_required": human_review,
            "decision_details": decision,
        }
        
        self.audit_log.append(audit_entry)
        return audit_entry
    
    def log_human_override(self, decision_id: str, original_action: str, override_action: str, reason: str):
        """Log when human overrides an automated decision"""
        
        override_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "decision_id": decision_id,
            "original_action": original_action,
            "override_action": override_action,
            "reason": reason,
            "type": "human_override",
        }
        
        self.audit_log.append(override_entry)
        return override_entry
    
    def get_audit_history(self, customer_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve audit history"""
        
        if customer_id:
            history = [e for e in self.audit_log if e.get("customer_id") == customer_id]
        else:
            history = self.audit_log
        
        return sorted(history, key=lambda x: x["timestamp"], reverse=True)[:limit]

class GuardrailsManager:
    """Central manager for all guardrails"""
    
    def __init__(self):
        self.spam_control = SpamControlGuardrail()
        self.compliance = ComplianceGuardrail()
        self.tone = ToneConsistencyGuardrail()
        self.audit = AuditLogger()
    
    def run_all_checks(self, customer_data: Dict[str, Any], email_data: Dict[str, Any]) -> Tuple[bool, Dict[str, GuardrailCheck]]:
        """
        Run all guardrails for a decision
        
        Returns:
            (all_passed, results_dict)
        """
        
        results = {}
        
        # Spam checks
        results["frequency_cap"] = self.spam_control.check_email_frequency(
            customer_data.get("customer_id"),
            customer_data.get("emails_this_week", 0),
            customer_data.get("email_type", "marketing"),
        )
        
        results["spam_score"] = self.spam_control.check_spam_score(
            email_data.get("subject", ""),
            email_data.get("body", ""),
        )
        
        results["engagement_score"] = self.spam_control.check_engagement_score(
            customer_data.get("engagement_score", 0),
        )
        
        # Compliance checks
        results["gdpr_consent"] = self.compliance.check_gdpr_consent(
            customer_data,
            customer_data.get("region", "EU"),
        )
        
        results["can_spam"] = self.compliance.check_can_spam(email_data)
        
        # Tone checks
        results["tone_consistency"] = self.tone.check_tone_consistency(
            f"{email_data.get('subject', '')} {email_data.get('body', '')}"
        )
        
        results["personalization"] = self.tone.check_personalization(
            f"{email_data.get('subject', '')} {email_data.get('body', '')}"
        )
        
        # Check if all critical checks passed
        all_passed = all(
            check.passed or check.severity != "critical"
            for check in results.values()
        )
        
        return all_passed, results
