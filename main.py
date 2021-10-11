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

# Web scraping of S&P 500 data
#


@st.cache
def load_data():
    # Import data from who_data.csv file and stores it as time_series
    time_series = pd.read_csv('daily_covid_data.csv')
    return time_series.dropna()


df = load_data()
country = df.groupby('Code')
# Sidebar - Country selection
sorted_country_unique = sorted(df['Entity'].unique())
selected_country = st.sidebar.multiselect(
    'Country', sorted_country_unique)


# Filtering data
df_selected_country = df[(df['Entity'].isin(selected_country))]

st.header('Display Selected Countries on 3/10/21')
st.write('This will display the number of covid cases on 3/10/21')
st.dataframe(df_selected_country.groupby('Entity').last())


def filedownload(df):
    csv = df.to_csv(index=False)
    # strings <-> bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="Covid-19.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(df_selected_country), unsafe_allow_html=True)

data = df_selected_country

# Plot daily cases


def daily_plot(code):
    df = data[data['Code'] == code]
    df.index = df['Day']
    plt.plot(pd.to_datetime(df.Day), df['Daily new confirmed cases of COVID-19'],
             color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(code)
    plt.xlabel("Date")
    plt.ylabel('Number of Daily Cases')
    return st.pyplot()


if st.button('Show Plots'):
    st.header('Daily cases')
    for i in list(df_selected_country.Code.unique()):
        daily_plot(i)
