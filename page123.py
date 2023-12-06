import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
df = pd.read_csv("data.csv", encoding='cp949')

st.title('해양쓔레기')
year = st.slider('Slide me', min_value=2018, max_value=2022)
# df['년도'] = df['년도'].astype(str)
trash = df.loc[df["년도"] == year]
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