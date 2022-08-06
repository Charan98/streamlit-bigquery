import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from datetime import datetime as dt

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

#Get start and end date for the query
try:
    dts = st.date_input(label='Date Range: ',
                value=(dt(year=2022, month=1, day=1, hour=00, minute=00), 
                        dt(year=2022, month=12, day=31, hour=23, minute=59)),
                key='#date_range',
                help="The start and end date time")
    st.write('Start: ', dts[0], "End: ", dts[1])

except:
    pass


start_date = dts[0].strftime("%Y%m%d")
end_date = dts[1].strftime("%Y%m%d")

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.experimental_memo to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query("SELECT COUNT(totals.transactions) AS Transactions FROM `bumblebee-233720.12646513.ga_sessions_2022*` WHERE date BETWEEN '%s' AND '%s'" % (start_date, end_date))

# Print results.
st.write("Total number of transaction between the selected dates")
for row in rows:
    st.write(row['Transactions'])