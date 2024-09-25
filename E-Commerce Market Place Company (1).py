#!/usr/bin/env python
# coding: utf-8

# #                       Marketing Analytics
# ##                                    For 
# ##           E-Commerce Market Place Company

# ### Business Objective:
# ##### The below are few Sample business questions to be addressed as part of this analysis. However this is not exhaustive list and you can add as many as analysis and provide insights on the same.

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import os
import datetime as dt
from datetime import datetime


# In[3]:


os.chdir('C:\\Users\\Adesh mishra\\OneDrive\\Desktop\\New folder (8)\\New folder')


# In[4]:


cust_df = pd.read_csv('CUSTOMERS.csv')
Geo_df = pd.read_csv('GEO_LOCATION.csv')
order_item=pd.read_csv('ORDER_ITEMS.csv')
order_pay=pd.read_csv('ORDER_PAYMENTS.csv')
order_review=pd.read_csv('ORDER_REVIEW_RATINGS.csv')
orders=pd.read_csv('ORDERS.csv')
sellers=pd.read_csv('SELLERS.csv')
product = pd.read_csv('PRODUCTS.csv')


# In[5]:


cust_df.head(3)


# In[6]:


Geo_df.head(3)


# In[7]:


order_item.head(3)


# In[8]:


order_pay.head(3)


# In[111]:


order_review.head()


# In[10]:


orders.head(3)


# In[11]:


sellers.head(3)


# In[12]:


product.head()


# In[13]:


# join the cust_df and orders 
cust_df_orders = pd.merge(cust_df,orders,left_on = 'customer_id',right_on ='customer_id',how ='left')
# join the seller and geo_df
seller_geo = pd.merge(sellers,Geo_df,left_on='seller_zip_code_prefix',right_on='geolocation_zip_code_prefix',how = 'left')
#join the cust_df_order and seller_geo
cust_order_sell_geo = pd.merge(cust_df_orders,seller_geo,left_on = 'customer_zip_code_prefix',right_on='geolocation_zip_code_prefix',how='left')
# join the oreder_item and order_pay
order_item_pay= pd.merge(order_item,order_pay,left_on='order_id',right_on='order_id',how ='left')
# join the order_itme_pay and order_review

order_item_pay_review = pd.merge(order_item_pay,order_review,left_on='order_id',right_on='order_id',how = 'left')
# join the order_item_pay_review
order_item_pay_review_pro = pd.merge(order_item_pay_review,product,left_on = 'product_id',right_on='product_id',how = 'left')
#final table
# join cust_order_sell_geo and order_item_pay_review
final_tbl = pd.merge(cust_order_sell_geo,order_item_pay_review_pro,left_on='order_id',right_on = 'order_id',how='left')


# In[14]:


cust_order_sell_geo.head(1)


# In[15]:


order_item_pay_review_pro .head(1)


# In[16]:


final_tbl.head(2)


# In[17]:


final_tbl = final_tbl.drop('seller_id_x',axis = 1)


# In[18]:


final_tbl.rename(columns={'seller_id_y':'seller_id'},inplace=True)


# In[19]:


final_tbl.info()


# In[20]:


final_tbl.isnull().sum()


# In[21]:


final_tbl = final_tbl.drop_duplicates()


# In[22]:


# Change data type to date columns for final_tbl
final_tbl['order_purchase_timestamp'] =pd.to_datetime(final_tbl.order_purchase_timestamp)
final_tbl['order_approved_at'] = pd.to_datetime(final_tbl.order_approved_at)
final_tbl['order_delivered_carrier_date']= pd.to_datetime(final_tbl.order_delivered_carrier_date)
final_tbl['order_delivered_customer_date'] = pd.to_datetime(final_tbl.order_delivered_customer_date)
final_tbl['order_estimated_delivery_date']=pd.to_datetime(final_tbl.order_estimated_delivery_date)

final_tbl['review_creation_date']=pd.to_datetime(final_tbl.review_creation_date)
final_tbl['review_answer_timestamp']= pd.to_datetime(final_tbl.review_answer_timestamp)
final_tbl['shipping_limit_date'] = pd.to_datetime(final_tbl.shipping_limit_date)


# In[23]:


final_tbl.info()


# In[24]:


final_tbl


# In[25]:


final_tbl.describe().head(3)


# In[26]:


final_tbl.columns


# ### Q1. Perform Detailed exploratory analysis

# ##### Q1a. Define & calculate high level metrics like (Total Revenue, Total quantity, Total products, Total categories, Total sellers, Total locations, Total channels, Total payment methods etc…)

# In[27]:


