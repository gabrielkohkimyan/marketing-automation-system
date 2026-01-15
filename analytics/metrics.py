"""
Analytics and measurement framework for KPI tracking and A/B testing
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import math

class MetricType(Enum):
    """Types of metrics"""
    CONVERSION = "conversion"
    ENGAGEMENT = "engagement"
    REVENUE = "revenue"
    EFFICIENCY = "efficiency"

@dataclass
class MetricPoint:
    """Single metric data point"""
    metric_name: str
    value: float
    timestamp: str
    dimension: str  # e.g., "campaign_id", "segment"
    dimension_value: str

class MetricsCollector:
    """Collects and aggregates marketing metrics"""
    
    def __init__(self):
        self.metrics: List[MetricPoint] = []
    
    def record_metric(self, metric_name: str, value: float, dimension: str = "", dimension_value: str = ""):
        """Record a metric data point"""
        
        point = MetricPoint(
            metric_name=metric_name,
            value=value,
            timestamp=datetime.utcnow().isoformat() + "Z",
            dimension=dimension,
            dimension_value=dimension_value,
        )
        
        self.metrics.append(point)
    
    def get_metrics(self, metric_name: str, dimension: str = "") -> List[MetricPoint]:
        """Retrieve metrics"""
        
        results = [
            m for m in self.metrics
            if m.metric_name == metric_name
        ]
        
        if dimension:
            results = [m for m in results if m.dimension == dimension]
        
        return results
    
    def get_aggregate(self, metric_name: str, dimension: str = "", operation: str = "avg") -> Dict[str, float]:
        """Get aggregated metric (sum, avg, count, etc.)"""
        
        points = self.get_metrics(metric_name, dimension)
        
        if not points:
            return {}
        
        values = [p.value for p in points]
        
        aggregates = {
            "count": len(values),
            "sum": sum(values),
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }
        
        return {operation: aggregates.get(operation, 0)}

@dataclass
class ABTestVariant:
    """A/B test variant"""
    variant_id: str
    name: str
    traffic_percentage: float
    conversions: int = 0
    impressions: int = 0
    revenue: float = 0.0
    
    @property
    def conversion_rate(self) -> float:
        """Conversion rate for this variant"""
        if self.impressions == 0:
            return 0
        return self.conversions / self.impressions
    
    @property
    def revenue_per_impression(self) -> float:
        """Revenue per impression"""
        if self.impressions == 0:
            return 0
        return self.revenue / self.impressions

@dataclass
class ABTest:
    """A/B test definition and results"""
    test_id: str
    name: str
    created_at: str
    variants: Dict[str, ABTestVariant] = field(default_factory=dict)
    status: str = "running"  # running, completed, archived
    winner: Optional[str] = None
    confidence_level: float = 0.95
    
    def record_event(self, variant_id: str, event_type: str, value: float = 1.0):
        """Record test event"""
        
        if variant_id not in self.variants:
            return
        
        variant = self.variants[variant_id]
        
        if event_type == "impression":
            variant.impressions += int(value)
        elif event_type == "conversion":
            variant.conversions += int(value)
        elif event_type == "revenue":
            variant.revenue += value
    
    def get_statistical_winner(self) -> Optional[str]:
        """Determine statistically significant winner using chi-square test"""
        
        if len(self.variants) < 2:
            return None
        
        variants_list = list(self.variants.values())
        control = variants_list[0]
        
        # Simple chi-square test
        for variant in variants_list[1:]:
            chi_square = self._calculate_chi_square(control, variant)
            p_value = self._chi_square_to_p_value(chi_square, df=1)
            
            if p_value < (1 - self.confidence_level):
                # Statistically significant difference
                if variant.conversion_rate > control.conversion_rate:
                    return variant.variant_id
        
        return None
    
    @staticmethod
    def _calculate_chi_square(variant1: ABTestVariant, variant2: ABTestVariant) -> float:
        """Calculate chi-square statistic"""
        
        # Chi-square formula for conversion rate comparison
        n1, n2 = variant1.impressions, variant2.impressions
        p1, p2 = variant1.conversion_rate, variant2.conversion_rate
        
        if n1 == 0 or n2 == 0:
            return 0
        
        p_pool = (variant1.conversions + variant2.conversions) / (n1 + n2)
        
        expected1 = n1 * p_pool
        expected2 = n2 * p_pool
        
        chi_square = (
            ((variant1.conversions - expected1) ** 2 / expected1) +
            ((variant2.conversions - expected2) ** 2 / expected2)
        )
        
        return chi_square
    
    @staticmethod
    def _chi_square_to_p_value(chi_square: float, df: int = 1) -> float:
        """Approximate p-value from chi-square (simplified)"""
        
        # Simplified approximation
        if chi_square < 2.7:
            return 0.10
        elif chi_square < 3.8:
            return 0.05
        elif chi_square < 6.6:
            return 0.01
        else:
            return 0.001

class FeedbackLoop:
    """Learning feedback loop for continuous improvement"""
    
    def __init__(self):
        self.learnings: List[Dict[str, Any]] = []
    
    def record_learning(self, agent_name: str, decision_id: str, outcome: Dict[str, Any]):
        """Record learning from a decision outcome"""
        
        learning = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": agent_name,
            "decision_id": decision_id,
            "outcome": outcome,
        }
        
        self.learnings.append(learning)
    
    def get_learnings_for_agent(self, agent_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent learnings for an agent"""
        
        agent_learnings = [
            l for l in self.learnings
            if l["agent"] == agent_name
        ]
        
        return sorted(agent_learnings, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def generate_recommendation(self, agent_name: str) -> Dict[str, Any]:
        """Generate optimization recommendations based on learnings"""
        
        learnings = self.get_learnings_for_agent(agent_name, limit=100)
        
        if not learnings:
            return {"recommendation": "Insufficient data", "confidence": 0}
        
        # Simple heuristic: find most common successful pattern
        successful_outcomes = [
            l["outcome"]
            for l in learnings
            if l["outcome"].get("success", False)
        ]
        
        if len(successful_outcomes) / len(learnings) > 0.7:
            return {
                "recommendation": "Current strategy is performing well. Continue.",
                "success_rate": len(successful_outcomes) / len(learnings),
                "confidence": 0.85,
            }
        else:
            return {
                "recommendation": "Adjust strategy. Success rate below 70%.",
                "success_rate": len(successful_outcomes) / len(learnings),
                "confidence": 0.75,
            }

class AnalyticsManager:
    """Central manager for analytics and measurement"""
    
    def __init__(self):
        self.metrics = MetricsCollector()
        self.ab_tests: Dict[str, ABTest] = {}
        self.feedback_loop = FeedbackLoop()
    
    def create_ab_test(self, test_id: str, name: str, variants: Dict[str, ABTestVariant]) -> ABTest:
        """Create a new A/B test"""
        
        test = ABTest(
            test_id=test_id,
            name=name,
            created_at=datetime.utcnow().isoformat() + "Z",
            variants=variants,
        )
        
        self.ab_tests[test_id] = test
        return test
    
    def get_north_star_metric(self) -> Dict[str, float]:
        """Get North Star metric: Revenue per Marketing Touch"""
        
        # This would aggregate across all campaigns
        # For now: return placeholder
        
        return {
            "metric": "revenue_per_touch",
            "current": 0.45,
            "target": 0.61,
            "progress_percent": 0.0,
        }
    
    def get_kpi_dashboard(self) -> Dict[str, Dict[str, Any]]:
        """Get all KPI metrics for dashboard"""
        
        return {
            "conversion_rate": {
                "current": 0.025,
                "target": 0.031,
                "progress": "80%",
            },
            "email_open_rate": {
                "current": 0.22,
                "target": 0.286,
                "progress": "77%",
            },
            "revenue_per_touch": {
                "current": 0.45,
                "target": 0.61,
                "progress": "0%",
            },
            "churn_rate": {
                "current": 0.05,
                "target": 0.04,
                "progress": "20%",
            },
        }
