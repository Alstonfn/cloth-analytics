# Cloth Analytics Platform
## Vendor Evaluation & Platform Recommendation

**Prepared for:** Cloth Executive Leadership  
**Prepared by:** Data Architecture Team  
**Date:** February 2026  
**Document Status:** Final Recommendation

---

## Executive Summary

Cloth is implementing a data analytics platform to support a strategic re-brand of its accessories line. While accessories currently represent a smaller portion of revenue, leadership believes this category is underperforming relative to its potential. Better customer insights will inform repositioning, pricing, and marketing strategies to grow accessories as a key revenue driver.

**Recommendation:** Microsoft Fabric

**Rationale:** Fabric provides the best balance of capability, cost, and time-to-value for Cloth's current scale and team composition. The unified platform reduces integration complexity, and the familiar Power BI interface minimizes training requirements. As Cloth scales, the architecture we've designed can migrate to more specialized platforms if needed.

**Estimated Annual Cost:** $3,600 - $7,200 (depending on usage)

---

## Business Requirements Recap

### Strategic Context

Cloth's accessories line (bags, watches, jewelry) currently accounts for approximately 12% of total revenue. Leadership has identified this as a growth opportunity—comparable streetwear brands see 25-30% of revenue from accessories. To inform the re-brand strategy, Cloth needs deeper insight into:

- Which customer segments are already purchasing accessories
- How accessories performance varies by region and demographics
- What price points resonate with different customer segments
- Whether accessories buyers differ from core apparel customers

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Consolidate customer, order, and product data into unified view | Must Have |
| FR-2 | Support demographic analysis for marketing targeting | Must Have |
| FR-3 | Enable geographic analysis of customer distribution | Must Have |
| FR-4 | Provide seasonal trend visibility for demand planning | Must Have |
| FR-5 | Self-service dashboards for three stakeholder groups | Must Have |
| FR-6 | Daily data refresh capability | Should Have |
| FR-7 | Support future accessories sales data integration | Should Have |
| FR-8 | Role-based access control | Could Have |

### Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Query response time | < 5 seconds for dashboard interactions |
| NFR-2 | Data freshness | Daily batch updates acceptable |
| NFR-3 | Availability | 99.5% uptime during business hours |
| NFR-4 | Scalability | Support 10x data growth over 3 years |
| NFR-5 | Total cost of ownership | < $10,000 annually at current scale |

### Technical Constraints

- **Team Size:** Small data team (1-2 people)
- **Existing Skills:** Strong Power BI, SQL, Python; limited Spark experience
- **Data Volume:** ~500K records currently; projected 2M in 3 years
- **Integration Needs:** CSV/API ingestion; no complex streaming requirements
- **Timeline:** Platform operational within 8 weeks

---

## Platforms Evaluated

### Option A: Microsoft Fabric

**Overview:** Unified analytics platform combining data lake, data warehouse, data engineering, data science, and business intelligence in a single SaaS offering.

**Architecture Pattern:**
```
Data Sources → OneLake (Lakehouse) → Notebooks/Dataflows → Semantic Model → Power BI
```

**Key Characteristics:**
- Single vendor, fully integrated platform
- Native Power BI integration
- Pay-per-use consumption model (Capacity Units)
- Built on Delta Lake / Parquet
- Familiar Microsoft ecosystem

### Option B: Databricks + Power BI

**Overview:** Databricks provides the lakehouse platform for storage and transformation; Power BI connects for visualization.

**Architecture Pattern:**
```
Data Sources → DBFS/Unity Catalog → Delta Lake → Databricks SQL → Power BI
```

**Key Characteristics:**
- Industry-leading Spark performance
- Mature MLOps capabilities
- Strong data engineering features
- Requires Power BI integration (additional cost)
- Steeper learning curve

### Option C: Snowflake + dbt + Power BI

**Overview:** Snowflake provides cloud data warehouse; dbt handles transformation; Power BI connects for visualization.

