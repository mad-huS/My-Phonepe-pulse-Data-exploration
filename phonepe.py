import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json



#Data frame creation

mydb = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="madhu123",
                                database="phonepe_data",
                                port = "3306"
                              )
                        
cursor = mydb.cursor()

#aggregated insurance df

cursor.execute("SELECT * FROM aggregated_insurance")

table1 = cursor.fetchall()

T1 = pd.DataFrame(table1, columns = ("States", "Years", "Quarter", "Transaction_type","Transaction_count","Transaction_amount"))

cursor.fetchall()

mydb.commit()

#aggregated transaction df

cursor.execute("SELECT * FROM aggregated_transaction")

table2 = cursor.fetchall()

T2 = pd.DataFrame(table2, columns = ("States", "Years", "Quarter", "Transaction_type","Transaction_count","Transaction_amount"))

cursor.fetchall()

mydb.commit()

#aggregated user df

cursor.execute("SELECT * FROM aggregated_user")

table3 = cursor.fetchall()

T3 = pd.DataFrame(table3, columns = ("States", "Years", "Quarter", "Brand","Transaction_count","Percentage"))

cursor.fetchall()

mydb.commit()

#map insurance df

cursor.execute("SELECT * FROM map_insurance")

table4 = cursor.fetchall()

T4 = pd.DataFrame(table4, columns = ("States", "Years", "Quarter", "Districts","Transaction_count","Transaction_amount"))

cursor.fetchall()

mydb.commit()

#map transaction df

cursor.execute("SELECT * FROM map_transaction")

table5 = cursor.fetchall()

T5 = pd.DataFrame(table5, columns = ("States", "Years", "Quarter", "Districts","Transaction_count","Transaction_amount"))

cursor.fetchall()

mydb.commit()

#map user df

cursor.execute("SELECT * FROM map_user")

table6 = cursor.fetchall()

T6 = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Districts","Registered_users","App_opens"))

cursor.fetchall()

mydb.commit()

#top insurance df

cursor.execute("SELECT * FROM top_insurance")

table7 = cursor.fetchall()

T7 = pd.DataFrame(table7, columns = ("States", "Years", "Quarter", "Pincodes","Transaction_count","Transaction_amount"))

cursor.fetchall()

mydb.commit()

#top transaction df

cursor.execute("SELECT * FROM top_transaction")

table8 = cursor.fetchall()

T8 = pd.DataFrame(table8, columns = ("States", "Years", "Quarter", "Pincodes","Transaction_count","Transaction_amount"))

cursor.fetchall()

mydb.commit()

#top user df

cursor.execute("SELECT * FROM top_user")

table9 = cursor.fetchall()

T9 = pd.DataFrame(table9, columns = ("States", "Years", "Quarter", "Pincodes","Registered_users"))

cursor.fetchall()

mydb.commit()


