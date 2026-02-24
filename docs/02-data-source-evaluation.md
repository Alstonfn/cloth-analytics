# Cloth Analytics Platform
## Data Source Evaluation Document

**Prepared by:** Data Architecture Team  
**Date:** February 2026  
**Purpose:** Evaluate public datasets to simulate Cloth's e-commerce operations for analytics platform development

---

## Executive Summary

Three candidate datasets were evaluated for their ability to simulate Cloth's e-commerce data needs. Based on completeness, joinability, realism, and alignment with our business questions, we recommend **Option A: Brazilian E-Commerce Dataset (Olist)** as the primary data source.

---

## Evaluation Criteria

Each dataset was scored against five criteria essential for our use case:

| Criteria | Weight | Definition |
|----------|--------|------------|
| **Completeness** | 25% | Does it contain the fields needed to answer our business questions? |
| **Joinability** | 25% | Can we link customers → orders → products → geography? |
| **Volume** | 15% | Is it large enough to be realistic but within free-tier limits? |
| **Quality** | 20% | How clean is the data? What issues need handling? |
| **Realism** | 15% | Does it feel like plausible e-commerce data for our scenario? |

---

## Option A: Brazilian E-Commerce Public Dataset (Olist)

**Source:** Kaggle (https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
**License:** CC BY-NC-SA 4.0 (free for non-commercial use)  
**Cost:** Free

### Overview

Real commercial data from Olist, a Brazilian e-commerce marketplace. Contains 100,000+ orders from 2016-2018 across multiple sellers and product categories. This is actual transaction data, anonymized for public release.

### Available Tables

| Table | Records | Key Fields |
|-------|---------|------------|
| `olist_customers_dataset` | ~99,000 | customer_id, customer_unique_id, zip_code, city, state |
| `olist_orders_dataset` | ~100,000 | order_id, customer_id, order_status, purchase_timestamp, delivered_timestamp |
| `olist_order_items_dataset` | ~113,000 | order_id, product_id, seller_id, price, freight_value |
| `olist_products_dataset` | ~33,000 | product_id, category_name, weight, dimensions |
| `olist_order_payments_dataset` | ~104,000 | order_id, payment_type, payment_value, installments |
| `olist_order_reviews_dataset` | ~100,000 | order_id, review_score, review_comment |
| `olist_sellers_dataset` | ~3,000 | seller_id, zip_code, city, state |
| `olist_geolocation_dataset` | ~1M | zip_code, latitude, longitude, city, state |
| `product_category_name_translation` | ~71 | category_name_portuguese, category_name_english |

### Evaluation Scores

| Criteria | Score | Notes |
|----------|-------|-------|
| Completeness | 4/5 | Has orders, products, geography. Missing: customer demographics (age, gender). |
| Joinability | 5/5 | Excellent relational structure with clear foreign keys across all tables. |
| Volume | 5/5 | 100K orders is substantial but well within Fabric free tier limits. |
| Quality | 4/5 | Real data means some nulls and edge cases. Category names need translation. |
| Realism | 5/5 | Actual commercial data—doesn't get more realistic than this. |

**Weighted Score: 4.5/5**

### Gap Analysis for Cloth Use Case

| Business Question | Can This Dataset Answer It? | Gap |
|------------------|----------------------------|-----|
| Customer demographics | Partial | No age/gender. Would need to simulate or supplement. |
| Geographic concentration | Yes | Full geolocation data with lat/lng coordinates. |
| Product category performance | Yes | Categories available, though not fashion-specific. |
| Seasonal order patterns | Yes | 2 years of timestamped orders. |
| Average order value trends | Yes | Full pricing and payment data. |
| Repeat purchase rates | Yes | customer_unique_id enables cohort analysis. |

### Recommendation

**Use as primary dataset.** The relational structure is ideal for demonstrating data modeling skills. The missing demographics can be simulated using synthetic generation—this is actually a realistic scenario (many companies have transaction data but limited customer profile data).

---

## Option B: UK Online Retail Dataset (UCI)

**Source:** UCI Machine Learning Repository (https://archive.ics.uci.edu/dataset/352/online+retail)  
**License:** CC BY 4.0  
**Cost:** Free

### Overview

Transactional data from a UK-based online gift retailer, covering December 2010 to December 2011. Contains ~541,000 transaction records.

### Available Fields

Single denormalized table with:
- InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

### Evaluation Scores

| Criteria | Score | Notes |
|----------|-------|-------|
| Completeness | 2/5 | Very limited fields. No product categories, no customer details, no geography beyond country. |
| Joinability | 2/5 | Single flat table—nothing to join. No dimensional modeling opportunity. |
| Volume | 4/5 | Good transaction volume. |
| Quality | 3/5 | Known issues with cancelled orders (negative quantities), missing CustomerIDs. |
| Realism | 3/5 | Real data but from a gift shop, not fashion retail. |

**Weighted Score: 2.5/5**

### Recommendation

**Do not use as primary dataset.** The flat structure doesn't allow us to demonstrate data modeling skills.

---

## Final Recommendation

### Primary Dataset: Olist Brazilian E-Commerce
- Provides the relational structure needed to demonstrate dimensional modeling
- Real commercial data adds credibility
- Geographic and temporal depth supports our business questions

### Architecture Implication

```
[Olist Data]
     │
     ▼
┌─────────────────────────────────────┐
│         Bronze Layer                │
│   (Raw ingestion, minimal transform)│
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│      Transformation Layer           │
│  (Conform, dedupe, business logic)  │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│        Gold Layer                   │
│   (Dimensional model for analysis)  │
└─────────────────────────────────────┘
```

---

## Cost Estimate

| Item | Cost |
|------|------|
| Olist Dataset | $0 (free download) |
| Microsoft Fabric Trial | $0 (60-day trial) |
| Power BI Desktop | $0 (free) |
| **Total** | **$0** |
