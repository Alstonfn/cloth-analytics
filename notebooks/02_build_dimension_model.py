# ## 02_build_dimension_model

# Dimension model for Cloth_analytics

# In[1]:


# Welcome to your new notebook
# Type here in the cell editor to add code!
# =============================================================================
# Cloth Analytics Platform - Dimensional Model Build
# =============================================================================
# This notebook transforms Bronze (raw) tables into Gold (dimensional model)
# 
# Target tables:
#   - dim_customer
#   - dim_product  
#   - dim_date
#   - dim_geography
#   - fact_orders
# =============================================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window

print("Setup complete. Ready to build dimensional model.")


# In[2]:


# =============================================================================
# dim_date - Date dimension
# =============================================================================

# Get min and max dates from orders
date_range = spark.sql("""
    SELECT 
        MIN(CAST(order_purchase_timestamp AS DATE)) as min_date,
        MAX(CAST(order_purchase_timestamp AS DATE)) as max_date
    FROM raw_orders
""").collect()[0]

min_date = date_range['min_date']
max_date = date_range['max_date']

print(f"Date range: {min_date} to {max_date}")

# Generate date spine
dim_date = spark.sql(f"""
    SELECT 
        CAST(DATE_FORMAT(date, 'yyyyMMdd') AS INT) as date_key,
        date as full_date,
        DATE_FORMAT(date, 'EEEE') as day_of_week,
        DAY(date) as day_of_month,
        WEEKOFYEAR(date) as week_of_year,
        MONTH(date) as month,
        DATE_FORMAT(date, 'MMMM') as month_name,
        QUARTER(date) as quarter,
        YEAR(date) as year,
        CASE WHEN DAYOFWEEK(date) IN (1, 7) THEN true ELSE false END as is_weekend
    FROM (
        SELECT EXPLODE(SEQUENCE(
            CAST('{min_date}' AS DATE), 
            CAST('{max_date}' AS DATE), 
            INTERVAL 1 DAY
        )) as date
    )
""")

# Write to table
dim_date.write.format("delta").mode("overwrite").saveAsTable("dim_date")

print(f"dim_date created: {dim_date.count()} rows")
dim_date.show(5)


# In[3]:


# =============================================================================
# dim_geography - Geography dimension
# =============================================================================

dim_geography = spark.sql("""
    SELECT 
        ROW_NUMBER() OVER (ORDER BY customer_state, customer_city) as geography_key,
        customer_city as city,
        customer_state as state,
        CASE customer_state
            WHEN 'SP' THEN 'São Paulo'
            WHEN 'RJ' THEN 'Rio de Janeiro'
            WHEN 'MG' THEN 'Minas Gerais'
            WHEN 'RS' THEN 'Rio Grande do Sul'
            WHEN 'PR' THEN 'Paraná'
            WHEN 'SC' THEN 'Santa Catarina'
            WHEN 'BA' THEN 'Bahia'
            WHEN 'DF' THEN 'Distrito Federal'
            WHEN 'ES' THEN 'Espírito Santo'
            WHEN 'GO' THEN 'Goiás'
            WHEN 'PE' THEN 'Pernambuco'
            WHEN 'CE' THEN 'Ceará'
            WHEN 'PA' THEN 'Pará'
            WHEN 'MT' THEN 'Mato Grosso'
            WHEN 'MA' THEN 'Maranhão'
            WHEN 'MS' THEN 'Mato Grosso do Sul'
            WHEN 'PB' THEN 'Paraíba'
            WHEN 'RN' THEN 'Rio Grande do Norte'
            WHEN 'AL' THEN 'Alagoas'
            WHEN 'PI' THEN 'Piauí'
            WHEN 'SE' THEN 'Sergipe'
            WHEN 'RO' THEN 'Rondônia'
            WHEN 'TO' THEN 'Tocantins'
            WHEN 'AC' THEN 'Acre'
            WHEN 'AP' THEN 'Amapá'
            WHEN 'AM' THEN 'Amazonas'
            WHEN 'RR' THEN 'Roraima'
            ELSE customer_state
        END as state_name,
        CASE 
            WHEN customer_state IN ('SP', 'RJ', 'MG', 'ES') THEN 'Southeast'
            WHEN customer_state IN ('PR', 'SC', 'RS') THEN 'South'
            WHEN customer_state IN ('BA', 'PE', 'CE', 'MA', 'PB', 'RN', 'AL', 'SE', 'PI') THEN 'Northeast'
            WHEN customer_state IN ('DF', 'GO', 'MT', 'MS') THEN 'Central-West'
            WHEN customer_state IN ('AM', 'PA', 'AC', 'RO', 'RR', 'AP', 'TO') THEN 'North'
            ELSE 'Unknown'
        END as region
    FROM raw_customers
    GROUP BY customer_city, customer_state
""")

