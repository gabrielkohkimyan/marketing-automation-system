"""
Data pipeline for ingesting, normalizing, and enriching customer data
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

@dataclass
class CustomerEvent:
    """Customer behavioral event"""
    event_id: str
    customer_id: str
    event_type: str
    event_data: Dict[str, Any]
    timestamp: str
    source: str

class DataProcessor:
    """Process and normalize raw customer data"""
    
    @staticmethod
    def normalize_customer_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw customer data into standard format"""
        
        normalized = {
            "customer_id": raw_data.get("id") or raw_data.get("customer_id"),
            "first_name": raw_data.get("first_name", "").strip(),
            "email": raw_data.get("email", "").lower().strip(),
            "phone": raw_data.get("phone", "").strip(),
            "lifecycle_stage": raw_data.get("lifecycle_stage", "active"),
            "engagement_score": float(raw_data.get("engagement_score", 0.5)),
            "customer_value": float(raw_data.get("ltv", raw_data.get("customer_value", 0))),
            "purchase_count": int(raw_data.get("purchases", raw_data.get("purchase_count", 0))),
            "days_since_signup": int(raw_data.get("days_signup", raw_data.get("days_since_signup", 0))),
            "days_since_last_activity": int(raw_data.get("days_inactive", raw_data.get("days_since_last_activity", 0))),
            "purchase_frequency_days": int(raw_data.get("freq_days", raw_data.get("purchase_frequency_days", 999))),
            "timezone": raw_data.get("timezone", "UTC"),
            "gdpr_consent": bool(raw_data.get("gdpr_consent", False)),
            "email_unsubscribed": bool(raw_data.get("unsubscribed", raw_data.get("email_unsubscribed", False))),
            "vip_status": bool(raw_data.get("vip", raw_data.get("vip_status", False))),
            "cart_value": float(raw_data.get("cart_value", 0)),
            "cart_items": raw_data.get("cart_items", []),
        }
        
        return normalized
    
    @staticmethod
    def calculate_churn_score(customer_data: Dict[str, Any]) -> float:
        """Calculate churn risk score (0-1)"""
        
        score = 0.0
        
        # Recency (most important)
        days_inactive = customer_data.get("days_since_last_activity", 0)
        if days_inactive > 180:
            score += 0.4
        elif days_inactive > 90:
            score += 0.2
        
        # Frequency
        freq_days = customer_data.get("purchase_frequency_days", 999)
        if freq_days > 120:
            score += 0.2
        elif freq_days > 60:
            score += 0.1
        
        # Monetary (negative factor)
        customer_value = customer_data.get("customer_value", 500)
        if customer_value < 200:
            score += 0.1
        
        return min(score, 1.0)
    
    @staticmethod
    def calculate_engagement_score(event_data: List[Dict[str, Any]]) -> float:
        """Calculate engagement score from recent events (0-1)"""
        
        if not event_data:
            return 0.5
        
        # Weight recent events more heavily
        score = 0.0
        total_weight = 0
        
        event_weights = {
            "email_open": 0.3,
            "email_click": 0.5,
            "purchase": 1.0,
            "page_view": 0.1,
            "add_to_cart": 0.4,
            "email_bounce": -0.5,
            "email_complaint": -1.0,
        }
        
        for i, event in enumerate(event_data[-30:]):  # Last 30 days
            weight = event_weights.get(event.get("type", "page_view"), 0.1)
            recency_factor = (i + 1) / 30  # More recent = higher weight
            
            score += weight * recency_factor
            total_weight += abs(weight) * recency_factor
        
        if total_weight == 0:
            return 0.5
        
        return min(max(score / total_weight, 0), 1.0)

class MockDataSource:
    """Mock data source for testing (in production: connects to real CRM/analytics)"""
    
    @staticmethod
    def get_customer(customer_id: str) -> Optional[Dict[str, Any]]:
        """Get customer data from mock source"""
        
        mock_customers = {
            "cust_001": {
                "id": "cust_001",
                "first_name": "Sarah",
                "email": "sarah@example.com",
                "phone": "+1234567890",
                "lifecycle_stage": "new",
                "engagement_score": 0.7,
                "ltv": 0,
                "purchases": 0,
                "days_signup": 2,
                "days_inactive": 1,
                "timezone": "UTC-5",
                "gdpr_consent": True,
                "vip": False,
                "cart_value": 0,
            },
            "cust_002": {
                "id": "cust_002",
                "first_name": "John",
                "email": "john@example.com",
                "phone": "+1987654321",
                "lifecycle_stage": "at_risk",
                "engagement_score": 0.2,
                "ltv": 750,
                "purchases": 3,
                "days_signup": 180,
                "days_inactive": 120,
                "freq_days": 90,
                "timezone": "UTC-7",
                "gdpr_consent": True,
                "vip": False,
                "cart_value": 0,
            },
            "cust_003": {
                "id": "cust_003",
                "first_name": "Emma",
                "email": "emma@example.com",
                "phone": "+1555555555",
                "lifecycle_stage": "active",
                "engagement_score": 0.65,
                "ltv": 2000,
                "purchases": 8,
                "days_signup": 100,
                "days_inactive": 5,
                "timezone": "UTC-5",
                "gdpr_consent": True,
                "vip": False,
                "cart_value": 250.00,
                "cart_items": ["Product A", "Product B"],
            },
        }
        
        return mock_customers.get(customer_id)
    
    @staticmethod
    def get_customer_events(customer_id: str, limit: int = 30) -> List[Dict[str, Any]]:
        """Get recent customer events"""
        
        mock_events = {
            "cust_001": [
                {"type": "page_view", "timestamp": "2024-01-14T10:00:00Z"},
                {"type": "page_view", "timestamp": "2024-01-14T10:05:00Z"},
                {"type": "email_open", "timestamp": "2024-01-13T09:30:00Z"},
            ],
            "cust_002": [
                {"type": "email_bounce", "timestamp": "2024-01-01T10:00:00Z"},
            ],
            "cust_003": [
                {"type": "add_to_cart", "timestamp": "2024-01-14T15:30:00Z"},
                {"type": "email_open", "timestamp": "2024-01-14T12:00:00Z"},
                {"type": "email_click", "timestamp": "2024-01-14T12:05:00Z"},
                {"type": "purchase", "timestamp": "2024-01-10T14:20:00Z"},
            ],
        }
        
        return mock_events.get(customer_id, [])[:limit]

class DataEnricher:
    """Enrich customer data with computed features"""
    
    @staticmethod
    def enrich_customer(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich customer data with calculated features"""
        
        # Normalize
        normalized = DataProcessor.normalize_customer_data(raw_data)
        
        # Calculate churn score
        normalized["churn_risk"] = DataProcessor.calculate_churn_score(normalized)
        
        # Get events and calculate engagement
        events = MockDataSource.get_customer_events(normalized["customer_id"])
        normalized["engagement_score"] = DataProcessor.calculate_engagement_score(events)
        
        # Add metadata
        normalized["last_enriched"] = datetime.utcnow().isoformat() + "Z"
        
        return normalized
