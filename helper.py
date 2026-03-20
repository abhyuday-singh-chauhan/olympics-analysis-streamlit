import numpy as np
import pandas as pd


# 🏅 Overall Medal Tally
def medal_tally(df):
    medal_tally = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    medal_tally = medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']].sum() \
                             .sort_values('Gold', ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally[['Gold', 'Silver', 'Bronze', 'Total']] = medal_tally[
        ['Gold', 'Silver', 'Bronze', 'Total']
    ].astype(int)

    return medal_tally


# 📅 Dropdown lists (Years & Countries)
def country_year_list(df):
    years = df['Year'].dropna().unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


# 🌍 Generic Data Over Time (Nations / Events / Athletes)
def data_over_time(df, col):
    data = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    data.columns = ['Year', 'Count']
    data = data.sort_values('Year')
    return data


# 🥇 Fetch Medal Tally based on filters
def fetch_medal_tally(year, country, medal_df):

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]

    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    else:
        temp_df = medal_df[
            (medal_df['Year'] == int(year)) &
            (medal_df['region'] == country)
        ]

    x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']] \
               .sum() \
               .sort_values('Gold', ascending=False) \
               .reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x


# ⭐ Most Successful Athletes
def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medals']

    return x.head(15)


# 🏳️ Country-wise year-wise medal tally (for heatmap)
def country_yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df.pivot_table(index='Year',
                            columns='Medal',
                            values='Name',
                            aggfunc='count').fillna(0).astype(int)

    return x


# 🏅 Country-wise event participation over time
def country_event_heatmap(df, country):
    temp_df = df[df['region'] == country]

    x = temp_df.pivot_table(index='Sport',
                            columns='Year',
                            values='Name',
                            aggfunc='count').fillna(0).astype(int)

    return x


# 👨‍🦰👩 Gender participation over time
def gender_over_time(df):

    x = df.drop_duplicates(['Year', 'Sex', 'Name']) \
          .groupby(['Year', 'Sex'])['Name'] \
          .count() \
          .unstack() \
          .fillna(0) \
          .astype(int)

    return x

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15)
    x.columns = ('Name', 'Medal_Count')   # 👈 important

    return x.merge(df, on='Name', how='left')[['Name','Medal_Count','Sport','region']].drop_duplicates('Name')


def country_yearwise_medal(df, country):
    temp_df = df[df['region'] == country]
    temp_df = temp_df.dropna(subset=['Medal'])
    final_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    # ⭐ FIX HERE — remove quotes
    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(
        index='Sport',
        columns='Year',
        values='Medal',
        aggfunc='count'
    ).fillna(0)

    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.columns = ['Name', 'Medal_Count']

    return x.merge(df, on='Name')[['Name','Medal_Count','Sport']].drop_duplicates('Name')

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)
    return final