#!/usr/bin/env python
# coding: utf-8

# ##  Basic Statistics Case Study

# ### BUSINESS PROBLEM - 1
# ### Using lending club loans data, the team would like to test below hypothesis on how different factors effecing each other (Hint: You may leverage hypothesis testing using statistical tests)
# ####  a. Intrest rate is varied for different loan amounts (Less intrest charged for high loan amounts)
# ####  b. Loan length is directly effecting intrest rate.
# ####  c. Inrest rate varies for different purpose of loans
# ####  d. There is relationship between FICO scores and Home Ownership. It means that, People with owning home will have high FICO scores.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import scipy.stats as stt
import os
import warnings
warnings.filterwarnings('ignore')


# In[2]:


os.chdir('C:\\Users\\Adesh mishra\\OneDrive\\Desktop\\New folder (8)')


# In[3]:


loan_df = pd.read_csv('LoansData.csv')


# ##### EDA(Exploratory data Analysis)

# In[4]:


loan_df.head()


# In[5]:


loan_df.tail()


# In[ ]:





# In[6]:


loan_df.info()


# In[7]:


loan_df.nunique()


# In[8]:


loan_df.isnull().sum()


# In[9]:


loan_df.shape


# In[10]:


(loan_df.isnull().sum()/(len(loan_df)))*100


# In[11]:


loan_df.duplicated().sum()


# ###### a. Intrest rate is varied for different loan amounts (Less intrest charged for high loan amounts)

# - Ho: Intrest rate does not varies for deffernt loan amount
# - Ha: Intrest rate does varies for differnt loan amount
# - CI = 95%
# - p-Value  = 0.05

# In[12]:


loan_df['Amount.Requested']


# In[13]:


loan_df['Interest.Rate']


# In[14]:


loan_df['Int_Rs']=pd.to_numeric(loan_df['Interest.Rate'].str.replace('%',' '))


# In[15]:


loan_df['Int_Rs']


# In[16]:


loan_df.fillna({'Int_Rs':loan_df.Int_Rs.mode()[0]},inplace = True)
loan_df.fillna({'Amount.Requested':loan_df['Amount.Requested'].mean()},inplace=True)
print(loan_df.Int_Rs.isna().sum())
print(loan_df['Amount.Requested'].isna().sum())          


# In[17]:


# perform the Test statitics.We will perform the correlation test as both the variable
print(stt.pearsonr(loan_df['Amount.Requested'],loan_df.Int_Rs))
print('there is +ve relationship with loan Amount requested and interest rate offer by bank')
print('Thus','intrest rate does varies for differnt loan amount')
print('P values is very less.''Thus,we reject the Null hypothesis' )


# #####  b. Loan length is directly effecting intrest rate.

# - Ho : loan length is not directly effecting intrest rate
# - Ha : loan length is directly effecting intrest rate. 
# - CI = 95%
# - P-value = 0.05

# In[18]:


for i in loan_df['Loan.Length'].unique():
    print(i)


# In[19]:


loan_df['Int_Rs']


# In[20]:


x1 = loan_df.loc[loan_df['Loan.Length']=='36 months','Int_Rs']
x2= loan_df.loc[loan_df['Loan.Length']=='60 months','Int_Rs']


# In[21]:


print('mean of Interest_Rate for x1:',x1.mean())
print('mean of Interest_Rate for x2:',x2.mean())


# In[22]:


# T-test

stt.ttest_ind(x1,x2)


# - P-Value is very less.thus , we reject the null hypothesis
# - Thus,Loan length dirctly effecting the intrest rate

# ###### C.Interest rate varies for different purpose of loans
# - Ho: interest rate doest not varies for different purpose of loans
# - Ha: Interest rate does varies for differnt purpose of loans
# - CI = 95%
# - P-value = 0.05

# In[23]:


for col in loan_df['Loan.Purpose'].unique():
    print(col)


# In[24]:


for i in loan_df['Int_Rs']:
    print(i)


# In[25]:


