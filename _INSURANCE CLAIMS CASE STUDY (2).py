#!/usr/bin/env python
# coding: utf-8

# # CASE STUDY:
# ##   DATA EXPLORATORY ANALYSIS AND HYPOTHESIS
# ##   TESTING FOR INSURANCE CLAIMS DATA
# 

# - ### Disclaimer: This material is protected under copyright act AnalytixLabs©2011-2018. Unauthorized use and/ or duplication of this material or any part of this material including data, in any form without explicit and written permission from AnalytixLabs is strictly prohibited. Any violation of this copyright will attract legal actions.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import os
import matplotlib.pyplot as plt


# - #### Q1. Import claims_data.csv and cust_data.csv which is provided to you           and combine the two datasets appropriately to create a 360-degree             view of the data. Use the same for the subsequent questions.

# In[2]:


os.chdir('C:\\Users\\Adesh mishra\\OneDrive\\Desktop\\New folder (7)\\New folder')


# In[3]:


claim_data = pd.read_csv('claims.csv')


# In[4]:


cust_data = pd.read_csv('cust_demographics.csv')


# In[5]:


claim_data.head(2)


# In[6]:


claim_data.isnull().sum()


# In[87]:


claim_data.rename(columns={'customer_id':'CUST_ID'},inplace=True)


# In[88]:


claim_data.head()


# In[89]:


print(claim_data.shape)
print('this data has 1100  rows and 10 columns')


# In[90]:


cust_data.head()


# In[91]:


cust_data.head(2)


# In[92]:


print(cust_data.shape)
print('this data has 1085 rows and 6 columns')


# In[93]:


claim_data.info()


# In[94]:


cust_data.info()


# In[95]:


print('Both table claim_amount and cust_Id are equal rows',1085)


# In[ ]:





# In[96]:


cust_claim = claim_data.merge(cust_data,left_on ='CUST_ID',right_on = 'CUST_ID',how = 'right')


# In[98]:


cust_claim.head(3)


# In[99]:


print(cust_claim.shape)
print('this data has 1092 rows and 15 columns')


# In[100]:


cust_claim.info()


# - #### Q 2. Perform a data audit for the datatypes and find out if there are any mismatch within the current datatypes of the columns and their business significance.

# In[101]:


cust_claim.info()


# In[102]:


# changing date from  object to date time 
cust_claim['claim_date'] = cust_claim['claim_date'].apply(lambda x:pd.to_datetime(x))


# In[103]:


# changing date from object to date time
cust_claim['DateOfBirth'] = cust_claim['DateOfBirth'].apply(lambda X:pd.to_datetime(X))


# In[104]:


cust_claim.info()


# - ####  Q3. Convert the column claim_amount to numeric. Use the appropriate modules/attributes to remove the $ sign.

# 
# 
# removing dollar $ sign from claim_ammount and converting it into int field
# 

# In[105]:


cust_claim['claim_amount'] = cust_claim['claim_amount'].str.replace('$',' ',regex=True)


# In[106]:


cust_claim.head(2)


# In[107]:


cust_claim['claim_amount'] = cust_claim['claim_amount'].astype('float')


# In[108]:


cust_claim.info()


# - ####  Q4. Of all the injury claims, some of them have gone unreported with the police. Create an alert flag (1,0) for all such claims.

# In[109]:


cust_claim['police_report_flag'] = np.where(cust_claim['police_report']=='Yes',1,0)


# In[110]:


cust_claim.head(3)


# In[167]:


cust_claim.groupby(by= ['claim_type','claim_id','CUST_ID'])[['CUST_ID']].head(5)


# - ####  Q5. One customer can claim for insurance more than once and in each claim,multiple categories of claims can be involved. However, customer ID should remain unique.Retain the most recent observation and delete any duplicated records in the data based on the customer ID column.

# In[168]:


cust_claim.drop_duplicates(subset='customer_id',keep = 'last')


# In[ ]:


cust_claim.duplicated().sum() # no duplicate record is present


# In[ ]:


cust_claim.info()


#  - ####  Q6. Check for missing values and impute the missing values with an appropriate value. (mean for continuous and mode for categorical)

# In[ ]:


cust_claim.isna().sum()


# In[112]:


