import streamlit as st
import random

# --- 페이지 설정 ---
st.set_page_config(page_title="가위바위보 게임", page_icon="🎮")

# --- 세션 상태 초기화 (전적 저장용) ---
if 'win' not in st.session_state:
    st.session_state.win = 0
if 'lose' not in st.session_state:
    st.session_state.lose = 0
if 'draw' not in st.session_state:
    st.session_state.draw = 0
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""
if 'battle_info' not in st.session_state:
    st.session_state.battle_info = "게임을 시작합니다!"


# --- 함수 정의 ---
def play(user_choice):
    options = ['Rock', 'Paper', 'Scissors']
    computer_choice = random.choice(options)

    # 치트키 로직 (Streamlit 사이드바에 배치 예정)
    if st.session_state.get('cheat_mode'):
        st.toast(f"🤫 컴퓨터의 선택은 {computer_choice}였습니다!")

    # 승패 판정
    if user_choice == computer_choice:
        st.session_state.last_result = "비겼습니다! 😐"
        st.session_state.draw += 1
    elif (user_choice == 'Scissors' and computer_choice == 'Paper') or \
            (user_choice == 'Rock' and computer_choice == 'Scissors') or \
            (user_choice == 'Paper' and computer_choice == 'Rock'):
        st.session_state.last_result = "당신이 이겼습니다! 😊"
        st.session_state.win += 1
    else:
        st.session_state.last_result = "당신이 졌습니다... 😭"
        st.session_state.lose += 1

    st.session_state.battle_info = f"나: {user_choice} vs 컴퓨터: {computer_choice}"


def reset_game():
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.draw = 0
    st.session_state.last_result = ""
    st.session_state.battle_info = "게임을 시작합니다!"


# --- UI 레이아웃 ---
st.title("✊✌️🖐️ 가위바위보 게임")

# 사이드바 설정 (치트키 및 설정)
with st.sidebar:
    st.header("설정")
    st.session_state.cheat_mode = st.checkbox("컴퓨터 패 미리보기 (치트키)")
    st.divider()
    if st.button("전적 초기화 (Reset)", on_click=reset_game):
        st.rerun()

# 전적 표시 (상단 대시보드)
col1, col2, col3 = st.columns(3)
col1.metric("승리", f"{st.session_state.win}회")
col2.metric("패배", f"{st.session_state.lose}회")
col3.metric("무승부", f"{st.session_state.draw}회")

st.divider()

# 사용자 선택 버튼
st.subheader("당신의 선택은?")
c1, c2, c3 = st.columns(3)
if c1.button("가위 (Scissors)", use_container_width=True):
    play("Scissors")
if c2.button("바위 (Rock)", use_container_width=True):
    play("Rock")
if c3.button("보 (Paper)", use_container_width=True):
    play("Paper")

# 결과 화면
st.write(f"### {st.session_state.battle_info}")
if st.session_state.last_result:
    if "이겼습니다" in st.session_state.last_result:
        st.success(st.session_state.last_result)
    elif "졌습니다" in st.session_state.last_result:
        st.error(st.session_state.last_result)
    else:
        st.info(st.session_state.last_result)

# 자동 대결 영역
st.divider()
st.subheader("연속 자동 대결")
count = st.radio("대결 횟수 선택", ["3", "5", "10"], horizontal=True)
if st.button(f"{count}회 자동 대결 시작"):
    options = ['Rock', 'Paper', 'Scissors']
    for _ in range(int(count)):
        play(random.choice(options))
    st.rerun()