def transaction_amount_count_y(df, year):
    
    tacy = df[df['Years'] == year]
    tacy.reset_index(drop = True, inplace = True)
    
    tacyg = tacy.groupby('States')[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    
    with col1:
        
        fig_amount = px.bar(tacyg, x = 'States', y ='Transaction_amount', title = f'Transaction Amount in the year {year}', color_discrete_sequence=px.colors.sequential.BuPu_r, height = 600, width = 550)
        
        st.plotly_chart(fig_amount)

    with col2:
    
        fig_count = px.bar(tacyg, x = 'States', y ='Transaction_count', title = f'Transaction Count in the year {year}', color_discrete_sequence=px.colors.sequential.Oryel_r, height = 600, width = 550)
        st.plotly_chart(fig_count)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    
    response = requests.get(url)
    
    data1 = json.loads(response.content)
    
    state_name = []
    for feature in data1['features']:
        state_name.append(feature['properties']['ST_NM'])
    
    state_name.sort()

    col1, col2 = st.columns(2)
    
    with col1:
        
    
        fig_india1 = px.choropleth(tacyg, geojson=data1,locations = "States", featureidkey = "properties.ST_NM", color = "Transaction_amount",
                                   color_continuous_scale="Plasma", range_color =(tacyg['Transaction_amount'].min(),tacyg['Transaction_amount'].max()),
                                    hover_name = "States", title = f"{year} TRANSACTION AMOUNT", fitbounds = "locations",height = 600, width = 550)

        fig_india1.update_layout(title=f"{year} TRANSACTION AMOUNT", geo=dict(bgcolor="Black",  showcoastlines=True ))
        
        fig_india1.update_geos(visible = False)
        
        st.plotly_chart(fig_india1)

    with col2:
        

        fig_india2 = px.choropleth(tacyg, geojson=data1,locations = "States", featureidkey = "properties.ST_NM", color = "Transaction_count",
                                   color_continuous_scale="Rainbow", range_color = (tacyg['Transaction_count'].min(),tacyg['Transaction_count'].max()),
                                    hover_name = "States", title = f"{year} TRANSACTION COUNT", fitbounds = "locations",height = 600, width = 550)

        fig_india2.update_layout(title=f"{year} TRANSACTION COUNT", geo=dict(bgcolor="Black",  showcoastlines=True ))
        
        fig_india2.update_geos(visible = False)
        
        st.plotly_chart(fig_india2)
        
    return tacy

def transaction_amount_count_Q(df, quarter):
    tacy = df[df['Quarter'] == quarter]
    tacy.reset_index(drop = True, inplace = True)
    
    tacyg = tacy.groupby('States')[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 = st.columns(2)

    with col1:
        
        fig_amount = px.bar(tacyg, x = 'States', y ='Transaction_amount', title = f'{tacy["Years"].unique()[0]} Year Transaction Amount in the Quarter {quarter}', color_discrete_sequence=px.colors.sequential.BuPu_r,height = 650, width = 550)
        
        st.plotly_chart(fig_amount)

    with col2:
    
        fig_count = px.bar(tacyg, x = 'States', y ='Transaction_count', title = f'{tacy["Years"].unique()[0]} Year Transaction Count in the Quarter {quarter}', 
                           color_discrete_sequence=px.colors.sequential.Oryel_r, height = 650, width = 550)
        st.plotly_chart(fig_count)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    
    response = requests.get(url)
    
    data1 = json.loads(response.content)
    
    state_name = []
    for feature in data1['features']:
        state_name.append(feature['properties']['ST_NM'])
    
    state_name.sort()
    
    col1,col2 = st.columns(2)

    with col1:
    
        fig_india1 = px.choropleth(tacyg, geojson=data1,locations = "States", featureidkey = "properties.ST_NM", color = "Transaction_amount",
                                   color_continuous_scale="Turbo", range_color = (tacyg['Transaction_amount'].min(),tacyg['Transaction_amount'].max()),
                                    hover_name = "States", title = f'{tacy["Years"].unique()[0]} Year Transaction Amount in the Quarter {quarter}', fitbounds = "locations",height = 600, width = 550)

        fig_india1.update_layout(title=f"{tacy['Years'].unique()[0]} TRANSACTION AMOUNT", geo=dict(bgcolor="Black", showcoastlines=True))
    
        fig_india1.update_geos(visible = False)
        
        st.plotly_chart(fig_india1)

    with col2:

        fig_india2 = px.choropleth(tacyg, geojson=data1,locations = "States", featureidkey = "properties.ST_NM", color = "Transaction_count",
                                   color_continuous_scale="Rainbow", range_color = (tacyg['Transaction_count'].min(),tacyg['Transaction_count'].max()),
                                    hover_name = "States", title = f'{tacy["Years"].unique()[0]} Year Transaction Count in the Quarter {quarter}', fitbounds = "locations",height = 600, width = 550)

        fig_india2.update_layout(title=f"{tacy['Years'].unique()[0]} TRANSACTION COUNT", geo=dict(bgcolor="Black", showcoastlines=True))

    
        fig_india2.update_geos(visible = False)
        
        st.plotly_chart(fig_india2)

    return tacy

def Agg_Trans_Transactiontype(tac_yAgg, states):
    
    tac_yAgg[tac_yAgg['States'] == states].reset_index(drop = True, inplace = True)
    tac_yAgg_g = tac_yAgg.groupby('Transaction_type')[["Transaction_count","Transaction_amount"]].sum()
    tac_yAgg_g.reset_index(inplace = True)
    pastel_colors = ['#B19CD9', '#FEC5BB', '#FFDE8A', '#B8F2E6']

    col1,col2 = st.columns(2)

    with col1:
        
        fig_pie = px.pie(tac_yAgg_g, names = 'Transaction_type', values = 'Transaction_amount', width = 600,
                         title = f'{states.upper()} Transaction Amount',hole = 0.60,color_discrete_sequence = pastel_colors)
        st.plotly_chart(fig_pie)

    with col2:
    
        fig_pie1 = px.pie(tac_yAgg_g, names = 'Transaction_type', values = 'Transaction_count', width = 600, title = f'{states.upper()} Transaction count',
                          hole = 0.60, color_discrete_sequence = pastel_colors)
        st.plotly_chart(fig_pie1)

def agg_user_TransCount(df, years):

    aguy = df[df['Years']==years]
    aguy.reset_index(drop = True, inplace = True)
    aguyg = pd.DataFrame(aguy.groupby('Brand')[["Transaction_count","Percentage"]].sum())
    aguyg.reset_index(inplace = True)
    fig_bar = px.bar(aguyg, x = 'Brand', y = 'Transaction_count', title = f'Brands Vs Transaction count of the year {years}', 
                     width = 900, height = 600, color_discrete_sequence = px.colors.sequential.Agsunset, hover_name = 'Brand')
    st.plotly_chart(fig_bar)
    
    return aguy

def agg_user_TransCountQ(df, quarter):

    aguyQ = df[df['Quarter']==quarter]
    aguyQ.reset_index(drop = True, inplace = True)
    aguyQg = pd.DataFrame(aguyQ.groupby('Brand')[["Transaction_count","Percentage"]].sum())
    aguyQg.reset_index(inplace = True)
    fig_bar1 = px.bar(aguyQg, x = 'Brand', y = 'Transaction_count', title=f"Brands Vs Transaction count of the year {aguyQ['Years'].unique()[0]} in Quarter {quarter}", width = 900, height = 600, color_discrete_sequence = px.colors.sequential.Blugrn, hover_name = 'Brand')
    st.plotly_chart(fig_bar1)
    return aguyQ

def agg_user_TransCountQ_state(df, states):

    aguyQS = df[df['States'] == states]
    aguyQS.reset_index(inplace = True)
    fig_line = px.line(aguyQS , x = 'Brand', y = 'Transaction_count', hover_data = 'Percentage', title = f'Analysis of Brands, Count and Percentage of state {states}', width = 1000, height = 600, markers = True)
    st.plotly_chart(fig_line)

def map_insur_district(df, states):
    
    a= df[df['States'] == states]
    a.reset_index(drop = True, inplace = True)
    Map_insur_g = a.groupby('Districts')[["Transaction_count","Transaction_amount"]].sum()
    Map_insur_g.reset_index(inplace = True)
    
    fig_bar = px.bar(Map_insur_g, x = 'Districts', y = 'Transaction_amount', width = 600, height = 600,
                 title = f'{states.upper()} Transaction Amount',color_discrete_sequence = px.colors.sequential.speed, orientation='v')
    
    st.plotly_chart(fig_bar)

    fig_bar1 = px.bar(Map_insur_g, x = 'Districts', y = 'Transaction_count', width = 600, height = 600, title = f'{states.upper()} Transaction count',
                     color_discrete_sequence = px.colors.sequential.RdBu,orientation='v')
    st.plotly_chart(fig_bar1)

    return a

def registeredUsers_appOpens_y(df, year):
    mapuY = df[df['Years'] == year]
    mapuY.reset_index(drop = True, inplace = True)
    
    mapuYg = mapuY.groupby('States')[["Registered_users","App_opens"]].sum()
    mapuYg.reset_index(inplace = True)

    col1,col2 = st.columns(2)

    with col1:
        
        fig_regUsers = px.bar(mapuYg, x = 'States', y ='Registered_users', title = f'Registered users in the year {year}', 
                            color_discrete_sequence=px.colors.sequential.BuPu_r,height = 650, width = 550)
        st.plotly_chart(fig_regUsers)

    with col2:
    
        fig_Appopens = px.bar(mapuYg, x = 'States', y ='App_opens', title = f'App Opens in the year {year}', 
                               
                           color_discrete_sequence=px.colors.sequential.BuPu_r, height = 650, width = 550)
        st.plotly_chart(fig_Appopens)
                    
    return mapuY

def mapUser_Q(df, quarter):
    mapuY = df[df['Quarter'] == quarter]
    mapuY.reset_index(drop = True, inplace = True)
    
    mapuYg = mapuY.groupby('States')[["Registered_users","App_opens"]].sum()
    mapuYg.reset_index(inplace = True)

    col1,col2 = st.columns(2)

    with col1:

        fig_RegUsers = px.bar(mapuYg, x = 'States', y ='Registered_users', title = f'{mapuY["Years"].unique()[0]} Year Registered users in the Quarter {quarter}', color_discrete_sequence=px.colors.sequential.BuPu_r,height = 500, width = 450)
        st.plotly_chart(fig_RegUsers)

    with col2:
    
        fig_Appopens = px.bar(mapuYg, x = 'States', y ='App_opens', title = f'{mapuY["Years"].unique()[0]} Year App opens in the Quarter {quarter}', 
                           color_discrete_sequence=px.colors.sequential.Oryel_r, height = 500, width = 450)
        st.plotly_chart(fig_Appopens)
    return mapuY


def mapUser_QState(df,states):
    a=df[df['States'] == states]
    a.reset_index(drop = True, inplace = True)

    col1,col2 = st.columns(2)

    with col1:
        
        fig_bar = px.line(a, x= 'Districts', y = 'Registered_users', title = f'Registered Users in the state of {states} of year {df["Years"].unique()[0]} of quarter {df["Quarter"].unique()[0]}',
                         color_discrete_sequence = px.colors.sequential.Sunsetdark_r,width = 600)
        st.plotly_chart(fig_bar)
    with col1:
         
        fig_bar1 = px.line(a, x= 'Districts', y = 'App_opens', title = f'App Opens in the state of {states} of year {df["Years"].unique()[0]} of quarter {df["Quarter"].unique()[0]}', color_discrete_sequence = px.colors.sequential.Plasma_r,width = 600)
        
        st.plotly_chart(fig_bar1)
    

def Top_insur_Ystate(df, states):   
    top = df[df['States'] == states]
    top.reset_index(drop = True, inplace = True)
    
    col1,col2 = st.columns(2)

    with col1:
    
        fig_bar = px.bar(df, x = 'Quarter', y = 'Transaction_amount', hover_data = 'Pincodes',width = 550, height = 600,
                         title = f'{states.upper()} Transaction Amount',color_discrete_sequence = px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_bar)
    with col2:
        
        fig_bar1 = px.bar(df, x = 'Quarter', y = 'Transaction_count', hover_data = 'Pincodes', width = 550,height = 600, title = f'{states.upper()} Transaction count', color_discrete_sequence = px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_bar1)
    
def Top_user_year(df,year):
    tucy = df[df['Years'] == year]
    tucy.reset_index(drop = True, inplace = True)
    tucyg = pd.DataFrame(tucy.groupby(['States', 'Quarter'])['Registered_users'].sum())
    tucyg.reset_index(inplace = True)
    fig_topUser = px.bar(tucyg, x = 'States', y = 'Registered_users', title = f'Registered users in India of the year {year}',
                         color_discrete_sequence = px.colors.sequential.turbid_r,width = 800)
    st.plotly_chart(fig_topUser) 

    return tucy

def Top_user_Ystate(df, states):   
    a=df[df['States'] == states]
    a.reset_index(drop = True, inplace = True)
    
    fig_bar = px.bar(df, x = 'Quarter', y = 'Registered_users',width = 600, height = 600,
                     title = f'{states.upper()} Quarter, Pincodes and Registered Users',hover_data='Pincodes',color_continuous_scale= px.colors.sequential.Agsunset_r)
    st.plotly_chart(fig_bar)

    return a

#Top chart part

def Top_chart_transaction_amount(table_name):

    mydb = mysql.connector.connect(
                                    host="localhost",
                                    user="root",
                                    password="madhu123",
                                    database="phonepe_data",
                                    port = "3306"
                                  )
                            
    cursor = mydb.cursor()
    
    query1 = f'''select States, sum(Transaction_amount) as Transaction_Amount from {table_name}
                group by States order by Transaction_Amount desc limit 10;'''
    cursor.execute(query1)
    
    table1 = cursor.fetchall()
    mydb.commit()
    
    df1 = pd.DataFrame(table1, columns = ('States', 'Transaction_amount'))

    col1,col2 = st.columns(2)

    with col1:
    
        fig_amount1 = px.bar(df1, x = 'States', y ='Transaction_amount', title = 'Top 10 high Transaction Amount', 
                               color_discrete_sequence=px.colors.sequential.Oryel_r, height = 650, width = 550)
        st.plotly_chart(fig_amount1)
    
    #plot 2
    
    query2 = f'''select States, sum(Transaction_amount) as Transaction_Amount from {table_name}
                group by States order by Transaction_Amount;'''
    cursor.execute(query2)
    
    table2 = cursor.fetchall()
    mydb.commit()
    
    df2 = pd.DataFrame(table2, columns = ('States', 'Transaction_Amount'))

    with col2:
        
        fig_amount2 = px.bar(df2, x = 'States', y ='Transaction_Amount', title = 'Transaction Amount', 
                               color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height = 650, width = 550)
        st.plotly_chart(fig_amount2)
    
    #plot 3
    
    query3 = f'''select States, avg(Transaction_amount) as Average_Transaction_Amount from {table_name}
                group by States order by Average_Transaction_Amount;'''
    cursor.execute(query3)
    
    table3 = cursor.fetchall()
    mydb.commit()
    
    df3 = pd.DataFrame(table3, columns = ('States', 'Average_Transaction_Amount'))
    
    fig_amount3 = px.bar(df3, x = 'States', y ='Average_Transaction_Amount', title = 'Average Transaction Amount', 
                           color_discrete_sequence=px.colors.sequential.Cividis_r, height = 650, width = 550)
    st.plotly_chart(fig_amount3)
    
#Top chart transaction count part:

def Top_chart_transaction_count(table_name):

    mydb = mysql.connector.connect(
                                    host="localhost",
                                    user="root",
                                    password="madhu123",
                                    database="phonepe_data",
                                    port = "3306"
                                  )
                            
    cursor = mydb.cursor()
    
    query1 = f'''select States, sum(Transaction_count) as Transaction_count from {table_name}
                group by States order by Transaction_count desc limit 10;'''
    cursor.execute(query1)
    
    table1 = cursor.fetchall()
    mydb.commit()
    
    df1 = pd.DataFrame(table1, columns = ('States', 'Transaction_count'))
    col1,col2 = st.columns(2)

    with col1:
    
        fig_amount1 = px.bar(df1, x = 'States', y ='Transaction_count', title = 'Top 10 high Transaction count', 
                               color_discrete_sequence=px.colors.sequential.Oryel_r, height = 650, width = 550)
        st.plotly_chart(fig_amount1)
    
    #plot 2
    
    query2 = f'''select States, sum(Transaction_count) as Transaction_Count from {table_name}
                group by States order by Transaction_count;'''
    cursor.execute(query2)
    
    table2 = cursor.fetchall()
    mydb.commit()
    
    df2 = pd.DataFrame(table2, columns = ('States', 'Transaction_count'))

    with col2:
        fig_amount2 = px.bar(df2, x = 'States', y ='Transaction_count', title = 'Transaction_count', 
                               color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height = 650, width = 550)
        st.plotly_chart(fig_amount2)
    
    #plot 3
    
    query3 = f'''select States, avg(Transaction_count) as Average_Transaction_count from {table_name}
                group by States order by Average_Transaction_count;'''
    cursor.execute(query3)
    
    table3 = cursor.fetchall()
    mydb.commit()
    
    df3 = pd.DataFrame(table3, columns = ('States', 'Average_Transaction_count'))
    
    fig_amount3 = px.bar(df3, x = 'States', y ='Average_Transaction_count', title = 'Average Transaction Count', 
                           color_discrete_sequence=px.colors.sequential.Cividis_r, height = 650, width = 550)
    st.plotly_chart(fig_amount3)
    
def Top_chart_Registered_user(tablename, states):

    mydb = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        password="madhu123",
                                        database="phonepe_data",
                                        port = "3306"
                                      )
                                
    cursor = mydb.cursor()
    
    query1 = f'''SELECT  DISTRICTS, SUM(Registered_users) as Registered_users FROM {tablename} WHERE States = '{states}' 
    GROUP BY DISTRICTS order by Registered_users desc limit 10'''
    
    cursor.execute(query1)
        
    table1 = cursor.fetchall()
    mydb.commit()
    
    df1 = pd.DataFrame(table1, columns = ('Districts','Registered_users'))

    col1,col2 = st.columns(2)

    with col1:
        
        fig_amount1 = px.bar(df1, x = 'Districts', y ='Registered_users', title = f'Top 10 Registered Users of state {states}', 
                               color_discrete_sequence=px.colors.sequential.Oryel_r, height = 650, width = 550)
        st.plotly_chart(fig_amount1)

    #plot 2 list of registered users of state

    query2 = f'''SELECT DISTRICTS, SUM(Registered_users) as Registered_users FROM {tablename} WHERE STATES = '{states}' 
            GROUP BY DISTRICTS order by Registered_users'''
    
    cursor.execute(query2)
        
    table2 = cursor.fetchall()
    mydb.commit()
    
    df2 = pd.DataFrame(table2, columns = ('Districts','Registered_users'))
    
    fig_amount2 = px.bar(df2, x = 'Districts', y ='Registered_users', title = f'Lists of Registered Users of state {states}', 
                           color_discrete_sequence=px.colors.sequential.Oryel_r, height = 650, width = 550)
    with col2:
        
        st.plotly_chart(fig_amount2)

    #plot 3 Average registered users of a state

    query3 = f'''SELECT DISTRICTS, avg(Registered_users) as Average_Registered_users FROM {tablename} WHERE STATES = '{states}' 
            GROUP BY DISTRICTS order by Average_Registered_users'''
    
    cursor.execute(query3)
        
    table3 = cursor.fetchall()
    mydb.commit()
    
    df3 = pd.DataFrame(table3, columns = ('Districts','Registered_users'))
    
    fig_amount3 = px.bar(df3, x = 'Districts', y ='Registered_users', title = f'Lists of Average Registered Users of state {states}', 
                           color_discrete_sequence=px.colors.sequential.Oryel_r, height = 650, width = 550)
    st.plotly_chart(fig_amount3)

def Top_chart_AppOpens(tablename, states):

    mydb = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        password="madhu123",
                                        database="phonepe_data",
                                        port = "3306"
                                      )
                                
    cursor = mydb.cursor()
    
    query1 = f'''SELECT  DISTRICTS, SUM(App_opens) as App_opens FROM {tablename} WHERE States = '{states}' 
    GROUP BY DISTRICTS order by App_opens desc limit 10'''
    
    cursor.execute(query1)
        
    table1 = cursor.fetchall()
    mydb.commit()
    
    df1 = pd.DataFrame(table1, columns = ('Districts','App_opens'))
    
    fig_amount1 = px.bar(df1, x = 'Districts', y ='App_opens', title = f'Top 10 App opens of state {states}', 
                           color_discrete_sequence=px.colors.sequential.Oryel_r, height = 650, width = 550)
    col1,col2 = st.columns(2)
    with col1:
        
        st.plotly_chart(fig_amount1)

    #plot 2 list of registered users of state

    query2 = f'''SELECT DISTRICTS, SUM(App_opens) as App_opens FROM {tablename} WHERE STATES = '{states}' 
            GROUP BY DISTRICTS order by App_opens'''
    
    cursor.execute(query2)
        
    table2 = cursor.fetchall()
    mydb.commit()
    
    df2 = pd.DataFrame(table2, columns = ('Districts','App_opens'))
    
    fig_amount2 = px.bar(df2, x = 'Districts', y ='App_opens', title = f'Lists of App opens of state {states}', 
                           color_discrete_sequence=px.colors.sequential.Oryel_r, height = 650, width = 550)
    with col2:   
        st.plotly_chart(fig_amount2)

    #plot 3 Average registered users of a state

    query3 = f'''SELECT DISTRICTS, avg(App_opens) as Average_App_opens FROM {tablename} WHERE STATES = '{states}' 
            GROUP BY DISTRICTS order by Average_App_opens'''
    
    cursor.execute(query3)
        
    table3 = cursor.fetchall()
    mydb.commit()
    
    df3 = pd.DataFrame(table3, columns = ('Districts','App_opens'))
    
    fig_amount3 = px.bar(df3, x = 'Districts', y ='App_opens', title = f'Lists of Average App opens of state {states}', 
                           color_discrete_sequence=px.colors.sequential.Oryel_r, height = 650, width = 550)
    st.plotly_chart(fig_amount3)


