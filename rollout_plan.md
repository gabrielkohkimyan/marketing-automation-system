# Measurement & Rollout Plan

## North Star Metric

### Revenue per Marketing Touch (RpMT)

**Definition**: Total marketing-attributed revenue / Total number of customer touches (emails, SMS, push, web)

**Formula**: 
```
RpMT = Total Revenue Attribution / Total Touches
     = $XXXX / Number of Emails + SMS + Push + Web Events
```

**Baseline** (current): $0.45 per touch  
**Target** (Year 1): $0.61 per touch (+35% improvement)  
**Stretch** (Year 2): $1.05 per touch (+133% improvement)

**Rationale**: 
- Single metric capturing both effectiveness (higher revenue) and efficiency (fewer touches needed)
- Aligns marketing incentives with business outcomes
- Directly measurable from marketing ops and finance data
- Resists gaming (can't just increase touches without revenue)

---

## Supporting Metrics

### Conversion & Revenue Metrics
| Metric | Baseline | Target | Unit | Business Impact |
|--------|----------|--------|------|-----------------|
| Conversion Rate | 2.5% | 3.1% | % of touches | +24% |
| Average Order Value | $85 | $95 | $ | +11% |
| Customer Lifetime Value | $500 | $700 | $ | +40% |
| Revenue per Email | $0.35 | $0.50 | $ | +43% |
| Revenue per SMS | $0.15 | $0.25 | $ | +67% |

### Engagement Metrics
| Metric | Baseline | Target | Unit | Business Impact |
|--------|----------|--------|------|-----------------|
| Email Open Rate | 22% | 28.6% | % | +30% |
| Email Click Rate | 3% | 4.05% | % | +35% |
| SMS Open Rate | 35% | 45% | % | +29% |
| Push Click Rate | 5% | 7% | % | +40% |

### Efficiency Metrics
| Metric | Baseline | Target | Unit | Business Impact |
|--------|----------|--------|------|-----------------|
| Cost per Acquisition | $45 | $30 | $ | -33% |
| Marketing Efficiency Ratio | 2.0:1 | 3.5:1 | Revenue:Spend | +75% |
| Email Frequency (touches/customer/month) | 8 | 5 | # | -38% |
| Campaign Launch Time | 5 days | 1.5 days | days | -70% |

### Retention & Loyalty Metrics
| Metric | Baseline | Target | Unit | Business Impact |
|--------|----------|--------|------|-----------------|
| Churn Rate | 5% | 4% | % annual | -20% |
| Retention Rate (12 months) | 95% | 96% | % | +1pp |
| Win-Back Conversion Rate | 8% | 15% | % | +88% |
| Repeat Purchase Rate | 65% | 75% | % | +15% |

### Quality & Compliance Metrics
| Metric | Baseline | Target | Unit | Business Impact |
|--------|----------|--------|------|-----------------|
| Spam Complaint Rate | 0.3% | <0.1% | % | -67% |
| Hard Bounce Rate | 3% | <1% | % | -67% |
| List Decay Rate | 0.5% | 0.2% | % monthly | -60% |
| Compliance Violations | 5/month | 0 | # per month | -100% |
| Brand Tone Consistency | 80% | 95% | % of content | +19% |

---

## Experimentation Framework

### A/B Testing Approach

**Test Cadence**:
- High-volume campaigns: Weekly
- Medium-volume: Bi-weekly
- Low-volume: Monthly or combined test groups

**Statistical Rigor**:
- Minimum sample size: 1,000 per variant
- Confidence level: 95%
- Power: 80% (detect 15%+ lift)
- Duration: Minimum 7 days (avoid day-of-week bias)

**Analysis Tool**: Mixpanel + custom Python scripts

**Test Allocation Strategy** (Multi-Armed Bandit):
- Control: 30% of traffic (proven baseline)
- Challenger 1: 35% of traffic
- Challenger 2: 35% of traffic
- At 95% confidence, promote winner; retire loser

**Sample Calculation**:
```
For 2-way test, detecting 15% relative uplift:
n = 2 × (1.96 + 0.84)² × (0.025×0.975 + 0.029×0.971) / (0.029 - 0.025)²
n ≈ 1,500 per variant
Total: 3,000 samples = ~10% of 30k monthly cohort
```

### Testing Calendar

| Week | Campaign | Test Type | Hypothesis |
|------|----------|-----------|-----------|
| 1-2 | Welcome Email | Copy variants (3 versions) | Conversational tone → +15% CTR |
| 3-4 | Cart Recovery | Incentive levels (2 levels) | 20% discount → +25% conversion |
| 5-6 | Engagement | Send time optimization | 10am sendtime → +20% open |
| 7-8 | Lifecycle | Subject line variants | Personalized → +30% open |
| 9-12 | Retention | Win-back offers (segments) | VIP special → +40% reactivation |

---

## 3-Phase Rollout Plan

### Phase 1: MVP (Weeks 1-4) - Foundation & Validation
**Goal**: Prove core agent functionality, establish guardrails, validate hypothesis

**Scope**:
- 5% of active customers (~5,000 customers)
- Campaign Orchestration Agent (email only)
- Basic frequency capping + compliance guardrails
- Manual review for all decisions
- Daily reporting dashboard

**Key Deliverables**:
1. Campaign Agent production deployment
2. Email execution channel integrated with SendGrid
3. Guardrails framework (frequency cap, compliance)
4. Manual review queue system
5. Basic KPI dashboard (daily reporting)
6. Audit logging infrastructure

**Success Criteria**:
- ✓ Zero compliance violations
- ✓ System uptime: 99%+
- ✓ Manual review time: <5 min per decision
- ✓ Email delivery rate: >95%
- ✓ Baseline metrics established
- ✓ Team trained on system operation

**Resources**:
- 2 Backend Engineers
- 1 Product Manager
- 1 Operations/QA Lead
- 1 Data Analyst (part-time)

**Milestones**:
- Week 1: Core agent framework + email channel
- Week 2: Guardrails implementation + audit logs
- Week 3: Manual review queue + monitoring
- Week 4: Pilot launch, monitoring, optimization

**KPIs to Track**:
- Uptime %
- Manual review SLA (target: <5 min)
- Email delivery rate
- Initial conversion baseline
- Guardrail violation rate

---

### Phase 2: Scale (Weeks 5-12) - Multi-Agent & Personalization
**Goal**: Deploy all agents, enable LLM-powered personalization, automate guardrails

**Scope**:
- 50% of active customers (~50,000 customers)
- All 4 agents deployed (Campaign, Lifecycle, Creative, Win-Back)
- Multi-channel execution (email + SMS + web)
- LLM-powered copy generation with human-in-the-loop review
- Automated A/B testing framework (80% of campaigns)
- ML-based guardrails (reduce manual review to 20%)
- Weekly learning loop

**Key Deliverables**:
1. Lifecycle & Retention Agent → production
2. Creative Testing Agent → production
3. Abandoned Cart & Win-Back Agent → production
4. LLM integration (GPT-4) for copy generation
5. SMS/WhatsApp channels fully operational
6. A/B testing framework (Mixpanel integration)
7. ML-based guardrail scoring
8. Enhanced analytics dashboard (real-time KPIs)
9. Feedback loop for continuous learning

**Success Criteria**:
- ✓ 20%+ conversion rate improvement
- ✓ 70%+ reduction in manual reviews (via ML)
- ✓ Email open rate: 25%+
- ✓ SMS delivery rate: >98%
- ✓ System latency: <2 seconds (p95)
- ✓ A/B test coverage: 80%+ of campaigns
- ✓ Creative quality score: 85%+

**Resources**:
- 4 Backend Engineers
- 2 Product Managers
- 2 Operations/QA
- 2 Data Scientists (ML guardrails)
- 1 LLM Specialist

**Milestones**:
- Week 5-6: Lifecycle Agent + SMS channel
- Week 7-8: Creative Testing Agent
- Week 9-10: LLM integration + copy generation
- Week 11-12: A/B testing framework, feedback loop

**KPIs to Track**:
- Conversion rate improvement
- Manual review % (target: <20% of decisions)
- A/B test statistical significance rate
- LLM copy approval rate (human review)
- Creative quality score

---

### Phase 3: Optimize (Weeks 13-16+) - Advanced ML & Autonomy
**Goal**: Full automation, predictive intelligence, maximum ROI

**Scope**:
- 100% customer coverage
- Behavioral & predictive targeting
  - Churn risk scoring (predict who will churn in next 30 days)
  - Conversion propensity (predict who's likely to buy)
  - Optimal send time personalization per customer
- Advanced A/B testing (multi-armed bandit)
- Autonomous budget allocation across channels
- Minimal human oversight (automated guardrails)
- Real-time dashboards with anomaly detection
- Predictive win-back campaigns
- Cross-sell/upsell intelligence

**Key Deliverables**:
1. Churn prediction model (RF/XGBoost)
2. Conversion propensity model
3. Optimal send-time ML model
4. Budget allocation algorithm
5. Multi-armed bandit testing framework
6. Anomaly detection system
7. Predictive personalization engine
8. Advanced dashboards with BI tooling (Tableau/Looker)
9. Autonomous decision execution (minimal review)

**Success Criteria**:
- ✓ Achieve all Phase 1 & 2 targets
- ✓ 35% conversion rate improvement (target achieved)
- ✓ Revenue per touch: $0.61+ (target achieved)
- ✓ Customer LTV: +40% (target achieved)
- ✓ Churn: -20% (target achieved)
- ✓ ROI: 10x+ achieved
- ✓ Autonomous decision rate: 95%+
- ✓ System uptime: 99.9%+

**Resources**:
- 5 Backend Engineers
- 3 Product Managers
- 3 Operations/QA
- 2 Data Scientists
- 1 ML Ops Engineer

**Milestones**:
- Week 13-14: Predictive models (churn, conversion, send-time)
- Week 15-16: Budget allocation, anomaly detection
- Week 17-20: Multi-armed bandit testing
- Week 21-24: Full production scaling and optimization

**KPIs to Track**:
- All metrics from Phase 1 & 2
- Churn prediction accuracy (AUC)
- Revenue impact from each agent
- Autonomous decision quality (approval rate >99%)
- System scalability (throughput, latency)

---

## Rollout by Cohort

### Cohort Strategy
```
Week 1-4 (Phase 1): Early Adopter Segment (5%)
  - High engagement customers (engagement_score > 0.7)
  - Email subscribers only
  - No chat/SMS complexity

Week 5-12 (Phase 2): Early Growth (50%)
  - All engagement levels
  - Multi-channel (email + SMS)
  - More complex decision logic

Week 13+ (Phase 3): Full Scale (100%)
  - All customer segments
  - All channels + web personalization
  - Maximum automation
```

### Gradual Rollout Schedule
```
Week 1-2:   5% of target cohort
Week 3-4:   20% of target cohort
Week 5-6:   40% of target cohort
Week 7-8:   70% of target cohort
Week 9-12:  100% of Phase 2 cohort
Week 13+:   Rolling expansion to 100% of all customers
```

---

## Measurement Approach

### Real-Time Monitoring
- **Dashboard**: Updated every 1 hour with key metrics
- **Alerts**: Anomaly detection (drop in metrics > 2 std dev)
- **SLA Tracking**: System uptime, latency, error rates

### Weekly Review
- Every Monday: Review KPI performance vs. targets
- Identify underperforming cohorts or agents
- Adjust campaign allocation or guardrail thresholds

### Monthly Analysis
- Full impact analysis with statistical testing
- Attribution modeling (which agent contributed to lift)
- Cohort comparison (test vs. control)
- Cost analysis and ROI tracking

### Learning Loop
- Every 7 days: Retrain guardrail models
- Every 14 days: Update LLM prompts based on top performers
- Every 30 days: Retrain predictive models
- Every quarter: Strategy adjustment based on learnings

---

## Risk Management & Contingency

### Risk 1: System doesn't hit conversion targets
**Probability**: Medium | **Impact**: High  
**Mitigation**:
- Extensive A/B testing in Phase 1 to validate assumptions
- Fallback: Adjust personalization strategy, increase testing scope
- Decision point: Week 4 go/no-go for Phase 2

### Risk 2: Compliance issues emerge
**Probability**: Low | **Impact**: Critical  
**Mitigation**:
- Guardrails review with legal team before Phase 1
- Conservative frequency caps in early phases
- Audit every decision for first month
- Decision point: Any violation → halt and review

### Risk 3: LLM integration underperforms
**Probability**: Medium | **Impact**: Medium  
**Mitigation**:
- Extensive human review in Phase 2 (80% sample)
- A/B test LLM copy vs. templates
- Fallback: Revert to template-based copy
- Alternative: Try Claude or Llama if GPT-4 underperforms

### Risk 4: High manual review burden (guardrails too strict)
**Probability**: Medium | **Impact**: Low  
**Mitigation**:
- Start conservative, relax thresholds weekly
- Track review SLA and volume
- Implement ML model to reduce reviews (Phase 2)
- Target: <20% manual review rate by Phase 2

---

## Success Dashboard

### Phase 1 Success = All These TRUE:
- [ ] 0 compliance violations
- [ ] 99%+ uptime
- [ ] <5 min avg manual review time
- [ ] Baseline metrics locked in
- [ ] Team fully trained

### Phase 2 Success = All These TRUE:
- [ ] 20%+ conversion improvement
- [ ] 70%+ reduction in manual reviews
- [ ] 80%+ A/B test coverage
- [ ] 85%+ creative quality score
- [ ] <2sec p95 latency

### Phase 3 Success = All These TRUE:
- [ ] 35% conversion improvement (all targets hit)
- [ ] 95%+ autonomous decisions
- [ ] 10x+ ROI achieved
- [ ] 99.9%+ uptime
- [ ] $2M+ annual revenue impact

---

## Post-Rollout Optimization

### Quarters 2-4 (Months 4-12)
- Expand creative personalization (images, product recs)
- Advanced segmentation (50+ segments)
- Channel expansion (mobile app, web chat)
- Predictive insights (when to contact each customer)
- Customer cohort analysis (who benefits most)

### Year 2+
- International expansion (localization)
- Competitive intelligence integration
- Predictive inventory/supply chain alignment
- Margin optimization (personalized pricing)
- Customer lifetime value maximization

---

**Document Version**: 1.0  
**Last Updated**: January 15, 2026  
**Status**: Ready for Execution
