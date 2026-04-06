import streamlit as st

# 페이지 설정
st.set_page_config(page_title="모임 회비 관리 계산기", page_icon="💰")

# 제목 및 설명
st.title("모임 회비 관리 계산기")
st.write("총 금액, 인원 수, 팁 비율을 입력하여 1인당 부담할 금액을 계산합니다.")

# 화면을 두 칸으로 나눕니다 (왼쪽: 입력, 오른쪽: 결과)
col_input, col_result = st.columns(2)

with col_input:
    st.subheader("입력 정보")
    # 총 금액 입력
    total_bill = st.number_input("총 금액 (원)", min_value=0, value=100000, step=1000)
    
    # 인원 수 입력
    num_people = st.number_input("인원 수 (명)", min_value=1, value=4, step=1)
    
    # 팁/서비스 비율 슬라이더
    tip_percentage = st.slider("팁/서비스 비율 (%)", min_value=0, max_value=20, value=10)

# 계산 로직
total_tip = total_bill * (tip_percentage / 100)
final_total = total_bill + total_tip
per_person = final_total / num_people

with col_result:
    st.subheader("계산 결과")
    # 결과 창 디자인 (회색 배경 느낌을 주기 위해 container 사용)
    with st.container(border=True):
        st.write("1인당 금액 (원)")
        st.title(f"{per_person:,.0f}")
        
        st.write("팁 포함 총 금액 (원)")
        st.subheader(f"{final_total:,.0f}")

# 하단 버튼 레이아웃
st.divider()
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    if st.button("Clear", use_container_width=True):
        st.rerun()

with col_btn2:
    # Streamlit은 입력값이 바뀔 때마다 실시간 계산되므로 
    # Submit 버튼은 시각적인 확인 용도로 배치합니다.
    st.button("Submit", type="primary", use_container_width=True)
