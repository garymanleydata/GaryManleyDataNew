# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# setup initial page config
st.set_page_config(
    page_title="Eastbourne parkrun Dashboard",
    page_icon="✅",
    layout="wide",
)

# Initialize connection.
conn = st.connection("snowflake")

option = st.sidebar.selectbox("Which Dashboard?", ('Top Performances', 'Latest Results', 'Event Summary','Club Page','Future Changes'), 2)

# If Top 1000 selected run the following
if option == 'Top Performances':

    # Query the top 100 ag view and return into a dataframe
    top50agQ = ('SELECT * FROM stg_top_100_ag')
    top50ag = pd.read_sql_query(top50agQ,conn);
    
    with st.sidebar:


#        displayoption = st.multiselect("Pick Age Bracket to Display",top50ag.AgeBracket.unique(),top50ag.AgeBracket.unique())
        displayoption = st.selectbox("Pick Age Bracket to Display",top50ag.AgeBracket.unique())

        
    st.title("Fastest Performances at Eastborune parkrun Dashboard")
   
    # Query the top 1000 view and return into a dataframe
    top1000Query = ('SELECT * FROM stg_top_1000')
    pdTop1000 = pd.read_sql_query(top1000Query,conn);

    st.write('**Top 1000 Times at Eastbourne parkrun**')  
    st.dataframe(pdTop1000,hide_index=True)

    # Query the top 1 view and return into a dataframe
    top1Query = ('SELECT * FROM stg_top1')
    pdTop1 = pd.read_sql_query(top1Query,conn);


    # Be good to break down / split out by year, and then do processing in df
    st.write('**First Finishers - Most and Most Eastbourne parkruns before 1st 1st**')  
    st.dataframe(pdTop1,hide_index=True)


    st.write('**Top 50 Times by Age Bracket at Eastbourne parkrun**')  
    top50ag = top50ag.loc[top50ag['AgeBracket'] == displayoption]      
    st.dataframe(top50ag,hide_index=True)

# Latest Event page
if option == 'Latest Results':
    # Query the tlatest event summary view and return into a dataframe
    toplatSummQ = ('SELECT * FROM stg_latest_event_v')
    toplatSumm = pd.read_sql_query(toplatSummQ,conn);

    st.write('**Latest Event Summary at Eastbourne parkrun**')  
    st.dataframe(toplatSumm,hide_index=True)
    
#stg_latest_event_all_v
    latALLQ = ('SELECT * FROM stg_latest_event_all_v')
    latSummAll = pd.read_sql_query(latALLQ,conn);

    st.write('**Latest Event Details at Eastbourne parkrun**')  
    st.dataframe(latSummAll,hide_index=True)

    fig = px.scatter(latSummAll, x="Position", y="TIMESECONDS",color="Club", hover_data=["Name", "Time"])
    st.plotly_chart(fig, use_container_width=True, sharing="streamlit")




# Should include bell shaped curve plot as well for last 10 events year on year change?



if option ==  'Event Summary':

## The have the event heat map


    # Query the tlatest event summary view and return into a dataframe
    topAllSummQ = ('SELECT * FROM stg_event_summy_v')
    topAllSumm = pd.read_sql_query(topAllSummQ,conn);
    
    st.write('**Eastbourne parkrun Attendance by Date**')  
    fig = px.bar(topAllSumm, x="Event Date", y="Total Athletes")
    st.plotly_chart(fig, use_container_width=True, sharing="streamlit")
    
    
    topAllSummBrQ = ('SELECT * FROM stg_bracket_by_year_v')
    topAllSummBr = pd.read_sql_query(topAllSummBrQ,conn);
    st.write('**Eastbourne parkrun by percentage in Finish Time Bracket**')  
    fig = px.line(topAllSummBr, x="Event Year", y=["Percent Sub 20","Percent 20-24:59 Count","Percent 25-29:59 Count","Percent 30-34:59 Count","Percent 35-40:59 Count", "Percent 40-44:59 Count" ,"Percent 45-49:59 Count","Percent 50-54:59 Count","Percent 55-59:59 Count", "Percent 60+ Count"])
    st.plotly_chart(fig, use_container_width=True, sharing="streamlit")    

    st.write('**Event Summary at Eastbourne parkrun**')  
    st.dataframe(topAllSumm,hide_index=True)



## have club page 
## Extract all views into GitHub








if option == 'Future Changes':
    st.write('**Planned Changes to the page**') 
    st.write('Add in some age grading calcuations')
    st.write('Add in some integration of weather data for analysis')
    st.write('Add first female finisher split to the 1st finishes page')