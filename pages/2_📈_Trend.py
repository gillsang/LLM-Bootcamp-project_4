import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# 파일 직접 로드
data = pd.read_csv('data_final.csv')

# 페이지 설정
st.set_page_config(
    page_title="채용공고 동향",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

# 서울의 모든 구를 추출 및 "전체" 옵션 추가
seoul_gu_names = data['직장 위치'].unique()
seoul_gu_names_sorted = sorted(seoul_gu_names)
seoul_gu_names_sorted.insert(0, "전체")

# 헤더 스타일링
st.markdown("## 📈채용공고 트렌드 서비스")
st.markdown("#### 채용공고의 동향을 그래프와 분포를 확인 할 수 있습니다.")
st.divider()
st.markdown("#### 📖메뉴얼 ")
st.markdown("###### 🔘아래 메뉴에서 관심 있는 구를 선택해보세요.")
st.markdown("###### 🔘직무별 채용 공고 수를 보여줍니다.")

st.divider()

# 사용자가 구를 선택할 수 있게 하는 드롭다운 메뉴 생성
selected_gu = st.selectbox('', seoul_gu_names_sorted)

# 선택된 구에 대한 데이터 필터링 또는 전체 데이터 사용
if selected_gu == "전체":
    filtered_data = data
else:
    filtered_data = data[data['직장 위치'] == selected_gu]

# 키워드별로 데이터 그룹화 및 공고 수 계산
keyword_counts = filtered_data['키워드'].value_counts().reset_index()
keyword_counts.columns = ['키워드', '공고 수']

# 무채색 팔레트를 위한 색상 리스트 생성
greyscale = ['#111111', '#333333', '#555555', '#777777', '#999999', '#BBBBBB', '#DDDDDD']

# 키워드별 공고 수에 대한 바 차트 생성
fig = px.bar(keyword_counts, x='키워드', y='공고 수', title=f'➡️{selected_gu} 직무별 채용 공고 수',
             color='키워드', color_discrete_sequence=greyscale)
# 차트 레이아웃 조정: 너비와 높이 설정
fig.update_layout(
    xaxis_title='키워드', 
    yaxis_title='공고 수', 
    xaxis={'categoryorder':'total descending'},
    title_font_family="Arial, bold", 
    title_font_color="black", 
    title_font_size=20,
    autosize=False, 
    width=800,  # 너비 설정
    height=600  # 높이 설정
)
st.plotly_chart(fig, use_container_width=True)
# 학력 요구사항에 따른 채용 공고의 분포 데이터 준비
education_counts = data['학력'].value_counts().reset_index()
education_counts.columns = ['학력', '공고 수']

# 파이 차트 생성
fig1 = px.pie(education_counts, names='학력', values='공고 수', title= f'➡️{selected_gu} 학력 요구사항에 따른 채용 공고의 분포', hole=0.3,
              color_discrete_sequence=px.colors.sequential.RdBu)

# 툴팁에 '공고 수' 포함
fig1.update_traces(hoverinfo='label+percent+value', textinfo='percent+label', textfont_size=13, 
                   textfont_color="white", textfont_family="Arial, bold")
fig1.update_layout(title_font_family="Arial, bold", title_font_color="black", title_font_size=20)

st.plotly_chart(fig1, use_container_width=True)



# '채용 형태(경력, 신입)' 컬럼을 기반으로 데이터 그룹화 및 공고 수 계산
career_type_counts = data['채용 형태(경력, 신입)'].value_counts().reset_index()
career_type_counts.columns = ['채용 형태', '공고 수']

# 경력 요구사항별 공고 수에 대한 파이 차트 생성
fig2 = px.pie(career_type_counts, names='채용 형태', values='공고 수', title= f'➡️{selected_gu} 경력 요구사항에 따른 채용 공고의 분포',
              color_discrete_sequence=px.colors.sequential.Viridis)

# 파이 차트 스타일링
fig2.update_traces(textinfo='percent+label', textfont_size=13, textfont_color="white", textfont_family="Arial, bold")
fig2.update_layout(title_font_family="Arial, bold", title_font_color="black", title_font_size=20)

st.plotly_chart(fig2, use_container_width=True)