"""
Base agent class for all marketing automation agents
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import uuid

@dataclass
class AgentInput:
    """Base input for agents"""
    customer_id: str
    customer_data: Dict[str, Any]
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentDecision:
    """Decision made by an agent"""
    decision_id: str
    agent_name: str
    customer_id: str
    action: str
    parameters: Dict[str, Any]
    confidence: float
    guardrail_checks: Dict[str, bool]
    requires_human_review: bool
    timestamp: str
    reasoning: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "agent_name": self.agent_name,
            "customer_id": self.customer_id,
            "action": self.action,
            "parameters": self.parameters,
            "confidence": self.confidence,
            "guardrail_checks": self.guardrail_checks,
            "requires_human_review": self.requires_human_review,
            "timestamp": self.timestamp,
            "reasoning": self.reasoning,
        }

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.decision_log: List[AgentDecision] = []
    
    @abstractmethod
    def decide(self, agent_input: AgentInput) -> AgentDecision:
        """
        Main decision-making method. Must be implemented by subclasses.
        
        Args:
            agent_input: Input containing customer data and context
            
        Returns:
            AgentDecision: Decision with action and parameters
        """
        pass
    
    def _generate_decision_id(self) -> str:
        """Generate unique decision ID"""
        return str(uuid.uuid4())
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.utcnow().isoformat() + "Z"
    
    def _create_decision(
        self,
        customer_id: str,
        action: str,
        parameters: Dict[str, Any],
        confidence: float = 0.85,
        guardrail_checks: Optional[Dict[str, bool]] = None,
        requires_human_review: bool = False,
        reasoning: str = "",
    ) -> AgentDecision:
        """
        Helper method to create a decision
        
        Args:
            customer_id: Customer ID
            action: Action to take
            parameters: Action parameters
            confidence: Confidence score (0-1)
            guardrail_checks: Dict of guardrail check results
            requires_human_review: Whether decision needs human review
            reasoning: Reasoning for the decision
            
        Returns:
            AgentDecision object
        """
        decision = AgentDecision(
            decision_id=self._generate_decision_id(),
            agent_name=self.name,
            customer_id=customer_id,
            action=action,
            parameters=parameters,
            confidence=confidence,
            guardrail_checks=guardrail_checks or {},
            requires_human_review=requires_human_review,
            timestamp=self._get_timestamp(),
            reasoning=reasoning,
        )
        self.decision_log.append(decision)
        return decision
    
    def get_decision_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent decision history"""
        return [d.to_dict() for d in self.decision_log[-limit:]]
    
    def clear_decision_log(self):
        """Clear decision log (for testing)"""
        self.decision_log = []