A1=loan_df.loc[loan_df['Loan.Purpose']=='debt_consolidation','Int_Rs']
A2=loan_df.loc[loan_df['Loan.Purpose']=='credit_card','Int_Rs']
A3=loan_df.loc[loan_df['Loan.Purpose']=='moving','Int_Rs']
A4=loan_df.loc[loan_df['Loan.Purpose']=='car','Int_Rs']
A5=loan_df.loc[loan_df['Loan.Purpose']=='vacation','Int_Rs']
A6=loan_df.loc[loan_df['Loan.Purpose']=='home_improvement','Int_Rs']
A7=loan_df.loc[loan_df['Loan.Purpose']=='house','Int_Rs']
A8=loan_df.loc[loan_df['Loan.Purpose']=='major_purchase','Int_Rs']
A9=loan_df.loc[loan_df['Loan.Purpose']=='educational','Int_Rs']
A10=loan_df.loc[loan_df['Loan.Purpose']=='medical','Int_Rs']
A11=loan_df.loc[loan_df['Loan.Purpose']=='wedding','Int_Rs']
A12=loan_df.loc[loan_df['Loan.Purpose']=='small_business','Int_Rs']
A13=loan_df.loc[loan_df['Loan.Purpose']=='renewable_energy','Int_Rs']
A14=loan_df.loc[loan_df['Loan.Purpose']=='other','Int_Rs']


# In[26]:


print('\n mean of bebt_consolidation:',A1.mean(),
      '\n mean of credit_card:', A2.mean(),
     '\n mean of moving :',A3.mean(),
      '\n mean of Car:',A4.mean(),
     '\n mean of vacation :',A5.mean(),
      '\n mean of home_improvement :',A6.mean(),
     '\n mean of house :',A7.mean(),
      '\n mean of major_purchase:',A8.mean(),
     '\n mean of educational:',A9.mean(),
      '\n mean of medical:',A10.mean(),
     '\n mean of wedding:',A11.mean(),
      '\n mean of small_business :',A12.mean(),
     '\n mean of renewable_energy :',A13.mean(),
    '\n mean of Other :',A14.mean())
# perform the ANOVA as the there are two categories for loan purpose


# In[27]:


# F-oneway test
stt.f_oneway(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A12,A13,A14)


# - P - value is low.Thus we reject null hypothesis
# - interest rate doest varies for diffrent purpose of loans

# ##### d. There is relationship between FICO scores and Home Ownership. It means that, People with owning home will have high FICO scores.
# - There is no relationship b/w FICO score and Home Ownership
# - There is relationship b/w FICO score and Home Ownership 
# - CI = 95%
# - P-Value = 0.05

# In[28]:


loan_df['FICO_min']=loan_df["FICO.Range"].str.split("-").str[0].dropna().astype('int64')
loan_df['FICO_max']=loan_df["FICO.Range"].str.split("-").str[1].dropna().astype('int64')


# In[29]:


loan_df.head(3)


# In[30]:


# calculate the FICO mean
loan_df['FICO_mean']=round(loan_df['FICO_min']+loan_df['FICO_max']/loan_df['FICO_min'].count(),2)


# In[31]:


#fill missing values
loan_df.FICO_mean.fillna(loan_df.FICO_mean.mean(),inplace=True)


# In[32]:


loan_df['Home.Ownership'].unique()


# In[33]:


Mortgage = loan_df.loc[loan_df['Home.Ownership']=='MORTGAGE','FICO_mean']
Rent = loan_df.loc[loan_df['Home.Ownership']=='RENT','FICO_mean']
Own = loan_df.loc[loan_df['Home.Ownership']=='OWN','FICO_mean']
Other= loan_df.loc[loan_df['Home.Ownership']=='OTHER','FICO_mean']


# In[34]:


print('mean of Mortgage: '+str(Mortgage.mean()),
    '\n mean of Rent: '+str(Rent.mean()),
    '\n mean  of Own: '+str(Own.mean()),
    '\n mean of Other: '+str(Other.mean()))
    


# In[35]:


#ANOVA/F_oneway test
f_test_home = stt.f_oneway(Mortgage,Rent,Own,Other)
f_test_home


# In[36]:


