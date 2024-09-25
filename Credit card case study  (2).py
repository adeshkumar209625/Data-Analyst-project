#!/usr/bin/env python
# coding: utf-8

#  ###                                     CASE STUDY:
#  #####            DATA EXPLORATORY ANALYSIS FOR CREDIT CARD DATA

# ### BUSINESS PROBLEM:
# 
# ###  In order to effectively produce quality decisions in the modern credit card        industry, knowledge  must be gained through effective data analysis and modeling. Through the  use of dynamic datadriven decision-making tools and procedures,    information can be gathered to successfully evaluate all aspects of credit card operations. PSPD Bank has banking operations in   more than 50 countries across the globe. Mr. Jim Watson, CEO, wants to evaluate areas of bankruptcy, fraud, and  collections, respond to customer requests for help with proactive offers  and service

# #### Following are some of Mr. Watson’s questions to a Consultant (like you) to understand the customers spend & repayment behavior.

# In[164]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# #### import the dataset

# In[165]:


os.chdir('C:\\Users\\Adesh mishra\\OneDrive\\Desktop\\New folder (7)')


# In[166]:


Credit = pd.read_excel('Credit Card Data.xlsx')


# In[167]:


customer = pd.read_csv('Customer Acqusition.csv')


# In[168]:


Repayment = pd.read_csv('Repayment.csv')


# In[169]:


spend = pd.read_csv('spend.csv')


# In[170]:


Credit.head(3)


# In[171]:


customer.head(3)


# In[172]:


Repayment.head()


# In[173]:


Repayment.dropna(axis=0,how = 'all')


# In[174]:


repay = Repayment.dropna(axis=1,how='all')


# In[175]:


repay.head()


# In[176]:


spend.head(3)


# In[177]:


print(Credit.shape)
print(customer.shape)
print(Repayment.shape)
print(spend.shape)


# In[178]:


repay.shape


# In[179]:


repay.dtypes


# In[180]:


Credit.dtypes


# In[181]:


customer.dtypes


# In[182]:


Repayment.dtypes


# In[183]:


spend.dtypes


# In[184]:


Credit.isnull().sum()


# ### 1. In the above dataset,

# #### a. In case age is less than 18, replace it with mean of age values.
# 
# 

# In[185]:


customer[customer.Age<18]


# In[186]:


mean_age =customer['Age'].mean()


# In[187]:


print('The mean of Age column is',mean_age)


# In[188]:


customer.loc[customer['Age']<18,'Age']=customer['Age'].mean()


# In[189]:


mean = customer['Age'].mean()


# In[190]:


print('new mean of Age columns is ',mean)


# In[191]:


customer.loc[customer['Age']<18,'Age']


# #### b. In case spend amount is more than the limit, replace it with 50% of that customer’s limit. (customer’s limit provided in acquisition table is the per transaction limit on his card)
# 

# In[192]:


customer .head(3)


# In[193]:


spend.head(3)


# In[194]:


cust_spend = pd.merge(left=customer,right=spend,on='Customer',how='inner')


# In[195]:


cust_spend.rename(columns={'Amount':'spend_amt'},inplace = True)


# In[196]:


cust_spend.head(3)


# In[197]:


cust_spend[cust_spend.spend_amt>cust_spend.Limit].head()


# In[198]:


cust_spend['spend_amt']=np.where(cust_spend.spend_amt>cust_spend.Limit,cust_spend.Limit*0.5,cust_spend.spend_amt)


# In[199]:


cust_spend.head(2)


# In[200]:


cust_spend[cust_spend.Customer=='A2'].head()


# #### c. Incase the repayment amount is more than the limit, replace the repayment with the limit.

# In[201]:


repay.head()


# In[202]:


customer.head(2)


# In[203]:


cust_repay = pd.merge(left=repay,right=customer,on='Customer',how = 'inner')


# In[204]:


cust_repay.rename(columns={'Amount':'repay_amt'},inplace=True)


# In[205]:


cust_repay.head()


# In[206]:


cust_repay[cust_repay['repay_amt']>cust_repay['Limit']]


# In[ ]:





# ### 2. From the above dataset create the following summaries

# #### a. How many distinct customers exist?

# In[207]:


customer.head(2)


# In[208]:


dist_cust =customer['Customer'].nunique()


# In[209]:


print('''Distinct customer exist are''',dist_cust)


# #### b. How many distinct categories exist?

# In[210]:


customer['Segment'].value_counts()


# In[211]:


dist_cat = customer['Segment'].nunique()


# In[212]:


print('''Nomber of distinct categories are''',dist_cat)


# #### c. What is the average monthly spend by customers?

# In[213]:


spend.head(3)


# In[214]:


spend['Month'] = pd.to_datetime(spend['Month'])


# In[215]:


spend.head(2)


# In[216]:


spend['Monthly']= spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format = '%B'))


# In[217]:


spend['Yearly']= spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format = '%Y'))


# In[218]:


spend.head(2)


# In[219]:


Monthly_avg= round(spend.groupby(by=['Yearly','Monthly']).mean(numeric_only=True),2)


# In[220]:


Monthly_avg.head()


# #### d. What is the average monthly repayment by customers?

# In[257]:


cust_repay.head(3)


# In[258]:


pd.options.mode.copy_on_write = True 


# In[259]:


cust_repay['Month'] =  pd.to_datetime(repay['Month'])


# In[260]:


cust_repay['Monthly']= spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format = '%B'))


# In[263]:


cust_repay['Yearly']= spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format = '%Y'))


# In[264]:


cust_repay.head()


# In[265]:


monthly_avg=round(cust_repay.groupby(by=['Yearly','Monthly']).mean(numeric_only=True),2)


# In[266]:


monthly_avg.head()


