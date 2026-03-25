# Cloth Retail Analytics Platform

An end-to-end data platform built in Microsoft Fabric to support a streetwear brand's accessories re-brand strategy. This project demonstrates data engineering, dimensional modeling, and solutions architecture thinking.

![Executive Dashboard](images/dashboard-executive.png)

---

## Business Context

**Cloth** is an online streetwear brand whose accessories line underperforms industry benchmarks (12% of revenue vs. 25-30% typical). Leadership is planning a Q2 re-brand and needs analytics to answer:

- Which customer segments are already buying accessories?
- How do accessories buyers differ from apparel-only customers?
- What pricing and regional strategies should inform the re-brand?

This platform consolidates customer, order, and product data into a unified view serving three stakeholders: CEO, Marketing Director, and COO.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA SOURCES                                  │
│                    Olist E-commerce Dataset (Kaggle)                    │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         BRONZE LAYER (Raw)                              │
│   raw_customers │ raw_orders │ raw_order_items │ raw_products │ ...     │
│                                                                         │
│   Loaded manually via CSV upload into Fabric Lakehouse                  │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         GOLD LAYER (Dimensional Model)                  │
│              Built via PySpark notebook (02_build_dimension_model)      │
│                                                                         │
│                           ┌──────────┐                                  │
│                           │ dim_date │                                  │
│                           └────┬─────┘                                  │
│                                │                                        │
│    ┌──────────────┐     ┌──────┴───────┐     ┌─────────────┐           │
│    │ dim_customer │─────│ fact_orders  │─────│ dim_product │           │
│    └──────────────┘     └──────┬───────┘     └─────────────┘           │
│                                │                                        │
│                         ┌──────┴───────┐                               │
│                         │dim_geography │                               │
│                         └──────────────┘                               │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         SEMANTIC LAYER                                  │
│              Power BI Semantic Model + DAX Measures                     │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                              │
│         Executive Summary │ Marketing Analysis │ Operations             │
└─────────────────────────────────────────────────────────────────────────┘
```

> **Architectural Note:** This project implements a simplified Bronze → Gold medallion pattern. The PySpark transformation notebook reads directly from raw bronze tables and builds the dimensional model in one step. In a production environment, a Silver layer would sit between Bronze and Gold to handle intermediate cleaning, null handling, deduplication, and data conformation before dimensional modeling. This design decision was intentional for a single-dataset project — the Olist data is well-structured enough that a full three-layer approach would add complexity without meaningful benefit at this scale.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Platform | Microsoft Fabric |
| Storage | Fabric Lakehouse (OneLake) |
| Transformation | PySpark Notebooks |
| Modeling | Star Schema (Dimensional) |
| Semantic | Power BI Semantic Model |
| Visualization | Power BI Reports |

---

## Quickstart

### Prerequisites
- Microsoft Fabric workspace (free trial or licensed)
- Access to the [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle

### Step 1 — Set Up Fabric Lakehouse
1. Create a new Fabric workspace
2. Create a Lakehouse named `cloth_analytics`

### Step 2 — Load Bronze Layer
Upload the following CSV files from the Olist dataset directly into the Lakehouse as tables:

| CSV File | Table Name |
|---|---|
| olist_customers_dataset.csv | raw_customers |
| olist_orders_dataset.csv | raw_orders |
| olist_order_items_dataset.csv | raw_order_items |
| olist_products_dataset.csv | raw_products |
| product_category_name_translation.csv | raw_category_translation |
| olist_order_payments_dataset.csv | raw_order_payments |

### Step 3 — Build the Dimensional Model
1. Import `notebooks/02_build_dimension_model.py` into your Fabric workspace as a new notebook
2. Attach it to your `cloth_analytics` lakehouse
3. Run all cells in order
4. Verify the gold layer tables are created (validation output prints at the end)

### Step 4 — Connect Power BI
1. Open Power BI via the Fabric workspace
2. Create a new semantic model pointing to the gold layer tables
3. Build DAX measures for revenue, order volume, and category mix
4. Build reports for each stakeholder persona (Executive, Marketing, Operations)

---

## Data Model

| Table | Rows | Description |
|---|---|---|
| dim_date | 774 | Date dimension with day/week/month/quarter/year attributes |
| dim_customer | 93,358 | Customer dimension with demographics and segmentation |
| dim_product | 32,951 | Product dimension with category mapping and price tiers |
| dim_geography | 4,310 | Geographic dimension with region groupings |
| fact_orders | 110,197 | Order line items with revenue and quantity measures |

![Lakehouse Tables](images/lakehouse-tables.png)

---

## Dashboards

### Executive Summary
High-level KPIs for CEO: revenue trends, category performance, regional breakdown.

![Executive Summary](images/dashboard-executive.png)

### Marketing Analysis
Customer segmentation for Marketing Director: demographics, segments, category performance by customer type.

![Marketing Analysis](images/dashboard-marketing.png)

### Operations
Operational metrics for COO: order volume patterns, day-of-week trends, fulfillment by region.

![Operations](images/dashboard-operations.png)

---

## Key Insights

- **Accessories = 11% of revenue ($1.45M)** — confirms underperformance vs. industry benchmark
- **25-34 age group is largest segment** — primary target for re-brand campaign
- **Southeast region dominates** (65% of revenue) — geographic expansion opportunity exists
- **97% of customers are "New"** — retention/loyalty is a challenge across all categories
- **Premium tier drives 56% of revenue** despite fewer orders — price tolerance exists

---

## Project Documentation

| Document | Description |
|---|---|
| [Business Context](docs/01-business-context.md) | Stakeholder requirements and success criteria |
| [Data Source Evaluation](docs/02-data-source-evaluation.md) | Assessment of candidate datasets |
| [Architecture Design](docs/03-architecture-design.md) | Dimensional model and technical decisions |
| [Vendor Evaluation](docs/04-vendor-evaluation.md) | Platform comparison and recommendation |

---

## What This Project Demonstrates

**Data Engineering**
- End-to-end pipeline from raw CSV to analytical model
- Medallion architecture (Bronze → Gold)
- PySpark transformations in Fabric notebooks

**Data Architecture**
- Dimensional modeling (star schema)
- Source-to-target mapping
- Data quality handling and validation

**Solutions Architecture**
- Business requirements gathering
- Platform evaluation with cost analysis
- Trade-off documentation and decision records

---

## Data Source

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — 100K orders from 2016-2018, used under CC BY-NC-SA 4.0 license.

## Data Source

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — 100K orders from 2016-2018, used under CC BY-NC-SA 4.0 license.
