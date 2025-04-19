# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 19:16:52 2024
@author: garym

To Do: 

    
Create graphics can be played with in streamlit and  generate image
Tiles to show: Total Male / Female / Unknown / Total PBs / Total First Timers / Vols 
Tile to Show Average Time 
Bar Graph to show split by age categories
Bar Graph to show breakdown by minute finished 
Bar graph showing participants in each run / volunteer club

Table showing Official Milestones Reached and Unoffical Milestone reached
Table or graphic showing numbers / breakdown by running club where num runners > 5 or 10
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def safe_int_conversion(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return np.nan

# Specify the path to your Excel file
file_path = "parkrunsample.xlsx"

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(file_path)

# Access the first row and first column value
volunteer_list = df.iloc[0, 6]

split_data = df['PARKRUNNER'].str.extract(r'([^\d]*)(\d+.*)')

# Renaming the columns
split_data.columns = ['Name', 'MilestonePrePro']

# Concatenating the split data with the original DataFrame
df_split = pd.concat([df, split_data], axis=1)

# Fill NaN values in Column1 with values from Column2
df_split['Name'] = df_split['Name'].fillna(df_split['PARKRUNNER'])

# Process Gender to only have the Gender
df_split['GENDER'] = df['GENDER'].str.split().str[0]
df_split['GENDER'].fillna('Unknown', inplace=True)

#Process the Age Group Column
df_split[['AgeBracket', 'AgeGrade']] = df_split['AGE GROUP'].str.split('\n', expand=True)
df_split['AgeGrade'] = df_split['AgeGrade'].replace({'[^0-9\.]': ''}, regex=True)

#Split run time and PB / First Timer Status
df_split[['TimeMMSS', 'RunStatus']] = df_split['TIME'].str.split('\n', expand=True)

#Process Milestone Columns into Total runs, run clubs and volunteer club
df_split[['Totalparkruns', 'MilestoneClubs']] = df_split['MilestonePrePro'].str.split('|', expand=True)
df_split['Totalparkruns'] = df_split['Totalparkruns'].replace({'[^0-9\.]': ''}, regex=True)

## Extract Milestone Numbers 
df_split['RunMilestone'] = df_split['MilestoneClubs'].str.extract(r'Member of the (\d+) Club')
df_split['VolMilestone'] = df_split['MilestoneClubs'].str.extract(r'Member of the Volunteer (\d+) Club')

# Process the time column 

split_time = df_split['TimeMMSS'].str.split(':', expand=True)
if len(split_time.columns) == 2:
    split_time.insert(0, 'Hours', 0)
split_time.columns = ['Hours', 'Minutes', 'Seconds']

df_split = pd.concat([df_split, split_time], axis=1)

# Adjusting the minutes column based on hours

# Apply the custom function to the 'Hours' and 'Minutes' columns
df_split['Hours'] = df_split['Hours'].apply(safe_int_conversion)
df_split['Minutes'] = df_split['Minutes'].apply(safe_int_conversion)
df_split['Seconds'] = df_split['Seconds'].apply(safe_int_conversion)

# Calculate total minutes
df_split['Minutes'] = (df_split['Hours'] * 60) + df_split['Minutes']
df_split['TotalSec'] = (df_split['Minutes'] * 60) + df_split['Seconds']

# Create a new column 'MilestoneInd' with default value 0
df_split[['MilestoneInd','PBCount','FirstAtEventCount','FirstTimerCount','VolunteerCount']] = 0

# Set the value to 1 where 'Totalparkruns' and 'RunMilestone' are equal
df_split.loc[df_split['Totalparkruns'] == df_split['RunMilestone'], 'MilestoneInd'] = 1
df_split.loc[df_split['RunStatus'] == 'New PB!', 'PBCount'] = 1
df_split.loc[df_split['RunStatus'] == 'First Timer!', 'FirstAtEventCount'] = 1
df_split.loc[(df_split['Totalparkruns'] == '1') & (df_split['FirstAtEventCount'] == 1), 'FirstTimerCount'] = 1

names_list = volunteer_list.split(", ")
num_names = len(names_list)
df_split.loc[0, 'VolunteerCount'] = num_names


# Drop the Original columns no longer needed
df_split.drop(['Volunteers','PARKRUNNER','AGE GROUP','TIME','MilestoneClubs','MilestonePrePro','Hours'], axis=1, inplace=True)

# Set up the plot
plt.figure(figsize=(8, 6))
sns.set_style("whitegrid")

# Create the bar plot
ax = sns.countplot(x='GENDER', data=df_split, palette='pastel')

# Customize the plot
ax.set_title("Gender Distribution")
ax.set_xlabel("Gender")
ax.set_ylabel("Count")

# Annotate the bars with the count values
for rect in ax.patches:
    height = rect.get_height()
    ax.annotate(f"{int(height)}", xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

# Show the plot
plt.show()

    # Sum the columns
df_sum = df_split[['MilestoneInd','PBCount','FirstAtEventCount','FirstTimerCount','VolunteerCount']].sum()
#df_sum.rename(columns={'MilestoneInd': 'RunMilestonesAchieved'}, inplace=True)#, 'PBCount': 'Count of PBs', 'FirstAtEventCount': 'First Timers At Event', 'FirstTimerCount': 'First Timers At parkrun', 'VolunteerCount': 'Volunteer Count'}, inplace=True)

dfMiles = df_split.loc[df_split['MilestoneInd'] == 1]
dfMiles = dfMiles[['Name','RunMilestone']]

#df_split.to_csv('output.csv', index=False)  