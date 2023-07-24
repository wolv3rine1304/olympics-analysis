import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import preprocess,helper

df = pd.read_csv('little_bit_sorted_for_analysis.csv')

df=preprocess.preprocess(df)

st.sidebar.title("Olympics Analysis")

user_menu=st.sidebar.radio(
 'Select an option',
 ('Medal Tally','Overall Analysis','Country wise Analysis')
)


if user_menu == 'Medal Tally':
 st.sidebar.header("Medal Tally")
 years,country = helper.country_year_list(df)

 selected_year = st.sidebar.selectbox("Select Year",years)
 selected_country = st.sidebar.selectbox("Select Country", country)
 medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
 if selected_year == 'Overall' and selected_country == 'Overall':
  st.title('Overall Tally')
 if selected_year != 'Overall' and selected_country == 'Overall':
  st.title("Medal Tally in " + str(selected_year) + " Olympics")
 if selected_year == 'Overall' and selected_country != 'Overall':
  st.title(selected_country + " overall performance")
 if selected_year != 'Overall' and selected_country != 'Overall':
  st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
 st.table(medal_tally)


if user_menu == 'Overall Analysis':
 editions=df['year'].unique().shape[0]
 cities=df['city'].unique().shape[0]
 sports=df['discipline_title'].unique().shape[0]
 athletes=df['athlete_full_name'].unique().shape[0]
 nations=df['country_name'].unique().shape[0]

 st.title("Top Statistcs")

 col1,col2,col3 = st.columns(3)
 with col1:
  st.header("Editions")
  st.title(editions)
 with col2:
  st.header("Hosts")
  st.title(cities)
 with col3:
  st.header("Sports")
  st.title(sports)

 col1,col2 = st.columns(2)
 with col1:
  st.header("Winning Nations")
  st.title(nations)
 with col2:
  st.header("Winning athletes")
  st.title(athletes)

 nations_over_time = helper.data_over_time(df,"country_name")
 fig = px.line(nations_over_time, x="Edition", y="country_name")
 st.title("Winning Nations over the years")
 st.plotly_chart(fig)

 events_over_time = helper.data_over_time(df, "discipline_title")
 fig = px.line(events_over_time, x="Edition", y="discipline_title")
 st.title("Events over the years")
 st.plotly_chart(fig)

 athletes_over_time = helper.data_over_time(df, "athlete_full_name")
 fig = px.line(athletes_over_time, x="Edition", y="athlete_full_name")
 st.title("Winning athletes over the years")
 st.plotly_chart(fig)

 st.title('Men vs Women vs Mixed participation over the years')
 final = helper.men_vs_women_mixed(df)
 fig = px.line(final, x='year', y=['Male', 'Female', 'Mixed'])
 st.plotly_chart(fig)

 st.title("No of events over time(Every Sport)")
 fig,ax=plt.subplots(figsize=(20,20))
 x = df.drop_duplicates(['year', 'discipline_title', 'event_title'])
 ax=sns.heatmap(x.pivot_table(index='discipline_title', columns='year', values='event_title', aggfunc='count').fillna(0).astype(int),
  annot=True)
 st.pyplot(fig)

 st.title("Most successful Athletes")
 sport_list=df['discipline_title'].unique().tolist()
 sport_list.sort()
 sport_list.insert(0,'Overall')

 selected_sport=st.selectbox('Select a sport',sport_list)
 x=helper.most_succesful(df,selected_sport)
 st.table(x)


if user_menu == 'Country wise Analysis':
 st.sidebar.title("Country wise Analysis")
 country_list=df['country_name'].unique().tolist()
 country_list.sort()

 selected_country=st.sidebar.selectbox("Select a country",country_list)

 country_df=helper.yearwise_medal_tally(df,selected_country)
 fig = px.line(country_df, x='year', y='medal_type')
 st.title(selected_country+ " Medal tally over the years")
 st.plotly_chart(fig)

 st.title(selected_country + " exceles in following sports")
 pt=helper.country_event_heatmap(df,selected_country)
 fig, ax = plt.subplots(figsize=(20, 20))
 ax = sns.heatmap(pt,annot=True)
 st.pyplot(fig)

 st.title("Top 10 atheletes of "+ selected_country)
 top10_df=helper.most_succesful_countrywise(df,selected_country)
 st.table(top10_df)
