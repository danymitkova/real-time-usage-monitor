
import streamlit as st, pandas as pd, time, os
st.set_page_config(page_title="Real‑Time Usage KPIs", layout="wide")
st.title("⚡ Live Product Usage Dashboard")

delta_path = os.environ.get("DELTA_PATH", "/tmp/delta/usage_agg")
placeholder = st.empty()

while True:
    try:
        df = pd.read_parquet(delta_path)
        df['minute'] = df['window'].apply(lambda x: x['start'])
        latest = df.sort_values('minute').tail(10)
        with placeholder.container():
            st.metric("Events (last min)", int(latest.tail(1)['events'].sum()))
            st.line_chart(latest.pivot(index='minute', columns='event_type', values='events'))
    except Exception as e:
        st.info("Waiting for data ...")
    time.sleep(5)
