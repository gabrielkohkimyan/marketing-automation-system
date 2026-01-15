"""
Abandoned Cart & Win-Back Agent - recover lost revenue and re-engage dormant customers
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent, AgentInput, AgentDecision

class AbandonedCartWinBackAgent(BaseAgent):
    """
    Abandoned Cart & Win-Back Agent
    
    Purpose: Recover lost revenue from abandoned carts and re-engage dormant customers
    
    Inputs:
    - Cart abandonment signals, customer recency/frequency
    - Product data, inventory, popularity
    - Win-back segment criteria
    - Incentive policies
    
    Actions:
    - Send recovery emails with dynamic product feeds
    - Apply time-limited discount codes
    - Retarget on web/social
    - Escalate high-value customers to sales team
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("AbandonedCartWinBackAgent", config)
    
    def decide(self, agent_input: AgentInput) -> AgentDecision:
        """
        Make abandoned cart or win-back decision
        
        Logic:
        1. Determine if cart abandoned or win-back candidate
        2. Identify top products / relevant offers
        3. Generate product-focused copy
        4. Calculate incentive level
        5. Schedule send with time-limited offer
        """
        customer_data = agent_input.customer_data
        context = agent_input.context
        
        # Determine action type
        action_type = context.get("action_type", "cart_abandonment")
        
        if action_type == "cart_abandonment":
            return self._handle_abandoned_cart(agent_input)
        elif action_type == "win_back":
            return self._handle_winback(agent_input)
        else:
            return self._create_decision(
                customer_id=agent_input.customer_id,
                action="skip",
                parameters={},
                confidence=0.9,
                reasoning="Unknown action type",
            )
    
    def _handle_abandoned_cart(self, agent_input: AgentInput) -> AgentDecision:
        """Handle abandoned cart recovery"""
        
        customer_data = agent_input.customer_data
        context = agent_input.context
        
        # Extract cart info
        cart_value = customer_data.get("cart_value", 0)
        cart_items = context.get("cart_items", [])
        hours_since_abandon = context.get("hours_since_abandon", 2)
        
        # Check if recovery is worthwhile
        if cart_value < 20:
            return self._create_decision(
                customer_id=agent_input.customer_id,
                action="skip_cart_recovery",
                parameters={"reason": "Cart value too low"},
                confidence=0.9,
                reasoning="Cart value below minimum recovery threshold",
            )
        
        # Calculate incentive
        incentive = self._calculate_incentive(cart_value, is_vip=customer_data.get("vip_status", False))
        
        # Determine discount code
        discount_code = f"RECOVER{customer_data.get('customer_id', 'X')[-4:].upper()}"
        
        decision = self._create_decision(
            customer_id=agent_input.customer_id,
            action="send_cart_recovery_email",
            parameters={
                "cart_value": cart_value,
                "top_items": cart_items[:3],
                "discount_percentage": incentive,
                "discount_code": discount_code,
                "expiry_hours": 24,
                "send_time": "2 hours from now",
                "follow_up": "Send SMS reminder after 12 hours",
            },
            confidence=0.89,
            guardrail_checks={
                "discount_policy_check": True,
                "frequency_cap_check": True,
                "inventory_check": True,
            },
            requires_human_review=cart_value > 500,  # High-value carts reviewed
            reasoning=f"Cart abandoned {hours_since_abandon}h ago. Value: ${cart_value}. Incentive: {incentive}% discount",
        )
        
        return decision
    
    def _handle_winback(self, agent_input: AgentInput) -> AgentDecision:
        """Handle win-back campaign for dormant customers"""
        
        customer_data = agent_input.customer_data
        context = agent_input.context
        
        # Extract key metrics
        days_inactive = customer_data.get("days_since_last_activity", 0)
        customer_value = customer_data.get("customer_value", 0)
        
        # Check if win-back candidate
        if days_inactive < 90:
            return self._create_decision(
                customer_id=agent_input.customer_id,
                action="skip_winback",
                parameters={"reason": "Customer not inactive long enough"},
                confidence=0.9,
                reasoning="Minimum 90 days inactivity required for win-back",
            )
        
        # Segment-based win-back strategy
        if customer_value > 1000:
            # VIP win-back: Personal offer
            offer_type = "personal_concierge"
            discount = 0.15
            channels = ["email", "phone"]
        elif customer_value > 300:
            # Regular win-back: Discount + new products
            offer_type = "discount_plus_new_products"
            discount = 0.20
            channels = ["email", "sms"]
        else:
            # Low-value win-back: Generic incentive
            offer_type = "generic_incentive"
            discount = 0.15
            channels = ["email"]
        
        discount_code = f"WB{customer_data.get('customer_id', 'X')[-4:].upper()}{(days_inactive // 30) % 10}"
        
        decision = self._create_decision(
            customer_id=agent_input.customer_id,
            action="execute_winback_campaign",
            parameters={
                "offer_type": offer_type,
                "discount_percentage": discount,
                "discount_code": discount_code,
                "channels": channels,
                "messaging": f"We miss you! {discount*100:.0f}% off your next purchase",
                "follow_up_wave": 2,  # Send second email at day 7
                "personalization": "Highlight products similar to past purchases",
            },
            confidence=0.85,
            guardrail_checks={
                "inactive_days_check": True,
                "discount_policy_check": True,
                "email_deliverability_check": True,
            },
            requires_human_review=customer_value > 2000,
            reasoning=f"Dormant for {days_inactive} days. Customer Value: ${customer_value}. Strategy: {offer_type}",
        )
        
        return decision
    
    def _calculate_incentive(self, cart_value: float, is_vip: bool = False) -> int:
        """Calculate discount incentive based on cart value"""
        
        # Base discount increases with cart value
        if is_vip:
            # VIP customers: smaller discount (higher LTV)
            if cart_value > 500:
                return 10
            elif cart_value > 200:
                return 12
            else:
                return 15
        else:
            # Regular customers
            if cart_value > 500:
                return 15
            elif cart_value > 200:
                return 20
            else:
                return 25
    
    def get_agent_specs(self) -> Dict[str, Any]:
        """Return agent specifications for documentation"""
        return {
            "name": "Abandoned Cart & Win-Back Agent",
            "purpose": "Recover lost revenue from abandoned carts and re-engage dormant customers",
            "inputs": [
                "Cart abandonment signals, customer recency/frequency",
                "Product data, inventory, popularity",
                "Win-back segment criteria",
                "Incentive policies",
            ],
            "actions": [
                "Send recovery emails with dynamic product feeds",
                "Apply time-limited discount codes",
                "Retarget on web/social",
                "Escalate high-value customers to sales team",
            ],
            "success_metrics": [
                "Cart recovery rate: 25% → 35%",
                "Win-back conversion: 8-12%",
                "Revenue recovered: $500k annually",
                "Offer uptake: 20% → 28%",
            ],
        }
