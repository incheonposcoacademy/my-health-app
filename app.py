import streamlit as st
import pandas as pd

# 1. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    file_path = '창의적 문제 해결 데이터 수집.xlsx'
    df = pd.read_excel(file_path)
    
    # '건강상태' 열의 결측치를 위에서 아래로 채움 (엑셀 병합 셀 대응)
    df['건강상태'] = df['건강상태'].ffill()
    
    # 사용자 친화적인 증상 매핑 (딕셔너리)
    friendly_names = {
        "수면": "😴 잠이 잘 안 오고 밤에 자주 깨요 (수면 개선)",
        "피로": "🔋 자도 자도 피곤하고 기운이 없어요 (피로 회복)",
        "눈": "👀 눈이 침침하고 건조해요 (눈 건강)",
        "혈당": "🩸 혈당 조절이 안돼고 당뇨병이 있어요",
        "장건강": "🍽️ 속이 더부룩하고 소화가 잘 안 돼요 (장건강)",
        "면역": "🛡️ 환절기만 되면 감기에 잘 걸려요 (면역력 증진)",
        "뼈/관절": "🦴골다공증이 있고 관절에 잦은 통증이 있어요 (관절건강)",
        "피부": "☹피부가 건조하고 퍽퍽해요(피부 건강 개선)",
        "심혈관계 질환": "🩸만성 심혈관계질환이 있어요"
    }
    
    # 매핑되지 않은 상태는 원본 그대로 유지
    df['사용자증상'] = df['건강상태'].map(lambda x: friendly_names.get(x, x))
    return df

try:
    df = load_data()

    # 2. 웹사이트 레이아웃 설정
    st.set_page_config(page_title="맞춤 영양제 추천 서비스", page_icon="💊")
    st.title("💊 나에게 딱 맞는 건강기능식품 찾기")
    st.write("현재 겪고 계신 증상을 선택하시면 최적의 영양제를 추천해 드립니다.")

    # 3. 사용자 입력 (증상 선택)
    symptoms = df['사용자증상'].unique()
    selected_symptom = st.selectbox("어디가 불편하신가요?", symptoms)

    # 4. 결과 필터링
    recommendations = df[df['사용자증상'] == selected_symptom]

    if not recommendations.empty:
        st.subheader(f"✅ '{selected_symptom.split('(')[0].strip()}'에 도움을 줄 수 있는 성분입니다.")
        
        # 추천 리스트 출력
        for index, row in recommendations.iterrows():
            with st.container():
                st.markdown(f"### 🧪 추천 성분: {row['섭취해야하는 성분']}")
                st.info(f"💡 **성분 정보:** {row['성분 정보']}")
                
                # 버튼을 누르면 상세 정보 표시
                with st.expander(f"🔍 '{row['섭취해야하는 성분']}' 함유 제품 및 상세 주의사항 보기"):
                    st.write(f"🏠 **추천 상품:** {row['성분을 포함하고 있는 건강기능식품']}")
                    st.write(f"🥄 **섭취 방법:** {row.get('섭취 방법', '정보 없음')}")
                    
                    # 의약품 병용 주의사항 (컬럼명이 길어 인덱스로 접근하거나 긴 이름 그대로 사용)
                    med_col = '같이 섭취하면 안되는 의약품\nhttps://data.mfds.go.kr/hid/opeab01/drugUsjntIntkAttnMttrDtl.do'
                    st.warning(f"⚠️ **같이 섭취하면 안 되는 의약품:**\n{row.get(med_col, '특이사항 없음')}")
                    
                    st.error(f"❗ **섭취 시 주의사항:**\n{row.get('주의사항', '정보 없음')}")
                st.divider()
    else:
        st.write("해당 증상에 대한 데이터를 찾을 수 없습니다.")

except Exception as e:
    st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
    st.info("'창의적 문제 해결 데이터 수집.xlsx' 파일이 코드와 같은 폴더에 있는지 확인해주세요.")