**Architecture Pattern:**
```
Data Sources → Snowflake Stage → dbt transformations → Snowflake Tables → Power BI
```

**Key Characteristics:**
- Separation of storage and compute
- SQL-centric transformation with dbt
- Strong data sharing capabilities
- Multi-tool integration required
- Per-second compute billing

### Option D: AWS Native (S3 + Glue + Redshift + QuickSight)

**Overview:** Fully AWS-native stack using S3 for storage, Glue for ETL, Redshift for warehousing, and QuickSight for visualization.

**Architecture Pattern:**
```
Data Sources → S3 → Glue ETL → Redshift → QuickSight
```

**Key Characteristics:**
- Deep AWS ecosystem integration
- QuickSight less mature than Power BI
- More components to manage
- Strong if already AWS-invested
- Requires more DevOps capability

---

## Evaluation Criteria

Criteria were weighted based on Cloth's priorities:

| Criteria | Weight | Description |
|----------|--------|-------------|
| **Time to Value** | 25% | How quickly can we deliver a working solution? |
| **Total Cost of Ownership** | 20% | Platform costs + labor + training over 3 years |
| **Team Skill Alignment** | 20% | Match with existing team capabilities |
| **Scalability** | 15% | Ability to handle 10x growth |
| **Feature Completeness** | 10% | Coverage of functional requirements |
| **Vendor Risk** | 10% | Platform maturity, market position, lock-in risk |

---

## Comparison Matrix

### Scoring (1-5 scale: 1=Poor, 5=Excellent)

| Criteria | Weight | Fabric | Databricks | Snowflake+dbt | AWS Native |
|----------|--------|--------|------------|---------------|------------|
| Time to Value | 25% | 5 | 3 | 3 | 2 |
| Total Cost of Ownership | 20% | 4 | 3 | 3 | 3 |
| Team Skill Alignment | 20% | 5 | 2 | 3 | 2 |
| Scalability | 15% | 4 | 5 | 5 | 4 |
| Feature Completeness | 10% | 4 | 5 | 4 | 4 |
| Vendor Risk | 10% | 4 | 4 | 4 | 4 |
| **Weighted Score** | 100% | **4.45** | **3.35** | **3.45** | **2.90** |

### Scoring Rationale

**Microsoft Fabric:**
- Time to Value (5): Unified platform eliminates integration work; native Power BI means no new visualization tool
- TCO (4): Consumption model favorable at low volume; included Power BI capacity
- Skill Alignment (5): Team already proficient in Power BI and SQL
- Scalability (4): Auto-scaling capabilities; may require capacity planning at very high scale
- Feature Completeness (4): Covers all requirements; real-time capabilities still maturing
- Vendor Risk (4): Microsoft financially stable; some platform lock-in; Fabric is relatively new (2023)

**Databricks:**
- Time to Value (3): Requires separate BI tool setup; steeper notebook learning curve
- TCO (3): Competitive compute pricing but Power BI licensing adds cost
- Skill Alignment (2): Team would need significant Spark/notebook training
- Scalability (5): Industry-leading for large-scale data processing
- Feature Completeness (5): Excellent data engineering and ML capabilities
- Vendor Risk (4): Strong market position; well-funded; potential Spark ecosystem shifts

**Snowflake + dbt:**
- Time to Value (3): Multi-tool setup required; dbt learning curve
- TCO (3): Competitive but three separate tools to license/manage
- Skill Alignment (3): SQL-centric (good) but dbt requires learning; Power BI familiar
- Scalability (5): Excellent auto-scaling; separation of storage/compute
- Feature Completeness (4): Strong warehousing; requires additional tools for data science
- Vendor Risk (4): Strong market position; multi-vendor dependency

**AWS Native:**
- Time to Value (2): Multiple services to configure and integrate; QuickSight learning curve
- TCO (3): Can be cost-effective but requires careful management; many moving parts
- Skill Alignment (2): Team lacks AWS experience; QuickSight unfamiliar
- Scalability (4): Can scale but requires more hands-on management
- Feature Completeness (4): All capabilities available but distributed across services
- Vendor Risk (4): AWS highly stable; significant lock-in; complex to migrate away

