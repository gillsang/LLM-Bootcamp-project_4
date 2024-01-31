import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static


# 페이지 설정
st.set_page_config(
    page_title="구인구직 지도",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.markdown("""
    <h2 style="color: #333;">🗺️채용공고 Map 서비스</h2>
    <h5 style="color: #555;">👀원하는 기업을 지도에서 한 눈에 확인할 수 있습니다.</h5>
""", unsafe_allow_html=True)

st.divider()

st.markdown("""<h5 style="color: #333;">📖메뉴얼</h5>""", unsafe_allow_html=True)
st.markdown("""<h6 style="color: #333;">🖱️지도 위에서 마우스 커서를 조정해 채용공고 기업의 위치를 확인 할 수 있습니다.</h6>""", unsafe_allow_html=True)
st.markdown("""<h6 style="color: #333;">🖱️지도 위 점들을 클릭해 기업의 정보를 확인 할 수있습니다.</h6>""", unsafe_allow_html=True)
st.markdown("""<h6 style="color: #333;">🖱️좌측 구 선택 슬라이더에서 원하는 구의 기업 정보만 확인 할 수 있습니다.</h6>""", unsafe_allow_html=True)
st.divider()
# CSV 파일 불러오기
df = pd.read_csv("companies_data.csv")

# 결측값이 있는 행 제거
df = df.dropna(subset=['latitude', 'longitude'])

# GeoJSON 파일 경로
geojson_path = 'hangjeongdong_서울특별시.geojson'

# 서울시 중심부의 위도와 경도
latitude = 37.5400456
longitude = 126.9921017

# Folium 지도 생성 및 GeoJSON 경계 추가
map = folium.Map(location=[latitude, longitude], zoom_start=12)
folium.GeoJson(geojson_path, name='geojson').add_to(map)

# 사이드바에 구 선택 슬라이더 추가
with st.sidebar.expander("구 선택", expanded=False):
    selected_districts = []
    for district in df['WORK_PARAR_BASS_ADRES_CN'].str.split().str[1].unique():
        if st.checkbox(district, True):  # 모든 체크박스를 기본적으로 선택
            selected_districts.append(district)

# 선택된 구에 해당하는 회사만 필터링
df_selected = df[df['WORK_PARAR_BASS_ADRES_CN'].str.contains('|'.join(selected_districts))]

# 필요한 컬럼 선택 (회사명, 위도, 경도, 구 정보, 추가 정보)
companies = df_selected[['CMPNY_NM', 'latitude', 'longitude', 'WORK_PARAR_BASS_ADRES_CN', 'HOLIDAY_NM', 'HOPE_WAGE', 'JOBCODE_NM']]


# 구별 색상 정의
district_colors = {
    '강남구': 'red',
    '서초구': 'green',
    '종로구': 'blue',
    '강서구': 'orange',
    '용산구': '#FF66FF',
    '영등포구': '#33FFFF',
    '동대문구': 'purple',
    '마포구': '#FFFF00',
    '노원구': '#770000',
    '중랑구': '#996600',
    '송파구': '#00FF00',
    '강북구': '#9999FF',
    '서대문구': '#CCFF66',
    '중구': '#003300'
    # 나머지 구에 대한 색상 매핑
}

# 색상을 할당하지 못한 구에 대한 기본 색상
default_color = 'gray'

# Folium 지도 생성
initial_location = [37.5400456, 126.9921017]
map = folium.Map(location=initial_location, zoom_start=12)

# 회사 위치에 대한 원형 마커 추가
for index, row in companies.iterrows():
    # 구 정보에서 구 이름 추출
    district_name = row['WORK_PARAR_BASS_ADRES_CN'].split()[1]  # '서울특별시 강남구'에서 '강남구' 추출
    # 구 이름에 해당하는 색상 가져오기
    marker_color = district_colors.get(district_name, default_color)

    # 팝업에 들어갈 HTML 내용
    popup_html = f"""
    <div>
        <h4>{row['CMPNY_NM']}</h4>
        <p>{row['HOLIDAY_NM']}</p>
        <p>{row['HOPE_WAGE']}</p>
        <p>{row['JOBCODE_NM']}</p>
    </div>
    """
    popup = folium.Popup(popup_html, max_width=300)
    tooltip_text = f"{row['CMPNY_NM']}"

    # 원형 마커 생성
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=7,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.7,
        popup=popup,
        tooltip=tooltip_text
    ).add_to(map)

st.empty()

# Streamlit에 지도 표시
col1, col2, col3 = st.columns([1,6,1])
with col2:
    folium_static(map)