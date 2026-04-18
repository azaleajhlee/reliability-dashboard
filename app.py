import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 이 코드는 data 폴더 안에 있는 모든 CSV 파일을 자동으로 찾아내어 사용자가 선택할 수 있는 메뉴를 만들어 줌
# 페이지 설정
st.set_page_config(page_title="주차별 신뢰성 데이터 분석", layout="wide")
st.title("📅 주차별 시험 결과 비교 대시보드")

# 1. 데이터 폴더 내 파일 목록 가져오기 함수
# os.listdir(): data 폴더에 파일을 추가하기만 하면 코드를 수정하지 않아도 대시보드에 자동으로 새로운 주차 메뉴 생성
def get_csv_files(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 파일명에 'test_result'가 포함된 csv 파일만 추출
    return [f for f in os.listdir(directory) if f.endswith('.csv')]

# 2. 데이터 로드 함수 (캐싱 적용: 100MB 파일을 매번 읽지 않도록 메모리에 저장)
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    # 시계열 데이터라면 여기서 날짜형 변환 등을 수행할 수 있습니다.
    return df

# 사이드바: 파일 선택 메뉴
data_dir = './data'
file_list = get_csv_files(data_dir)

if file_list:
    st.sidebar.header("📂 데이터 선택")
    # 파일 목록을 내림차순으로 정렬 (최신 주차가 위로 오게)
    selected_file = st.sidebar.selectbox(
        "분석할 시험 주차를 선택하세요",
        sorted(file_list, reverse=True)
    )

    # 선택된 파일의 전체 경로
    target_path = os.path.join(data_dir, selected_file)
    
    # 데이터 로드
    with st.spinner('대용량 데이터를 분석 중입니다...'):
        df = load_data(target_path)

    # 화면 구성 (2개 컬럼)
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("📋 데이터 요약")
        st.write(f"**선택된 파일:** {selected_file}")
        st.write(f"**전체 데이터 수:** {len(df):,} 개")
        st.write("**데이터 샘플 (상위 5행)**")
        st.dataframe(df.head(5))

    with col2:
        st.subheader("📈 시각화 분석")
        # 컬럼 선택 (x축, y축)
        cols = df.columns.tolist()
        x_axis = st.selectbox("X축 선택", cols, index=0)
        y_axis = st.selectbox("Y축 선택", cols, index=1 if len(cols)>1 else 0)

        # 그래프 생성
        fig = px.line(df, x=x_axis, y=y_axis, title=f"{selected_file} - {y_axis} 추이", markers=True)
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("`./data` 폴더에 CSV 파일이 없습니다. 파일을 업로드해주세요.")