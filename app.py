import streamlit as st
import pandas as pd
import plotly.express as px


def upload_data_file():
    # 메인 화면에 파일 업로드 기능 배치
    return st.file_uploader("CSV 파일 업로드", type=["csv"])


def create_sidebar_controls(dataframe):
    # 이미지와 동일한 형태의 사이드바 UI 구성
    st.sidebar.markdown("**산점도 대상 컬럼 선택 🔗**")

    columns = dataframe.columns.tolist()

    # 편의를 위해 지정된 컬럼명 존재 시 기본값으로 설정, 없으면 첫 번째 컬럼 선택
    idx_study = columns.index("공부시간") if "공부시간" in columns else 0
    idx_score = columns.index("점수") if "점수" in columns else 0
    idx_major = columns.index("전공") if "전공" in columns else 0

    x_col = st.sidebar.selectbox("X축(설명 변수)", columns, index=idx_study)
    y_col = st.sidebar.selectbox("Y축(반응 변수)", columns, index=idx_score)
    color_col = st.sidebar.selectbox("색상으로 구분할 범주 컬럼 (선택)", columns, index=idx_major)
    show_trend = st.sidebar.checkbox("추세선(회귀선) 표시", value=True)

    return x_col, y_col, color_col, show_trend


def draw_scatter_plot(dataframe, x_col, y_col, color_col, show_trend):
    # Plotly를 이용한 산점도 생성 (웹 브라우저 폰트를 사용하여 한글 깨짐 방지)
    # 추세선 체크 여부에 따라 ordinary least squares(ols) 방식 회귀선 추가
    trendline_option = "ols" if show_trend else None

    try:
        fig = px.scatter(
            dataframe,
            x=x_col,
            y=y_col,
            color=color_col,
            trendline=trendline_option,
            title=f"{x_col}와(과) {y_col}의 관계 (Scatter Plot)"
        )
        # 그래프 영역이 화면에 꽉 차도록 설정
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"그래프 생성 오류: {e}")
        st.info("터미널에 'pip install statsmodels'를 입력하여 추세선 분석 라이브러리를 설치해주세요.")


def main():
    st.title("데이터 산점도 분석 프로그램")

    # 1. 파일 업로드
    uploaded_file = upload_data_file()

    if uploaded_file is not None:
        # 2. 데이터 확인
        dataframe = pd.read_csv(uploaded_file)
        st.write("원본 데이터 미리보기")
        st.dataframe(dataframe.head())

        # 3. 비교 항목(컬럼) 선택
        x_col, y_col, color_col, show_trend = create_sidebar_controls(dataframe)

        # 4. 그래프 시각화
        draw_scatter_plot(dataframe, x_col, y_col, color_col, show_trend)


if __name__ == "__main__":
    main()