---

## Cost Analysis (3-Year Projection)

### Assumptions
- Current data volume: 500K records (~500 MB)
- Year 3 projected volume: 2M records (~2 GB)
- Daily refresh during business hours
- 3 dashboard users (executives)
- 1-2 data team members

### Microsoft Fabric

| Component | Year 1 | Year 2 | Year 3 |
|-----------|--------|--------|--------|
| Fabric Capacity (F2) | $3,600 | $3,600 | $5,400* |
| Power BI Pro (included) | $0 | $0 | $0 |
| Training | $500 | $0 | $0 |
| **Annual Total** | **$4,100** | **$3,600** | **$5,400** |

*Assumes capacity upgrade in Year 3 due to growth

**3-Year Total: $13,100**

### Databricks + Power BI

| Component | Year 1 | Year 2 | Year 3 |
|-----------|--------|--------|--------|
| Databricks (DBUs) | $4,800 | $4,800 | $7,200 |
| Power BI Pro (3 users) | $360 | $360 | $360 |
| Cloud Storage | $100 | $150 | $200 |
| Training | $2,000 | $500 | $0 |
| **Annual Total** | **$7,260** | **$5,810** | **$7,760** |

**3-Year Total: $20,830**

### Snowflake + dbt + Power BI

| Component | Year 1 | Year 2 | Year 3 |
|-----------|--------|--------|--------|
| Snowflake Compute | $3,600 | $3,600 | $5,400 |
| Snowflake Storage | $200 | $300 | $400 |
| dbt Cloud (Team) | $1,200 | $1,200 | $1,200 |
| Power BI Pro (3 users) | $360 | $360 | $360 |
| Training | $1,500 | $500 | $0 |
| **Annual Total** | **$6,860** | **$5,960** | **$7,360** |

**3-Year Total: $20,180**

### AWS Native

| Component | Year 1 | Year 2 | Year 3 |
|-----------|--------|--------|--------|
| S3 Storage | $50 | $75 | $100 |
| Glue ETL | $600 | $600 | $900 |
| Redshift Serverless | $3,600 | $3,600 | $5,400 |
| QuickSight (3 users) | $720 | $720 | $720 |
| Training | $2,500 | $500 | $0 |
| **Annual Total** | **$7,470** | **$5,495** | **$7,120** |

**3-Year Total: $20,085**

### Cost Summary

| Platform | 3-Year TCO | Rank |
|----------|------------|------|
| Microsoft Fabric | $13,100 | 1 |
| Snowflake + dbt | $20,180 | 2 |
| AWS Native | $20,085 | 3 |
| Databricks | $20,830 | 4 |

---

## Recommendation

### Primary Recommendation: Microsoft Fabric

**Why Fabric is the right choice for Cloth today:**

1. **Fastest path to value.** Cloth needs insights to inform the accessories re-brand strategy this quarter. Fabric's unified platform eliminates integration work between separate tools. We estimate 4-6 weeks to production versus 8-12 weeks for alternatives.

2. **Skill alignment reduces risk.** The team already knows Power BI. Fabric extends that knowledge rather than requiring new tool adoption. This reduces both timeline and the risk of implementation failure.

3. **Cost-effective at current scale.** At ~500K records with daily batch processing, Fabric's consumption model is highly efficient. The included Power BI capacity eliminates separate licensing.

4. **Room to grow.** Fabric can handle Cloth's projected 10x growth. If the accessories re-brand succeeds and requirements eventually exceed Fabric's capabilities (e.g., complex ML workloads, multi-cloud requirements), the Delta Lake foundation allows migration to Databricks with minimal rework.

### When to Reconsider This Decision

Fabric may not remain the optimal choice if:

- **Data volume exceeds 10M+ records** with complex transformations → Consider Databricks for compute performance
- **Multi-cloud strategy becomes mandatory** → Consider Snowflake for cloud portability
- **Advanced ML/AI becomes core to the business** → Consider Databricks for MLOps maturity
- **Real-time streaming becomes critical** → Re-evaluate all options for streaming capabilities

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Fabric platform lock-in | Architecture uses standard Delta Lake format; data portable to Databricks if needed |
| Fabric still maturing (launched 2023) | Design for simplicity; avoid bleeding-edge features until stable |
| Single vendor dependency | Document architecture decisions; maintain option to migrate |

---

## Implementation Considerations

### Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Microsoft Fabric                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│   │   Bronze    │────▶│   Silver    │────▶│    Gold     │   │
│   │   (Raw)     │     │  (Cleaned)  │     │  (Curated)  │   │
│   └─────────────┘     └─────────────┘     └─────────────┘   │
│         │                   │                   │           │
│         └───────────────────┴───────────────────┘           │
│                     OneLake (Lakehouse)                     │
│                                                             │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│   │  Notebooks  │     │  Semantic   │     │   Power BI  │   │
│   │  (PySpark)  │     │    Model    │     │   Reports   │   │
│   └─────────────┘     └─────────────┘     └─────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Implementation Phases

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| 1. Foundation | Week 1-2 | Workspace setup, Bronze layer ingestion |
| 2. Transformation | Week 3-4 | Silver/Gold layers, dimensional model |
| 3. Semantic Layer | Week 5 | Power BI semantic model, DAX measures |
| 4. Reporting | Week 6 | Stakeholder dashboards |
| 5. Hardening | Week 7-8 | Testing, documentation, training |

### Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Platform operational | Week 8 | All dashboards accessible to stakeholders |
| Query performance | < 5 seconds | 95th percentile dashboard interaction time |
| Data freshness | Daily by 8 AM | Automated monitoring |
| Stakeholder adoption | 3/3 executives | Weekly active users after 30 days |
| Budget adherence | < $5,000 Year 1 | Monthly cost tracking |

---

## Appendix A: Detailed Feature Comparison

| Feature | Fabric | Databricks | Snowflake+dbt | AWS Native |
|---------|--------|------------|---------------|------------|
| Lakehouse storage | Yes - OneLake | Yes - DBFS/Unity | Partial - Requires S3 | Yes - S3 |
| SQL analytics | Yes - Native | Yes - Databricks SQL | Yes - Native | Yes - Redshift |
| Spark processing | Yes - Native | Yes - Best-in-class | No - Requires add-on | Partial - Glue |
| Transformation | Yes - Notebooks/Dataflows | Yes - Notebooks | Yes - dbt | Partial - Glue/Step Functions |
| BI/Visualization | Yes - Power BI (native) | Partial - Requires integration | Partial - Requires integration | Yes - QuickSight |
| Real-time streaming | Partial - Maturing | Yes - Structured Streaming | Partial - Snowpipe | Yes - Kinesis |
| Machine learning | Partial - Basic | Yes - MLflow native | Partial - Requires add-on | Yes - SageMaker |
| Data sharing | Yes - OneLake shortcuts | Yes - Delta Sharing | Yes - Native | Partial - Complex |
| Governance | Yes - Purview integration | Yes - Unity Catalog | Yes - Native + Horizon | Partial - Multiple tools |

---

## Appendix B: Decision Log

| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
| Feb 2026 | Selected Fabric over Databricks | Skill alignment, cost, time-to-value | Data Architecture Team |
| Feb 2026 | Chose Lakehouse over Warehouse mode | Flexibility for future unstructured data | Data Architecture Team |
| Feb 2026 | Star schema over OBT | Query performance, stakeholder familiarity | Data Architecture Team |
| Feb 2026 | Medallion architecture (Bronze/Silver/Gold) | Industry standard, clear lineage | Data Architecture Team |

---

## Document Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Data Architect | | | |
| Project Sponsor | | | |
| Finance Approval | | | |

---

*This document should be reviewed annually or when significant changes occur in data volume, business requirements, or platform capabilities.*
