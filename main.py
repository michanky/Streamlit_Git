import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Covid-19 Data')

st.markdown("""
This app displays the information of Covid-19 cases around the world
""")

st.sidebar.header('User Input Features')


@st.cache
def load_data():
    # Import data from who_data.csv file and stores it as time_series
    # File is from World Health Organisation
    time_series = pd.read_csv('WHO-COVID-19-global-data.csv')
    time_series['Date_reported'] = pd.to_datetime(
        time_series['Date_reported']).dt.date
    return time_series.dropna()


df = load_data()


# Sidebar - Country selection
sorted_country_unique = sorted(df['Country'].unique())
selected_country = st.sidebar.multiselect(
    'Country', sorted_country_unique)

# Sidebar - Data selection
min_date = df['Date_reported'].min()
max_date = df['Date_reported'].max()

a_date = st.sidebar.date_input("Pick a date", (min_date, max_date))

# Filtering data
date_mask = (df['Date_reported'] >= a_date[0]) & (
    df['Date_reported'] <= a_date[1])
df_selected_country = df[(df['Country'].isin(selected_country))]
df_selected_country_and_date = df_selected_country[date_mask]

st.header('Display Selected Countries')
st.write('This will display the number of covid cases from ' +
         str(a_date[0]) + ' to ' + str(a_date[1]))
st.dataframe(df_selected_country_and_date)


def filedownload(df):
    csv = df.to_csv(index=False)
    # strings <-> bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="Covid-19.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(df_selected_country_and_date), unsafe_allow_html=True)

data = df_selected_country_and_date

# Plot daily cases
def daily_plot(country):
    df = data[data['Country'] == country]
    df.index = df['Date_reported']
    plt.plot(pd.to_datetime(df.Date_reported), df['New_cases'],
             color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(country)
    plt.xlabel("Date")
    plt.ylabel('Number of Daily Cases')
    return st.pyplot()


if st.button('Show Plots'):
    st.header('Daily cases')
    for i in list(df_selected_country_and_date.Country.unique()):
        daily_plot(i)