cust_claim['total_policy_claims'].value_counts()


# In[113]:


cust_claim.claim_amount.mean()


# In[114]:


cust_claim.info()


# In[115]:


cust_claim['total_policy_claims']=cust_claim.total_policy_claims.fillna(1.0)


# In[116]:


cust_claim.info()


# - ####  7. Calculate the age of customers in years. Based on the age, categorize the customers according to the below criteria
#   #### Children < 18
#   #### Youth 18-30
#   #### Adult 30-60
#   #### Senior > 60

# In[117]:


current_year = pd.to_datetime('today').year
current_year


# In[118]:


cust_claim['DateOfBirth']=cust_claim['DateOfBirth'].dt.year


# In[119]:


cust_claim.info()


# In[120]:


cust_claim['DateOfBirth']


# In[121]:


cust_claim['new_yearofBirth']=np.where(cust_claim['DateOfBirth']>current_year,cust_claim['DateOfBirth']-100,cust_claim['DateOfBirth'])


# In[122]:


cust_claim.head(2)


# In[123]:


cust_claim['Age']=current_year-cust_claim['new_yearofBirth']


# In[124]:


cust_claim.loc[(cust_claim.Age<18)&(cust_claim.Age>0),'Age_group']='Children'
cust_claim.loc[(cust_claim.Age>=18)&(cust_claim.Age<30),'Age_group']='Youth'
cust_claim.loc[(cust_claim.Age>=30)&(cust_claim.Age<60),'Age_group']='Adult'
cust_claim.loc[(cust_claim.Age>=60),'Age_group']='Senior'


# In[125]:


cust_claim.head(2)


# - #### Q8. What is the average amount claimed by the customers from various segments?

# In[126]:


cust_claim.groupby('Segment')[['claim_amount']].mean()


# - #### Q9. What is the total claim amount based on incident cause for all the claims that have been done at least 20 days prior to 1st of October, 2018.

# In[127]:


cust_claim[cust_claim.claim_date<'2018-09-10'].groupby('incident_cause')['claim_amount'].mean().reset_index()


# In[128]:


cust_claim['claim_amount'].sum()


# - #### Q10. How many adults from TX, DE and AK claimed insurance for driver related issues and causes?

# In[129]:


cust_claim.loc[(cust_claim.incident_cause.str.lower().str.contains('drive') & ((cust_claim.State=='TX')|(cust_claim.State=='DE')|(cust_claim.State =='AK'))),:].groupby('State')['State'].count()


# - ####  Q11. Draw a pie chart between the aggregated value of claim amount based on gender and segment. Represent the claim amount as a percentage on  the pie chart

# In[130]:


claim_amt = pd.pivot_table(data = cust_claim,index = 'Segment',columns=['gender'],values='claim_amount',aggfunc='sum')


# In[131]:


claim_amt


# In[132]:


claim_amt.plot(kind ='pie',labels=['Gold','Platinum','Silver'],subplots = True,autopct ='%.1f%%')
plt.title('pie chart of claim amount')
plt.axis('equal')
plt.show()


# - #### Q12. Among males and females, which gender had claimed the most for any type of driver related issues? E.g. This metric can be compared using a bar chart

# In[133]:


Gender = cust_claim[(cust_claim.incident_cause.str.lower().str.contains('driver',na = False))].groupby(['gender'])[['gender']].count().add_prefix('count_').reset_index()


# In[134]:


Gender


# In[135]:


pd.pivot_table(data=Gender,index='gender',values='count_gender').plot(kind='bar')


# - #### Q13. Which age group had the maximum fraudulent policy claims? Visualize it on a bar chart.

# In[136]:


age_gp = cust_claim.groupby(['Age_group'])['fraudulent'].count().reset_index()
pd.pivot_table(age_gp,index='Age_group',values='fraudulent').plot(kind='bar')


# - #### Q14. Visualize the monthly trend of the total amount that has been claimed by the customers. Ensure that on the “month” axis, the month is in a chronological order not alphabetical order. 

# In[137]:


cust_claim.columns


# In[138]:


cust_claim['claim_month']=cust_claim['claim_date'].apply(lambda x:x.month)


# In[139]:


cust_claim.head(1)


# In[140]:


monthly_trend=pd.pivot_table(data=cust_claim,index='claim_month',values='claim_amount',aggfunc='sum')


# In[141]:


monthly_trend


# In[142]:


monthly_trend.plot(kind='bar')


# - #### Q15. What is the average claim amount for gender and age categories and suitably represent the above using a facetted bar chart, one facet that represents fraudulent claims and the other for non-fraudulent claims.Based on the conclusions from exploratory analysis as well as suitable statistical tests, answer the below questions. Please include a detailed write-up on the parameters taken into consideration, the Hypothesis testing steps, conclusion from the p-values and the business implications of the statements.

# In[143]:


claim_age=pd.pivot_table(data=cust_claim,index=['Age_group','gender'],columns=['fraudulent'],values='claim_amount',aggfunc='mean')


# In[144]:


claim_age


# In[145]:


claim_age.plot(kind='barh',subplots=True)


# - #### Q16. Is there any similarity in the amount claimed by males and females?

# In[146]:


male = cust_claim['claim_amount'].loc[cust_claim['gender']=='Male']
female = cust_claim['claim_amount'].loc[cust_claim['gender']=='Female']


# In[147]:


#H0: there is  similarity
#Ha: there is not a similarity
#CI = 95%
#p - 0.05
import scipy.stats as stt


# In[148]:


print('male: ',male.mean(),'| female: ',female.mean())


# In[149]:


stt.ttest_ind(male,female)


# In[ ]:


#?....


# - #### Q17. Is there any relationship between age category and segment?

# In[151]:


cat_seg = pd.crosstab(cust_claim.Age_group,cust_claim.Segment,margins=True)
cat_seg


# In[155]:


chi_t =stt.chi2_contingency(observed=cat_seg)
chi_t


# In[160]:


print('the chi2 stat is {} and the p value is {}'.format(chi_t[0],chi_t[1]))
print('Since the significance value of the test is greter than 0.05, we fail reject the null hypothesis. Therefore there is no relationship between age category and segment')


# - #### Q18. The current year has shown a significant rise in claim amounts as compared to 2016-17 fiscal average which was $10,000.

# In[98]:


# Here we will check the pearson coeffecient.
# The H0= No relationship between the 2016-17 claim amount and current claim amounts
# Ha = Retionship exists;
# the CI=95%,p=0.05


# In[162]:


cust_claim['year']=pd.DatetimeIndex(cust_claim.claim_date).year
A = cust_claim.loc[cust_claim.year==2018]['claim_amount']
B = cust_claim.loc[cust_claim.year==2017]['claim_amount']
A.corr(other=B)
# No correlation between current year and previous year


# - #### Q19. Is there any difference between age groups and insurance claims?

# In[163]:


# Here we will perform Ftest ANOVA
# H0:mean(Agegroup[Youth])==mean(Agegroup[Adult])(No difference between age groups and insurance claim or no influence of age groups on unsurence claim)
# Ha:mean(Agegroup[Youth])!=mean(Agegroup[Adult]) (There is some difference between age groups and insurance claims or there is some influence of age groups on insurance claims)  


# In[165]:


x1 = cust_claim['total_policy_claims'].loc[cust_claim['Age_group']=='Youth']
x2 = cust_claim['total_policy_claims'].loc[cust_claim['Age_group']=='Adult']

# perfrom the Anova
anova= stt.f_oneway(x1,x2)
# statistic: F value
f=anova.statistic
p=anova.pvalue
print('The f-value is {} and the p value is {}'.format(f,p))
if(p<0.05):
    print('we reject null hypothesis')
else:
    print('we fail to reject null hypothesis')


# In[1]:


# Since the significance value of the test is greater than 0.05 , we fail reject the null hypothesis. Therefore, there is no difference between age groups and insurance claims or no influence of age groups on insurance claims


# - #### Q20. Is there any relationship between total number of policy claims and the claimed amount?

# In[100]:


cust_claim['total_policy_claims']=pd.to_numeric(cust_claim['total_policy_claims'])


# In[101]:


cust_claim.total_policy_claims.corr(other=cust_claim.claim_amount)


# In[102]:


print(' As the correlation is negative the number of policy claims in inversely propotional to the claim amount') 


# In[ ]:




