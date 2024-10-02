# streamlit_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load all datasets
customers_dataset = pd.read_csv('data/customers_dataset.csv')
geolocation_dataset = pd.read_csv('data/geolocation_dataset.csv')
order_items_dataset = pd.read_csv('data/order_items_dataset.csv')
order_payments_dataset = pd.read_csv('data/order_payments_dataset.csv')
order_reviews_dataset = pd.read_csv('data/order_reviews_dataset.csv')
orders_dataset = pd.read_csv('data/orders_dataset.csv')
product_category_name_translation = pd.read_csv('data/product_category_name_translation.csv')
products_dataset = pd.read_csv('data/products_dataset.csv')
sellers_dataset = pd.read_csv('dta/sellers_dataset.csv')

# Merge datasets
customers_orders = pd.merge(orders_dataset, customers_dataset, on='customer_id', how='left')
orders_payments = pd.merge(customers_orders, order_payments_dataset, on='order_id', how='left')
orders_items = pd.merge(orders_payments, order_items_dataset, on='order_id', how='left')
orders_reviews = pd.merge(orders_items, order_reviews_dataset, on='order_id', how='left')
orders_products = pd.merge(orders_reviews, products_dataset, on='product_id', how='left')
final_merged_data = pd.merge(orders_products, sellers_dataset, on='seller_id', how='left')

# Imputation of missing values
for col in final_merged_data.columns:
    if final_merged_data[col].dtype == 'object':
        if final_merged_data[col].isnull().mean() < 0.5:
            final_merged_data[col].fillna(final_merged_data[col].mode()[0], inplace=True)
        else:
            final_merged_data.drop(columns=[col], inplace=True)
    else:
        if final_merged_data[col].isnull().mean() < 0.5:
            final_merged_data[col].fillna(final_merged_data[col].median(), inplace=True)
        else:
            final_merged_data.drop(columns=[col], inplace=True)

# Streamlit page title
st.title('Business Analysis Dashboard')

# Analysis for Question 1: Product Categories by Demand and Geographic Distribution
st.subheader("Question 1: Product Categories by Demand and Geographic Distribution")

merged_data = pd.merge(final_merged_data, product_category_name_translation, on='product_category_name', how='left')

# Top 5 product categories by demand
category_demand = merged_data['product_category_name_english'].value_counts().reset_index()
category_demand.columns = ['Product Category', 'Order Count']
top_categories = category_demand.head()

st.write("Top 5 Product Categories by Demand")
st.dataframe(top_categories, use_container_width=True)

# Plot the top product categories
fig, ax = plt.subplots()
sns.barplot(x='Order Count', y='Product Category', data=top_categories, palette="Blues_d", ax=ax)
ax.set_title('Top 5 Product Categories by Demand')
st.pyplot(fig)

# Geographic Distribution by City
geo_demand = merged_data.groupby(['product_category_name_english', 'customer_city']).size().reset_index(name='Order Count')
geo_top_categories = geo_demand[geo_demand['product_category_name_english'].isin(top_categories['Product Category'])]

st.write("Geographic Distribution for Top Product Categories")
st.dataframe(geo_top_categories.head(), use_container_width=True)

# Plot Geographic Distribution
fig, ax = plt.subplots(figsize=(12, 8))
sns.scatterplot(x='customer_city', y='Order Count', hue='product_category_name_english', data=geo_top_categories, palette="Set1", s=100, ax=ax)
ax.set_title('Geographic Distribution of Top Product Categories by City')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
st.pyplot(fig)

# Analysis for Question 2: Payment Methods and Demographics
st.subheader("Question 2: Payment Methods and Demographics")

# Payment method preferences
payment_preferences = final_merged_data['payment_type'].value_counts().reset_index()
payment_preferences.columns = ['Payment Type', 'Count']

st.write("Overall Payment Method Preferences")
st.dataframe(payment_preferences, use_container_width=True)

# Plot payment method preferences
fig, ax = plt.subplots()
sns.barplot(x='Count', y='Payment Type', data=payment_preferences, palette="Blues_d", ax=ax)
ax.set_title('Overall Payment Method Preferences')
st.pyplot(fig)

# Payment preferences by state
payment_by_state = final_merged_data.groupby(['customer_state', 'payment_type']).size().reset_index(name='Count')
st.write("Payment Method Preferences by State")
st.dataframe(payment_by_state, use_container_width=True)

# Plot payment preferences by state
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='Count', y='customer_state', hue='payment_type', data=payment_by_state, palette="Set1", ax=ax)
ax.set_title('Payment Method Preferences by State')
st.pyplot(fig)

# Payment preferences by city (optional)
payment_by_city = final_merged_data.groupby(['customer_city', 'payment_type']).size().reset_index(name='Count')
st.write("Payment Method Preferences by City (Top 20 Cities)")
st.dataframe(payment_by_city.head(20), use_container_width=True)

# Plot payment preferences by city
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='Count', y='customer_city', hue='payment_type', data=payment_by_city.head(20), palette="Set2", ax=ax)
ax.set_title('Payment Method Preferences by City (Top 20 Cities)')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
st.pyplot(fig)

# Merge necessary datasets for clustering
orders_customers = pd.merge(orders_dataset, customers_dataset, on='customer_id', how='left')
orders_payments = pd.merge(orders_customers, order_payments_dataset, on='order_id', how='left')
orders_items = pd.merge(orders_payments, order_items_dataset, on='order_id', how='left')

# Calculate Q1 and Q3 for payment_value
q1 = orders_items['payment_value'].quantile(0.25)
q3 = orders_items['payment_value'].quantile(0.75)

# Define rules for clustering based on payment_value quartiles
def customer_segment_clustering(row):
    if row['payment_value'] < q1:
        return 'Low Spend'
    elif q1 <= row['payment_value'] <= q3:
        return 'Medium Spend'
    elif row['payment_value'] > q3:
        return 'High Spend'

# Apply rule-based clustering based on customer spending segments
orders_items['cluster'] = orders_items.apply(customer_segment_clustering, axis=1)

# Streamlit page title
st.title('Customer Segmentation Based on Spending')

# Show the resulting clustered data
st.subheader('Clustered Data')
clustered_data = orders_items[['order_id', 'customer_id', 'payment_value', 'cluster']]
st.dataframe(clustered_data.head())

# Count the number of orders per cluster
cluster_counts = clustered_data['cluster'].value_counts().reset_index()
cluster_counts.columns = ['Cluster', 'Number of Orders']

# Show the cluster counts
st.subheader('Number of Orders per Customer Segment')
st.dataframe(cluster_counts)

# Plot the clusters
st.subheader('Order Distribution by Customer Spending Cluster')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Cluster', y='Number of Orders', data=cluster_counts, palette="Set2", ax=ax)
ax.set_title('Order Distribution by Customer Spending Cluster')
ax.set_xlabel('Cluster')
ax.set_ylabel('Number of Orders')
st.pyplot(fig)