def Top_chart_RegisteredUserTopuser(table_name):

    mydb = mysql.connector.connect(
                                    host="localhost",
                                    user="root",
                                    password="madhu123",
                                    database="phonepe_data",
                                    port = "3306"
                                  )
                            
    cursor = mydb.cursor()
    
    query1 = f'''select states, sum(Registered_users) as Registered_users from {table_name} 
            group by states order by Registered_users desc limit 10;'''
    cursor.execute(query1)
    
    table1 = cursor.fetchall()
    mydb.commit()
    
    df1 = pd.DataFrame(table1, columns = ('States', 'Registered_users'))
    
    fig_amount1 = px.bar(df1, x = 'States', y ='Registered_users', title = 'Top 10 states having high count of Registered users', 
                           color_discrete_sequence=px.colors.sequential.Oryel_r, height = 650, width = 550)
    
    col1,col2 = st.columns(2)
    with col1:
        
        st.plotly_chart(fig_amount1)
    
    #plot 2
    
    query2 = f'''select states, sum(Registered_users) as Registered_users from {table_name} 
                group by states order by Registered_users'''
    cursor.execute(query2)
    
    table2 = cursor.fetchall()
    mydb.commit()
    
    df2 = pd.DataFrame(table2, columns = ('States', 'Registered_users'))
    
    fig_amount2 = px.bar(df2, x = 'States', y ='Registered_users', title = 'Lists of Registered_users', 
                           color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height = 650, width = 550)

    with col2:
        st.plotly_chart(fig_amount2)
    
    #plot 3
    
    query3 = f'''select states, avg(Registered_users) as Avg_Registered_users from {table_name} 
            group by states order by Avg_Registered_users'''
    cursor.execute(query3)
    
    table3 = cursor.fetchall()
    mydb.commit()
    
    df3 = pd.DataFrame(table3, columns = ('States', 'Average_Registered_users'))
    
    fig_amount3 = px.bar(df3, x = 'States', y ='Average_Registered_users', title = 'Average Registered users', 
                           color_discrete_sequence=px.colors.sequential.Cividis_r, height = 650, width = 600)
    st.plotly_chart(fig_amount3)
    

