import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
st.set_page_config(page_title='COVID Visual Dashboard', layout='wide')

# load CSS
css_file = Path(__file__).parent / 'style.css'
if css_file.exists():
    st.markdown(f'<style>{css_file.read_text()}</style>', unsafe_allow_html=True)

# decorative orbs
st.markdown('<div class="orb s a"></div><div class="orb m b"></div>', unsafe_allow_html=True)

st.markdown('<h1 class="title">COVID-19 Visual Dashboard ✨</h1>', unsafe_allow_html=True)
st.markdown('<div class="small-muted">Interactive dashboard with gradient background, animated visuals and Plotly charts.</div>', unsafe_allow_html=True)

# Data loading: prefer full local dataset, otherwise use bundled sample
RAW_LOCAL = Path('data/raw/owid-covid-data.csv')
SAMPLE = Path('data/raw/owid-covid-data.csv')

@st.cache_data
def load_data():
    if RAW_LOCAL.exists():
        df = pd.read_csv(RAW_LOCAL, parse_dates=['date'])
        st.warning('Loaded local full dataset (data/raw/owid-covid-data.csv)') 
    else:
        df = pd.read_csv(SAMPLE, parse_dates=['date'])
        st.info('Using bundled sample dataset (data/raw/owid-covid-data.csv)')
    return df

df = load_data()

# Sidebar
st.sidebar.header('Controls')
countries = st.sidebar.multiselect('Countries', sorted(df['location'].unique()), default=list(df['location'].unique())[:3])
metric = st.sidebar.selectbox('Metric', ['total_cases','new_cases','total_deaths','people_vaccinated'], index=0)

if not countries:
    st.warning('Select at least one country in the sidebar.')
    st.stop()

filtered = df[df['location'].isin(countries)].sort_values(['location','date'])

# KPIs
with st.container():
    kcols = st.columns(len(countries))
    for i, c in enumerate(countries):
        sub = filtered[filtered['location']==c]
        if sub.empty:
            kcols[i].metric(label=c, value='—', delta='—')
        else:
            latest = sub.iloc[-1]
            kcols[i].markdown(f'<div class="card"><div class="metric-big">{int(latest.get("total_cases",0)):,}</div><div class="small-muted">Total cases • {c}</div></div>', unsafe_allow_html=True)

# Plotly line
st.markdown('<div class="card" style="margin-top:12px;padding:12px">', unsafe_allow_html=True)
fig = px.line(filtered, x='date', y=metric, color='location', markers=True, title=f'{metric} over time')
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Small table and download
st.markdown('<div class="card" style="margin-top:12px;padding:12px">', unsafe_allow_html=True)
st.write('Data snapshot (last 20 rows)')
st.dataframe(filtered.tail(20))
csv = filtered.to_csv(index=False)
st.download_button('Download filtered CSV', data=csv, file_name='covid_filtered.csv', mime='text/csv')
st.markdown('</div>', unsafe_allow_html=True)

# Tips box
st.markdown('<div style="margin-top:14px" class="small-muted">Tip: To use the full dataset, place <code>owid-covid-data.csv</code> into <code>data/raw/</code> (the app will auto-detect it).</div>', unsafe_allow_html=True)
