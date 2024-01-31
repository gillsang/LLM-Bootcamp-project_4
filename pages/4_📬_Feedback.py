import streamlit as st
import pandas as pd
import os
from io import BytesIO
import base64  # base64 모듈 추가
import openpyxl

# 페이지 설정
st.set_page_config(
    page_title="취업의신 사용자 피드백",
      page_icon="📝",
      layout="centered",
)

# 피드백 양식 제목
st.title("📬 사용자 피드백")

# 피드백 양식 설명
st.write("👋 여러분의 소중한 의견을 들려주세요. 저희 서비스 개선에 큰 도움이 됩니다!")

# 피드백 양식 입력 필드
with st.form(key='feedback_form'):
    name = st.text_input("👤 이름")
    email = st.text_input("📧 이메일")
    feedback = st.text_area("💬 피드백")
    submit_button = st.form_submit_button('📤 제출하기')

# 엑셀 파일 경로
excel_file = 'user_feedback.xlsx'

# 기존 데이터를 불러오거나 새로운 DataFrame을 초기화하는 함수
def load_feedback_data(file_path):
    if os.path.exists(file_path):
        return pd.read_excel(file_path, engine='openpyxl')
    else:
        return pd.DataFrame(columns=["Name", "Email", "Feedback"])

# 기존 데이터 불러오기
feedback_data = load_feedback_data(excel_file)

# 제출 버튼이 클릭되었을 때의 동작
if submit_button:
     # 새로운 피드백을 DataFrame에 추가
    new_feedback = pd.DataFrame([{"Name": name, "Email": email, "Feedback": feedback}])
    feedback_data = pd.concat([feedback_data, new_feedback], ignore_index=True)

    # 업데이트된 DataFrame을 엑셀 파일로 저장
    feedback_data.to_excel(excel_file, index=False, engine='openpyxl')
    
    # 사용자에게 피드백이 제출되었음을 알림
    st.success("🎉 피드백이 성공적으로 제출되었습니다. 감사합니다!")

# 추가적인 내용이나 안내사항
st.info("🔒 여러분의 개인정보는 안전하게 보호됩니다.")

# 관리자 비밀번호 설정
admin_password = "991224"

# 비밀번호 입력 필드와 메시지를 숨기기 위한 상태 변수
if 'show_password_input' not in st.session_state:
    st.session_state['show_password_input'] = False

# "피드백 다운로드" 버튼
if st.button('피드백 다운로드'):
    st.session_state['show_password_input'] = True

# 비밀번호 입력 필드와 메시지 표시
if st.session_state['show_password_input']:
    st.write("⚠️ 피드백 다운로드는 관리자만 접근 가능합니다.")
    input_password = st.text_input("비밀번호를 입력하세요", type="password")

    # 비밀번호 검증
    if input_password:
        if input_password == admin_password:
            # 파일을 메모리에 저장

            with open(excel_file, "rb") as file:
                towrite = BytesIO()
                towrite.write(file.read())
                towrite.seek(0)
                b64 = base64.b64encode(towrite.read()).decode()
        # 성공 메시지 내에 다운로드 링크를 포함
                st.markdown(
                    f'<div style="color: green; padding: 10px; border-radius: 5px; border: 1px solid green;">'
                    f'<h4>✅ Accept! <a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{excel_file}">파일을 다운로드합니다.</a></h4>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
          st.error("❌ 잘못된 비밀번호입니다.")