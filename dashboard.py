#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 17:34:12 2022

@author: erishachand

Dashboard of Daily Stats

"""

import pandas as pd
import plotly
import plotly.express as px
import streamlit as st
#from plotdailysankey import *


def genSankey(df,cat_cols=[],value_cols='',title=''):
    # maximum of 6 value cols -> 6 colors
    #colorPalette = ['#4B8BBE','#306998','#FFE873','#FFD43B','#646464']
    colorPalette = ['#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB', '#B5EAD7', '#C7CEEA']
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp
        
    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))
    
    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum
        
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
    
    # creating the sankey diagram
    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count']
        )
      )
    
    layout =  dict(
        title = title,
        font = dict(
          size = 10
        )
    )
       
    fig = dict(data=[data], layout=layout)
    
    return fig



st.set_page_config(layout="wide")

df = pd.DataFrame(px.data.gapminder())

def dailystat():
    
    # Start of dashboard
    st.title('Daily Statistics')

    st.header('Friday 30th September 2022')

    st.markdown('#')
    
    st.write('Data Analysed:')
    st.caption('- Morning: 8am-10am')
    st.caption('- Midday: 11am-1pm')
    st.caption('- Afternoon: 2pm-4pm')
    st.caption('- Evening: 5pm-7pm')

    # Daily breakdown

    # Breakdown of flow origin, no. of GB & packets transferred

    st.markdown('#')

    # st.subheader('Breakdown of Flows')
    
    # st.write('Flow Origin:')
    # df = pd.read_csv('/Users/erishachand/Desktop/UNIVERSITY/T3 2022/ThesisC/Code/floworigindaily.csv', sep="|")
    
    # col1, col2, col3, col4 = st.columns(4) 
    # with col1: 
    #     st.write(' ') 
    # with col2: 
    #     st.write(px.bar(df, x="Time of Day", y="No. of Bytes (GB)", color="Host Type"))
    # with col3:
    #     st.write(' ') 
    # with col4:
    #     st.write(' ') 


    df = pd.read_csv("dailybreakdown.csv", sep="|")

    option = st.selectbox(
        'Total Transferred:',
        ('Bytes', 'Packets'))

    if (option == 'Bytes'):
        col1, col2, col3, col4 = st.columns(4) 
        with col1: 
            st.write(' ') 
        with col2: 
            st.write(px.bar(x= df['time'], y=df['byte'], color_discrete_sequence =['skyblue'],
                            labels={'x': 'Time of Day', 'y':'No. of Bytes (GB)'}))
        with col3:
            st.write(' ') 
        with col4:
            st.write(' ') 

    elif (option == 'Packets'):
        col1, col2, col3, col4 = st.columns(4) 
        with col1: 
            st.write(' ') 
        with col2: 
            st.write(px.bar(x= df['time'], y=df['packet'], color_discrete_sequence =['skyblue'],
                            labels={'x': 'Time of Day', 'y':'No. of Packets'}))
        with col3:
            st.write(' ') 
        with col4:
            st.write(' ') 
        

    # Breakdown of no. of entities & services at different times of day -> line graph

    df = pd.read_csv("dailybreakdown.csv", sep="|")

    option1 = st.selectbox(
        'Total Communicated:',
        ('Entities', 'Services'))

    if (option1 == 'Entities'):
        col1, col2, col3, col4 = st.columns(4) 
        with col1: 
            st.write(' ') 
        with col2: 
            st.write(px.bar(x= df['time'], y=df['orgs'], color_discrete_sequence =['plum'],
                            labels={'x': 'Time of Day', 'y':'No. of Entities'}))
        with col3:
            st.write(' ') 
        with col4:
            st.write(' ') 

    elif (option1 == 'Services'):
        col1, col2, col3, col4 = st.columns(4) 
        with col1: 
            st.write(' ') 
        with col2: 
            st.write(px.bar(x= df['time'], y=df['ports'], color_discrete_sequence =['plum'],
                            labels={'x': 'Time of Day', 'y':'No. of Services'}))
        with col3:
            st.write(' ') 
        with col4:
            st.write(' ') 



    # Plot Sankey Diagram

    st.subheader('Sankey Diagram')
    
    option1 = st.selectbox(
        'Type of Diagram:',
        ('Technical', 'High-Level'))

    if (option1 == 'Technical'):
        df = pd.read_csv("dailysankey.csv", sep="|")
        cat = ["UNSW EE Building", "time", "protocol", "service", "org", "country"]
        fig = genSankey(df,cat,"byte", '')

        st.plotly_chart(fig,use_container_width=True)

    elif (option1 == 'High-Level'):
        df = pd.read_csv("highleveldailysankey.csv", sep="|")
        cat = ["UNSW EE Building", "day", "service", "org", "country"]
        fig = genSankey(df,cat,"byte", '')
    
        st.plotly_chart(fig,use_container_width=True)

        st.write('Categorised By Service Type')
        st.caption('- Conferencing: plethora, cleanerliverc, twrpc')
        st.caption('- Web Browsing: https, http & threshold: <3.5MB')
        st.caption('- Video Streaming: https, http & threshold: >=3.5MB, <3.125MB/s')
        st.caption('- Gaming: xbox, palace-2')
        st.caption('- Emailing: imaps')
        st.caption('- Printing: hp-pdl-datastr')

        st.markdown('#')

    # Plot sunburst diagrams

    # Top ext entities
    st.subheader('External Entities Distribution')
    
    option2 = st.selectbox(
        'Time:',
        ('Morning', 'Midday', 'Afternoon', 'Evening'))
    
    if (option2 == 'Morning'):
       
        df = pd.read_csv("csventitiesunburst09308-10.csv", sep="|")
    
        df["time"] = "Morning"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "org"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
        

    elif (option2 == 'Midday'):
        
        df = pd.read_csv("csventitiesunburst093011-13.csv", sep="|")
    
        df["time"] = "Midday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "org"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
    
    
    elif (option2 == 'Afternoon'):
        
        df = pd.read_csv("csventitiesunburst093014-16.csv", sep="|")
    
        df["time"] = "Afternoon"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "org"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
        
    
    elif (option2 == 'Evening'):
        
        df = pd.read_csv("csventitiesunburst093017-19.csv", sep="|")
    
        df["time"] = "Evening"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "org"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
        
    
    

    # df = pd.read_csv("/Users/erishachand/Desktop/UNIVERSITY/T3 2022/ThesisC/Code/dailysunburstcompanies.csv", sep="|")
    # df["day"] = "Mon 26th Sept"
    # df = df.reset_index()

    # fig = px.sunburst(df,
    #                   path=["day", "time", "org"],
    #                   values='byte',
    #                   title="", color_continuous_scale="purpor")

    # st.plotly_chart(fig,use_container_width=True)
    
    # st.write('Top Companies Include:')
    # st.caption('1. Microsoft Corporation')
    # st.caption('2. Vocus')
    # st.caption('3. Google LLC')
    # st.caption('4. Cloudfare, Inc.')
    # st.caption('5. Akamai Technologies, Inc.')

    #st.markdown('#')

    # Top services 
    st.subheader('Services Distribution')
    
    option3 = st.selectbox(
        ' Time:',
        ('Morning', 'Midday', 'Afternoon', 'Evening'))
    
    if (option3 == 'Morning'):

        df = pd.read_csv("csvdailytimesunburst09308-10.csv", sep="|")
    
        df["time"] = "Morning"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "high", "service"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
        

    elif (option3 == 'Midday'):
        
        df = pd.read_csv("csvdailytimesunburst093011-13.csv", sep="|")
    
        df["time"] = "Midday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "high", "service"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
    
    
    elif (option3 == 'Afternoon'):
        
        df = pd.read_csv("csvdailytimesunburst093014-16.csv", sep="|")
    
        df["time"] = "Afternoon"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "high", "service"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
        
    
    elif (option3 == 'Evening'):
        
        df = pd.read_csv("csvdailytimesunburst093017-19.csv", sep="|")
    
        df["time"] = "Evening"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "high", "service"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
        

    # df = pd.read_csv("/Users/erishachand/Desktop/UNIVERSITY/T3 2022/ThesisC/Code/dailysunburstservices.csv", sep="|")

    # df["day"] = "Mon 26th Sept"
    # df = df.reset_index()

    # fig = px.sunburst(df,
    #                   path=["day", "time", "service"],
    #                   values='byte',
    #                   title="", color_continuous_scale="sunset")

    # st.plotly_chart(fig,use_container_width=True)

    # st.write('Top Services Include:')
    # st.caption('1. plethora')
    # st.caption('2. https')
    # st.caption('3. cleanerliverc')
    # st.caption('4. twrpc')
    # st.caption('5. http')
    


def weeklystat():
    
    # Start of dashboard
    st.title('Weekly Statistics')

    st.header('Week 3')

    st.markdown('#')

    st.write('Data Analysed:') 
    st.caption('- 26-30/09/22 (Monday-Friday) 9am-5pm')

    # Daily breakdown
    
    # Breakdown of flow origin, no. of GB & packets transferred

    st.markdown('#')

    # st.subheader('Breakdown of Flows')
    
    # st.write('Flow Origin:')
    # df = pd.read_csv('/Users/erishachand/Desktop/UNIVERSITY/T3 2022/ThesisC/Code/floworiginweekly.csv', sep="|")
    
    # col1, col2, col3, col4 = st.columns(4) 
    # with col1: 
    #     st.write(' ') 
    # with col2: 
    #     st.write(px.bar(df, x="Time of Day", y="No. of Bytes (GB)", color="Host Type"))
    # with col3:
    #     st.write(' ') 
    # with col4:
    #     st.write(' ') 
        

    df = pd.read_csv("weeklybreakdown.csv", sep="|")

    option = st.selectbox(
        'Total Transferred:',
        ('Bytes', 'Packets'))

    if (option == 'Bytes'):
        col1, col2, col3, col4 = st.columns(4) 
        with col1: 
            st.write(' ') 
        with col2: 
            st.write(px.bar(x= df['time'], y=df['byte'], color_discrete_sequence =['skyblue'],
                            labels={'x': 'Day', 'y':'No. of Bytes (GB)'}))
        with col3:
            st.write(' ') 
        with col4:
            st.write(' ') 

    elif (option == 'Packets'):
        col1, col2, col3, col4 = st.columns(4) 
        with col1: 
            st.write(' ') 
        with col2: 
            st.write(px.bar(x= df['time'], y=df['packet'], color_discrete_sequence =['skyblue'],
                            labels={'x': 'Day', 'y':'No. of Packets'}))
        with col3:
            st.write(' ') 
        with col4:
            st.write(' ') 
        

    # Breakdown of no. of entities & services at different times of day -> line graph

    df = pd.read_csv("weeklybreakdown.csv", sep="|")

    option1 = st.selectbox(
        'Total Communicated:',
        ('Entities', 'Services'))

    if (option1 == 'Entities'):
        col1, col2, col3, col4 = st.columns(4) 
        with col1: 
            st.write(' ') 
        with col2: 
            st.write(px.bar(x= df['time'], y=df['orgs'], color_discrete_sequence =['plum'],
                            labels={'x': 'Day', 'y':'No. of Entities'}))
        with col3:
            st.write(' ') 
        with col4:
            st.write(' ') 

    elif (option1 == 'Services'):
        col1, col2, col3, col4 = st.columns(4) 
        with col1: 
            st.write(' ') 
        with col2: 
            st.write(px.bar(x= df['time'], y=df['ports'], color_discrete_sequence =['plum'],
                            labels={'x': 'Day', 'y':'No. of Services'}))
        with col3:
            st.write(' ') 
        with col4:
            st.write(' ') 



    # Plot Sankey Diagram

    st.subheader('Sankey Diagram')
    
    option1 = st.selectbox(
        'Type of Diagram:',
        ('Technical', 'High-Level'))

    if (option1 == 'Technical'):
        df = pd.read_csv("weeklysankey.csv", sep="|")
        cat = ["UNSW EE Building", "time", "protocol", "service", "org", "country"]
        fig = genSankey(df,cat,"byte", '')

        st.plotly_chart(fig,use_container_width=True)

    elif (option1 == 'High-Level'):
        df = pd.read_csv("highlevelweeklysankey.csv", sep="|")
        cat = ["UNSW EE Building", "day", "service", "org", "country"]
        fig = genSankey(df,cat,"byte", '')
    
        st.plotly_chart(fig,use_container_width=True)

        st.write('Categorised By Service Type')
        st.caption('- Conferencing: plethora, cleanerliverc, twrpc')
        st.caption('- Web Browsing: https, http & threshold: <3.5MB')
        st.caption('- Video Streaming: https, http & threshold: >=3.5MB, <3.125MB/s')
        st.caption('- Gaming: xbox, palace-2')
        st.caption('- Emailing: imaps')
        st.caption('- Printing: hp-pdl-datastr')

        st.markdown('#')




    # Plot sunburst diagrams

    # Top ext entities
    st.subheader('External Entities Distribution')
    
    option2 = st.selectbox(
        'Time:',
        ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'))
    
    if (option2 == 'Monday'):

        df = pd.read_csv("csventitiesunburstmonday.csv", sep="|")
    
        df["time"] = "Monday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "org"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
        

    elif (option2 == 'Tuesday'):
        
        df = pd.read_csv("csventitiesunbursttuesday.csv", sep="|")
    
        df["time"] = "Tuesday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "org"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
    
    
    elif (option2 == 'Wednesday'):
        
        df = pd.read_csv("csventitiesunburstwednesday.csv", sep="|")
    
        df["time"] = "Wednesday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "org"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
        
    
    elif (option2 == 'Thursday'):
        
        df = pd.read_csv("csventitiesunburstthursday.csv", sep="|")
    
        df["time"] = "Thursday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "org"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
    
    
    elif (option2 == 'Friday'):
        
        df = pd.read_csv("csventitiesunburstfriday.csv", sep="|")
    
        df["time"] = "Friday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "org"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)


    # df = pd.read_csv("/Users/erishachand/Desktop/UNIVERSITY/T3 2022/ThesisC/Code/weeklysunburstcompanies.csv", sep="|")
    # df["week"] = "Week 3"
    # df = df.reset_index()

    # fig = px.sunburst(df,
    #                   path=["week", "time", "org"],
    #                   values='byte',
    #                   title="", color_continuous_scale="purpor")

    # st.plotly_chart(fig,use_container_width=True)

    # st.write('Top Companies Include:')
    # st.caption('1. Microsoft Corporation')
    # st.caption('2. Google LLC')
    # st.caption('3. Akamai Technologies, Inc.')
    # st.caption('4. Cloudfare, Inc.')
    # st.caption('5. Vocus')

    # st.markdown('#')

    # Top services 
    st.subheader('Services Distribution')
    
    option3 = st.selectbox(
        ' Time:',
        ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'))
    
    if (option3 == 'Monday'):

        df = pd.read_csv("csvdailytimesunburstmonday.csv", sep="|")
    
        df["time"] = "Monday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "high", "service"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
        

    elif (option3 == 'Tuesday'):
        
        df = pd.read_csv("csvdailytimesunbursttuesday.csv", sep="|")
    
        df["time"] = "Tuesday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "high", "service"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
    
    
    elif (option3 == 'Wednesday'):
        
        df = pd.read_csv("csvdailytimesunburstwednesday.csv", sep="|")
    
        df["time"] = "Wednesday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "high", "service"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
        
    
    elif (option3 == 'Thursday'):
        
        df = pd.read_csv("csvdailytimesunburstthursday.csv", sep="|")
    
        df["time"] = "Thursday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "high", "service"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)
    
    
    elif (option3 == 'Friday'):
        
        df = pd.read_csv("csvdailytimesunburstfriday.csv", sep="|")
    
        df["time"] = "Friday"
        df = df.reset_index()
    
        fig = px.sunburst(df,
                          path=["time", "high", "service"],
                          values='byte',
                          title="", color_continuous_scale="sunset")
        
        st.plotly_chart(fig,use_container_width=True)


    # df = pd.read_csv("/Users/erishachand/Desktop/UNIVERSITY/T3 2022/ThesisC/Code/weeklysunburstservices.csv", sep="|")

    # df["week"] = "Week 3"
    # df = df.reset_index()

    # fig = px.sunburst(df,
    #                   path=["week", "time", "service"],
    #                   values='byte',
    #                   title="", color_continuous_scale="sunset")

    # st.plotly_chart(fig,use_container_width=True)

    # st.write('Top Services Include:')
    # st.caption('1. https')
    # st.caption('2. plethora')
    # st.caption('3. cleanerliverc')
    # st.caption('4. http')
    # st.caption('5. twrpc')



# Page Preference 

page = st.sidebar.selectbox('Select Dashboard Page:',['Daily Statistics','Weekly Statistics']) 
if page == 'Daily Statistics':
    dailystat()
else:
    weeklystat()





