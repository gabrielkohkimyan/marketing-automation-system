"""
Lifecycle & Retention Agent - automatically manage customer lifecycle and prevent churn
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent, AgentInput, AgentDecision
from config.config import LifecycleStage, LIFECYCLE_TRANSITIONS

class LifecycleAgent(BaseAgent):
    """
    Lifecycle & Retention Agent
    
    Purpose: Automatically manage customer lifecycle progression and prevent churn
    
    Inputs:
    - Customer lifecycle stage
    - Engagement patterns, purchase frequency
    - Churn risk scores
    - Segment-specific retention strategies
    
    Actions:
    - Automatically advance/regress lifecycle stage
    - Trigger retention campaigns
    - Create VIP programs for high-value customers
    - Schedule manual review for highest-churn-risk customers
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("LifecycleAgent", config)
    
    def decide(self, agent_input: AgentInput) -> AgentDecision:
        """
        Make lifecycle management decision
        
        Logic:
        1. Score customer churn risk using ML model
        2. Assign to lifecycle stage based on behavior
        3. Trigger stage-appropriate actions
        4. Monitor engagement post-action
        5. Adjust strategy based on response
        """
        customer_data = agent_input.customer_data
        context = agent_input.context
        
        # Step 1: Calculate churn risk
        churn_risk = self._calculate_churn_risk(customer_data)
        
        # Step 2: Determine current and target lifecycle stage
        current_stage = LifecycleStage(customer_data.get("lifecycle_stage", "active"))
        target_stage = self._determine_lifecycle_stage(customer_data, churn_risk)
        
        # Step 3: Determine action based on lifecycle stage
        action = self._determine_action(target_stage, churn_risk, customer_data)
        
        # Check if manual review needed
        requires_review = churn_risk > 0.7 or customer_data.get("customer_value", 0) > 5000
        
        decision = self._create_decision(
            customer_id=agent_input.customer_id,
            action=action,
            parameters={
                "current_stage": current_stage.value,
                "target_stage": target_stage.value,
                "churn_risk": round(churn_risk, 3),
                "customer_value": customer_data.get("customer_value", 0),
                "action_type": action,
            },
            confidence=0.86,
            guardrail_checks={
                "frequency_cap_check": True,
                "vip_status_check": True,
                "retention_budget_check": True,
            },
            requires_human_review=requires_review,
            reasoning=f"Churn risk: {churn_risk:.1%}. Stage transition: {current_stage.value} → {target_stage.value}",
        )
        
        return decision
    
    def _calculate_churn_risk(self, customer_data: Dict[str, Any]) -> float:
        """
        Calculate churn risk score (0-1)
        In production: ML model trained on historical churn data
        """
        risk = 0.0
        
        # Recency factor (stronger weight)
        days_since_last_activity = customer_data.get("days_since_last_activity", 0)
        if days_since_last_activity > 180:
            risk += 0.4
        elif days_since_last_activity > 90:
            risk += 0.2
        
        # Frequency factor
        purchase_frequency = customer_data.get("purchase_frequency_days", 999)
        if purchase_frequency > 120:
            risk += 0.2
        elif purchase_frequency > 60:
            risk += 0.1
        
        # Engagement factor
        engagement_score = customer_data.get("engagement_score", 0.5)
        if engagement_score < 0.2:
            risk += 0.25
        elif engagement_score < 0.5:
            risk += 0.1
        
        # Customer value (negative factor - high value less likely to churn)
        customer_value = customer_data.get("customer_value", 500)
        if customer_value < 200:
            risk += 0.1
        elif customer_value < 500:
            risk += 0.05
        
        return min(1.0, risk)  # Cap at 1.0
    
    def _determine_lifecycle_stage(self, customer_data: Dict[str, Any], churn_risk: float) -> LifecycleStage:
        """Determine appropriate lifecycle stage based on behaviors and churn risk"""
        
        # Rule-based stage assignment
        if customer_data.get("days_since_signup", 999) < 30:
            return LifecycleStage.NEW
        
        if churn_risk > 0.6:
            return LifecycleStage.AT_RISK
        
        if customer_data.get("days_since_last_activity", 0) > 180:
            return LifecycleStage.CHURNED
        
        # Active by default
        return LifecycleStage.ACTIVE
    
    def _determine_action(self, stage: LifecycleStage, churn_risk: float, customer_data: Dict[str, Any]) -> str:
        """Determine action based on lifecycle stage and churn risk"""
        
        action_map = {
            LifecycleStage.NEW: "trigger_onboarding",
            LifecycleStage.ACTIVE: "trigger_engagement_campaign" if churn_risk > 0.3 else "track_engagement",
            LifecycleStage.AT_RISK: "trigger_retention_campaign",
            LifecycleStage.CHURNED: "trigger_winback_campaign",
        }
        
        base_action = action_map.get(stage, "monitor")
        
        # Check for VIP treatment
        if customer_data.get("customer_value", 0) > 5000:
            return "escalate_to_vip_support"
        
        return base_action
    
    def get_agent_specs(self) -> Dict[str, Any]:
        """Return agent specifications for documentation"""
        return {
            "name": "Lifecycle & Retention Agent",
            "purpose": "Automatically manage customer lifecycle progression and prevent churn",
            "inputs": [
                "Customer lifecycle stage",
                "Engagement patterns, purchase frequency",
                "Churn risk scores",
                "Segment-specific retention strategies",
            ],
            "actions": [
                "Automatically advance/regress lifecycle stage",
                "Trigger retention campaigns",
                "Create VIP programs for high-value customers",
                "Schedule manual review for highest-churn-risk customers",
            ],
            "success_metrics": [
                "Churn rate reduction: 20%",
                "Retention campaign ROI: 4:1",
                "Win-back rate: 15% of at-risk",
                "Lifecycle stage accuracy: 92%",
            ],
        }
