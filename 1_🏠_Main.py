import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import openai

st.set_page_config(
    page_title="알쓸신JOB Main homepage",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

# CSS 애니메이션 추가
st.markdown("""
<style>
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

.animated-text {
    animation: fadeIn 2s;
}

@keyframes popIn {
    0% {transform: scale(0);}
    80% {transform: scale(1.1);}
    100% {transform: scale(1);}
}

.pop-in {
    animation: popIn 0.5s ease-out;
}

/* 기존 스타일링 코드 */
/* ... (나머지 기존 CSS 코드) ... */

</style>
""", unsafe_allow_html=True)

# 취업의 신 제목 부분에 애니메이션 적용
st.markdown("""
<div style="background-color: #f2f2f2; padding: 20px; border-radius: 15px; border: 1px solid #cccccc; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
    <h1 class="animated-text" style="color: #333; text-align: center; font-family: 'Arial', sans-serif;">🔍 <span class="pop-in" style="color: navy;">알쓸신JOB</span> </h1>
    <h2 style="text-align: center; color: #555; font-family: 'Arial', sans-serif;">알아두면 쓸모있는 JOB 지식</h2>
    <h5 style="text-align: center; color: #555; font-family: 'Arial', sans-serif;">취업은 해야하는데 어떻게 찾아야 되는지 힘들다고? 시간이 부족하다고?</h5>
    <h5 style="text-align: center; color: #555; font-family: 'Arial', sans-serif;">우리가 도와줄게 당신의 맞춤 구인구직 기업들을 추천해줄 수 있어!!</h5>
</div>
""", unsafe_allow_html=True)

# 사이트 배경색 및 컨테이너 스타일 설정
st.markdown("""
<style>
/* 컨테이너 스타일 */
.css-1d391kg {
    padding-top: 0 !important;
}
/* 링크 스타일 */
a.card {
    border: 1px solid #eee;  /* 테두리 설정 */
    border-radius: 10px;     /* 테두리 둥글게 설정 */
    display: block;          /* 블록 요소로 설정 */
    margin: 30px 0;          /* 상하 여백 설정, 위아래 여백을 30px로 설정 */
    padding: 20px;           /* 내부 여백 설정, 패딩을 20px로 설정 */
    transition: transform 0.3s; /* 변환 효과 설정 */
    text-align: center;      /* 텍스트 중앙 정렬 */
    width: 100%;             /* 너비 100% 설정 */
}
a.card:hover {
    transform: scale(1.05);  /* 마우스 오버 시 커지는 효과 */
    background-color: #f8f9fa; /* 배경색 변경 */
}
/* 링크 밑줄 제거 */
a.card, a.card:hover, a.card:visited, a.card:active {
    text-decoration: none; /* 링크의 밑줄 제거 */
}

# /* 이미지 스타일 */
# .img-fluid {
#     max-width: 100%;
#     height: auto;
# }
/* 제목 스타일 */
h3 {
    font-size: 16px;
    color: #333;
    padding: 0 16px 10px;       /* 제목 글씨 크기 설정 */
}
/* 설명 텍스트 스타일 */
p {
    font-size: 14px;
    color: #666;
    padding: 0 16px 16px;        /* 설명 텍스트 글씨 크기 설정 */
}
</style>
""", unsafe_allow_html=True) 

st.divider()

# 취업 정보 테이블 생성
st.header("🔥2024년도 인기 직무 채용 정보관")
st.subheader("최근 가장 조회수가 높은 채용 정보입니다. 해당 카드를 클릭하면 해당 구인구직 사이트로 이동합니다.🔥")

job_info1 = [
    {"emoji": "🗄️", "title": "데이터엔지니어링팀 데이터 플랫폼 엔지니어 채용", "company": "GS리테일", "link": "https://gsretail.recruiter.co.kr/career/jobs/11790"},
    {"emoji": "🛡️", "title": "IT 정보보안 엔지니어 채용", "company": "잡코리아(유)", "link": "https://www.jobkorea.co.kr/Recruit/GI_Read/43832214?Oem_Code=C1&logpath=1&stext=%EC%A0%95%EB%B3%B4%EB%B3%B4%EC%95%88&listno=1"},
    {"emoji": "📋", "title": "2024 DB 생명 상반기 지원직 신입사원 모집", "company": "DB 생명", "link": "https://dbgroup.recruiter.co.kr/app/jobnotice/view?systemKindCode=MRS2&jobnoticeSn=169233"},
    {"emoji": "👨🏻‍💻", "title": "DevOps Engineer (산업기능요원) 채용", "company": "Toss", "link": "https://toss.im/career/job-detail?job_id=5611026003&company=%ED%86%A0%EC%8A%A4"}
]
job_info2 = [
    {"emoji": "♞", "title": "BKR FOOD & TECH 전략영업팀 정규직 직원 채용", "company": "BKR", "link": "https://recruit.bkr.co.kr/recruit/recruit001.do"},
    {"emoji": "⚔️", "title": "마비노기 집중 채용", "company": "Nexon", "link": "https://mabinogi.career.greetinghr.com/?utm_campaign=2024%20%EB%A7%88%EB%B9%84%EB%85%B8%EA%B8%B0%20%EC%A7%91%EC%A4%91%EC%B1%84%EC%9A%A9&utm_medium=mass&utm_source=jobkorea&utm_content=post"},
    {"emoji": "📲", "title": "UI/UX 디자이너 채용", "company": "잡코리아(유)", "link": "https://www.jobkorea.co.kr/Recruit/GI_Read/43757370?Oem_Code=C1&logpath=1&stext=ui%20ux%20%EC%8B%A0%EC%9E%85&listno=1"},
    {"emoji": "📊", "title": "데이터 사이언티스트(LLM) 경력직 모집", "company": "HSAD LG Careers", "link": "https://careers.lg.com/app/job/RetrieveJobNoticesDetail.rpi"}
]

# 스타일링 업데이트 - 높이 고정 추가
st.markdown("""
<style>
/* 기존 스타일에 높이를 고정하는 속성 추가 */
.card {
    height: 250px; /* 높이를 250px로 고정하거나 원하는 값으로 설정 */
    padding: 0;
    /* 나머지 스타일은 그대로 유지 */
}
/* 카드 내용을 중앙에 배치 */
.card-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# 각 취업 정보에 대한 컨테이너를 생성하고 스타일링
cols = st.columns(len(job_info1), gap="medium")
cols = st.columns(len(job_info2), gap="medium")

# 각 취업 정보에 대한 컨테이너 생성 및 스타일링
for idx, job in enumerate(job_info1):
    with cols[idx]:
        # <a> 태그로 감싸는 HTML 구조
        link_html = f'''
        <a href="{job["link"]}" target="_blank" class="card" style="padding:0">
            <div class="card-content">
                <div style="font-size: 4em;">{job["emoji"]}</div>
                <h3 style="font-size: 1em;">{job["title"]}</h3>
                <p style="font-size: 1em; color: #FF0000"><strong style="color: #666666">기업:</strong> {job["company"]}</p>
            </div>
        </a>
        '''
        st.markdown(link_html, unsafe_allow_html=True)

for idx, job in enumerate(job_info2):
    with cols[idx]:
        # <a> 태그로 감싸는 HTML 구조
        link_html = f'''
        <a href="{job["link"]}" target="_blank" class="card" style="padding:0">
            <div class="card-content">
                <div style="font-size: 4em;">{job["emoji"]}</div>
                <h3 style="font-size: 1em">{job["title"]}</h3>
                <p style="font-size: 1em; color: #FF0000"><strong style="color: #666666">기업:</strong> {job["company"]}</p>
            </div>
        </a>
        '''
        st.markdown(link_html, unsafe_allow_html=True)
###########################################################################

st.divider()

st.header("☘️ 맞춤형 직무 추천 서비스")
st.subheader("✅ 원하는 직무를 선택하세요.")
st.subheader("✅ 본인에게 맞는 2024 기업 채용 정보 추천 서비스입니다.")
st.subheader("✅ 해당 카드를 클릭하면 해당 구인구직 사이트로 이동합니다.")

st.subheader("")
# st.info(
#     "이곳은 메뉴얼 입니다.",
#     icon="ℹ️",
# )
st.subheader("\n\n")
# 주 카테고리와 이모지
categories = {
    "공학": "🛠",
    "상경": "💼",
    "자연과학": "🔬"
}

# 세부 카테고리와 이모지
subcategories = {
    "공학": {"컴퓨터공학": "💻", "머신러닝": "🤖", "자연어처리": "📝"},
    "상경": {"경제학": "📈", "경영학": "🏢", "회계학": "🧮"},
    "자연과학": {"물리학": "⚛️", "화학": "🧪", "생물학": "🔬"}
}


category_job_info = {
    "컴퓨터공학":[
    {"emoji": "💻", "title": "현대자동차 Frontend Developer 채용", "company": "현대자동차", "link": "https://talent.hyundai.com/apply/applyView.hc?recuYy=2023&recuType=N2&recuCls=549"},
    {"emoji": "✈️", "title": "아시아나 IDT 경력직 채용", "company": "아시아나IDT", "link": "https://asianaidt.recruiter.co.kr/app/jobnotice/view?systemKindCode=MRS2&jobnoticeSn=169577"},
    {"emoji": "🔙", "title": "백엔드 개발자 채용", "company": "코오롱그룹", "link": "https://dream.kolon.com/RECRUIT_KOLON/hr/rec/recruit/jobopen/controller/candidate/JobOpen320WebController/view.hr?"},
    {"emoji": "🕵️", "title": "Quality Assurance 경력직 채용", "company": "SSG.COM", "link": "https://ssg.career.greetinghr.com/o/99240"}
    ],
    "머신러닝":[
    {"emoji": "🧠", "title": "2024 LINE ADS AI/ML Internship 정규직 채용", "company": "LINE CAREERS", "link": "https://careers.linecorp.com/ko/jobs/2111"},
    {"emoji": "🇦🇮", "title": "AI Researcher 채용", "company": "현대오토에버(주)", "link": "https://recruit.hyundai-autoever.com/?page=156184575&id=257148&list=270136750&scroll=4800"},
    {"emoji": "🔗", "title": "블록체인 엔지니어 채용", "company": "LOVO", "link": "https://lovo.ai/post/lovo-%EC%B1%84%EC%9A%A9%EA%B3%B5%EA%B3%A0"},
    {"emoji": "🤖", "title": "머신러닝 엔지니어 채용", "company": "INDENT", "link": "https://career.indentcorp.com/"}
    ],
    "자연어처리":[
    {"emoji": "🗣️", "title": "2024년도 가을학기 KT AI석사과정 신입생 모집", "company": "KT", "link": "https://recruit.kt.com/careers/169357"},
    {"emoji": "🚚", "title": "서비스부문 배달시간예측서비스팀 Data Scientist 모집", "company": "우아한 형제들", "link": "https://career.woowahan.com/recruitment/R2308049/detail?category=jobGroupCodes%3ABA005001&keyword=&jobCodes=BA007005"},
    {"emoji": "👨🏻‍💻", "title": "리서치 사이언티스트 (NLP) 모집", "company": "넥슨", "link": "https://career.nexon.com/user/recruit/member/postDetail?joinCorp=NX&reNo=20230116&currentPage=0"},
    {"emoji": "🤖", "title": "대규모 언어모델(LLM) 개발자 모집", "company": "코난테크놀로지", "link": "https://konantec.career.greetinghr.com/o/78708"}
    ],
    "경제학":[
    {"emoji": "📈", "title": "2024 경력 및 신입 인재 채용", "company": "CUCKOO", "link": "https://recruit.cuckoo.co.kr/recruit/BASE/RecruitPost/view.do?hmCode=HM010&seq=168"},
    {"emoji": "🗄️", "title": "본사 설계사 수수료 담당 채용", "company": "HK금융파트너스", "link": "https://taekwang.recruiter.co.kr/app/jobnotice/view?systemKindCode=MRS2&jobnoticeSn=169585"},
    {"emoji": "💵", "title": "회계부문(서울) 경력직원 채용", "company": "BNK투자증권", "link": "https://www.bnkfn.co.kr:43674/aboutus/recruit.jspx?bbsId=recruit&cmd=view&bbsSeq=47039"},
    {"emoji": "🧾", "title": "2024년 상반기 지원직 신입사원 모집", "company": "DB생명", "link": "https://dbgroup.recruiter.co.kr/app/jobnotice/view?systemKindCode=MRS2&jobnoticeSn=169233"}
    ],
    "경영학":[
    {"emoji": "👨🏻‍💼", "title": "2024 경력 및 신입 인재 채용", "company": "CUCKOO", "link": "https://recruit.cuckoo.co.kr/recruit/BASE/RecruitPost/view.do?hmCode=HM010&seq=168"},
    {"emoji": "👩🏻‍💼", "title": "[경력] 영업부문 기술지원 담당자 모집 공고", "company": "다인정공", "link": "https://dine09.career.greetinghr.com/o/95646"},
    {"emoji": "👨🏻‍💻", "title": "[신입] 영업부문 기술지원 담당자 모집 공고", "company": "다인정공", "link": "https://dine09.career.greetinghr.com/o/95645"},
    {"emoji": "🗄️", "title": "재무/회계 경력직 모집", "company": "엠큐닉", "link": "https://www.jobkorea.co.kr/Recruit/GI_Read/43741928?Oem_Code=C1"}
    ],
    "회계학":[
    {"emoji": "💻", "title": "2024 경력 및 신입 인재 채용", "company": "CUCKOO", "link": "https://recruit.cuckoo.co.kr/recruit/BASE/RecruitPost/view.do?hmCode=HM010&seq=168"},
    {"emoji": "🗄️", "title": "재무회계 우수 경력사원 수시모집", "company": "이노엔", "link": "https://inno-n.recruiter.co.kr/app/jobnotice/view?systemKindCode=MRS2&jobnoticeSn=169563"},
    {"emoji": "👨🏻‍💻", "title": "2024년 상반기 경영관리 담당자 채용", "company": "동아쏘시오그룹", "link": "https://donga.recruiter.co.kr/app/jobnotice/view?systemKindCode=MRS2&jobnoticeSn=169393"},
    {"emoji": "📈", "title": "투자 오퍼레이션 계약직원 채용", "company": "KIC 한국투자공사", "link": "https://www.kic.kr/ko/recruit/01.jsp?mode=view&no=1217"}
    ],

"물리학":[
    {"emoji": "☢", "title": "한국핵융합에너지연구원 계약직(1차) 채용", "company": "한국핵융합에너지연구원", "link": "https://kfe.recruitment.kr/app/jobnotice/view?systemKindCode=MRS2&jobnoticeSn=29"},
    {"emoji": "⚛️", "title": "기초과학연구원 지하실험 연구단 연구기술직 채용", "company": "ibs 기초과학연구원", "link": "https://www.ibs.re.kr/prog/recruit/kor/sub04_01/view.do;jsessionid=3D2E0C5C1538B733AA3DCEE3B5B8F3F4?pageIndex=1&searchCondition=&searchKeyword=&idx=1689"},
    {"emoji": "👨‍💻", "title": "중앙연구소 기반기술 공정 및 해석 연구원 채용", "company": "아이씨디", "link": "https://icd.career.greetinghr.com/o/95291"},
    {"emoji": "⚡", "title": "Siemens Electronic Design Automation (Korea) LLC", "company": "SIEMENS", "link": "https://jobs-disw.siemens.com/careers/job/563156117103892?microsite=DISW"}
    ],
    "화학":[
    {"emoji": "👩🏻‍🔬", "title": "신소재 연구 대졸 신입사원 채용", "company": "KCC", "link": "https://recruit.kccworld.co.kr/recruit/recruitMain.do?SiteType=A"},
    {"emoji": "💊", "title": "전문 의약품 영업우수 경력사원 모집", "company": "이노엔", "link": "https://inno-n.recruiter.co.kr/app/jobnotice/view?systemKindCode=MRS2&jobnoticeSn=169563"},
    {"emoji": "⚛", "title": "2024년 상반기 신입/경력사원 모집", "company": "W-SCOPE", "link": "https://wcp.kr/home/sub.php?menukey=81&mod=view&no=382&scode=99999999"},
    {"emoji": "🧪", "title": "2024년 상반기 임상개발 담당자 채용", "company": "동아쏘시오그룹", "link": "https://donga.recruiter.co.kr/app/jobnotice/view?systemKindCode=MRS2&jobnoticeSn=169393"}
    ],
    "생물학":[
    {"emoji": "🥼", "title": "임상시험/PMS 업무 담당자 모집", "company": "건일제약", "link": "https://kuhnil.ninehire.site/job_posting/VVlQRvcB"},
    {"emoji": "💻", "title": "식품 분석/데이터엔지니어 경력사원 모집", "company": "NS홈쇼핑", "link": "https://ns.recruiter.co.kr/app/jobnotice/view?systemKindCode=MRS2&jobnoticeSn=169815"},
    {"emoji": "🧬", "title": "연구중심병원 육성 R&D 사업(역분화줄기세포) 계약직 연구원 채용", "company": "삼성서울병원", "link": "https://www.samsunghospital.com/home/recruit/recruitInfo/recruitNoticeView.do?RECRUIT_CD=2024EAJ0003&cPage=1"},
    {"emoji": "💊", "title": "신입/경력 수시채용", "company": "셀트리온제약", "link": "http://recruit.celltrionph.com/"}
    ],

}

# 주 카테고리 선택
category_keys = list(categories.keys())
selected_category_key = st.selectbox("원하는 직무를 선택하세요.", category_keys, format_func=lambda x: f"{categories[x]} {x}")

# 세부 카테고리 선택
subcategory_keys = list(subcategories[selected_category_key].keys())
selected_subcategory_key = st.selectbox("세부 카테고리를 선택하세요.", subcategory_keys, format_func=lambda x: f"{subcategories[selected_category_key][x]} {x}")

st.subheader("\n\n")
st.subheader("\n\n")
st.subheader(f"📝 {selected_category_key}에서 {selected_subcategory_key} 관련 구인구직 정보 입니다.")

job_info = category_job_info[selected_subcategory_key]

cols = st.columns(4, gap="medium")

for idx, job in enumerate(job_info):
    with cols[idx % 4]:
        # <a> 태그로 감싸는 HTML 구조
        link_html = f'''
        <a href="{job["link"]}" target="_blank" class="card" style="padding:0">
            <div class="card-content">
                <div style="font-size: 4em;">{job["emoji"]}</div>
                <h3 style="font-size: 1em;">{job["title"]}</h3>
                <p style="font-size: 1em; color: #FF0000"><strong style="color: #666666">기업:</strong> {job["company"]}</p>
            </div>
        </a>
        '''
        st.markdown(link_html, unsafe_allow_html=True)

st.divider()
st.header("🤖알쓸신JOB 챗봇")
st.subheader("이곳은 Q&A를 통해 실시간 기업의 채용공고의 정보를 개인 맞춤형으로 제공해드리는 서비스 입니다.")

st.markdown("""
<div style="background-color: #f2f2f2; padding: 10px; border-radius: 15px; border: 1px solid #cccccc; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
    <h5 style="color: #333;">📖메뉴얼</h5>
    <h6 style="color: #333;">⌨️메인 홈페이지 가장 하단에 있는 챗봇의 입력창에 궁금하신 내용을 물어보세요.</h6>
    <h6 style="color: #333;">⌨️챗봇의 답변에 추가 원하는 정보가 있다면 더욱 구체적으로 재질문 해주실수록 좋습니다.</h6>
    <h6 style="color: #333;">⌨️질문에 원하는 채용정보를 입력하실 때 oo역을 포함하여 입력하여 주세요!!.</h6>
    <h6 style="color: #333;">⌨️ex) 강변역 근처에 채용공고가 올라온 기업 2개만 소개시켜줘.</h6>
</div>
""", unsafe_allow_html=True)

st.subheader("")
st.subheader("")
st.subheader("⏬⏬채팅 내용⏬⏬.")

################################################################

def get_companies_df(df_api_key):
    url = "http://openAPI.seoul.go.kr:8088/{}/xml/GetJobInfo/1/1000/".format(df_api_key)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"API 요청 실패. 상태 코드: {response.status_code}")
        return None

    root = ET.fromstring(response.content)
    data = []

    for job in root.findall(".//row"):
        # 모든 필요한 필드를 추출합니다.
        company_data = {
            "JO_REQST_NO": job.find("JO_REQST_NO").text
            if job.find("JO_REQST_NO") is not None
            else None,  # 구인신청번호
            "JO_REGIST_NO": job.find("JO_REGIST_NO").text
            if job.find("JO_REGIST_NO") is not None
            else None,  # 구인등록번호
            "CMPNY_NM": job.find("CMPNY_NM").text
            if job.find("CMPNY_NM") is not None
            else None,  # 기업명칭
            "BSNS_SUMRY_CN": job.find("BSNS_SUMRY_CN").text
            if job.find("BSNS_SUMRY_CN") is not None
            else None,  # 사업요약내용
            "RCRIT_JSSFC_CMMN_CODE_SE": job.find("RCRIT_JSSFC_CMMN_CODE_SE").text
            if job.find("RCRIT_JSSFC_CMMN_CODE_SE") is not None
            else None,  # 모집직종코드
            "JOBCODE_NM": job.find("JOBCODE_NM").text
            if job.find("JOBCODE_NM") is not None
            else None,  # 모집직종코드명
            "RCRIT_NMPR_CO": job.find("RCRIT_NMPR_CO").text
            if job.find("RCRIT_NMPR_CO") is not None
            else None,  # 모집인원수
            "ACDMCR_CMMN_CODE_SE": job.find("ACDMCR_CMMN_CODE_SE").text
            if job.find("ACDMCR_CMMN_CODE_SE") is not None
            else None,  # 학력코드
            "ACDMCR_NM": job.find("ACDMCR_NM").text
            if job.find("ACDMCR_NM") is not None
            else None,  # 학력코드명
            "EMPLYM_STLE_CMMN_CODE_SE": job.find("EMPLYM_STLE_CMMN_CODE_SE").text
            if job.find("EMPLYM_STLE_CMMN_CODE_SE") is not None
            else None,  # 고용형태코드
            "EMPLYM_STLE_CMMN_MM": job.find("EMPLYM_STLE_CMMN_MM").text
            if job.find("EMPLYM_STLE_CMMN_MM") is not None
            else None,  # 고용형태코드명
            "WORK_PARAR_BASS_ADRES_CN": job.find("WORK_PARAR_BASS_ADRES_CN").text
            if job.find("WORK_PARAR_BASS_ADRES_CN") is not None
            else None,  # 근무예정지 주소
            "SUBWAY_NM": job.find("SUBWAY_NM").text
            if job.find("SUBWAY_NM") is not None
            else None,  # 인접전철역
            "DTY_CN": job.find("DTY_CN").text
            if job.find("DTY_CN") is not None
            else None,  # 직무내용
            "CAREER_CND_CMMN_CODE_SE": job.find("CAREER_CND_CMMN_CODE_SE").text
            if job.find("CAREER_CND_CMMN_CODE_SE") is not None
            else None,  # 경력조건코드
            "CAREER_CND_NM": job.find("CAREER_CND_NM").text
            if job.find("CAREER_CND_NM") is not None
            else None,  # 경력조건코드명
            "HOPE_WAGE": job.find("HOPE_WAGE").text
            if job.find("HOPE_WAGE") is not None
            else None,  # 급여조건
            "RET_GRANTS_NM": job.find("RET_GRANTS_NM").text
            if job.find("RET_GRANTS_NM") is not None
            else None,  # 퇴직금구분
            "WORK_TIME_NM": job.find("WORK_TIME_NM").text
            if job.find("WORK_TIME_NM") is not None
            else None,  # 근무시간
            "WORK_TM_NM": job.find("WORK_TM_NM").text
            if job.find("WORK_TM_NM") is not None
            else None,  # 근무형태
            "HOLIDAY_NM": job.find("HOLIDAY_NM").text
            if job.find("HOLIDAY_NM") is not None
            else None,  # 공휴일
            "WEEK_WORK_HR": job.find("WEEK_WORK_HR").text
            if job.find("WEEK_WORK_HR") is not None
            else None,  # 주당근무시간
            "JO_FEINSR_SBSCRB_NM": job.find("JO_FEINSR_SBSCRB_NM").text
            if job.find("JO_FEINSR_SBSCRB_NM") is not None
            else None,  # 4대보험
            "RCEPT_CLOS_NM": job.find("RCEPT_CLOS_NM").text
            if job.find("RCEPT_CLOS_NM") is not None
            else None,  # 마감일
            "RCEPT_MTH_IEM_NM": job.find("RCEPT_MTH_IEM_NM").text
            if job.find("RCEPT_MTH_IEM_NM") is not None
            else None,  # 전형장소
            "MODEL_MTH_NM": job.find("MODEL_MTH_NM").text
            if job.find("MODEL_MTH_NM") is not None
            else None,  # 전형방법
            "RCEPT_MTH_NM": job.find("RCEPT_MTH_NM").text
            if job.find("RCEPT_MTH_NM") is not None
            else None,  # 접수방법
            "PRECENTN_PAPERS_NM": job.find("PRECENTN_PAPERS_NM").text
            if job.find("PRECENTN_PAPERS_NM") is not None
            else None,  # 제출서류
            "MNGR_NM": job.find("MNGR_NM").text
            if job.find("MNGR_NM") is not None
            else None,  # 담당상담사명
            "MNGR_PHON_NO": job.find("MNGR_PHON_NO").text
            if job.find("MNGR_PHON_NO") is not None
            else None,  # 담당 상담사 전화번호
            "MNGR_INSTT_NM": job.find("MNGR_INSTT_NM").text
            if job.find("MNGR_INSTT_NM") is not None
            else None,  # 담당 상담사 소속기관명
            "BASS_ADRES_CN": job.find("BASS_ADRES_CN").text
            if job.find("BASS_ADRES_CN") is not None
            else None,  # 기업주소
            "JO_SJ": job.find("JO_SJ").text
            if job.find("JO_SJ") is not None
            else None,  # 구인제목
            "JO_REG_DT": job.find("JO_REG_DT").text
            if job.find("JO_REG_DT") is not None
            else None,  # 등록일
            "GUI_LN": job.find("GUI_LN").text
            if job.find("GUI_LN") is not None
            else None,  # 모집요강
        }

        # 지하철역 이름이 요청한 지하철역과 일치하면 리스트에 추가합니다.
        
        data.append(company_data)

    return pd.DataFrame(data)
df = get_companies_df("api")


# 여기에 해당 분야 챗봇 관련 코드 추가
############################################################
import re

# OpenAI API 키 설정
openai.api_key = "api"

# Streamlit 세션 상태 초기화
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "궁금한건 나한테 물어봐!!"}
    ]

# Streamlit 채팅 인터페이스
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Chating Go!! GO!!")

information = None

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # 사용자 질문에서 지하철역 이름 추출
        subway_station_match = re.search(r"(\w+)역", prompt)
        if subway_station_match:
            subway_station = subway_station_match.group(1).strip()
            subway_station = subway_station.upper()

            # 해당 지하철역 이름을 정확히 일치하는 행 필터링
            filtered_df = df[df['SUBWAY_NM'].str.upper() == subway_station]
            if not filtered_df.empty:
                # 데이터프레임 정보를 텍스트로 변환
                df_text = filtered_df.to_string()

                # GPT 모델을 사용하여 데이터 요약 요청
                gpt_prompt = f"다음은 {subway_station} 인근의 기업들에 대한 정보입니다:\n{df_text}\n\n이 정보를 간략하게 요약해주세요."
                for gpt_response in openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "user", "content": prompt},
                            {"role": "assistant", "content": gpt_prompt},
                    ],
                    stream=True,
                ):
                    
                    summary = gpt_response.choices[0].delta.content
                    if summary is not None:
                        full_response += summary
                    message_placeholder.markdown(full_response + "▌")
            else:
                full_response += f"{subway_station} 인근에 있는 기업 정보가 없습니다."
        else:
            for response in openai.chat.completions.create(
                model = st.session_state["openai_model"],
                messages=[
                    {"role":m["role"],"content":m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                
                con = response.choices[0].delta.content
                if con is not None:
                    full_response += con
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    information = full_response
###################################################################################################
    
st.divider()
st.subheader("📑챗봇으로 제공된 기업의 추천 자소서를 제공 해주는 서비스입니다.")

if information:
    if subway_station_match:
        # GPT 모델을 사용하여 자기소개서 초안 요청
        personal_info_prompt = f"위의 요약된 {information}를 바탕으로 자기소개서를 작성해주세요. 포함될 내용은 다음과 같습니다:\n"

        gpt_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": personal_info_prompt},
                    {"role": "assistant", "content": personal_info_prompt},
            ]
        )
            # 여기도 수정합니다
        personal_info_summary = gpt_response.choices[0].message.content
        
        st.write("자소서 추천")
        st.write(personal_info_summary)
        st.info(
            "사용자님께서 입력하신 정보를 바탕으로 기업을 추천하고 추천 기업에 대한 참고 자소서를 제공해드렸습니다.",
            icon="ℹ️",
        )

    else:
        st.write("아직 기업의 정보가 입력되지 않았습니다.")
        st.info(
            "아직 자소서가 없습니다.",
            icon="ℹ️",
        )
else:
    st.write("아직 기업의 정보가 입력되지 않았습니다.")
    st.info(
            "아직 자소서가 없습니다.",
            icon="ℹ️",
        )