#streamlit part

st.set_page_config(layout="wide", page_title="Streamlit App", page_icon=":rocket:", initial_sidebar_state="expanded")



with st.sidebar:
    select = option_menu("PhonePe Pulse",["Home","Data Exploration", "Top Charts"])

if select == "Home":
    st.title("Phonepe Data Visualization and Exploration")
    st.header("About Pulse")
    st.video('E:/Madhu/Guvi/Phonepe data/videoplayback.mp4')
    st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
        font-family: Arial, sans-serif;
        font-size: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


    st.markdown('''
<p class="centered-text">
    The Indian digital payments story has truly captured the world's imagination. 
    From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration 
    of mobile phones and data.
</p>
<br>
<p class="centered-text">
    When PhonePe started 5 years back, we were constantly looking for definitive data sources on 
    digital payments in India.  Some of the questions we were seeking answers to were -
    How are consumers truly using digital payments? 
    What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes?
</p>
<br>
<p class="centered-text">
    This year as we became India's largest digital payments platform with 46% UPI market share, 
    we decided to demystify the what, why and how of digital payments in India.
</p>
<br>
<br>
<p class="centered-text">
    This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, 
    we thought as India's largest digital payments platform with 46% UPI market share, 
    we have a ring-side view of how India sends, spends, manages and grows its money. 
    So it was time to demystify and share the what, why and how of digital payments in India.
</p>
<br>
''', unsafe_allow_html=True)

    if st.button("DOWNLOAD THE APP NOW"):
        st.write('<a href="https://www.phonepe.com/app-download/" target="_blank">Download the app now</a>', unsafe_allow_html=True)

elif select == "Data Exploration":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.selectbox("Select the Method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":

            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year to analyse", T1["Years"].min(),T1["Years"].max())
            tac_Y = transaction_amount_count_y(T1, years)

            col1, col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select the Quarter to analyse", tac_Y["Quarter"].min(),tac_Y["Quarter"].max())

            transaction_amount_count_Q(tac_Y,quarters )
            
            
        elif method == "Transaction Analysis":
            
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year to analyse", T2["Years"].min(),T2["Years"].max())
            Agg_trans_tac_Y = transaction_amount_count_y(T2, years)

            col1, col2 = st.columns(2)
            
            with col1:
                states = st.selectbox("Select State to analyse", Agg_trans_tac_Y['States'].unique())
            Agg_trans = Agg_Trans_Transactiontype(Agg_trans_tac_Y,states)
            
            col1, col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select the Quarter to analyse", Agg_trans_tac_Y["Quarter"].min(),Agg_trans_tac_Y["Quarter"].max())
            Agg_trans_Q = transaction_amount_count_Q(Agg_trans_tac_Y,quarters )

            col1, col2 = st.columns(2)
            
            with col1:
                states = st.selectbox(f"Select State to analyse based on Quarter {Agg_trans_Q['Quarter'].unique()[0]}", Agg_trans_tac_Y['States'].unique())
                
            Agg_trans_QQ = Agg_Trans_Transactiontype(Agg_trans_Q,states)
            
        elif method == "User Analysis":

            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year to analyse", T3["Years"].min(),T3["Years"].max())
            Aggre_user_tac_Y = agg_user_TransCount(T3, years)

            col1, col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select the Quarter to analyse", Aggre_user_tac_Y["Quarter"].min(),Aggre_user_tac_Y["Quarter"].max())
            Aggre_user_tac_Q = agg_user_TransCountQ(Aggre_user_tac_Y,quarters )

            col1, col2 = st.columns(2)
            
            with col1:
                states = st.selectbox("Select State to analyse", Aggre_user_tac_Q['States'].unique())
            Agg_user_tac_QS = agg_user_TransCountQ_state(Aggre_user_tac_Q,states)
            
            
            
    with tab2:
        method2 = st.selectbox("Select the Method", ["Map Insurance", "Map Transaction", "Map User"])

        if method2 == "Map Insurance":
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year to analyse", T4["Years"].min(),T4["Years"].max(), key="year_selectbox")
            Map_insur = transaction_amount_count_y(T4, years) 

            col1, col2 = st.columns(2)
            
            with col1:
                states1 = st.selectbox("Select State to analyse", Map_insur['States'].unique(), key="state_selectbox")
            map_insur_Statedata = map_insur_district(Map_insur, states1)

            col1, col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select the Quarter to analyse", Map_insur["Quarter"].min(),
                                     Map_insur["Quarter"].max(),key="Quarter_selectbox")
            map_insur_Quarter = transaction_amount_count_Q(Map_insur,quarters)

            col1, col2 = st.columns(2)
            
            with col1:
                states2 = st.selectbox(f"Select State to analyse of Quarter {map_insur_Quarter['Quarter'].unique()[0]}", map_insur_Quarter['States'].unique(), key="state1_selectbox")
            map_insur_Statedata = map_insur_district(map_insur_Quarter, states2)
            
        elif method2 == "Map Transaction":
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year to analyse", T4["Years"].min(),T4["Years"].max(), key="year1_selectbox")
            Map_trans = transaction_amount_count_y(T5, years) 

            col1, col2 = st.columns(2)
            
            with col1:
                states2 = st.selectbox("Select State to analyse", Map_trans['States'].unique(), key="state_selectbox1")
            map_trans_Statedata = map_insur_district(Map_trans, states2)

            col1, col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select the Quarter to analyse", Map_trans["Quarter"].min(),
                                     Map_trans["Quarter"].max(),key="Quarter_selectbox1")
            map_trans_Quarter = transaction_amount_count_Q(Map_trans,quarters)

            col1, col2 = st.columns(2)
            
            with col1:
                states2 = st.selectbox(f"Select State to analyse of Quarter {map_trans_Quarter['Quarter'].unique()[0]}", map_trans_Quarter['States'].unique(), key="state1_selectbox1")
            map_trans_Statedata = map_insur_district(map_trans_Quarter, states2)
            
        elif method2 == "Map User":
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year to analyse", T6["Years"].min(),T6["Years"].max(), key="year2_selectbox")
            Map_user = registeredUsers_appOpens_y(T6, years)

            col1, col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select the Quarter to analyse", Map_user["Quarter"].min(),
                                     Map_user["Quarter"].max(),key="Quarter_selectbox2")
            mapUserYQ = mapUser_Q(Map_user,quarters)

            col1, col2 = st.columns(2)
            with col1:
                states3 = st.selectbox(f"Select State to analyse of Quarter {mapUserYQ['Quarter'].unique()[0]}", mapUserYQ['States'].unique(), key="state2_selectbox2")
            map_user_Statedata = mapUser_QState(mapUserYQ, states3)
            
            

    with tab3:
    
        method3 = st.selectbox("Select the Method", ["Top Insurance", "Top Transaction", "Top User"], key="method3")  
        
        if method3 == "Top Insurance":
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year to analyse", T7["Years"].min(),T7["Years"].max(), key="year1_selectbox")
            Top_insur = transaction_amount_count_y(T7, years) 

            col1, col2 = st.columns(2)
            
            with col1:
                states = st.selectbox(f"Select State to analyse ", Top_insur['States'].unique())
            top_insur_yS = Top_insur_Ystate(Top_insur,states)
            
            col1, col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select the Quarter to analyse", Top_insur["Quarter"].min(),
                                     Top_insur["Quarter"].max(),key="1Quarter_selectbox2")
            TopInsurYQ = transaction_amount_count_Q(Top_insur,quarters)


        
        elif method3 == "Top Transaction":
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year to analyse", T8["Years"].min(),T8["Years"].max(), key="1year_selectbox")
            Top_trans = transaction_amount_count_y(T8, years) 

            col1, col2 = st.columns(2)
            
            with col1:
                states = st.selectbox(f"Select State to analyse ", Top_trans['States'].unique())
            top_trans_yS = Top_insur_Ystate(Top_trans,states)
            
            col1, col2 = st.columns(2)
            
            with col1:
                quarters = st.slider("Select the Quarter to analyse", Top_trans["Quarter"].min(),
                                     Top_trans["Quarter"].max(),key="2Quarter_selectbox2")
            TopTransYQ = transaction_amount_count_Q(Top_trans,quarters)
            
        elif method3 == "Top User":
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the Year to analyse", T9["Years"].min(),T9["Years"].max(), key="2year_selectbox")
            Top_user = Top_user_year(T9, years) 

            col1, col2 = st.columns(2)
            
            with col1:
                states = st.selectbox(f"Select State to analyse ", Top_user['States'].unique(), key = "statebox")
            topuserYstate = Top_user_Ystate(Top_user,states)

elif select == "Top Charts":
    questions = st.selectbox("Select the question", ["1. Transaction amount and count of aggregated insurance",
                                                    "2. Transaction amount and count of Map insurance",
                                                    "3. Transaction amount and count of Top insurance",
                                                    "4. Transaction amount and count of Aggregated Transaction",
                                                    "5. Transaction amount and count of Map Transaction",
                                                    "6. Transaction amount and count of Top Transaction",
                                                    "7. Transaction count of Aggregated User",
                                                    "8. Registered Users of Map Users",
                                                    "9. App Opens of Map Users",
                                                   "10. Registered Users of Top users"])
    if questions == '1. Transaction amount and count of aggregated insurance':
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("aggregated_insurance")

    elif questions == "2. Transaction amount and count of Map insurance":
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("map_insurance")
        
    elif questions == "3. Transaction amount and count of Top insurance":
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("top_insurance")

    elif questions == "4. Transaction amount and count of Aggregated Transaction":
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("aggregated_transaction")   

    elif questions == "5. Transaction amount and count of Map Transaction":
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("map_transaction")   

    elif questions == "6. Transaction amount and count of Top Transaction":
        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("top_transaction") 
        
    elif questions == "7. Transaction count of Aggregated User":
        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("aggregated_user")

    elif questions == "8. Registered Users of Map Users":
        st.subheader("REGISTERED USERS")
        states = st.selectbox(f"Select State to analyse ", T6['States'].unique(), key = "statebox1")
        Top_chart_Registered_user('map_user',states)

    elif questions == "9. App Opens of Map Users":
        st.subheader("APP OPENS")
        states = st.selectbox(f"Select State to analyse ", T6['States'].unique(), key = "statebox1")
        Top_chart_AppOpens('map_user',states)
        
    elif questions == "10. Registered Users of Top users":
        st.subheader("REGISTERED USERS")
        Top_chart_RegisteredUserTopuser('top_user')