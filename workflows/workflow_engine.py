"""
Workflow engine for orchestrating multi-agent decisions and execution
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import json

@dataclass
class WorkflowState:
    """State of a workflow execution"""
    workflow_id: str
    customer_id: str
    status: str  # pending, running, completed, failed, paused
    steps: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "customer_id": self.customer_id,
            "status": self.status,
            "steps": self.steps,
            "decisions": self.decisions,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

@dataclass
class WorkflowStep:
    """Single step in a workflow"""
    step_id: str
    name: str
    agent_name: str
    input_data: Dict[str, Any]
    output: Optional[Dict[str, Any]] = None
    status: str = "pending"  # pending, running, completed, failed, skipped
    error: Optional[str] = None

class WorkflowEngine:
    """
    Orchestrates multi-step workflows involving multiple agents and guardrails
    """
    
    def __init__(self):
        self.workflows: Dict[str, WorkflowState] = {}
        self.registered_agents = {}
        self.registered_guardrails = {}
    
    def register_agent(self, agent_name: str, agent):
        """Register an agent for use in workflows"""
        self.registered_agents[agent_name] = agent
    
    def register_guardrail(self, guardrail_name: str, check_func: Callable):
        """Register a guardrail check function"""
        self.registered_guardrails[guardrail_name] = check_func
    
    def create_workflow(self, workflow_id: str, customer_id: str) -> WorkflowState:
        """Create a new workflow instance"""
        workflow = WorkflowState(
            workflow_id=workflow_id,
            customer_id=customer_id,
            status="pending",
        )
        self.workflows[workflow_id] = workflow
        return workflow
    
    def execute_workflow(self, workflow_id: str, steps: List[WorkflowStep]) -> WorkflowState:
        """
        Execute a workflow with multiple steps
        
        Args:
            workflow_id: Unique workflow identifier
            steps: List of workflow steps to execute
            
        Returns:
            Final workflow state
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow.status = "running"
        
        for step in steps:
            try:
                # Execute step
                result = self._execute_step(step)
                
                # Record in workflow
                workflow.steps.append({
                    "step_id": step.step_id,
                    "name": step.name,
                    "agent": step.agent_name,
                    "status": "completed",
                    "result": result,
                })
                
                # Record decision if applicable
                if hasattr(result, 'to_dict'):
                    workflow.decisions.append(result.to_dict())
                
            except Exception as e:
                workflow.steps.append({
                    "step_id": step.step_id,
                    "name": step.name,
                    "agent": step.agent_name,
                    "status": "failed",
                    "error": str(e),
                })
                workflow.status = "failed"
                raise
        
        workflow.status = "completed"
        workflow.updated_at = datetime.utcnow().isoformat() + "Z"
        
        return workflow
    
    def _execute_step(self, step: WorkflowStep):
        """Execute a single workflow step"""
        
        agent_name = step.agent_name
        if agent_name not in self.registered_agents:
            raise ValueError(f"Agent {agent_name} not registered")
        
        agent = self.registered_agents[agent_name]
        
        # Call agent's decide method
        result = agent.decide(step.input_data)
        
        return result
    
    def get_workflow_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """Get current state of a workflow"""
        return self.workflows.get(workflow_id)
    
    def get_workflow_history(self, customer_id: str, limit: int = 10) -> List[WorkflowState]:
        """Get workflow history for a customer"""
        customer_workflows = [
            w for w in self.workflows.values()
            if w.customer_id == customer_id
        ]
        return sorted(customer_workflows, key=lambda w: w.created_at, reverse=True)[:limit]

# Workflow templates for common scenarios

ABANDONED_CART_WORKFLOW = {
    "name": "Abandoned Cart Recovery",
    "description": "Recover revenue from abandoned shopping carts",
    "trigger": "cart_abandoned",
    "steps": [
        {
            "name": "Guardrail Check",
            "type": "guardrail",
            "checks": ["frequency_cap", "compliance", "customer_eligibility"],
        },
        {
            "name": "Abandoned Cart Recovery",
            "type": "agent",
            "agent": "AbandonedCartWinBackAgent",
        },
        {
            "name": "Audit & Logging",
            "type": "guardrail",
            "checks": ["decision_audit", "human_review_queue"],
        },
        {
            "name": "Execute",
            "type": "execution",
            "channels": ["email", "sms"],
        },
        {
            "name": "Measure",
            "type": "analytics",
            "metrics": ["open_rate", "click_rate", "conversion"],
        },
    ],
}

LIFECYCLE_ENGAGEMENT_WORKFLOW = {
    "name": "Lifecycle-Based Engagement",
    "description": "Trigger personalized campaigns based on lifecycle stage",
    "trigger": "lifecycle_stage_change",
    "steps": [
        {
            "name": "Lifecycle Assessment",
            "type": "agent",
            "agent": "LifecycleAgent",
        },
        {
            "name": "Campaign Selection",
            "type": "agent",
            "agent": "CampaignAgent",
        },
        {
            "name": "Guardrail Validation",
            "type": "guardrail",
            "checks": ["frequency_cap", "compliance", "tone_consistency"],
        },
        {
            "name": "Execute Campaign",
            "type": "execution",
            "channels": ["email", "web", "push"],
        },
        {
            "name": "Track Engagement",
            "type": "analytics",
            "metrics": ["open_rate", "engagement_score"],
        },
    ],
}

CREATIVE_TESTING_WORKFLOW = {
    "name": "Creative Testing & Optimization",
    "description": "Automatically test and optimize creative assets",
    "trigger": "campaign_launch",
    "steps": [
        {
            "name": "Eligibility Check",
            "type": "guardrail",
            "checks": ["minimum_volume", "test_frequency"],
        },
        {
            "name": "Generate Variations",
            "type": "agent",
            "agent": "CreativeTestingAgent",
        },
        {
            "name": "Design Test",
            "type": "analytics",
            "action": "create_ab_test",
        },
        {
            "name": "Execute Test",
            "type": "execution",
            "channels": ["email"],
        },
        {
            "name": "Analyze Results",
            "type": "analytics",
            "metrics": ["statistical_significance", "winner_identification"],
        },
    ],
}

WINBACK_WORKFLOW = {
    "name": "Win-Back Campaign",
    "description": "Re-engage dormant and churned customers",
    "trigger": "customer_dormant",
    "steps": [
        {
            "name": "Dormancy Check",
            "type": "guardrail",
            "checks": ["minimum_inactivity_days", "customer_value_check"],
        },
        {
            "name": "Win-Back Strategy",
            "type": "agent",
            "agent": "AbandonedCartWinBackAgent",
        },
        {
            "name": "Personalization",
            "type": "agent",
            "agent": "CampaignAgent",
        },
        {
            "name": "Compliance Check",
            "type": "guardrail",
            "checks": ["consent_validation", "suppression_list"],
        },
        {
            "name": "Execute Campaign",
            "type": "execution",
            "channels": ["email", "sms"],
        },
        {
            "name": "Track Win-Back Success",
            "type": "analytics",
            "metrics": ["reactivation_rate", "roi"],
        },
    ],
}
