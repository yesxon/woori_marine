import streamlit as st
import FinanceDataReader as fdr
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO
import plotly.graph_objects as go
import openpyxl
import pandas as pd
import plotly.figure_factory as ff
import plotly.io as pio # Plotly input output
import plotly.express as px # 빠르게 그리는 방법
import plotly.graph_objects as go # 디테일한 설정
import plotly.figure_factory as ff # 템플릿 불러오기
from plotly.subplots import make_subplots # subplot 만들기
from plotly.validators.scatter.marker import SymbolValidator # Symbol 꾸미기에 사용됨

df = pd.read_csv("data.csv", encoding='cp949')
df['년도'] = df['년도'].astype(str)
provinces = df.팔도.unique()

with st.sidebar:
    st.header("지역별 해양 쓰레기")
    province = st.selectbox("도를 선택하세요.", provinces)
    regions = df[df['팔도'] == province].지역.unique()
    region = st.selectbox("지역을 선택하세요.", regions)

if province and region:
    fig = px.bar(df[df['지역']==region], 
             x="년도", 
             y="무게", 
             color="년도", 
             labels={'무게': '무게 (kg)'})
    
    line_chart = go.Scatter(x=df[df['지역']==region]['년도'], 
                            y=df[df['지역']==region]['무게'], 
                            mode='lines+markers',  # 마커를 추가하기 위해 'markers' 옵션 사용
                            line=dict(color='darkblue', width=3),
                            marker=dict(color='darkblue', size=8),  # 동그라미의 색상과 크기 설정
                            name='증감 추이')
    fig.add_trace(line_chart)

    fig.update_layout(title_text=f'{region} 연도별 무게 비교')

    st.plotly_chart(fig)