# Cloth Analytics Platform
## Architecture Design Document

**Version:** 1.0  
**Prepared by:** Data Architecture Team  
**Date:** February 2026  
**Status:** Approved for Implementation

---

## Overview

**Goal:** Build a dimensional model that answers Cloth's business questions about customer demographics, geographic distribution, product performance, and seasonal trends.

**Pattern:** Medallion Architecture (Bronze → Gold) with Star Schema

---

## Data Flow

```
CSV Files (Kaggle)
       │
       ▼
┌─────────────────┐
│  BRONZE (Raw)   │  ← Raw CSV files, no transformation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GOLD (Curated) │  ← Dimensional model (star schema)
└────────┬────────┘
         │
         ▼
    Power BI
```

---

## Dimensional Model

```
              dim_date
                  │
dim_customer ── fact_orders ── dim_product
                  │
            dim_geography
```

### Fact Table

| fact_orders | |
|-------------|---|
| order_item_key | PK |
| customer_key | FK |
| product_key | FK |
| date_key | FK |
| geography_key | FK |
| quantity | |
| unit_price | |
| freight_value | |
| total_price | |
| order_total | |

**Grain:** One row per order line item

### Dimension Tables

**dim_customer**
| Column | Description |
|--------|-------------|
| customer_key | Surrogate primary key |
| customer_id | Natural key |
| customer_unique_id | Unique identifier across orders |
| age_group | Synthetic: '18-24', '25-34', '35-44', '45-54', '55+' |
| gender | Synthetic: 'Male', 'Female' |
| city | Customer city |
| state | Customer state |
| first_order_date | Acquisition date |
| customer_segment | 'New', 'Returning', 'Loyal' |

**dim_product**
| Column | Description |
|--------|-------------|
| product_key | Surrogate primary key |
| product_id | Natural key |
| product_category | Cloth business category |
| product_subcategory | Detailed category |
| product_line | 'Core Apparel', 'Accessories', 'Other' |
| price_tier | 'Budget', 'Mid-Range', 'Premium' |

**dim_date**
| Column | Description |
|--------|-------------|
| date_key | Surrogate key (YYYYMMDD) |
| full_date | Calendar date |
| day_of_week | Monday through Sunday |
| month | 1-12 |
| month_name | January through December |
| quarter | 1-4 |
| year | Calendar year |
| is_weekend | True for Saturday/Sunday |

**dim_geography**
| Column | Description |
|--------|-------------|
| geography_key | Surrogate primary key |
| city | City name |
| state | State code |
| state_name | Full state name |
| region | Southeast, South, Northeast, Central-West, North |

---

## Key Mappings

### Customer Segments
- **New:** 1 order
- **Returning:** 2-3 orders  
- **Loyal:** 4+ orders

### Price Tiers
- **Budget:** < $50
- **Mid-Range:** $50-$149
- **Premium:** $150+

### Product Lines (Olist → Cloth)
| Olist Category | Cloth Product Line |
|----------------|-------------------|
| fashion_male_clothing, fashion_female_clothing, fashion_shoes | Core Apparel |
| fashion_bags_accessories, watches_gifts, fashion_jewelry | Accessories |
| All others | Other |

---

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Fact grain** | Item-level | Maximum flexibility for product analysis |
| **Keys** | Surrogate + Natural | Performance for joins, traceability for debugging |
| **Demographics** | Synthetic (modeled) | Olist lacks age/gender; generated using hash for reproducibility |
| **SCD Type** | Type 1 (overwrite) | Historical snapshot, no live updates |
| **Architecture** | Medallion (Bronze/Gold) | Industry standard, clear lineage |

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Storage | Fabric Lakehouse |
| Ingestion | Fabric Data Pipeline |
| Transformation | Fabric Notebooks (PySpark) |
| Semantic | Power BI Dataset |
| Visualization | Power BI Reports |

---

## Implementation Phases

| Phase | Scope | Duration |
|-------|-------|----------|
| 1 | Infrastructure Setup | 1 session |
| 2 | Data Ingestion (Bronze) | 1-2 sessions |
| 3 | Transformation (Gold) | 2-3 sessions |
| 4 | Semantic Layer | 1-2 sessions |
| 5 | Reporting | 1-2 sessions |