# Total Revenue
print('Total_revenue  : ',final_tbl['price'].sum())
#Total quantity
print('Total_quantity : ',final_tbl['order_id'].count())
# Total products
print('Total_products : ',final_tbl.product_id.nunique())
# Total categories
print('Total_categories :',final_tbl['product_category_name'].nunique())
# Total sellers
print('Total_sellers : ',final_tbl['seller_id'].nunique())
# Total locations
print('Total_locations :',final_tbl['geolocation_zip_code_prefix'].nunique())
# Total channels
print('Total_channels :',final_tbl['payment_type'].nunique())
# Total payment methods
print('Total_payment_methods : ',final_tbl['payment_type'].nunique())


# ###### Q1-b. Understanding how many new customers acquired every month

# In[28]:


final_tbl['month_year']=final_tbl['order_purchase_timestamp'].apply(lambda x : pd.Timestamp.strftime(x,format='%Y-%m'))


# In[29]:


new_cust_month_wise = final_tbl.drop_duplicates(subset=['customer_unique_id'],keep = 'first').groupby('month_year')['customer_unique_id'].nunique().reset_index()
new_cust_month_wise.head(3)


# In[30]:


new_cust_month_wise.plot(kind = 'bar',figsize = (6,3))
plt.ylabel('Count of customer')
plt.xlabel('Year_month')
plt.title('New customers acquired every month')
plt.show()


# ###### Q1-c. Understand the retention of customers on month on month basis
# 

# In[31]:


month_basis =  final_tbl.groupby(by=['month_year'])[['customer_unique_id']].count().reset_index()
month_basis.head(3)


# In[32]:


month_basis.customer_unique_id.sum()


# In[33]:


# join new_cust_month_wise and month_basis
new_cust_basis=pd.merge(new_cust_month_wise,month_basis,how = 'left',on = 'month_year')
new_cust_basis.head()


# In[34]:


new_cust_basis['reten_cust'] = new_cust_basis.customer_unique_id_y-new_cust_basis.customer_unique_id_x
new_cust_basis.head(3)


# In[35]:


new_cust_basis.plot(kind= 'bar',x='month_year',y = 'reten_cust',figsize=(6,3))
plt.ylabel('count of customers')
plt.title('Retention of customers on month on month basis')
plt.show()


# ###### Q1-d. How the revenues from existing/new customers on month on month basis
# 

# In[36]:


final_tbl['net_price'] = final_tbl.price + final_tbl.freight_value 


# In[37]:


ren_month = final_tbl.groupby('month_year')[['net_price']].sum()
ren_month.head(3)


# In[38]:


ren_month.plot(kind = 'bar',figsize = (6,3))
plt.ylabel('Total Amount')
plt.title('Total revenue on month on month basis')
plt.show()


# ###### Q1-e. Understand the trends/seasonality of sales, quantity by category, location, month, week, day, time, channel, payment method etc…
# 

# In[39]:


final_tbl['month'] = final_tbl.order_purchase_timestamp.apply(lambda x:pd.Timestamp.strftime(x,format = '%b'))


# In[40]:


final_tbl.head(3)


# In[41]:


# seasonality of sales,quantity by cagtegory
cat_qty = final_tbl.groupby(by=['product_category_name']).agg({'product_id':'count','price':'sum'}).reset_index().rename(columns={'product_id':'Qty','price':'sales'})


# In[42]:


cat_qty.head()


# In[43]:


# seasonality of sales,quantity by month
month_qty = final_tbl.groupby(by=['month']).agg({'product_id':'count','price':'sum'}).reset_index().rename(columns={'product_id':'Qty','price':'sales'})


# In[44]:


month_qty


# In[45]:


sale_by_channel =  final_tbl.groupby(by=['payment_type'])[['payment_value']].sum()
sale_by_channel


# In[46]:


sale_by_channel.plot(kind = 'bar',figsize = (5,3))
plt.xlabel('payment type')
plt.show()


# ###### Q1-f. Popular Products by month, seller, state, category.
# 

# In[47]:


popular_prod = final_tbl.groupby(by=['order_id','month_year','month'])[['payment_value']].sum().reset_index().sort_values(by='payment_value',ascending = False)
popular_prod.head()


# In[48]:


popular_prod_seller =  final_tbl.groupby(by=['seller_id'])[['payment_value']].sum().reset_index().sort_values(by='payment_value',ascending = False)
popular_prod_seller.head()


# In[49]:


popular_prod_state =  final_tbl.groupby(by=['customer_state'])[['payment_value']].sum().reset_index().sort_values(by='payment_value',ascending = False)
popular_prod_state.head()


# In[50]:


popular_prod_cat =  final_tbl.groupby(by=['product_category_name'])[['payment_value']].sum().reset_index().sort_values(by='payment_value',ascending = False)
popular_prod_cat.head()


# ###### Q1-g. Popular categories by state, month
# 

# In[51]:


popular_cat_state_month =  final_tbl.groupby(by = ['customer_state','month_year','product_category_name']).agg({'product_category_name':'count'}).rename(columns ={'product_category_name':'count_cat'}).reset_index().sort_values(by=['count_cat','month_year','customer_state'],ascending = False).drop_duplicates(subset = ['month_year','customer_state'],keep = 'first')
popular_cat_state_month.head()


