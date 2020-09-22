import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
import base64

def load_data():
    # Read data
    insurance = pd.read_csv('data/autoinsurance.csv')
    
    return(insurance)


def plot_age(data):
    
    # ---- Age group of customer

    def age_grouping(data):
        if(data.age <= 24):
            return '19 - 24'
        elif(data.age > 24 and data.age <= 30) : 
            return '25 - 30'
        elif(data.age > 30 and data.age <= 35) : 
            return '31 - 35'
        elif(data.age > 35 and data.age <= 40) : 
            return '36 - 40'
        elif(data.age > 40 and data.age <= 45) : 
            return '41 - 45'
        elif(data.age > 45 and data.age <= 50) : 
            return '46 - 50'
        elif(data.age > 50 and data.age <= 55) : 
            return '51 - 55'
        elif(data.age > 55 and data.age <= 59) : 
            return '56 - 59'
        else : 
            return '60+'

    data['age_group'] = data.apply(age_grouping,axis = 1)

    fraud_data = data[data['fraud_reported'] == 'Y']
    age_profile = pd.crosstab(index=fraud_data['age_group'],columns='count')

    ax = age_profile.plot.barh(title = "Fraud Reported by Age group", 
    legend= False, 
    color = '#00b3ff', 
    figsize = (8,6))
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_premium(data):

    def tocolor(data):
        if(data.fraud_reported == 'Y'):
            return '#53a4b1'
        else : 
            return '#c34454'
    
    data.fcolor = data.apply(tocolor,axis=1)
    
    # ---- Months as Customer per Policy Annual Premium

    ax = data.plot.scatter(x= 'months_as_customer', 
                       y = 'policy_annual_premium', 
                       c=data.fcolor,title = "Months as Customer per Policy Annual Premium",
                       figsize=(8, 6))


    # Plot Configuration
    lab_y = mpatches.Patch(color='#53a4b1', label='Y')
    lab_n = mpatches.Patch(color='#c34454', label='N')
    plt.legend(handles = [lab_y ,lab_n])
    plt.xlabel("Months as Customer")
    plt.ylabel("Policy Annual Premium")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)



def plot_incident(data):

    def tonum(data):
        if(data.fraud_reported == 'Y'):
            return 1
        else : 
            return 0
    
    data['fnum'] = data.apply(tonum,axis=1)

    timeseries = data.pivot_table(
                index='incident_date',
                values='fraud_reported',
                aggfunc='count').ffill()

    # ---- Number of Report per Day

    ax = timeseries.plot(legend=False, title = "Number of Fraud per Day",color='#c34454', figsize=(8, 6))

    # Plot Configuration
    plt.xlabel('')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_report(data):

    df_fraud = data[data.fraud_reported == 'Y'].pivot_table(index='police_report_available',values='fraud_reported',aggfunc='count')
    
    df_nfraud = data[data.fraud_reported == 'N'].pivot_table(index='police_report_available',values='fraud_reported',aggfunc='count')

    # ---- Police Report Availability

    ax = pd.concat([df_fraud,df_nfraud],axis=1).plot.bar(stacked = True,color =['#f50000','#00ff37'],title = "Police Report Availability", figsize=(8, 6))
    
    # Plot Configuration
    plt.legend(['fraud','not fraud'], bbox_to_anchor=(1, 1))
    plt.xlabel("police report available'")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_severity(data):

    insurance_fraud = data[data['fraud_reported']=='Y']
    insurance_not_fraud = data[data['fraud_reported']=='N']
    
    hipotesa = data[data['incident_severity']=='Major Damage']

    pd.crosstab(index=hipotesa['fraud_reported'],
            columns= 'proporsi',
           normalize=True).round(4)

    proporsi_fraud=pd.crosstab(index=insurance_fraud['incident_severity'],
            columns= 'Fraud')
    proporsi_not_fraud=pd.crosstab(index=insurance_not_fraud['incident_severity'],
            columns= 'Fraud')
    proporsi_total=pd.crosstab(index=data['incident_severity'],
            columns= 'Total')
    proporsi_total['Fraud']=proporsi_fraud['Fraud']
    proporsi_total['Not Fraud']=proporsi_not_fraud['Fraud']
    proporsi_total.plot.barh(color =['#2600fc','#f50000','#00ff37'],title='Fraud Reported by Incident Severity',figsize=(11, 6))
    plt.legend(['Total','Fraud','Not fraud'], bbox_to_anchor=(1, 1))
    plt.ylabel('Incident Severity')

     # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_claim(data):

    def claim_amount_grouping(data):
        if(data.total_claim_amount <= 10000):
            return '0 - 10.000'
        elif(data.total_claim_amount > 10000 and data.total_claim_amount <= 30000) : 
            return '10.001 - 30.000'
        elif(data.total_claim_amount > 30000 and data.total_claim_amount <= 50000) : 
            return '30.001 - 50.000'
        elif(data.total_claim_amount > 50000 and data.total_claim_amount <= 70000) : 
            return '50.001 - 70.000'
        elif(data.total_claim_amount > 70000 and data.total_claim_amount <= 90000) : 
            return '70.001 - 90.000'
        else : 
            return '90.000+'

    data['claim_amount_group'] = data.apply(claim_amount_grouping,axis = 1)

    claim_amount_group_order = ['0 - 10.000', '10.001 - 30.000', '30.001 - 50.000', '50.001 - 70.000', '70.001 - 90.000', '90.000+']
    data['claim_amount_group'] = pd.Categorical(data['claim_amount_group'], categories = claim_amount_group_order, ordered=True)

    fraud_data = data[data['fraud_reported'] == 'Y']

    claim_profile = pd.crosstab(index=fraud_data['claim_amount_group'],columns='count')

    ax = claim_profile.plot.barh(title = "Fraud Reported by Total Claim Amount Group", legend= False, color = '#e600ff',figsize=(12, 6))
    plt.ylabel('Total Claim Amount (US$)')

     # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)