"""
Execution channels for delivering personalized messages across multiple channels
"""
from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime

@dataclass
class ExecutionResult:
    """Result of message execution"""
    channel: str
    customer_id: str
    message_id: str
    status: str  # sent, queued, failed, skipped
    timestamp: str
    details: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "channel": self.channel,
            "customer_id": self.customer_id,
            "message_id": self.message_id,
            "status": self.status,
            "timestamp": self.timestamp,
            "details": self.details,
        }

class EmailChannel:
    """Email execution channel"""
    
    def send_email(self, customer_id: str, email: str, subject: str, body: str, html: str = "") -> ExecutionResult:
        """Send email message"""
        
        # In production: Call SendGrid API
        # For now: Simulate send
        
        message_id = f"email_{customer_id}_{int(datetime.utcnow().timestamp())}"
        
        result = ExecutionResult(
            channel="email",
            customer_id=customer_id,
            message_id=message_id,
            status="sent",
            timestamp=datetime.utcnow().isoformat() + "Z",
            details={
                "email": email,
                "subject": subject,
                "body_length": len(body),
                "html_sent": bool(html),
                "provider": "SendGrid",
            }
        )
        
        return result

class SMSChannel:
    """SMS execution channel"""
    
    def send_sms(self, customer_id: str, phone: str, message: str) -> ExecutionResult:
        """Send SMS message"""
        
        # In production: Call Twilio/SNS API
        # For now: Simulate send
        
        message_id = f"sms_{customer_id}_{int(datetime.utcnow().timestamp())}"
        
        result = ExecutionResult(
            channel="sms",
            customer_id=customer_id,
            message_id=message_id,
            status="sent",
            timestamp=datetime.utcnow().isoformat() + "Z",
            details={
                "phone": phone[-4:] + "***" if len(phone) > 4 else phone,
                "message_length": len(message),
                "provider": "Twilio",
            }
        )
        
        return result

class WhatsAppChannel:
    """WhatsApp execution channel"""
    
    def send_whatsapp(self, customer_id: str, phone: str, message: str, has_consent: bool = True) -> ExecutionResult:
        """Send WhatsApp message (requires consent)"""
        
        if not has_consent:
            return ExecutionResult(
                channel="whatsapp",
                customer_id=customer_id,
                message_id="",
                status="skipped",
                timestamp=datetime.utcnow().isoformat() + "Z",
                details={"reason": "No WhatsApp consent"},
            )
        
        # In production: Call WhatsApp API
        message_id = f"whatsapp_{customer_id}_{int(datetime.utcnow().timestamp())}"
        
        result = ExecutionResult(
            channel="whatsapp",
            customer_id=customer_id,
            message_id=message_id,
            status="sent",
            timestamp=datetime.utcnow().isoformat() + "Z",
            details={
                "phone": phone[-4:] + "***" if len(phone) > 4 else phone,
                "message_length": len(message),
                "template_used": False,
                "provider": "WhatsApp Business API",
            }
        )
        
        return result

class WebPersonalizationChannel:
    """Web personalization execution channel"""
    
    def set_web_personalization(self, customer_id: str, variations: Dict[str, str]) -> ExecutionResult:
        """Set web personalization rules"""
        
        # In production: Update CDN/personalization engine
        message_id = f"web_{customer_id}_{int(datetime.utcnow().timestamp())}"
        
        result = ExecutionResult(
            channel="web",
            customer_id=customer_id,
            message_id=message_id,
            status="sent",
            timestamp=datetime.utcnow().isoformat() + "Z",
            details={
                "variations_count": len(variations),
                "variation_types": list(variations.keys()),
                "ttl_hours": 24,
            }
        )
        
        return result

class PushNotificationChannel:
    """Mobile push notification execution channel"""
    
    def send_push(self, customer_id: str, title: str, body: str, platform: str = "all") -> ExecutionResult:
        """Send push notification"""
        
        # In production: Call Firebase/OneSignal API
        message_id = f"push_{customer_id}_{int(datetime.utcnow().timestamp())}"
        
        result = ExecutionResult(
            channel="push",
            customer_id=customer_id,
            message_id=message_id,
            status="sent",
            timestamp=datetime.utcnow().isoformat() + "Z",
            details={
                "title": title,
                "platform": platform,
                "provider": "Firebase Cloud Messaging",
            }
        )
        
        return result

class ExecutionManager:
    """Manages execution across all channels"""
    
    def __init__(self):
        self.email = EmailChannel()
        self.sms = SMSChannel()
        self.whatsapp = WhatsAppChannel()
        self.web = WebPersonalizationChannel()
        self.push = PushNotificationChannel()
        self.execution_history = []
    
    def execute_campaign(self, customer_id: str, customer_data: Dict[str, Any], campaign_data: Dict[str, Any]) -> List[ExecutionResult]:
        """Execute campaign across specified channels"""
        
        channels = campaign_data.get("channels", ["email"])
        results = []
        
        for channel in channels:
            if channel == "email":
                result = self.email.send_email(
                    customer_id,
                    customer_data.get("email"),
                    campaign_data.get("subject"),
                    campaign_data.get("body"),
                    campaign_data.get("html", ""),
                )
            elif channel == "sms":
                result = self.sms.send_sms(
                    customer_id,
                    customer_data.get("phone"),
                    campaign_data.get("sms_message", campaign_data.get("body")),
                )
            elif channel == "whatsapp":
                result = self.whatsapp.send_whatsapp(
                    customer_id,
                    customer_data.get("phone"),
                    campaign_data.get("whatsapp_message", campaign_data.get("body")),
                    customer_data.get("whatsapp_consent", False),
                )
            elif channel == "web":
                result = self.web.set_web_personalization(
                    customer_id,
                    campaign_data.get("web_variations", {}),
                )
            elif channel == "push":
                result = self.push.send_push(
                    customer_id,
                    campaign_data.get("push_title", "New offer"),
                    campaign_data.get("push_body", campaign_data.get("body")),
                )
            else:
                continue
            
            results.append(result)
            self.execution_history.append(result)
        
        return results
