#!/usr/bin/env python
# coding: utf-8

#  ##                                  CASE STUDY:
# ##                    CUSTOMER ANALYSIS FOR RETAIL

# #### BUSINESS PROBLEM:
# ###### A Retail store is required to analyze the day-to-day transactions and keep a track   of its customers spread across various locations along with their purchases/returns across various categories.

# #### Create a report and display the below calculated metrics, reports and inferences.

# In[1]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[2]:


os.chdir('C:\\Users\\Adesh mishra\\OneDrive\\Desktop\\python class\\Case Study 1 - Retail Case Study')


# In[3]:


customer_table = pd.read_csv('Customer.csv')
customer_table.head(2)


# In[4]:


product_table = pd.read_csv('prod_cat_info.csv')
product_table.head(2)


# In[5]:


transaction_table = pd.read_csv('Transactions.csv')
transaction_table.head(2)


# In[6]:


print(customer_table.shape)
print(product_table.shape)
print(transaction_table.shape)


# In[7]:


product_table.rename(columns={'prod_sub_cat_code':'prod_subcat_code'},inplace=True)


# In[8]:


product_table.head()


# ### 1. Merge the datasets Customers, Product Hierarchy and Transactions as Customer_Final. Ensure tokeep all customers who have done transactions with us and select the join type accordingly.

# In[9]:


prod_tran =pd.merge(left=product_table,right=transaction_table,left_on = 'prod_cat_code',right_on='prod_subcat_code',how='left')


# In[10]:


prod_tran.head()


# In[11]:


prod_tran.shape


# In[13]:


prod_tran.isnull().sum()


# In[14]:


Customer_final = pd.merge(prod_tran,customer_table,left_on='cust_id',right_on='customer_Id',how='left')
Customer_final


# In[15]:


Customer_final.info()


# In[16]:


Customer_final.shape


# In[17]:


prod_tran.shape


# #### both table CUSTOMER_TABLE and TRANSACTION_TABLE rows are same. That means all the transaction done at theRetail store are present in the customer finale table
# 
# 
# 

# In[18]:


Customer_final['DOB'] = pd.to_datetime(Customer_final['DOB'], format='%d-%m-%Y')


# In[19]:


Customer_final['DOB'].head(4)


# In[20]:


Customer_final['tran_date']=pd.to_datetime(Customer_final['tran_date'])


# In[21]:


Customer_final['tran_date'].head()


# In[22]:


Customer_final.duplicated().sum()


# In[23]:


# drop dupicate
Customer_final.drop_duplicates(inplace=True)


# In[24]:


Customer_final.duplicated().sum()


# ## 2. Prepare a summary report for the merged data set.
#  - a. Get the column names and their corresponding data types
#  - b. Top/Bottom 10 observations
#  - c. “Five-number summary” for continuous variables (min, Q1, median, Q3 and max)
#  - d. Frequency tables for all the categorical variables

# #### a.Get the column names and their corresponding data types

# In[25]:


Customer_final.columns


# In[26]:


print(Customer_final.dtypes)


# In[27]:


Customer_final.info()


# #### b. Top/Bottom 10 observations

# In[28]:


Customer_final.head(10)


# In[29]:


Customer_final.tail(10)


# ##### c. “Five-number summary” for continuous variables (min, Q1, median, Q3 and max)

# In[30]:


Customer_final.describe().T


# ##### d. Frequency tables for all the categorical variables

# In[31]:


Customer_final.loc[:,Customer_final.dtypes=='object'].describe()


# ### 3. Generate histograms for all continuous variables and frequency bars for categorical variables.

# In[32]:


Customer_final.columns


# In[33]:


conti_variable = Customer_final.loc[:,[ 'prod_subcat_code_x','prod_cat_code_y','Qty','Rate','Tax','total_amt']]


# In[34]:


conti_variable.columns


# In[35]:


def treat_outlier(x):
   return x.clip(lower=lr,upper=ur)


# In[36]:


for i in conti_variable:
    plt.figure(figsize=(5,3))
    conti_variable[i].plot(kind='hist')
    plt.show()


# #### bars chart  

# In[37]:


cate_variable = Customer_final.loc[:,Customer_final.dtypes=='object']


# In[38]:


cate_variable.head()


# In[39]:


plt.figure(figsize=(8,5))
sns.histplot(cate_variable['prod_cat'])
plt.xlabel('Product Category')
plt.show()


# In[40]:


plt.figure(figsize=(7,5))
cate_variable.groupby(by='prod_subcat')['prod_subcat'].count().plot(kind='barh')
plt.xlabel('Count')
plt.ylabel('Product Subcategory')
plt.show()


# In[41]:


plt.figure(figsize=(8,5))
sns.histplot(cate_variable['Store_type']).plot(kind='bar')
plt.xlabel('Store Type')
plt.show()


# In[42]:


plt.figure(figsize=(3,4))
sns.histplot(cate_variable['Gender'])
plt.xlabel('Gender')
plt.show()