# ###### Q1-h. List top 10 most expensive products sorted by price

# In[52]:


Top_10_prod = final_tbl.loc[:,['product_id','price']].drop_duplicates(subset =['product_id']).sort_values('price',ascending = False)
Top_10_prod.head(10)


# ### Q2. Performing Customers/sellers Segmentation
# 

# ##### Q2-a. Divide the customers into groups based on the revenue generated 
# 

# In[53]:


generat_tbl = final_tbl.groupby(by=['customer_unique_id'])[['payment_value']].sum().rename(columns = {'payment_value':'Amount_spend'})
generat_tbl.head()


# In[54]:


base = [((generat_tbl.Amount_spend>=0)&(generat_tbl.Amount_spend<=2000)),
       ((generat_tbl.Amount_spend>2000)&(generat_tbl.Amount_spend<=4000)),
       ((generat_tbl.Amount_spend>4000)&(generat_tbl.Amount_spend<=6000)),
       ((generat_tbl.Amount_spend>6000))]


# In[55]:


value = [('Low_sales_customer'),('Decent_sales_customer'),('medium_sales_customer'),('High_sales_customer')]


# In[56]:


generat_tbl['customer_group'] = np.select(base, value)
generat_tbl.head()


# In[57]:


cust_group_base_tbl=generat_tbl.groupby(by=['customer_group','customer_unique_id'])[['Amount_spend']].sum()
cust_group_base_tbl.head(10)


# In[ ]:





# ##### Q2-b. Divide the sellers into groups based on the revenue generated

# In[58]:


base_tbl = final_tbl.groupby('seller_id')[['payment_value']].sum().reset_index()
base_tbl.head()


# In[59]:


selle_divid =  [((base_tbl.payment_value>=0)&(base_tbl.payment_value<=2000)),
       ((base_tbl.payment_value>2000)&(base_tbl.payment_value<=4000)),
       ((base_tbl.payment_value>4000)&(base_tbl.payment_value<=6000)),
       ((base_tbl.payment_value>6000))]


# In[60]:


Value =  [('Low_sales_customer'),('Decent_sales_customer'),('medium_sales_customer'),('High_sales_customer')]


# In[61]:


base_tbl['seller_group'] = np.select(selle_divid,Value)


# In[62]:


base_tbl.groupby(by = ['seller_group','seller_id'])[['payment_value']].sum()


# ### 3. Cross-Selling (Which products are selling together)
# ##### Hint: We need to find which of the top 10 combinations of products are selling together in each transaction. (combination of 2 or 3 buying together)

# In[63]:


final_tbl.columns


# In[64]:


cross = final_tbl.groupby(by=['customer_id','product_category_name'])[['payment_value']].sum().reset_index().sort_values(by= 'payment_value',ascending=False)
cross.head()


# In[65]:


selling = cross.pivot(index = 'customer_id',columns = 'product_category_name',values ='payment_value')
selling.head()


# In[66]:


print('With given data cross-selling is not found')


# ### Q4. Payment Behaviour
# 

# ##### Q4-a. How customers are paying?
# 

# In[69]:


final_tbl.groupby('payment_type')[['order_id']].count().reset_index().sort_values('order_id',ascending = False)


# ##### Q4-b. Which payment channels are used by most customers?

# In[70]:


final_tbl.groupby(by=['payment_type'])[['order_item_id']].count().sort_values('order_item_id',ascending = False)


# ### Q5. Customer satisfaction towards category & product
# 

# ###### Q5-a. Which categories (top 10) are maximum rated & minimum rated?
# 

# In[82]:


max_min_cat = final_tbl.groupby('product_category_name')[['review_score']].sum().reset_index().sort_values('review_score',ascending = False)
max_min_cat.head(10)


# In[85]:


max_min_cat.sort_values('review_score',ascending = True) .head(10)


# In[ ]:





# ##### Q5-b. Which products (top10) are maximum rated & minimum rated?
# 

# In[107]:


min_max_rate = final_tbl.groupby(by=['product_id'])[['review_score']].sum().sort_values('review_score',ascending = False)
min_max_rate.head(10)


# In[108]:


min_max_rate.tail(10)


# ##### Q5-c. Average rating by location, seller, product, category, month etc.

# In[119]:


# Average rating by location
Avg_rat = final_tbl.groupby(by=['customer_state'])[['review_score']].mean()
Avg_rat.plot(kind = 'barh')
plt.show()


# In[120]:


# Average rating by seller
final_tbl.groupby(by=['seller_id'])[['review_score']].mean()


# In[122]:


# Average rating by product category name
final_tbl.groupby(by=['product_category_name'])[['review_score']].mean()


# In[127]:


# Average rating by month
final_tbl.groupby('month')[['review_score']].mean().plot(kind = 'barh',grid = True)
plt.show()


# In[ ]:




