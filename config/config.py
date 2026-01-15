"""
Configuration and KPI definitions for the marketing automation system
"""
from dataclasses import dataclass
from typing import Dict, List
from enum import Enum

class LifecycleStage(Enum):
    """Customer lifecycle stages"""
    NEW = "new"
    ACTIVE = "active"
    AT_RISK = "at_risk"
    CHURNED = "churned"

class Channel(Enum):
    """Marketing channels"""
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    WEB = "web"
    PUSH = "push"

@dataclass
class KPI:
    """Key Performance Indicator definition"""
    name: str
    description: str
    target: float
    baseline: float
    unit: str

class Config:
    """System configuration"""
    
    # LLM Configuration
    LLM_MODEL = "gpt-4-turbo-preview"
    LLM_TEMPERATURE = 0.7
    LLM_MAX_TOKENS = 300
    LLM_TIMEOUT = 10
    
    # Database
    DB_URL = "postgresql://user:password@localhost:5432/marketing_automation"
    REDIS_URL = "redis://localhost:6379/0"
    
    # API Keys
    OPENAI_API_KEY = "${OPENAI_API_KEY}"
    SENDGRID_API_KEY = "${SENDGRID_API_KEY}"
    
    # Guardrails
    MAX_EMAILS_PER_WEEK = 3
    MIN_ENGAGEMENT_SCORE = 0.3
    TONE_CONSISTENCY_THRESHOLD = 0.85
    SPAM_SCORE_THRESHOLD = 0.7
    MAX_DISCOUNT_PERCENT = 30
    HIGH_VALUE_CUSTOMER_THRESHOLD = 1000  # $CLV
    
    # Decision thresholds
    HUMAN_REVIEW_CONVERSION_PROBABILITY_THRESHOLD = 0.1
    HUMAN_REVIEW_DISCOUNT_THRESHOLD = 0.2  # 20%
    AUTONOMOUS_DECISION_CONFIDENCE_THRESHOLD = 0.85
    
    # A/B Testing
    MIN_SAMPLE_SIZE = 1000
    CONFIDENCE_LEVEL = 0.95
    MIN_TEST_DURATION_DAYS = 7
    
    # Learning & Feedback
    LEARNING_LOOP_FREQUENCY_DAYS = 7
    MODEL_UPDATE_FREQUENCY_DAYS = 14
    
    # Monitoring
    ALERT_LATENCY_THRESHOLD_MS = 2000
    ALERT_ERROR_RATE_THRESHOLD = 0.01
    ALERT_UPTIME_THRESHOLD = 0.995

# KPIs Definition
KPIS: Dict[str, KPI] = {
    "conversion_rate": KPI(
        name="Conversion Rate",
        description="Percentage of contacts that convert to purchase",
        target=0.031,  # 3.1%
        baseline=0.025,  # 2.5%
        unit="%"
    ),
    "email_open_rate": KPI(
        name="Email Open Rate",
        description="Percentage of emails opened",
        target=0.286,
        baseline=0.22,
        unit="%"
    ),
    "click_through_rate": KPI(
        name="Click-Through Rate",
        description="Percentage of clicks per email sent",
        target=0.0405,
        baseline=0.03,
        unit="%"
    ),
    "customer_lifetime_value": KPI(
        name="Customer Lifetime Value",
        description="Total expected revenue from a customer",
        target=700,
        baseline=500,
        unit="$"
    ),
    "churn_rate": KPI(
        name="Churn Rate",
        description="Percentage of customers that churn annually",
        target=0.04,
        baseline=0.05,
        unit="%"
    ),
    "revenue_per_touch": KPI(
        name="Revenue per Marketing Touch",
        description="Total revenue / total marketing touches (emails, SMS, push, web)",
        target=0.61,
        baseline=0.45,
        unit="$"
    ),
    "time_to_campaign_launch": KPI(
        name="Time to Campaign Launch",
        description="Time from campaign conception to execution",
        target=1.5,
        baseline=5,
        unit="days"
    ),
    "manual_workload_hours": KPI(
        name="Marketing Team Weekly Workload",
        description="Hours per week spent on manual campaign tasks",
        target=16,
        baseline=40,
        unit="hours"
    ),
}

# Lifecycle stage transitions
LIFECYCLE_TRANSITIONS = {
    LifecycleStage.NEW: {
        "conditions": {
            "days_since_signup": 30,
            "engagement_score": 0.5,
        },
        "next_stage": LifecycleStage.ACTIVE,
    },
    LifecycleStage.ACTIVE: {
        "conditions": {
            "days_since_last_purchase": 90,
            "engagement_score": 0.2,
        },
        "next_stage": LifecycleStage.AT_RISK,
    },
    LifecycleStage.AT_RISK: {
        "conditions": {
            "days_since_last_activity": 180,
        },
        "next_stage": LifecycleStage.CHURNED,
    },
}

# Campaign templates for each lifecycle stage
CAMPAIGN_TEMPLATES = {
    LifecycleStage.NEW: [
        {
            "name": "Welcome Series",
            "channels": [Channel.EMAIL, Channel.WEB],
            "subject_template": "Welcome to {{brand_name}}, {{first_name}}!",
            "ltp_days": 7,
        },
        {
            "name": "Feature Education",
            "channels": [Channel.EMAIL],
            "subject_template": "Here's how to get the most from {{brand_name}}",
            "ltp_days": 3,
        }
    ],
    LifecycleStage.ACTIVE: [
        {
            "name": "Engagement Booster",
            "channels": [Channel.EMAIL, Channel.PUSH],
            "subject_template": "{{first_name}}, exclusive offer inside",
            "ltp_days": 14,
        },
        {
            "name": "Upsell Opportunity",
            "channels": [Channel.EMAIL, Channel.WEB],
            "subject_template": "Customers like you love this: {{product_name}}",
            "ltp_days": 30,
        }
    ],
    LifecycleStage.AT_RISK: [
        {
            "name": "Win-Back Special",
            "channels": [Channel.EMAIL, Channel.SMS],
            "subject_template": "We miss you {{first_name}} - 20% off inside",
            "ltp_days": 7,
        }
    ],
}

# Discount policies
DISCOUNT_POLICY = {
    "new_customer": 0.15,  # 15% discount
    "at_risk": 0.20,  # 20% discount
    "vip": 0.10,  # 10% discount (smaller discount, higher CLV)
    "high_value_abandoned_cart": 0.25,  # 25% discount for high-value carts
}

# Tone guidelines for brand consistency
TONE_GUIDELINES = {
    "voice": "friendly, conversational, empowering",
    "style": "concise, action-oriented, benefit-focused",
    "forbidden_words": ["spam", "cheap", "limited", "urgent", "act now"],
    "required_elements": ["personalization (first name)", "clear CTA", "brand signature"],
    "examples": [
        {
            "good": "Hi Sarah, here's something we think you'll love based on your style.",
            "bad": "URGENT: Limited time offer - ACT NOW!",
        }
    ]
}

# Compliance rules
COMPLIANCE_RULES = {
    "gdpr": {
        "regions": ["EU"],
        "required_consent": True,
        "right_to_be_forgotten": True,
    },
    "can_spam": {
        "regions": ["US"],
        "required_elements": ["physical_address", "unsubscribe_link", "clear_subject"],
    },
    "ccpa": {
        "regions": ["CA"],
        "data_sale_opt_out": True,
        "deletion_sla_days": 45,
    }
}

# Email frequency cap rules
FREQUENCY_CAP_RULES = {
    "marketing": 3,  # per week
    "transactional": 999,  # no limit
    "promotional": 2,  # per week
    "newsletter": 1,  # per week
}
