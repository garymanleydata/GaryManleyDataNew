# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 18:13:22 2024

@author: garym
"""
# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# setup initial page config
st.set_page_config(
    page_title="parkrun Report Genator",
    page_icon="✅",
    layout="wide",
)

# Create a file uploader for Excel files
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
  try:

    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(uploaded_file)

    # Display the DataFrame in a table format
    st.dataframe(df.head(5),hide_index=True)

    # Display a success message
    st.success("Excel file uploaded successfully! Please check rows above")
    
    def safe_int_conversion(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return np.nan

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

    # Calculate gender counts
    gender_counts = df_split['GENDER'].value_counts()

    # Create a bar chart using Plotly Express
    fig = px.bar(x=gender_counts.index, y=gender_counts.values, labels={'x': 'Gender', 'y': 'Count'},
             title='Gender Distribution', color=gender_counts.index)
    # Customize the chart
    fig.update_traces(texttemplate='%{y}', textposition='inside')  # Display count above each bar
    fig.update_layout(
        legend=dict(orientation='h', yanchor='top', y=1.1),  # Set legend above the chart
            width=500, #
        )

    # Sum the columns
    df_to_sum = df_split[['MilestoneInd','PBCount','FirstAtEventCount','FirstTimerCount','VolunteerCount']]
    df_to_sum.rename(columns={'MilestoneInd': 'Run Milestones Achieved', 'PBCount': 'Count of PBs', 'FirstAtEventCount': 'First Timers At Event', 'FirstTimerCount': 'First Timers At parkrun', 'VolunteerCount': 'Volunteer Count'}, inplace=True)
    
    df_sum = df_to_sum[['Run Milestones Achieved','Count of PBs','First Timers At Event','First Timers At parkrun','Volunteer Count']].sum()

#    df_sum.columns.name = None
    df_sum.index.rename('', inplace=True)

    # Define desired colors (replace with your color choices)
    colours = ['red', 'green', 'blue', 'purple','orange']
          
    # Create the bar chart
    fig2 = px.bar(df_sum, x=df_sum.index, y=df_sum.values, text=df_sum.values,
             labels={'x': 'Metrics', 'y': 'Total Count'},
             title='Summary of Key Stats'
             ,  color=colours)
    fig2.update_layout(showlegend=False, width=500,)


    # Create two columns
    col1, col2 = st.columns(2)

# Add components to each column
    with col1:
        # Display the interactive chart in Streamlit
        st.plotly_chart(fig)

    with col2:


    # Display the chart
        st.plotly_chart(fig2)

  except:
     #Handle any potential errors
    st.error("An error occurred while processing the Excel file.")

else:
  st.info("Please upload an Excel file to proceed.")
  
  
