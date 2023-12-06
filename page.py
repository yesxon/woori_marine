import streamlit as st
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

df = pd.read_csv("data.csv", encoding='cp949', skiprows=1, skipfooter=1, engine='python')
colors = px.colors.qualitative.Plotly[:len(df.지역.unique())]

data = {
    '지역': ['지역A', '지역B', '지역C'],
    '연도': [2020, 2021, 2022],
}
df1 = pd.DataFrame(data)

# 사이드바 생성
with st.sidebar:
    st.header('메뉴')

    # 메뉴1: 지역별 해양 쓰레기 barchart
    with st.expander("지역별 해양 쓰레기"):
        region = st.selectbox("지역을 선택하세요.", df1['지역'].unique())
        button_result = st.button('추가 데이터 확인')

    st.divider()

    # 메뉴2: 연도별 해양 쓰레기 지도
    with st.expander("연도 별 해양 쓰레기 지도"):
        year = st.selectbox("연도", df1['연도'].unique())
        button_result = st.button('데이터 확인')

#함수1: 지역별 해양쓰레기

#함수2: 연도별 해양쓰레기 