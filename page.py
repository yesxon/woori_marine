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

df = pd.read_csv("data.csv", encoding='cp949')
df['년도'] = df['년도'].astype(str)
provinces = df.팔도.unique()
colors = px.colors.qualitative.Plotly[:len(df.지역.unique())]


# 사이드바 생성
with st.sidebar:
    st.header('메뉴')

    # 메뉴1: 지역별 해양 쓰레기 barchart
    with st.expander("지역별 해양 쓰레기"):
        province = st.selectbox("도를 선택하세요.", provinces)
        regions = df[df['팔도'] == province].지역.unique()
        region = st.selectbox("지역을 선택하세요.", regions)


    st.divider()

    # 메뉴2: 연도별 해양 쓰레기 지도
    with st.expander("연도 별 해양 쓰레기 지도"):
        year = st.selectbox("연도", df['년도'].unique())


#함수1: 지역별 해양쓰레기
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

#함수2: 연도별 해양쓰레기 
st.title('해양쓔레기')
# df['년도'] = df['년도'].astype(str)
year = st.slider('Slide me', min_value=2018, max_value=2022)
trash = df.loc[df["년도"] == str(year)]
# 'Value' 열을 문자열로 변환
trash['무게'] = trash['무게'].astype(str)
trash = trash.reset_index(drop=True)
# 지도 초기화
# st.write(df)
# st.write(trash_2018)

m = folium.Map(location=[36.5, 127.5], zoom_start=7.2,control_scale=False, zoom_control = False, scrollWheelZoom=False)
# 버블 차트를 지도에 추가
for i in range(len(trash)):
    folium.CircleMarker(
        location=[trash['위도'][i], trash['경도'][i]],
        radius=float(trash['무게'][i])/20,  # 'Value'를 다시 float 형태로 변환
        color= None,
        fill=True,
        fill_color='blue',
        fill_opacity=0.5,
        popup=f"{trash['지역'][i]}: {trash['무게'][i]}"
    ).add_child(folium.Popup(f"{trash['지역'][i]}: {trash['무게'][i]}", parse_html=True)).add_to(m)
# 지도 표시
folium_static(m)