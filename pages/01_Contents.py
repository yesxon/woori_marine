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
df = pd.read_csv("../woori_marine/data.csv", encoding='cp949')
rawdf = pd.read_csv("../woori_marine/raw_data.csv", encoding='cp949')
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
    with st.expander("연도별 해양 쓰레기 지도"):
        year = st.slider('연도를 설정해 주세요.', min_value=2018, max_value=2022)



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

    # fig.update_layout(title_text=f'{region} 연도별 무게 비교')
    st.markdown(f"<h3 style='text-align: center;'>[{region} 연도별 무게 비교]</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)
st.markdown("---")
#함수2: 연도별 해양쓰레기 
df = pd.read_csv("data.csv", encoding='cp949')

trash = df.loc[df["년도"] == year]
# 'Value' 열을 문자열로 변환
trash['무게'] = trash['무게'].astype(str)
trash = trash.reset_index(drop=True)
# 지도 초기화
trash['무게'] = trash['무게'].astype(float)
quan = trash.groupby('년도')['무게'].sum().reset_index()
        


m = folium.Map(location=[36.5, 127.5], zoom_start=6,control_scale=False, zoom_control = True, scrollWheelZoom=False)
# 버블 차트를 지도에 추가
for i in range(len(trash)):
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    popup_html = f"""
            <b>지역:</b> {trash['지역'][i]}<br>
            <b>무게:</b> {trash['무게'][i]}<br>
            <b>년도:</b> {trash['년도'][i]}
        """
    folium.CircleMarker(
        location=[trash['위도'][i], trash['경도'][i]],
        radius=float(trash['무게'][i])/15,  # 'Value'를 다시 float 형태로 변환
        color=None,
        fill=True,
        fill_color=color,
        fill_opacity=0.5,
        popup=folium.Popup(popup_html,max_width=300)
    ).add_to(m)
# 지도 표시
st.markdown(f"<h3 style='text-align: center;'>[{region} 연도별 해양쓰레기 지도]</h3>", unsafe_allow_html=True)
folium_static(m)

# 연도별 쓰레기 총량 그래프
st.write(f'  - {year}년 총 무게: {quan.무게[0]}')
quan2 = df.groupby('년도')['무게'].sum().reset_index()
fig = px.line(quan2, x = '년도', y = '무게', markers=True, line_shape="linear")
st.markdown("---")
st.markdown(f"<h3 style='text-align: center;'>[연도별 쓰레기 총량]</h3>", unsafe_allow_html=True)
st.write(fig)