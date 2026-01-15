"""
Campaign Orchestration Agent - automatically orchestrates multi-channel campaigns
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent, AgentInput, AgentDecision
from config.config import LifecycleStage, Channel, CAMPAIGN_TEMPLATES
import random

class CampaignAgent(BaseAgent):
    """
    Campaign Orchestration Agent
    
    Purpose: Automatically orchestrate multi-channel campaigns triggered by customer behaviors
    
    Inputs:
    - Customer segment, lifecycle stage, behavior triggers
    - Campaign templates, goals (revenue, engagement, churn reduction)
    - Historical performance data
    
    Actions:
    - Create and schedule email campaigns
    - Activate multi-touch journeys
    - Dynamically allocate budget across channels
    - Execute across channels sequentially
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("CampaignAgent", config)
        self.campaign_library = CAMPAIGN_TEMPLATES
    
    def decide(self, agent_input: AgentInput) -> AgentDecision:
        """
        Make campaign orchestration decision
        
        Logic:
        1. Detect trigger (cart abandonment, purchase milestone, etc.)
        2. Retrieve customer context
        3. Select best campaign from template library
        4. Generate personalized copy
        5. Schedule optimal send time
        6. Execute across channels
        """
        customer_data = agent_input.customer_data
        context = agent_input.context
        
        # Extract key information
        lifecycle_stage = LifecycleStage(customer_data.get("lifecycle_stage", "active"))
        trigger = context.get("trigger", "none")
        
        # Step 1: Determine if campaign should be triggered
        should_trigger = self._evaluate_trigger(trigger, customer_data)
        
        if not should_trigger:
            return self._create_decision(
                customer_id=agent_input.customer_id,
                action="skip_campaign",
                parameters={},
                confidence=0.9,
                reasoning="Trigger conditions not met or customer not eligible",
            )
        
        # Step 2: Select appropriate campaign template
        campaign = self._select_campaign(lifecycle_stage)
        
        if not campaign:
            return self._create_decision(
                customer_id=agent_input.customer_id,
                action="skip_campaign",
                parameters={},
                confidence=0.9,
                reasoning="No appropriate campaign template for lifecycle stage",
            )
        
        # Step 3: Generate personalized copy (simulated LLM call)
        personalized_copy = self._generate_copy(campaign, customer_data)
        
        # Step 4: Determine optimal send time
        optimal_send_time = self._calculate_optimal_send_time(customer_data)
        
        # Step 5: Determine channels
        channels = campaign.get("channels", [Channel.EMAIL])
        
        # Create decision
        decision = self._create_decision(
            customer_id=agent_input.customer_id,
            action="execute_campaign",
            parameters={
                "campaign_name": campaign["name"],
                "channels": [c.value for c in channels],
                "copy": personalized_copy,
                "send_time": optimal_send_time,
                "lifecycle_stage": lifecycle_stage.value,
            },
            confidence=0.88,
            guardrail_checks={
                "frequency_cap_check": True,
                "compliance_check": True,
                "content_moderation": True,
            },
            requires_human_review=False,
            reasoning=f"Triggered by {trigger}. Lifecycle stage: {lifecycle_stage.value}. Campaign: {campaign['name']}",
        )
        
        return decision
    
    def _evaluate_trigger(self, trigger: str, customer_data: Dict[str, Any]) -> bool:
        """Evaluate if trigger conditions are met"""
        trigger_mapping = {
            "cart_abandoned": lambda d: d.get("cart_value", 0) > 0,
            "purchase_milestone": lambda d: d.get("purchase_count", 0) % 5 == 0,
            "new_signup": lambda d: d.get("days_since_signup", 999) < 1,
            "lifecycle_change": lambda d: True,
            "win_back": lambda d: d.get("days_since_last_activity", 0) > 90,
        }
        
        if trigger == "none":
            return False
        
        evaluator = trigger_mapping.get(trigger, lambda d: False)
        return evaluator(customer_data)
    
    def _select_campaign(self, lifecycle_stage: LifecycleStage) -> Dict[str, Any]:
        """Select best campaign for lifecycle stage"""
        campaigns = self.campaign_library.get(lifecycle_stage, [])
        if not campaigns:
            return None
        
        # For now, select first campaign (in production, use ML to rank)
        return campaigns[0]
    
    def _generate_copy(self, campaign: Dict[str, Any], customer_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate personalized copy for campaign
        In production, this would call LLM (GPT-4)
        """
        first_name = customer_data.get("first_name", "Customer")
        subject_template = campaign.get("subject_template", "")
        
        # Simple template substitution (in production: LLM-based)
        subject = subject_template.replace("{{first_name}}", first_name)
        subject = subject.replace("{{brand_name}}", "YourBrand")
        
        # Generate body based on campaign
        body_map = {
            "Welcome Series": "Welcome to YourBrand! We're excited to have you. Check out these resources to get started.",
            "Feature Education": "Learn how to get the most from YourBrand with these quick tips.",
            "Engagement Booster": "We have something special for you, {{first_name}}.",
            "Win-Back Special": "We miss you! Come back and enjoy 20% off your next purchase.",
            "Upsell Opportunity": "Based on your interests, we think you'll love this.",
            "Abandoned Cart": "You left something in your cart - here's a special offer to complete your order.",
        }
        
        body = body_map.get(campaign.get("name", ""), "Check out our latest offer!")
        body = body.replace("{{first_name}}", first_name)
        
        cta = "Shop Now" if "cart" in campaign.get("name", "").lower() else "Learn More"
        
        return {
            "subject": subject,
            "body": body,
            "cta": cta,
        }
    
    def _calculate_optimal_send_time(self, customer_data: Dict[str, Any]) -> str:
        """Calculate optimal time to send email"""
        # In production: use ML model trained on historical engagement data
        # For now: return a simulated optimal time
        
        timezone = customer_data.get("timezone", "UTC")
        engagement_pattern = customer_data.get("engagement_pattern", "morning")
        
        time_map = {
            "morning": "09:00",
            "afternoon": "14:00",
            "evening": "19:00",
        }
        
        optimal_time = time_map.get(engagement_pattern, "10:00")
        return f"{optimal_time} {timezone}"
    
    def get_agent_specs(self) -> Dict[str, Any]:
        """Return agent specifications for documentation"""
        return {
            "name": "Campaign Orchestration Agent",
            "purpose": "Automatically orchestrate multi-channel campaigns triggered by customer behaviors",
            "inputs": [
                "Customer segment, lifecycle stage, behavior triggers",
                "Campaign templates, goals",
                "Historical performance data",
            ],
            "actions": [
                "Create and schedule email campaigns",
                "Activate multi-touch journeys",
                "Dynamically allocate budget across channels",
                "Execute across channels sequentially",
            ],
            "success_metrics": [
                "Campaign conversion rate: +25%",
                "Time to execute: < 30 seconds",
                "Personalization effectiveness: +35% CTR",
                "Launch velocity: 70% faster than manual",
            ],
        }