P_value=f_test_home.pvalue
if(P_value<0.05):
    print('we reject the Null Hypothisis')
else:
    print('we fail to reject null hypothesis')


# In[37]:


print('In output, the p-value is low. So we will reject null Hypothesis and conclude that FICO scores are not impacted by home ownership. there are others factors as well which contribute to FICO score.')


# ## BUSINESS PROBLEM - 2
# 
# ##### BUSINESS PROBLEM: We would like to assess if there is any difference in the average price quotes provided by Mary and Barry.

# - Ho : there is No difference in the average price quotes provided by Mary and Barry
# - Ha : there is different in the average price quotes provided by Mary and Barry
# - CI =95
# - P-value = 0.05

# In[38]:


price_q = pd.read_csv('Price_Quotes.csv')


# In[39]:


price_q.head()


# In[40]:


price_q.info()


# In[41]:


price_q['Mary_Price'].describe()


# In[42]:


price_q['Barry_Price'].describe()


# In[43]:


#T-test
PV = stt.ttest_rel(price_q.Barry_Price,price_q.Mary_Price)
PV


# In[44]:


P = PV.pvalue
if(P<0.05):
    print('we reject null hypothesis')
else:
    print('we fail to reject null hypothesis')


#  - p is low will go ,p is high null will fly
# 
# - There is difference in the average price quotes provided by Mary and Barry.
#  

# ## BUSINESS PROBLEM-3
# ##### BUSINESS PROBLEM: Determine what effect, if any, the reengineering effort had on the incidence behavioral problems and staff turnover. i.e To determine if the reengineering effortchanged the critical incidence rate. Isthere evidence that the critical incidence rate improved?

# In[45]:


Treat_F = pd.read_csv('Treatment_Facility.csv')
Treat_F.head(2)


# In[46]:


Treat_F.rename(columns = {'VAR4':'TRFF(%)','VAR5':'CI(%)'},inplace=True)


# In[47]:


Treat_F.info()


# In[48]:


Treat_F.isnull().sum()


# In[49]:


print(Treat_F.shape)
print('this data has 20 rows and 5 columns')


# In[50]:


Treat_F.head(3)


# In[51]:


x1 = Treat_F.loc[Treat_F.Reengineer=='Prior','CI(%)']
x2 = Treat_F.loc[Treat_F.Reengineer=='Post','CI(%)']


# In[52]:


print('mean of x1: ',round(x1.mean(),1),
        '| mean of x2: ',round(x2.mean(),1))


# In[53]:


# Ho: u2<= u1
# Ha: u2> u1
# CI: 95%
# p: 0.05

# p ia low null will go, p is high null will fly
# t-test
print(stt.ttest_ind(x1,x2))
# conclusion
#With the give data we can not say that their is any effect on the reengineering efforts.


# ## BUSINESS PROBLEM-4
# 
# ##### BUSINESS PROBLEM: We will focus on the prioritization system. If the system is working, thenhigh priority jobs, on average, should be completed more quickly than medium priority jobs,and medium priority jobs should be completed more quickly than low priority jobs. Use thedata provided to determine whether thisis, in fact, occurring.

# In[54]:


pri_ass = pd.read_csv('Priority_Assessment.csv')
pri_ass.head(3)


# In[58]:


#EDA


# In[59]:


pri_ass.shape


# In[60]:


pri_ass.info()


# In[61]:


pri_ass.isnull().sum()


# In[68]:


# Ho: No corelation ,independant
# Ha: variables are related ,dependant

#CI: 95%
#P: 0.05

#  p is low null will go, p is high null will fly

# 
stt.spearmanr(pri_ass.Days,pri_ass.Priority)

# the given data we cannot say that priopritization system is working


# ## BUSINESS PROBLEM-5
# ######  BUSINESS PROBLEM: Use the survey resultsto addressthe following questions
# ###### a. What isthe overall level of customer satisfaction?
# ###### b. What factors are linked to satisfaction?
# ###### c. What is the demographic profile of Film on the Rocks patrons?
# ###### d. In what media outlet(s) should the film series be advertised?

# In[71]:


