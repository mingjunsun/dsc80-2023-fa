# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def clean_universities(df):
    
    res = df.copy()
    #replace /n in institution
    res['institution'] = res['institution'].str.replace('\n', ', ')
    
    #Change the data type of the 'broad_impact' column to int
    res['broad_impact']= res['broad_impact'].astype(int)
    
    #Split 'national_rank' into two columns!!!!!!
    res[['nation','national_rank_cleaned']] = res.national_rank.str.split(", ",expand=True) 
    res = res.drop(columns=['national_rank'])
    res['nation'] = res['nation'].replace({
        'Czechia': 'Czech Republic',
        'UK': 'United Kingdom',
        'USA': 'United States'
    })
    res['national_rank_cleaned'] = res['national_rank_cleaned'].astype(int)
    
    
    res['is_r1_public'] = ((res['control'].notna()) & (res['city'].notna()) & (res['state'].notna()) & (res['control'] == 'Public'))
    res['is_r1_public'].fillna(False, inplace=True)  
    
    return res

def university_info(cleaned):
    lowest_mean_state = (cleaned.groupby('state')
            .filter(lambda df: df['institution'].count() >= 3)
            .groupby('state')['score']
            .mean().idxmin())
    
    proportions_within_100 = (cleaned[(cleaned['world_rank'] <= 100) 
                                      & (cleaned['quality_of_faculty'] <=100)].shape[0] /100)
    
    percentage = cleaned.groupby('state')['is_r1_public'].mean()
    num_state_50 = int(percentage[percentage <= 0.5].count())
    
    national_1 = cleaned[cleaned['national_rank_cleaned'] == 1].set_index('institution')
    lowest_world_rank = national_1['world_rank'].sort_values(ascending=False).idxmax()
    
    return [lowest_mean_state, proportions_within_100, num_state_50, lowest_world_rank]



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def std_scores_by_nation(cleaned):
    stdized = cleaned.groupby('nation')['score'].transform(lambda x: (x - x.mean()) / x.std(ddof=0))
    out = cleaned[['institution', 'nation']].assign(score=stdized)
    return out


def su_and_spread():
    return [2, 'United States']


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def read_linkedin_survey(dirname):
    
    files = [os.path.join(dirname, file) for file in os.listdir(dirname)]
    df_list = [pd.read_csv(file) for file in files]

    for df in df_list:
        df.columns = df.columns.str.lower().str.replace('_', ' ')

    df = pd.concat(df_list, sort=True)
    df = df[['first name', 'last name', 'current company', 'job title', 'email', 'university']]
    df = df.reset_index(drop=True)
    
    return df


def com_stats(df):
    ohios= df[df['university'].str.contains('Ohio', case=False, na = False)]
    ohio_nurse_prop = (ohios.loc[(ohios['job title'].str.contains('Nurse', case=False, na = False))].shape[0] / ohios.shape[0])
    
    endwith_engineer = df[df['job title'].str.endswith('Engineer', na=False)]['job title'].nunique()
    
    longest_title = df['job title'][df['job title'].str.len().idxmax()]
    
    manager_count = df.loc[df['job title'].str.contains('manager', case=False, na=False)].shape[0]
    
    return [ohio_nurse_prop, endwith_engineer, longest_title, manager_count]



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def read_student_surveys(dirname):
    
    files = [os.path.join(dirname, file) for file in os.listdir(dirname)]
    file_list = [pd.read_csv(f, index_col='id') for f in files]
    combined = pd.concat(file_list, axis=1, sort=True)

    return combined


def check_credit(df):
    ec = ((df.drop('name', axis=1).notnull().mean(axis=1) >= 0.5)
          .replace({False: 0, True: 5}))

    ec += min(((df.drop('name', axis=1).notnull().mean() >= 0.8).any().astype(int)),2)
        
    out = pd.concat([df[['name']], ec], axis=1, sort=True)
    
    out.columns = ['name', 'ec']

    return out


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def most_popular_procedure(pets, procedure_history):
    merged = pets.merge(right=procedure_history, on='PetID')
    return merged['ProcedureType'].value_counts().idxmax()

def pet_name_by_owner(owners, pets):
    pets = pets.rename(columns = {'Name': 'Petname'})
    merged_df = owners.merge(pets, on='OwnerID')
    res = (merged_df.groupby(['Name', 'Surname'])['Petname']
           .agg(lambda x: list(x) if len(x) > 1 else x.iloc[0])
           .reset_index('Surname')
           .drop('Surname', axis = 1)['Petname'])
    return res


def total_cost_per_city(owners, pets, procedure_history, procedure_detail):
    pets = pets.rename(columns = {'Name': 'Petname'})
    pet_owners=owners.merge(right=pets,how='left', on='OwnerID')
    pet_owners_history=pet_owners.merge(right=procedure_history,how='left', on='PetID')
    pet_owners_history_detail=pet_owners_history.merge(right=procedure_detail, how='left', on=['ProcedureType', 'ProcedureSubCode'])
    return pet_owners_history_detail.groupby('City')['Price'].sum()


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def average_seller(sales):
    sales = sales.copy().fillna(0)
    series=sales.groupby('Name')['Total'].mean().astype(int)
    res=pd.DataFrame({'Average Sales':series})
    return res

def product_name(sales):
    pivot=sales.pivot_table(
    index='Name',
    columns='Product',
    values='Total', 
    aggfunc='count')
    return pivot

def count_product(sales):
    return sales.pivot_table(index=['Product', 'Name'], 
                  columns='Date', 
                  values='Total', 
                  aggfunc='sum',
                 fill_value=0)

def total_by_month(sales):
    dates = sales["Date"]
    dates = pd.to_datetime(dates, format='%m.%d.%Y')
    months = dates.dt.month_name()
    sales['Month'] = months
    return sales.pivot_table(index=['Name', 'Product'], 
                  columns='Month', 
                  values='Total', 
                  aggfunc='sum',
                 fill_value=0)
