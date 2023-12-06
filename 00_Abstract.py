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
import folium
from streamlit_folium import folium_static
import random
from PIL import Image

st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f4;  /* 원하는 배경색으로 변경 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 이미지 로드
image = Image.open("spot.JPG")  # 이미지 파일 경로에 맞게 수정

st.markdown("<h1 style='text-align: center;'>연도·지역별 해양쓰레기 조사량<br>시각화 보고서</h1>", unsafe_allow_html=True)
st.markdown("---")
# st.title('연도·지역별 해양쓰레기 조사량 시각화 보고서')
st.header('■ 개요')
st.markdown("""    - 본 페이지는 「국가 해양쓰레기 모니터링 사업」으로 지자체별로
            전국 60개소에서 2018년부터<br>수집한 쓰레기 조사량 데이터의 시각화 자료를 제공합니다.<br>
            다양한 차트를 통해 지역별, 연도별 쓰레기 수집량에 대한 인사이트를 손쉽게 얻을 수 있습니다.<br>
            <br>
            """, unsafe_allow_html=True)
st.markdown("---")

st.subheader('■ 데이터 보고서 url')
st.markdown('    - https://www.koem.or.kr/site/koem/ex/board/View.do?cbIdx=370&bcIdx=31247')

st.markdown("---")

st.subheader('■ 데이터 수집 지역')
st.image(image, caption='국가 해안쓰레기 모니터링 정점 위치도(60곳)', use_column_width=True)

st.markdown("---")

df = pd.read_csv("data.csv", encoding='cp949')
rawdf = pd.read_csv("raw_data.csv", encoding='cp949')
df['년도'] = df['년도'].astype(str)
provinces = df.팔도.unique()
colors = px.colors.qualitative.Plotly[:len(df.지역.unique())]


st.subheader('■ 사용 데이터')
col1, col2 = st.columns(2)  # 2개의 열 생성

# 각 열에 데이터프레임 출력
col1.write('<원본 데이터>')
col2.write('<가공 데이터>')
col1.dataframe(rawdf)
col2.dataframe(df)
st.markdown("---")
