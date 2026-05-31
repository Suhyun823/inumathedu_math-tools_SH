import streamlit as st
import numpy as np
import pandas as pd

# 탭 제목 및 아이콘 설정
st.set_page_config(page_title="큰 수의 법칙", page_icon="🪙")

# 현재 페이지 상태를 저장하는 공간 (처음 들어오면 1페이지로 설정)
if 'page_number' not in st.session_state:
    st.session_state.page_number = 1

# ---------------------------------------------------------
# 1페이지: 개념 설명 및 생각 열기 질문
# ---------------------------------------------------------
if st.session_state.page_number == 1:
    st.title("🪙 동전으로 알아보는 큰 수의 법칙")
    
    st.markdown("---")
    st.subheader("📖 개념 알아보기")
    st.info(
        "어떤 시행을 여러 번 반복할 때, 특정 사건이 일어나는 **상대도수(실제 일어난 비율)**는 "
        "시행 횟수가 늘어날수록 **수학적 확률**에 가까워집니다. "
        "우리는 이것을 **큰 수의 법칙**이라고 불러요."
    )
    
    st.write(
        "가장 대표적인 예시가 바로 **동전 던지기**입니다! "
        "정상적인 동전을 던졌을 때 앞면이 나올 수학적 확률은 1/2 (0.5), "
        "뒷면이 나올 확률도 1/2 (0.5)라는 것을 이미 알고 있죠."
    )
    
    st.markdown("---")
    st.subheader("🤔 여기서 잠깐! 생각해볼 질문")
    st.warning(
        "친구가 동전을 **10번** 던졌는데 앞면이 **8번**이나 나왔습니다. "
        "친구는 *'이 동전은 앞면이 훨씬 잘 나오는 조작된 동전이야!'*라고 주장하고 있어요. "
        "친구의 주장이 맞을까요? \n\n"
        "만약 동전을 **10,000번** 던졌을 때 앞면이 **8,000번** 나왔다면 어떨까요?"
    )
    
    # 버튼을 누르면 2페이지로 이동하도록 상태 변경 후 새로고침
    if st.button("정답 확인 및 시뮬레이션 하러 가기 🚀"):
        st.session_state.page_number = 2
        st.rerun()

# ---------------------------------------------------------
# 2페이지: 정답 해설 및 시뮬레이션
# ---------------------------------------------------------
elif st.session_state.page_number == 2:
    st.title("📊 시뮬레이션으로 확인하기")
    
    st.subheader("💡 질문에 대한 정답")
    st.success(
        "동전을 10번 던져서 앞면이 8번(80%) 나오는 것은 우연히 일어날 수 있는 일입니다. "
        "하지만 시행 횟수가 10,000번처럼 충분히 커지면, 앞면이 나올 비율은 반드시 1/2 (50%)에 가까워져야 해요. "
        "따라서 10,000번 던졌는데 8,000번이 나왔다면 그 동전은 정말 조작됐을 가능성이 매우 높습니다!"
    )
    
    st.markdown("---")
    st.subheader("🎲 직접 해보는 동전 던지기 실험")
    st.write("슬라이더를 움직여 동전을 몇 번 던질지 정하고 실험을 시작해 보세요!")
    
    # 시행 횟수 설정 슬라이더
    trials = st.slider("동전 던지기 횟수", min_value=10, max_value=5000, value=100, step=10)
    
    if st.button("실험 시작!"):
        # 0: 앞면, 1: 뒷면으로 가정하고 무작위 추출
        flips = np.random.randint(0, 2, size=trials)
        
        # 앞면(0)이 나온 경우만 1로 변환하여 카운트
        heads = (flips == 0).astype(int)
        
        # 누적 앞면 횟수 계산
        cumulative_heads = np.cumsum(heads)
        
        # 1부터 trials까지의 시행 횟수 배열
        trial_numbers = np.arange(1, trials + 1)
        
        # 단계별 상대도수 (누적 앞면 횟수 / 현재 시행 횟수)
        relative_frequencies = cumulative_heads / trial_numbers
        
        # 그래프를 그리기 위한 데이터 정리
        chart_data = pd.DataFrame({
            "시행 횟수": trial_numbers,
            "상대도수 (앞면)": relative_frequencies,
            "수학적 확률 (1/2)": 0.5
        })
        
        st.line_chart(chart_data, x="시행 횟수", y=["상대도수 (앞면)", "수학적 확률 (1/2)"])
        
        final_rate = relative_frequencies[-1]
        st.write(
            f"**총 {trials}번** 던진 결과, 앞면이 나온 상대도수는 **{final_rate:.4f}**로 "
            "수학적 확률인 0.5에 가까워진 것을 볼 수 있습니다."
        )
    
    st.markdown("---")
    # 버튼을 누르면 다시 1페이지로 돌아가도록 상태 변경 후 새로고침
    if st.button("⬅️ 개념 페이지로 돌아가기"):
        st.session_state.page_number = 1
        st.rerun()