dim_geography.write.format("delta").mode("overwrite").saveAsTable("dim_geography")

print(f"dim_geography created: {dim_geography.count()} rows")
dim_geography.show(5)


# In[5]:


# =============================================================================
# dim_product - Product dimension with Cloth category mapping
# =============================================================================

dim_product = spark.sql("""
    WITH product_prices AS (
        SELECT 
            product_id,
            AVG(price) as avg_price
        FROM raw_order_items
        GROUP BY product_id
    ),
    translated AS (
        SELECT 
            p.product_id,
            COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') as category_english,
            p.product_category_name as category_original,
            pp.avg_price
        FROM raw_products p
        LEFT JOIN raw_category_translation t 
            ON p.product_category_name = t.product_category_name
        LEFT JOIN product_prices pp
            ON p.product_id = pp.product_id
    )
    SELECT 
        ROW_NUMBER() OVER (ORDER BY product_id) as product_key,
        product_id,
        category_english as product_subcategory,
        CASE 
            WHEN category_english IN ('fashion_male_clothing', 'fashion_female_clothing', 
                'fashion_childrens_clothing', 'fashion_sport', 'fashio_female_clothing') 
                THEN 'Apparel'
            WHEN category_english IN ('fashion_bags_accessories', 'watches_gifts', 
                'fashion_jewelry', 'luggage_accessories') 
                THEN 'Accessories'
            WHEN category_english IN ('fashion_shoes', 'baby_gear') 
                THEN 'Footwear'
            WHEN category_english IN ('sports_leisure', 'fashion_underwear_beach') 
                THEN 'Activewear'
            ELSE 'Other'
        END as product_category,
        CASE 
            WHEN category_english IN ('fashion_male_clothing', 'fashion_female_clothing', 
                'fashion_childrens_clothing', 'fashion_shoes', 'fashion_sport',
                'fashion_underwear_beach', 'fashio_female_clothing') 
                THEN 'Core Apparel'
            WHEN category_english IN ('fashion_bags_accessories', 'watches_gifts', 
                'fashion_jewelry', 'luggage_accessories') 
                THEN 'Accessories'
            ELSE 'Other'
        END as product_line,
        CASE 
            WHEN avg_price < 50 THEN 'Budget'
            WHEN avg_price >= 50 AND avg_price < 150 THEN 'Mid-Range'
            WHEN avg_price >= 150 THEN 'Premium'
            ELSE 'Unknown'
        END as price_tier
    FROM translated
""")

dim_product.write.format("delta").mode("overwrite").saveAsTable("dim_product")

print(f"dim_product created: {dim_product.count()} rows")
dim_product.show(5)


# In[8]:


# =============================================================================
# dim_customer - Customer dimension with synthetic demographics
# =============================================================================

# Build customer dimension with order-based segmentation
# Demographics are synthetically generated using hash for reproducibility
dim_customer = spark.sql("""
    WITH customer_orders AS (
        SELECT 
            c.customer_unique_id,
            MIN(c.customer_id) as customer_id,
            MIN(c.customer_city) as city,
            MIN(c.customer_state) as state,
            MIN(CAST(o.order_purchase_timestamp AS DATE)) as first_order_date,
            COUNT(DISTINCT o.order_id) as order_count
        FROM raw_customers c
        JOIN raw_orders o ON c.customer_id = o.customer_id
        WHERE o.order_status = 'delivered'
        GROUP BY c.customer_unique_id
    )
    SELECT 
        ROW_NUMBER() OVER (ORDER BY customer_unique_id) as customer_key,
        customer_id,
        customer_unique_id,
        -- Synthetic demographics based on hash for reproducibility
        -- Distribution: 18-24 (15%), 25-34 (35%), 35-44 (25%), 45-54 (15%), 55+ (10%)
        CASE 
            WHEN ABS(HASH(customer_unique_id)) % 100 < 15 THEN '18-24'
            WHEN ABS(HASH(customer_unique_id)) % 100 < 50 THEN '25-34'
            WHEN ABS(HASH(customer_unique_id)) % 100 < 75 THEN '35-44'
            WHEN ABS(HASH(customer_unique_id)) % 100 < 90 THEN '45-54'
            ELSE '55+'
        END as age_group,
        -- Distribution: Female (60%), Male (40%) - typical fashion retail
        CASE 
            WHEN ABS(HASH(CONCAT(customer_unique_id, 'g'))) % 10 < 6 THEN 'Female'
            ELSE 'Male'
        END as gender,
        city,
        state,
        first_order_date,
        CASE 
            WHEN order_count = 1 THEN 'New'
            WHEN order_count BETWEEN 2 AND 3 THEN 'Returning'
            ELSE 'Loyal'
        END as customer_segment
    FROM customer_orders
""")

dim_customer.write.format("delta").mode("overwrite").saveAsTable("dim_customer")

print(f"dim_customer created: {dim_customer.count()} rows")
dim_customer.show(5)

# Show demographic distribution
print("\nAge distribution:")
dim_customer.groupBy("age_group").count().orderBy("age_group").show()

print("Gender distribution:")
dim_customer.groupBy("gender").count().show()


# In[9]:


# =============================================================================
# fact_orders - Fact table at order line item grain
# =============================================================================

fact_orders = spark.sql("""
    WITH order_totals AS (
        SELECT 
            order_id,
            SUM(price + freight_value) as order_total
        FROM raw_order_items
        GROUP BY order_id
    )
    SELECT 
        ROW_NUMBER() OVER (ORDER BY oi.order_id, oi.order_item_id) as order_item_key,
        oi.order_id,
        dc.customer_key,
        dp.product_key,
        CAST(DATE_FORMAT(CAST(o.order_purchase_timestamp AS DATE), 'yyyyMMdd') AS INT) as date_key,
        dg.geography_key,
        1 as quantity,
        CAST(oi.price AS DECIMAL(10,2)) as unit_price,
        CAST(oi.freight_value AS DECIMAL(10,2)) as freight_value,
        CAST(oi.price AS DECIMAL(10,2)) as total_price,
        CAST(ot.order_total AS DECIMAL(10,2)) as order_total
    FROM raw_order_items oi
    JOIN raw_orders o ON oi.order_id = o.order_id
    JOIN raw_customers c ON o.customer_id = c.customer_id
    JOIN dim_customer dc ON c.customer_unique_id = dc.customer_unique_id
    JOIN dim_product dp ON oi.product_id = dp.product_id
    JOIN dim_geography dg ON c.customer_city = dg.city AND c.customer_state = dg.state
    JOIN order_totals ot ON oi.order_id = ot.order_id
    WHERE o.order_status = 'delivered'
""")

fact_orders.write.format("delta").mode("overwrite").saveAsTable("fact_orders")

print(f"fact_orders created: {fact_orders.count()} rows")
fact_orders.show(5)


# In[10]:


# =============================================================================
# Validation - Verify all Gold layer tables
# =============================================================================

tables = ['dim_date', 'dim_geography', 'dim_product', 'dim_customer', 'fact_orders']

print("=" * 60)
print("GOLD LAYER VALIDATION")
print("=" * 60)

for table in tables:
    count = spark.sql(f"SELECT COUNT(*) as cnt FROM {table}").collect()[0]['cnt']
    print(f"{table}: {count:,} rows")

print("=" * 60)

# Quick data quality check - verify fact table joins work
print("\nSample joined query (Revenue by Product Category):")
spark.sql("""
    SELECT 
        p.product_category,
        COUNT(*) as order_lines,
        ROUND(SUM(f.total_price), 2) as total_revenue
    FROM fact_orders f
    JOIN dim_product p ON f.product_key = p.product_key
    GROUP BY p.product_category
    ORDER BY total_revenue DESC
""").show()
