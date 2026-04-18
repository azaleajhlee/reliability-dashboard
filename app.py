# app.py (서버/클라우드에서 실행될 대시보드 코드)
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 웹 페이지 기본 설정
st.set_page_config(page_title="신뢰성 데이터 대시보드", layout="wide")
st.title("📊 시험결과 데이터 시각화 Dashboard")

# CSV 파일 읽기
data_path = './data/test_result.csv'

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    
    st.subheader("1. 데이터 미리보기")
    st.dataframe(df.head(10)) # 데이터 표 출력
    
    st.subheader("2. y = x^2 분석 그래프")
    # Plotly를 이용한 반응형 그래프 생성
    fig = px.line(df, x='x', y='y', title='y = x^2 Graph', markers=True)
    fig.update_layout(height=600)
    
    # 그래프를 대시보드에 렌더링
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error(f"데이터 파일을 찾을 수 없습니다: {data_path}")
    st.info("로컬 PC에서 CSV 파일이 정상적으로 전송되었는지 확인해주세요.")