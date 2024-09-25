#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


os.chdir('C:\\Users\\Adesh mishra\\OneDrive\\Desktop\\New folder (7)')


# In[3]:


sales = pd.read_csv('SalesData.csv')


# In[4]:


sales.head()


# In[29]:


sales.drop_duplicates().head()


# In[30]:


print('this data has no duplicates values')


# In[36]:


sales.isna().sum().sum()


# In[31]:


sales.info()


# In[34]:


print(sales.shape)
print('this data has 3709 rows and 14 columns')


# In[7]:


sales.columns


# ## Q1. Compare Sales by region for 2016 with 2015 using bar chart

# In[8]:


sale_reg= sales.groupby('Region')[['Sales2015','Sales2016']].sum()


# In[9]:


sale_reg.plot(kind = 'bar',figsize=(6,3))
plt.ylabel('Sales')
plt.title('Sales by region for 2016 with 2015')
plt.show()


# #### - we can conclude that sales in 2016 more as compared to sales in 2015 in all region . East region has contributed maximum

# ## Q2. What are the contributing factors to the sales for each region in 2016. Visualize it using a Pie Chart.
# 

# In[10]:


sales.head()


# In[11]:


Each_reg=sales.groupby('Region')['Sales2016'].sum()


# In[12]:


Each_reg


# In[13]:


plt.pie(Each_reg,autopct='%1.0f%%',labels=['Central','East','West'])
plt.title('contributing factors to the sales for each region in 2016')
plt.show()


# #### - East region has  contributed the maximum sales in 2016

# 
# ## Q3. Compare the total sales of 2015 and 2016 with respect to Region and Tiers
# 

# In[14]:


comp_sale=sales.groupby(by=['Region','Tier'])[['Sales2015','Sales2016']].sum()


# In[15]:


comp_sale.plot(kind='barh',xlabel='Sales',ylabel='Region/Tier',figsize=(6,5))
plt.title('total sales of 2015-16 with respect to Region and Tiers')
plt.show()


# - we can conclude that East region and Hingh tier in 2016 have contributed the maximum. Also sales in 2015  and sales in 2016 both is maximum in East region and high tier

# ## Q4. In East region, which state registered a decline in 2016 as compared to 2015?
# 

# In[16]:


seg_st = sales.groupby(['Region','State'])[['Sales2015','Sales2016']].sum()


# In[37]:


seg_st.head()


# In[18]:


east_sale=seg_st.loc['East'] # filtering out sales for East region in 2015-16


# In[19]:


east_sale


# In[20]:


east_sale.plot(kind='bar',ylabel='Sales',figsize=(8,3))
plt.title('Sales comparison between 2015 and 2016 for East Region')
plt.show()


# - NY state registered a decline in sales in 2016 as compared to 2015

# ## 5. In all the High tier, which Division saw a decline in number of units sold in 2016 compared to 2015?
# 

# In[38]:


sales.head(2)


# In[60]:


# Gruping data tier and division to find total sum of sales in 2015-16 
T_D = sales.groupby(by=['Tier','Division'])[['Units2015','Units2016']].sum()
T_D.head()


# In[61]:


H_T =T_D.loc['High']
H_T.head()


# In[68]:


H_T.plot(kind = 'barh',xlabel = 'Units')
plt.title('unit sold between 2015 - 16')
plt.show()
print('Not division show decline in number of units sold in 2016 compared to 2015')


# ## 6. Create a new column Qtr using numpy.where() or any suitable utility in the imported dataset. The Quarters are based on months and defined as -
# ### • Jan - Mar : Q1 
# ### • Apr - Jun : Q2
# ### • Jul - Sep : Q3
# ### • Oct - Dec : Q4 
# 

# In[71]:


sales.Month = pd.to_datetime(sales.Month,format='%b')


# In[72]:


sales['Qtr'] = np.where(sales['Month'].dt.month.isin([1,2,3]),'Q1',
                       np.where(sales['Month'].dt.month.isin([4,5,6]),'Q2',
                               np.where(sales['Month'].dt.month.isin([7,8,9]),'Q3','Q4')))


# In[74]:


sales.head(3)


# ## 7. Compare Qtr wise sales in 2015 and 2016 in a bar plot
# 

# In[78]:


Qtr_wise = sales.groupby(['Qtr'])[['Sales2015','Sales2016']].sum()


# In[86]:


Qtr_wise.plot(kind='bar',figsize=(8,4))
plt.ylabel('Sales')
plt.xlabel('Quater')
plt.title('Qtr wise sales in 2015 and 2016 ')
plt.show()


# ## 8. Determine the composition of Qtr wise sales in and 2016 with regards to all the Tiers in a pie chart
# ### (Draw 4 pie charts representing a Quarter for each Tier)

# In[93]:


Qtrwise_16 = sales.groupby(by=['Qtr','Tier'])[['Sales2016']].sum().unstack()


# In[96]:


Qtrwise_16[Qtrwise_16<0]=0
Quarter = Qtrwise_16.index


# In[108]:


for Qtr in Quarter:
    Qtrwise_16.loc[Qtr].plot(kind = 'pie',title=f'Quarter {Qtr} Sales composition',autopct='%1.1f%%')
    plt.ylabel('')
    plt.show()


# In[ ]:




