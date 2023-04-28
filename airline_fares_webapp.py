# Import the libraries
import pandas as pd
import numpy as np

import plotly.express as px
import matplotlib.pyplot as plt

import folium

from streamlit_folium import st_folium, folium_static
import folium
import streamlit as st

############################################################################################################################
###################################################   Read the datasets   ##################################################
############################################################################################################################

data1 = pd.read_csv("new_dataset_1.csv")
data2 = pd.read_csv("new_dataset_2.csv")

#data = data1.append(data2)
data = pd.concat((data1, data2), axis = 0)
data.reset_index(inplace=True)
data = data.drop(['Unnamed: 0','index'],axis=1)

############################################################################################################################
##########################################     Coordinates of the capitals     #############################################
############################################################################################################################

#[Latitude,Longitude]

cities_lat_lng = {'Delhi': [28.679079, 77.069710],
                  'Mumbai': [19.076090, 72.877426],
                  'Bangalore': [12.972442, 77.580643],
                  'Hyderabad': [17.387140, 78.491684],
                  'Kolkata': [22.572645, 88.363892],
                  'Chennai': [13.067439, 80.237617],
                  'Ahmedabad': [23.033863, 72.585022]}

cities = data['Arrival city'].values
############################################################################################################################
##############################################     Define some functions     ###############################################
############################################################################################################################

def stacked_barplots_2_variables(df, variables, axes):
    
    # create the a table by grouping on the given variables
    conn_var = df.groupby(variables).size().unstack()
    conn_var = round((conn_var/conn_var.sum()),4).T

    # create the percentages for the variable of x-axis
    perc_b = round((df[variables[1]].value_counts()/df[variables[1]].value_counts().sum())*100,2)
    perc_b = perc_b.to_frame()
    #perc_b = perc_b.rename(columns={variables[1]:"Percentage on data"})
    perc_b = perc_b.rename(columns={'count':'Percentage on data'})
    perc_b = perc_b.reset_index()
    perc_b = perc_b.rename(columns={'index':variables[1]})
    
    # merge the tables which have been created above
    conn_var_copy = conn_var.copy()
    conn_var_copy.reset_index(inplace=True)
    unify = conn_var_copy.merge(perc_b, on=variables[1])
    
    # plot the stacked bars
    conn_var.plot(ax=axes, kind='bar', width=0.2, stacked=True)
    
    # give labels on x-axis
    for_x_axis = unify[[variables[1],'Percentage on data']]
    x_ticks = np.arange(len(unify[variables[1]])) 
    x_ticklabels = for_x_axis[variables[1]].values
    axes.set_xticks(x_ticks)
    axes.set_xticklabels(x_ticklabels, fontsize=18, rotation=25)
    axes.set_xlabel(variables[1], fontsize=22, labelpad=15)

    # give labels on y-axis
    y_ticks, y_ticklabels = [0.25,0.5,0.75,1], [25,50,75,100]
    axes.set_yticks(y_ticks)
    axes.set_yticklabels(y_ticklabels, fontsize=18)
    axes.set_ylim(0,1.66)

    # legendbox
    axes.legend(loc='upper center', fontsize=18)
    
    # show the percentages of each key value on x-axis, if they are larger than 15%
    for p in axes.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height!=0 and height>=0.15:
            axes.text(x+width/2, y+height/2, '{:.1f}%'.format(height*100), 
                    horizontalalignment='center', verticalalignment='center',fontsize=18)
    
    # show the percentages of the x-axis variable which is in the whole dataset
    for count, value in enumerate(unify['Percentage on data']):
        axes.text(count, 1.04, '{:.2f}%'.format(value), 
                  horizontalalignment='center', 
                  verticalalignment='center',
                  fontsize=22)
                
############################################################################################################################
# ------------------------------------------------------------------------------------------------------------------------ #
############################################################################################################################
###################################################  Start of the code  ####################################################
############################################################################################################################
# ------------------------------------------------------------------------------------------------------------------------ #
############################################################################################################################
############################################################################################################################
##################################################  First row of plots  ####################################################
############################################################################################################################

st.set_page_config(layout="wide")
title = '<p style="text-align: center; font-size: 24px;"><strong>This Web App shows data related to the prices of airline companies which are are operating flights around 7 cities in India.</strong></p>'
st.write(title, unsafe_allow_html=True)
#st.write("## This Web App shows data related to the prices of airline companies which are are operating flights around 7 cities in India.")
st.write("###### Created by Antonios Raptakis")
st.write("")
st.write("")
st.write("The csv file has been taken by kaggle.")


col1, col2 = st.columns((1,1), gap="large")

airlines = round((data.Airline.value_counts()/data.Airline.value_counts().sum())*100,2)

with col1:
    column_title = '<p style="text-align: center; font-size: 22px;">Listed Airlines with the respective percentage in the dataset</p>'
    col1.write(column_title, unsafe_allow_html=True)
    
    fig = px.bar(airlines, orientation='h', width=640, height=480)
    fig.update_layout(xaxis_title="Percentage (%)",
                      xaxis_title_font = dict(size=25),
                      xaxis = dict(tickfont = dict(size=20)),
                      yaxis_title="Airlines",
                      yaxis = dict(tickfont = dict(size=20)),
                      yaxis_title_font = dict(size=25),
                      showlegend=False)
    fig.update_xaxes(title_font_family="Times New Roman")

    st.plotly_chart(fig)
    
# Map visualization with all of the airbnb listings of the specific city by highlighting the neighbourhoods
with col2:
    column_title = '<p style="text-align: center; font-size: 22px;">Location of the cities on the map</p>'
    col2.write(column_title, unsafe_allow_html=True)
    map = folium.Map(location=[20.89,78.07],
                   tiles="Stamen Terrain", zoom_start=5.2)#Stamen Terrain
    for key,val in cities_lat_lng.items():
        folium.Marker(location=val).add_to(map)


    folium_static(map, width=600, height=460)

############################################################################################################################
############################################################################################################################

st.write("")
st.write("")
text = '<p style="text-align: center; font-size: 20px;">Use the drop down menus to select different values and see the price comparison of the airlines grouped by class.</p>'
st.write(text, unsafe_allow_html=True)

st.write("")

text = '<p style="text-align: center; font-size: 20px;">The left graph shows the boxplot comparison of fares prices between. By selecting a particular airline, you can examine for that airline the fare prices over the days remaining for the journey, grouped by class, and the fare prices over the duration of the journey in hours, grouped by the total number of stops, as shown in the middle and right plots. The total number of stops indicates the number of connecting flights.</p>'
st.write(text, unsafe_allow_html=True)
st.write("")
st.write("")

############################################################################################################################
#------------------------------------------------  First row of options  --------------------------------------------------#
############################################################################################################################

col1, col2, col3, col4, col5 = st.columns((1,1,1,1,1))

with col1:
    select_departure_city = st.selectbox('Select the city of departure', data['Departure city'].unique(),0)
with col2:
    cities_of_arrival = [city for city in data['Arrival city'].unique() if city!=select_departure_city]
    select_arrival_city = st.selectbox('Select the city of arrival', cities_of_arrival, 0)
with col3:
    select_journey_day = st.selectbox('Select the day of journey', data['Weekday'].unique(),0)
with col4:
    select_departure_time = st.selectbox('Select the time of departure', data.Departure.unique(),0)
with col5:
    select_arrival_time = st.selectbox('Select the time arrival', data.Arrival.unique(),0)

############################################################################################################################
#------------------------------------------------  Second row of options  -------------------------------------------------#
############################################################################################################################

dataset = data[(data.Departure==select_departure_time) & (data.Arrival==select_arrival_time) & 
               (data['Departure city']==select_departure_city) & (data['Arrival city']==select_arrival_city) & 
               (data['Weekday']==select_journey_day)]



_, _, _, col, _ = st.columns((1,1,1,1,1))

with col:
    select_airline = st.radio('Select the airline 👇', dataset.Airline.unique(),0)

############################################################################################################################
##################################################  Second row of plots  ###################################################
############################################################################################################################

col1, col2, col3 = st.columns((1,1,1))


with col1:
    fig = px.box(dataset, x="Airline", y="Fare(€)", color="Class")
                 #color_discrete_sequence=['steelblue','firebrick'])
    fig.update_layout(title_text="Comparison of fare prices for the different airlines", title_x=0.15)
    fig.update_traces(quartilemethod="exclusive")
    st.plotly_chart(fig, use_container_width=True)
    
    
with col2:
    fig = px.line(dataset[dataset.Airline==select_airline], x="Days left", y="Fare(€)", color="Class")
    st.plotly_chart(fig, use_container_width=True)

    
with col3:
    fig = px.scatter(dataset[dataset.Airline==select_airline], x="Duration in hours", y="Fare(€)", color='Total stops')
    st.plotly_chart(fig, use_container_width=True)
    
############################################################################################################################
############################################################################################################################
# ----------------------------------------------------   New Section   --------------------------------------------------- #
############################################################################################################################
############################################################################################################################

text = '<p style="text-align: center; font-size: 28px;"><strong>Descriptive Statistics</strong></p>'
st.write(text, unsafe_allow_html=True)

st.write("")

text = '<p style="text-align: center; font-size: 20px;">Explore the dataset further by selecting the values for which you want to see the percentages in the dataset.</p>'
st.write(text, unsafe_allow_html=True)

st.write("")
st.write("")

############################################################################################################################
############################################################################################################################
# ------------------------------------------------------------------------------------------------------------------------ #
############################################################################################################################
############################################################################################################################
############################################################################################################################
#-------------------------------------------------  Third row of options  -------------------------------------------------#
############################################################################################################################

col1, col2 = st.columns((1,1))

not_included_options = ['Date of journey','Duration in hours','Flight code','Departure - Arrival','Days left','Fare(€)']
options = [col for col in data.columns if col not in not_included_options]


with col1:
    col1_1, col1_2 = st.columns((1,1))
    with col1_1:
        select_xaxis = st.selectbox('Select variable for x-axis', options,0) #refers to the variable on x-axis
    with col1_2:
        for_stacked = [col for col in options if col!=select_xaxis]
        select_stacked_bar = st.selectbox('Select variable for stacked bars', for_stacked,0) #refers to the variable for stacked bar
  
excluded_options = [select_xaxis, select_stacked_bar]        
with col2:
    col2_1, col2_2 = st.columns((1,1))    
    with col2_1:
        options2_1 = [col for col in options if col not in excluded_options]
        select_xaxis2_1 = st.selectbox('Select variable for x-axis', options2_1,0) #refers to the variable on x-axis
        excluded_options.append(select_xaxis2_1)
    with col2_2:
        for_stacked2 = [col for col in options if col not in excluded_options]
        select_stacked_bar2_1 = st.selectbox('Select variable for stacked bars', for_stacked2,0) #refers to the variable for stacked bar
        excluded_options.append(select_stacked_bar2_1)   
    

############################################################################################################################
#-------------------------------------------------  Fourth row of options  ------------------------------------------------#
############################################################################################################################

_ , col2 = st.columns((1,1))


with col2:
    col2_1, col2_2 = st.columns((1,1))
    with col2_1:
        for_stacked_fixed_value_col2 = st.radio('Select the %s' %select_stacked_bar, data[select_stacked_bar].unique(), 0)     
    with col2_2:
        select_xaxis_fixed_value_col2 = st.radio('Select the %s' %select_xaxis, data[select_xaxis].unique(), 0)
                
############################################################################################################################
##################################################  Third row of plots  ###################################################
############################################################################################################################

col1 , col2 = st.columns((1,1))


with col1:
         
    fig, ax = plt.subplots(1,1,figsize=(20,13))
    stacked_barplots_2_variables(data,[select_stacked_bar,select_xaxis],ax)
    ax.set_ylabel('Percentage (%)', fontsize=22, labelpad=20)
    st.pyplot(fig)

    
with col2:            
    fig, ax = plt.subplots(1,1,figsize=(20,13))
    
    dataset_col2 = data[(data[select_stacked_bar]==for_stacked_fixed_value_col2) &
                        (data[select_xaxis]==select_xaxis_fixed_value_col2)]
    if dataset_col2.shape[0]==0:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        warn = '<p style="text-align: center; font-size: 20px;">No data for plot with these options! Please, select other options!</p>'
        col2.write(warn, unsafe_allow_html=True)
    else:
        stacked_barplots_2_variables(dataset_col2,[select_stacked_bar2_1,select_xaxis2_1],ax)
        st.pyplot(fig)

        
############################################################################################################################
#-------------------------------------------------  Fifth row of options  -------------------------------------------------#
############################################################################################################################

col1, col2 = st.columns((1,1))


with col1:
    col1_1, col1_2 = st.columns((1,1))
    with col1_1:
        options3_1 = [col for col in options if col not in excluded_options]
        select_xaxis3_1 = st.selectbox('Select variable for x-axis', options3_1,0) #refers to the variable on x-axis
        excluded_options.append(select_xaxis3_1)
    with col1_2:
        for_stacked3 = [col for col in options if col not in excluded_options]
        select_stacked_bar3_1 = st.selectbox('Select variable for stacked bars', for_stacked3,0) #refers to the variable for stacked bar
        excluded_options.append(select_stacked_bar3_1)   

with col2:
    options4_1 = [col for col in options if col not in excluded_options]
    select_xaxis4_1 = st.selectbox('Select variable for x-axis', options4_1,0) #refers to the variable on x-axis
    excluded_options.append(select_xaxis4_1)
    remaining_option = [x for x in options if x not in excluded_options][0]
   
        
    
############################################################################################################################
#-------------------------------------------------  Sixth row of options  -------------------------------------------------#
############################################################################################################################

col1, col2 = st.columns((1,1))


with col1:
    col1_1, col1_2 = st.columns((1,1))
    with col1_1:
        for_stacked_fixed_value_col3 = st.radio('Select the %s' %select_stacked_bar2_1, data[select_stacked_bar2_1].unique(), 0)
    with col1_2:
        select_xaxis_fixed_value_col3 = st.radio('Select the %s' %select_xaxis2_1, data[select_xaxis2_1].unique(), 0)
   
    
with col2:
    col2_1, col2_2 = st.columns((1,1))
    with col2_1:
        for_stacked_fixed_value_col4_1 = st.radio('Select the %s' %select_stacked_bar3_1, data[select_stacked_bar3_1].unique(), 0)
    with col2_2:   
         select_xaxis_fixed_value_col4_2 = st.radio('Select the %s' %select_xaxis3_1, data[select_xaxis3_1].unique(), 0)


############################################################################################################################
##################################################  Third row of plots  ###################################################
############################################################################################################################

col1, col2 = st.columns((1,1))


with col1:
    dataset_col3 = dataset_col2[(dataset_col2[select_stacked_bar2_1]==for_stacked_fixed_value_col3) & 
                                (dataset_col2[select_xaxis2_1]==select_xaxis_fixed_value_col3)]
    if dataset_col3.shape[0]==0:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        warn = '<p style="text-align: center; font-size: 20px;">No data for plot with these options! Please, select other options!</p>'
        col1.write(warn, unsafe_allow_html=True)
    else:
        fig, ax = plt.subplots(1,1,figsize=(20,13))
        stacked_barplots_2_variables(dataset_col3,[select_stacked_bar3_1,select_xaxis3_1],ax)
        ax.set_ylabel('Percentage (%)', fontsize=22, labelpad=20)
        st.pyplot(fig)

    
with col2:
    dataset_last = dataset_col3[(dataset_col3[select_stacked_bar3_1]==for_stacked_fixed_value_col4_1) & 
                                (dataset_col3[select_xaxis3_1]==select_xaxis_fixed_value_col4_2)]
    if dataset_last.shape[0]==0:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        warn = '<p style="text-align: center; font-size: 20px;">No data for plot with these options! Please, select other options!</p>'
        col2.write(warn, unsafe_allow_html=True)
    else:
        fig, ax = plt.subplots(1,1,figsize=(20,13))
        stacked_barplots_2_variables(dataset_last,[remaining_option,select_xaxis4_1],ax)
        st.pyplot(fig)
