import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
import random
import plotly.express as px
import plotly.graph_objects as go
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
trash['무게'] = trash['무게'].astype(float)
quan = trash.groupby('년도')['무게'].sum().reset_index()
quan2 = df.groupby('년도')['무게'].sum().reset_index()
fig = px.line(quan2, x = '년도', y = '무게', title='연도별 쓰레기 총량', markers=True, line_shape="linear")
# fig.update_layout(xaxis=dict(dtick=1, range=[2018, 2022]))
st.write(fig)

m = folium.Map(location=[36.5, 127.5], zoom_start=6,control_scale=False, zoom_control = True, scrollWheelZoom=False)
# 버블 차트를 지도에 추가
for i in range(len(trash)):
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    folium.CircleMarker(
        location=[trash['위도'][i], trash['경도'][i]],
        radius=float(trash['무게'][i])/10,  # 'Value'를 다시 float 형태로 변환
        color=None,
        fill=True,
        fill_color=color,
        fill_opacity=0.5,
        popup=f"{trash['지역'][i]}: {trash['무게'][i]}"
    ).add_child(folium.Popup(f"{trash['지역'][i]}: {trash['무게'][i]}", parse_html=True)).add_to(m)
# 지도 표시
m.fit_bounds([[trash['위도'].min(), trash['경도'].min()], [trash['위도'].max(), trash['경도'].max()]])


# quan = pd.DataFrame(quan)
folium_static(m)
# st.write(quan)
# st.write(type(quan))
st.write(f'총 무게: {quan.무게[0]}')
# st.write(quan.loc['년도' == year])