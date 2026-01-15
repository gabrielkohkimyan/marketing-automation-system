"""
Example workflows demonstrating system usage
"""
from typing import Dict, Any
from agents import CampaignAgent, LifecycleAgent, CreativeTestingAgent, AbandonedCartWinBackAgent, AgentInput

def abandoned_cart_recovery_workflow(customer_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Abandoned Cart Recovery Workflow
    
    TRIGGER: Cart Abandoned (2+ hours)
    ↓
    DECISION: Retrieve top products, calculate incentive
    ↓
    PERSONALIZATION: Generate subject line, add product images
    ↓
    GUARDRAILS: Check customer email frequency, compliance
    ↓
    EXECUTION: Send email at optimal time
    ↓
    MEASUREMENT: Track open (2h), click (24h), conversion (7d)
    ↓
    FEEDBACK: Update churn risk score, creative performance
    """
    
    # Initialize agent
    cart_agent = AbandonedCartWinBackAgent()
    
    # Create agent input
    agent_input = AgentInput(
        customer_id=customer_data["customer_id"],
        customer_data=customer_data,
        context={
            "action_type": "cart_abandonment",
            "cart_items": customer_data.get("cart_items", []),
            "hours_since_abandon": 2,
        }
    )
    
    # Get decision
    decision = cart_agent.decide(agent_input)
    
    return {
        "workflow": "abandoned_cart_recovery",
        "customer_id": customer_data["customer_id"],
        "decision": decision.to_dict(),
        "next_steps": [
            "1. Check frequency cap (max 3 emails/week)",
            "2. Validate compliance (GDPR, CAN-SPAM)",
            "3. Generate personalized copy",
            "4. Schedule email for optimal send time",
            "5. Add discount code to email",
            "6. Track open/click/conversion metrics",
            "7. Update customer engagement score",
        ]
    }

def lifecycle_engagement_workflow(customer_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lifecycle-Based Engagement Workflow
    
    TRIGGER: New Customer Registration OR Lifecycle Stage Change
    ↓
    DECISION: Identify lifecycle stage (new/active/at-risk)
    ↓
    PERSONALIZATION: Select stage-appropriate campaign template
    ↓
    GUARDRAILS: Frequency cap, compliance check
    ↓
    EXECUTION: Launch multi-touch journey:
      - Day 1: Welcome email
      - Day 3: Feature education
      - Day 7: Social proof / testimonials
    ↓
    MEASUREMENT: Track engagement, conversion, NPS
    ↓
    FEEDBACK: Assess effectiveness, update segment targeting
    """
    
    # Initialize agents
    lifecycle_agent = LifecycleAgent()
    campaign_agent = CampaignAgent()
    
    # Step 1: Assess lifecycle
    lifecycle_input = AgentInput(
        customer_id=customer_data["customer_id"],
        customer_data=customer_data,
        context={},
    )
    
    lifecycle_decision = lifecycle_agent.decide(lifecycle_input)
    
    # Step 2: Select and execute campaign
    campaign_input = AgentInput(
        customer_id=customer_data["customer_id"],
        customer_data=customer_data,
        context={
            "trigger": lifecycle_decision.parameters.get("action_type", "lifecycle_change"),
        }
    )
    
    campaign_decision = campaign_agent.decide(campaign_input)
    
    return {
        "workflow": "lifecycle_engagement",
        "customer_id": customer_data["customer_id"],
        "lifecycle_decision": lifecycle_decision.to_dict(),
        "campaign_decision": campaign_decision.to_dict(),
        "journey_plan": {
            "day_1": "Welcome email + onboarding",
            "day_3": "Feature education",
            "day_7": "Social proof / testimonials",
            "day_14": "Engagement booster or upsell",
        },
        "success_metrics": [
            "Open rate: 30%+",
            "Click rate: 5%+",
            "Conversion rate (to purchase): 2%+",
        ]
    }

def creative_testing_workflow(campaign_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creative Testing & Optimization Workflow
    
    TRIGGER: New campaign creation OR Performance plateau
    ↓
    DECISION: Generate 3 subject line variations via LLM
    ↓
    PERSONALIZATION: Tailor variations to segment preferences
    ↓
    GUARDRAILS: Tone/compliance check on all variations
    ↓
    EXECUTION: Deploy 3-way test:
      - Control: Original
      - Variant A: 40% traffic
      - Variant B: 40% traffic
    ↓
    MEASUREMENT: Hourly statistical analysis
    ↓
    FEEDBACK: Promote winner at 95% confidence, analyze learnings
    """
    
    # Initialize agent
    creative_agent = CreativeTestingAgent()
    
    # Create agent input
    agent_input = AgentInput(
        customer_id="campaign_" + campaign_data.get("campaign_id", "default"),
        customer_data={
            "campaign_id": campaign_data.get("campaign_id", "default"),
        },
        context={
            "campaign_id": campaign_data.get("campaign_id", "default"),
            "original_creative": campaign_data.get("original_creative", {}),
            "expected_volume": campaign_data.get("expected_volume", 10000),
            "days_since_last_test": campaign_data.get("days_since_last_test", 14),
        }
    )
    
    # Get decision
    decision = creative_agent.decide(agent_input)
    
    return {
        "workflow": "creative_testing",
        "campaign_id": campaign_data.get("campaign_id", "default"),
        "decision": decision.to_dict(),
        "test_timeline": {
            "t=0": "Launch test with 3-5 variations",
            "t=24h": "First statistical analysis",
            "t=7d": "Full week analysis",
            "t=7d+": "Promote winner, retire losers",
        },
        "success_metrics": [
            "Statistical significance: p < 0.05",
            "Winner uplift: 15-35% CTR improvement",
            "Template quality: 85%+ consistency",
        ]
    }

def winback_campaign_workflow(customer_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Win-Back Campaign Workflow
    
    TRIGGER: Dormant customer detection (90+ days inactive)
    ↓
    DECISION: Identify customer value tier
    ↓
    PERSONALIZATION: Create segment-appropriate win-back offer
    ↓
    GUARDRAILS: Validate consent, check suppression lists
    ↓
    EXECUTION: Launch multi-channel campaign:
      - Wave 1 (Day 0): Email with personalized incentive
      - Wave 2 (Day 7): SMS reminder + social retargeting
    ↓
    MEASUREMENT: Track reactivation, revenue impact
    ↓
    FEEDBACK: Update customer segment, track lifetime value
    """
    
    # Initialize agent
    winback_agent = AbandonedCartWinBackAgent()
    
    # Create agent input
    agent_input = AgentInput(
        customer_id=customer_data["customer_id"],
        customer_data=customer_data,
        context={
            "action_type": "win_back",
        }
    )
    
    # Get decision
    decision = winback_agent.decide(agent_input)
    
    return {
        "workflow": "winback_campaign",
        "customer_id": customer_data["customer_id"],
        "decision": decision.to_dict(),
        "campaign_phases": {
            "phase_1": {
                "day": 0,
                "channel": "email",
                "message": "We miss you! Come back and enjoy special offer",
                "offer": decision.parameters.get("discount_percentage", 20),
            },
            "phase_2": {
                "day": 7,
                "channel": "sms",
                "message": "Last chance: Your exclusive offer expires in 24h",
            },
            "phase_3": {
                "day": 14,
                "channel": "social",
                "message": "See what you're missing - exclusive products",
            }
        },
        "success_metrics": [
            "Win-back conversion rate: 8-12%",
            "Revenue recovered per successful reactivation: $150+",
            "Retention post-reactivation: 70%+ (90 days)",
        ]
    }

# Helper function to run all examples
def run_all_workflow_examples():
    """Run all workflow examples with sample data"""
    
    # Sample customers
    sample_customers = {
        "new_signup": {
            "customer_id": "cust_001",
            "first_name": "Sarah",
            "email": "sarah@example.com",
            "lifecycle_stage": "new",
            "days_since_signup": 2,
            "engagement_score": 0.7,
            "cart_value": 0,
            "customer_value": 0,
            "days_since_last_activity": 1,
            "purchase_count": 0,
        },
        "at_risk": {
            "customer_id": "cust_002",
            "first_name": "John",
            "email": "john@example.com",
            "lifecycle_stage": "at_risk",
            "days_since_signup": 180,
            "engagement_score": 0.2,
            "cart_value": 0,
            "customer_value": 750,
            "days_since_last_activity": 120,
            "purchase_count": 3,
            "purchase_frequency_days": 90,
        },
        "abandoned_cart": {
            "customer_id": "cust_003",
            "first_name": "Emma",
            "email": "emma@example.com",
            "lifecycle_stage": "active",
            "days_since_signup": 100,
            "engagement_score": 0.65,
            "cart_value": 250,
            "cart_items": ["Product A", "Product B"],
            "customer_value": 2000,
            "days_since_last_activity": 5,
            "purchase_count": 8,
            "vip_status": False,
        },
        "dormant": {
            "customer_id": "cust_004",
            "first_name": "Michael",
            "email": "michael@example.com",
            "lifecycle_stage": "churned",
            "days_since_signup": 365,
            "engagement_score": 0.0,
            "cart_value": 0,
            "customer_value": 1200,
            "days_since_last_activity": 200,
            "purchase_count": 12,
        }
    }
    
    sample_campaign = {
        "campaign_id": "camp_001",
        "original_creative": {
            "subject": "Don't miss out on our latest offer",
            "body": "We have something special for you",
            "cta": "Shop Now",
        },
        "expected_volume": 50000,
        "days_since_last_test": 30,
    }
    
    results = {
        "abandoned_cart": abandoned_cart_recovery_workflow(sample_customers["abandoned_cart"]),
        "lifecycle": lifecycle_engagement_workflow(sample_customers["new_signup"]),
        "creative_test": creative_testing_workflow(sample_campaign),
        "winback": winback_campaign_workflow(sample_customers["dormant"]),
    }
    
    return results