# ### 4. Calculate the following information using the merged dataset :
# -  a. Time period of the available transaction data
# -  b. Count of transactions where the total amount of transaction was negative

# - a. Time period of the available transaction data

# In[43]:


Customer_final.sort_values(by='tran_date')


# In[44]:


min_date= Customer_final['tran_date'].min()
min_date


# In[45]:


max_date = Customer_final['tran_date'].max()
max_date


# In[46]:


print('Time period of the available transaction data is from 1/1/2012 to 9/9/2013')


# #### b. Count of transactions where the total amount of transaction was negative

# In[47]:


Customer_final.head()


# In[48]:


negative_transaction = Customer_final.loc[Customer_final['total_amt']<0,'transaction_id'].count()


# In[49]:


negative_transaction


# In[ ]:





# ### 5. Analyze which product categories are more popular among females vs male customers.

# In[50]:


Customer_final.head(3)


# In[51]:


prod_cat = Customer_final.groupby(by=['Gender','prod_cat'])[['Qty']].sum().reset_index()


# In[52]:


prod_cat


# In[53]:


prod_cat.pivot_table(index='Gender', values='Qty',aggfunc='sum',columns='prod_cat')


# In[ ]:





# ### 6. Which City code has the maximum customers and what was the percentage of customers from that city?

# In[54]:


city_code =  Customer_final.groupby(by='city_code')['customer_Id' ].count().sort_values(ascending = False)


# In[55]:


city_code


# In[56]:


percentage_cust = round((city_code[5.0]/city_code.sum())*100,2)


# In[57]:


percentage_cust


# ### 7. Which store type sells the maximum products by value and by quantity?

# In[58]:


Customer_final.head(2)


# In[59]:


Customer_final.groupby(by='Store_type')['Qty','Rate'].sum().sort_values(by='Qty',ascending=False)


# - e-shope store Type sell maximum products by value and by quantity

# ### 8. What was the total amount earned from the "Electronics" and "Clothing" categories fromFlagship Stores?

# In[60]:


Customer_final.head(2)


# In[61]:


store_cat =round(Customer_final.pivot_table(index='Store_type',columns='prod_cat',values='total_amt',aggfunc='sum'),2).T


# In[62]:


store_cat


# In[63]:


store_cat.loc[['Electronics','Clothing'],'Flagship store']


# In[64]:


store_cat.loc[['Electronics','Clothing'],'Flagship store'].sum()


# ### 9. What was the total amount earned from "Male" customers under the "Electronics" category?

# In[65]:


Customer_final.head(1)


# In[66]:


Ern_amt=round(Customer_final.pivot_table(index='prod_cat',columns='Gender',values='total_amt',aggfunc='sum'),2)


# In[67]:


Ern_amt


# In[68]:


Ern_amt.loc['Electronics','M']


# - total amount earned from Male customers under the Electronics category is 15664513.15

# ### 10. How many customers have more than 10 unique transactions, after removing all transactions which have any negative amounts?

# In[69]:


customer_tran = Customer_final.loc[Customer_final['total_amt']>0]


# In[70]:


customer_tran.head(2)


# In[71]:


unique_tran =customer_tran.groupby(by=['customer_Id','prod_cat','prod_subcat'])['transaction_id'].count().reset_index()


# In[72]:


unique_tran


# In[73]:


unique_tran[unique_tran['transaction_id']>10]


# - There are no unique transactions greater than 10 

# ### 11. For all customers aged between 25 - 35, find out:
# -  a. What was the total amount spent for “Electronics” and “Books” product categories?
# -  b. What was the total amount spent by these customers between 1st Jan, 2014 to 1st Mar, 2014?

# In[74]:


Customer_final.head(2)


# In[111]:


import datetime


# In[114]:


Customer_final['Age'] = datetime.datetime.now().year - pd.to_datetime(Customer_final['DOB']).dt.year


# In[120]:


customer_Age=Customer_final[(Customer_final.Age>=25)&(Customer_final.Age<=35)]


# In[135]:


customer_Age.head()


#  #### a. What was the total amount spent for “Electronics” and “Books” product categories?

# In[128]:


amt_spent=customer_Age.loc[(Customer_final.prod_cat=='Electronics')|(Customer_final.prod_cat=='Books')].reset_index()


# In[131]:


amt_spent.groupby(by='prod_cat')['total_amt'].sum()


# In[132]:


amt_spent.groupby(by='prod_cat')['total_amt'].sum().sum()


# #### b. What was the total amount spent by these customers between 1st Jan, 2014 to 1st Mar, 2014?

# In[137]:


customer_Age.head(1)


# In[151]:


spent_amt=customer_Age.loc[(customer_Age.tran_date>=pd.to_datetime('2014-01-01'))&(customer_Age.tran_date<=pd.to_datetime('2014-03-01'))]


# In[152]:


spent_amt


# In[153]:


spent_amt['total_amt'].sum()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