films=pd.read_csv('Films.csv')
films.head(3)


# In[72]:


#EDA


# In[73]:


films.shape


# In[74]:


films.isnull().sum()


# In[75]:


films.info()


# In[79]:


for i in films.columns:
    films[i].fillna(value=films[i].mode()[0],inplace=True)


# In[80]:


def gender(x):
    if x.Gender=='Male':
        return '1'
    elif x.Gender == 'Female':
        return '0'
    elif x.Gender == '1':
        return '1'
    else:
        return '0'


# In[81]:


# convert males to 1 and female to 0
films.Gender =  films.apply(gender,axis =1)


# In[116]:


def married_stt(x):
    if x.Marital_Status == 'Married':
        return '1'
    elif x.Marital_Status == 'single':
        return '0'
    elif x.Marital_Status == '1':
        return '1'
    else:
        return '0'


# In[121]:


# converting married to 1 and single to 0

films.Marital_Status =films.apply(married_stt,axis =1)


# In[ ]:


#a. What isthe overall level of customer satisfaction


# In[132]:


films.Overall.plot(kind = 'hist',figsize=(6,3))
plt.title('overall level of customer satisfaction')
plt.show()
print('overall customer satisfaction is good')


# In[140]:


#b. What factors are linked to satisfaction?
observed = pd.crosstab(films.Sinage,films.Overall)
# Ho: No relationship,independant
# Ha: variables are related, dependant
# CI: 95%
# P: 0.05
# p is low null will go , p is high null will fly
# test

stt.chi2_contingency(observed)
# with incerease in sinage rating overall staifaction is also increases


# In[146]:


# chi square test
observed = pd.crosstab(films.Parking,films.Overall)
# Ho: No relationship,independant
# Ha: variables are related, dependant
# CI: 95%
# P: 0.05
# p is low null will go , p is high null will fly

# test
stt.chi2_contingency(observed)
# with incerease in parking rating overall staifaction is also increases


# In[149]:


# chi square test
observed = pd.crosstab(films.Clean,films.Overall)
# Ho: No relationship,independant
# Ha: variables are related, dependant
# CI: 95%
# P: 0.05
# p is low null will go , p is high null will fly

# test
stt.chi2_contingency(observed)


# In[152]:


#c. What is the demographic profile of Film on the Rocks patrons?

#Demographic on Gender
gender = films.groupby('Gender')[['Gender']].count()
gender = gender.rename(columns={'Gender':'count'}).reset_index()
gender['profile'] = gender['count']/gender['count'].sum()
print(gender)
print('as Gender 0 is female and 1  is male.that means their is 64% probability audiance is female')


# In[157]:


#Demographic on martial status
Mr_stt = films.groupby('Marital_Status')[['Marital_Status']].count()
Mr_stt = Mr_stt.rename(columns ={'Marital_Status':'count'}).reset_index()
Mr_stt['Prob'] = Mr_stt['count']/Mr_stt['count'].sum()
print(Mr_stt)
print('their is 69% probability that the audiance is married')


# In[159]:


# Demographic on martial status
Age = films.groupby('Age')[['Age']].count()
Age = Age.rename(columns={'Age':'count'}).reset_index()
Age['prob'] = Age['count']/Age['count'].sum()
print(Age)
print('their is 53% probabilty that the age of the audiance is b/w 13-30')


# In[161]:


# Demographic on Income
income = films.groupby('Income')[['Income']].count()
income = income.rename(columns = {'Income':'count'}).reset_index()
income['prob']=income['count']/income['count'].sum()
print(income)
print('their is 47% probabilty that the income of the audiance is less than 50k')


# In[ ]:


#d. In what media outlet(s) should the film series be advertised?


# In[163]:


# Demographic on Income
out_let = films.groupby('Hear_About')[['Hear_About']].count()
out_let = out_let.rename(columns={'Hear_About':'count'}).reset_index()
out_let['prob']=out_let['count']/out_let['count'].sum()
print(out_let.sort_values(by='prob',ascending = False))
print('Their is 70% probabilty that the audiance heard about the film series solely through word of mouth.')


# In[ ]:




