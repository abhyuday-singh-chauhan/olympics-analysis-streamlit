import streamlit as st
import pandas as pd
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

st.set_page_config(page_title="Olympics Analysis", layout="wide")

st.title("🏅 Olympics Medal Tally Analysis")

# Load data
df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

# Merge datasets
df = df.merge(region_df, on='NOC', how='left')

# One-hot encoding for medals
df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

# ================= SIDEBAR =================
st.sidebar.title("Filters")

user_menu = st.sidebar.selectbox(
    "Menu",
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete wise Analysis")
)
st.sidebar.image('https://tse3.mm.bing.net/th/id/OIP.5aPO5kgtUSrnBJbbFWnqlQHaEK?pid=Api&P=0&h=180')

# ================= MEDAL TALLY =================
if user_menu == "Medal Tally":

    # ⭐ Filters on page (column-wise)
    st.subheader("Filters")

    years, countries = helper.country_year_list(df)

    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox("Select Year", years, key="medal_year")

    with col2:
        selected_country = st.selectbox("Select Country", countries, key="medal_country")
    # ⭐ Titles (same as your logic)
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} Overall Performance")

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " olympics")

    # ⭐ Fetch medal tally (unchanged)
    medal_tally = helper.fetch_medal_tally(
        selected_year,
        selected_country,
        df
    )

    st.header("Medal Tally")
    st.table(medal_tally)
# ================= OVERALL ANALYSIS =================
elif user_menu == 'Overall Analysis':

    st.title("Overall Analysis")

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Cities")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.header("Events")
        st.title(events)

    with col5:
        st.header("Athletes")
        st.title(athletes)

    with col6:
        st.header("Nations")
        st.title(nations)

    # Nations over time
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Year", y="Count")
    st.title("Participating Nations over time")
    st.plotly_chart(fig)

    # Events over time
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Year", y="Count")
    st.title("Events over time")
    st.plotly_chart(fig)

    # Athletes over time
    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Year", y="Count")
    st.title("Athletes over time")
    st.plotly_chart(fig)

    # Heatmap
    st.title("No. of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Event', 'Sport'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year',
                      values='Event', aggfunc='count')
        .fillna(0).astype('int'),
        annot=True
    )
    st.pyplot(fig)

    # Most successful athletes
    st.title("Most Successful Athletes")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

# ================= COUNTRY-WISE ANALYSIS =================
elif user_menu == 'Country-wise Analysis':

    st.title("🏳️ Country-wise Analysis")

    # Country dropdown
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.selectbox("Select Country", country_list)

    # Get data
    final_df = helper.country_yearwise_medal(df, selected_country)

    # Show table
    st.dataframe(final_df)

    # Plot
    fig = px.line(final_df, x="Year", y="Medal")

    fig.update_layout(
        title={
            'text': f"{selected_country} Medal Tally Over The Years",
            'x': 0.5,  # center title
            'xanchor': 'center',
            'font': dict(size=26)  # bigger = looks bold
        }
    )

    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)

    if pt.empty:
        st.info("No event data available for this country")
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.heatmap(pt, annot=True, ax=ax)
        st.pyplot(fig)

        st.title("Top 10 athletes of " + selected_country)
        top10_df = helper.most_successful_countrywise(df,selected_country)
        st.table(top10_df)


import plotly.express as px

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    athlete_df['Age'] = pd.to_numeric(athlete_df['Age'], errors='coerce')

    fig = px.histogram(
        athlete_df,
        x='Age',
        color='Medal',
        marginal='rug',
        nbins=40,
        title='Age Distribution of Athletes'
    )

    st.plotly_chart(fig)

    import plotly.express as px

    x = []
    name = []

    famous_sports = [
        'Aquatics', 'Archery', 'Athletics', 'Badminton', 'Baseball', 'Basketball',
        'Boxing', 'Canoeing', 'Cycling', 'Equestrian', 'Fencing', 'Football',
        'Golf', 'Gymnastics', 'Handball', 'Hockey', 'Judo', 'Modern Pentathlon',
        'Rowing', 'Rugby', 'Sailing', 'Shooting', 'Table Tennis', 'Taekwondo',
        'Tennis', 'Triathlon', 'Volleyball', 'Weightlifting', 'Wrestling'
    ]

    # Create filtered dataframe for gold medalists
    gold_df = athlete_df[athlete_df['Medal'] == 'Gold']

    fig = px.histogram(
        gold_df,
        x="Age",
        color="Sport",
        nbins=40,
        title="Distribution of Age (Gold Medalists by Sport)"
    )

    fig.update_layout(width=1000, height=600)

    st.title("Distribution of Age(Gold Medalists)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Weight vs Height")
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(
        x=temp_df['Weight'],
        y=temp_df['Height'],
        hue=temp_df['Medal'],
        style=temp_df['Sex'],
        s=50
    )
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)