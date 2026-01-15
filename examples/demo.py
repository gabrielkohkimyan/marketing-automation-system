"""
Example script demonstrating the marketing automation system
Run this to see the system in action
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import MarketingAutomationSystem, print_system_overview
from workflows import run_all_workflow_examples
import json

def demo_single_customer_processing():
    """Demonstrate processing a single customer"""
    
    print("\n" + "="*70)
    print("DEMO 1: Single Customer Processing (End-to-End)")
    print("="*70)
    
    system = MarketingAutomationSystem()
    
    # Process a customer with cart abandonment
    result = system.process_customer("cust_003", "cart_abandoned")
    
    print("\nDecision Details:")
    print(json.dumps(result["decision"], indent=2))
    
    print("\nGuardrail Checks:")
    for check_name, check in result["guardrails"]["checks"].items():
        status = "✓ PASS" if check["passed"] else "✗ FAIL"
        print(f"  {status}: {check_name} ({check['severity']})")

def demo_workflow_examples():
    """Demonstrate all workflow examples"""
    
    print("\n" + "="*70)
    print("DEMO 2: Workflow Examples")
    print("="*70)
    
    examples = run_all_workflow_examples()
    
    for workflow_name, result in examples.items():
        print(f"\n### {workflow_name.upper()}")
        print(f"Customer: {result.get('customer_id', 'N/A')}")
        print(f"Action: {result.get('decision', {}).get('action', 'N/A')}")
        print(f"Success Metrics:")
        for metric in result.get('success_metrics', []):
            print(f"  • {metric}")

def demo_agent_specifications():
    """Show specifications for each agent"""
    
    print("\n" + "="*70)
    print("DEMO 3: Agent Specifications")
    print("="*70)
    
    system = MarketingAutomationSystem()
    
    agents = [
        system.campaign_agent,
        system.lifecycle_agent,
        system.creative_agent,
        system.winback_agent,
    ]
    
    for agent in agents:
        specs = agent.get_agent_specs()
        
        print(f"\n### {specs['name']}")
        print(f"Purpose: {specs['purpose']}")
        print(f"\nInputs:")
        for inp in specs['inputs']:
            print(f"  • {inp}")
        print(f"\nActions:")
        for action in specs['actions']:
            print(f"  • {action}")
        print(f"\nSuccess Metrics:")
        for metric in specs['success_metrics']:
            print(f"  • {metric}")

def demo_guardrails():
    """Demonstrate guardrails in action"""
    
    print("\n" + "="*70)
    print("DEMO 4: Guardrails & Compliance Checks")
    print("="*70)
    
    system = MarketingAutomationSystem()
    
    # Test data
    test_customer = {
        "customer_id": "test_001",
        "first_name": "Test User",
        "engagement_score": 0.6,
        "emails_this_week": 2,
        "email_type": "marketing",
        "region": "EU",
        "gdpr_consent": True,
    }
    
    test_email = {
        "subject": "Don't miss out - limited time offer!!!",
        "body": "This is GUARANTEED to work! Click here now!",
        "from_address": "noreply@brand.com",
        "unsubscribe_link": "https://brand.com/unsubscribe",
        "physical_address": "123 Main St, City, Country",
    }
    
    # Run guardrails
    passed, results = system.guardrails.run_all_checks(test_customer, test_email)
    
    print(f"\nOverall Result: {'✓ PASSED' if passed else '✗ FAILED'}")
    print("\nDetailed Checks:")
    
    for check_name, check_result in results.items():
        status = "✓" if check_result.passed else "✗"
        severity_emoji = {
            "warning": "⚠️",
            "error": "🔴",
            "critical": "🚨",
        }.get(check_result.severity, "ℹ️")
        
        print(f"\n{status} {check_name} {severity_emoji}")
        print(f"  Severity: {check_result.severity}")
        print(f"  Details: {check_result.details}")

def demo_analytics():
    """Demonstrate analytics and A/B testing"""
    
    print("\n" + "="*70)
    print("DEMO 5: Analytics & A/B Testing")
    print("="*70)
    
    system = MarketingAutomationSystem()
    
    print("\nNorth Star Metric:")
    north_star = system.analytics.get_north_star_metric()
    print(f"  Current: ${north_star['current']:.2f}")
    print(f"  Target: ${north_star['target']:.2f}")
    print(f"  Progress: {north_star['progress_percent']:.0%}")
    
    print("\nKPI Dashboard:")
    kpis = system.analytics.get_kpi_dashboard()
    for kpi_name, kpi_data in kpis.items():
        print(f"\n  {kpi_name}:")
        print(f"    Current: {kpi_data['current']}")
        print(f"    Target: {kpi_data['target']}")
        print(f"    Progress: {kpi_data['progress']}")

def demo_full_system_processing():
    """Run complete end-to-end processing"""
    
    print("\n" + "="*70)
    print("DEMO 6: Full System Processing (3 Customer Scenarios)")
    print("="*70)
    
    system = MarketingAutomationSystem()
    
    scenarios = [
        ("cust_001", "lifecycle_change", "New customer onboarding"),
        ("cust_003", "cart_abandoned", "Abandoned cart recovery"),
        ("cust_004", "win_back", "Dormant customer reactivation"),
    ]
    
    for customer_id, trigger, description in scenarios:
        print(f"\n--- Scenario: {description} ---")
        result = system.process_customer(customer_id, trigger)
        
        if result["status"] == "success":
            print(f"✓ Success")
            print(f"  Decision: {result['decision']['action']}")
            print(f"  Guardrails: {'All Passed' if result['guardrails']['passed'] else 'Some Failed'}")
            if result['execution']:
                print(f"  Execution: {len(result['execution'])} channel(s) executed")
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")

def main():
    """Run all demonstrations"""
    
    try:
        print_system_overview()
    except UnicodeEncodeError:
        print("System initialized (Unicode output unavailable on this terminal)")
    
    # Run demos
    demo_agent_specifications()
    demo_guardrails()
    demo_analytics()
    demo_workflow_examples()
    demo_single_customer_processing()
    demo_full_system_processing()
    
    print("\n" + "="*70)
    print("ALL DEMONSTRATIONS COMPLETE")
    print("="*70)
    print("""
Next Steps:
1. Review the README.md for system overview
2. Check tech_stack.md for implementation details
3. Review rollout_plan.md for deployment strategy
4. Explore agents/ directory for agent implementations
5. Check workflows/ for workflow definitions
6. Review guardrails/ for compliance rules

Key Files:
  • main.py - System orchestration
  • config/config.py - Configuration & KPIs
  • agents/*.py - Individual agent implementations
  • workflows/*.py - Workflow definitions
  • guardrails/*.py - Compliance & safety
  • analytics/*.py - Metrics & measurement

To run the system in production:
  python main.py

To test against specific customer:
  system = MarketingAutomationSystem()
  system.process_customer("cust_001", "lifecycle_change")
    """)

if __name__ == "__main__":
    main()