# #### e. If the monthly rate of interest is 2.9%, what is the profit for the bank for each month? (Profit is defined as interest earned on Monthly Profit. Monthly Profit = Monthly repayment – Monthly spend. Interest is earned only on positive profits and not on negative amounts)

# In[267]:


bank_repay_spend = pd.merge(left=cust_spend,right=cust_repay,on = ['Customer'],how = 'inner')


# In[268]:


bank_repay_spend.head(3)


# In[269]:


bank_repay_spend.rename(columns={'Amount_x':'spend_amt','Amount_y':'repay_amt'},inplace = True)


# In[270]:


bank_repay_spend.head()


# In[271]:


cust_repay_spend=bank_repay_spend.groupby(['Yearly','Monthly'])[['spend_amt','repay_amt']].sum()


# In[274]:


cust_repay_spend.head()


# In[275]:


cust_repay_spend['Monthly_profit']= cust_repay_spend['repay_amt'] - cust_repay_spend['spend_amt']


# In[276]:


cust_repay_spend


# In[277]:


cust_repay_spend['Profit']=np.where(cust_repay_spend['Monthly_profit']>0,2.9*(cust_repay_spend['Monthly_profit'])/100,0)
cust_repay_spend


# #### f. What are the top 5 product types?

# In[278]:


spend.head(2)


# In[279]:


spend.groupby('Type')['Amount'].count().reset_index().sort_values(by='Amount',ascending = False).reset_index(drop=True).iloc[:,0].head(5)


# In[280]:


spend.groupby('Type')['Amount'].count().reset_index().sort_values(by='Amount',ascending = False).reset_index(drop=True).plot(kind='bar')
plt.show()


# #### g. Which city is having maximum spend?
# 

# In[281]:


cust_spend.head(2)


# In[282]:


cust_spend.groupby('City')[['spend_amt']].max().sort_values(by ='spend_amt',ascending=False).head(1)


# #### h. Which age group is spending more money?
# 

# In[283]:


Age_range = [18,30,40,50,60,70,80]
labels = ['18-30','31-40','41-50','51-60','61-70','71-80']
cust_spend['Age_group'] = pd.cut(cust_spend['Age'],bins=Age_range,labels = labels)
cust_spend.groupby('Age_group')[['spend_amt']].max().sort_values(by='spend_amt',ascending = False)


# #### i. Who are the top 10 customers in terms of repayment?

# In[284]:


cust_repay


# In[286]:


cust_repay.groupby('Customer')[['repay_amt']].sum().sort_values(by='repay_amt',ascending = False).head(10)


# ### 3. Calculate the city wise spend on each product on yearly basis. Also include a graphical representation for the same.

# In[287]:


cust_spend['Month'] = pd.to_datetime(cust_spend['Month'])


# In[288]:


cust_spend['Monthly'] = cust_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format = '%B'))


# In[289]:


cust_spend['Yearly'] = cust_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format = '%Y'))
                                                                             


# In[290]:


cust_spend.head()


# In[296]:


cust_spend_yearly =pd.pivot_table(data = cust_spend,index = 'City',columns= ['Product','Yearly'],aggfunc = sum,values = 'spend_amt')


# In[298]:


cust_spend_yearly.head()


# In[299]:


cust_spend_yearly.plot(kind='bar',stacked = True)
plt.show()


# ### 4. Create graphs for
# 

# #### a. Monthly comparison of total spends, city wise
# 

# In[300]:


cust_spend.head(2)


# In[302]:


city_wise=cust_spend.groupby(by=['City','Monthly'])[['spend_amt']].sum().sort_index().reset_index()


# In[303]:


city_wise = pd.pivot_table(data = cust_spend,index = 'City',values = 'spend_amt',columns = 'Monthly',aggfunc='sum')


# In[304]:


city_wise.head()


# In[305]:


city_wise.plot(kind = 'bar',stacked=True,figsize=(8,7),width = 0.9)
plt.show()


# #### b. Comparison of yearly spend on air tickets
# 

# In[306]:


Air_ticket=cust_spend.groupby(by=['Yearly','Type'])[['spend_amt']].sum().reset_index()


# In[307]:


Air_ticket.head()


# In[309]:


yearly_tkt  =Air_ticket.loc[Air_ticket['Type']=='AIR TICKET']


# In[313]:


yearly_tkt.plot(kind='bar', x='Yearly', y='spend_amt',  figsize = (5,3))
plt.show()


# #### c. Comparison of monthly spend for each product (look for any seasonalitythat exists in terms of spend)

# In[315]:


term_prod=cust_spend.groupby(by=['Yearly','Monthly','Product'])[['spend_amt']].sum().reset_index()


# In[316]:


Monthly_product=pd.pivot_table(data=term_prod,index='Product',values='spend_amt',columns='Monthly')


# In[317]:


Monthly_product.plot(kind = 'bar',figsize = (10,10))
plt.show()


# ### 5. Write user defined PYTHON function to perform the following analysis:
# 

# ### You need to find top 10 customers for each city in terms of their repayment amount by different products and by different time periods i.e. year or month. The user should be able to specify the product (Gold/Silver/Platinum) and time period (yearly or monthly) and the function should automatically take these inputs while identifying the top 10 customers.

# In[318]:


cust_repay_tbl = cust_repay.copy()


# In[319]:


cust_repay_tbl.head(2)


# In[324]:


def top_ten_cust(Product,time_period):
    return pd.DataFrame(cust_repay_tbl[cust_repay_tbl.Product==Product].groupby(['City','Customer','Product',time_period])\
   ['repay_amt'].sum().reset_index().sort_values(by='repay_amt',ascending = False)).pivot_table(index=['Product','City','Customer'],columns = time_period,values='repay_amt')
                    


# In[325]:


top_ten_cust('Silver','Yearly')


# In[ ]:




