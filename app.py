import streamlit as st
import numpy as np
import pandas as pd

# 탭 제목 및 아이콘 설정
st.set_page_config(page_title="큰 수의 법칙", page_icon="🎲")

# 현재 페이지 상태를 저장하는 공간
if 'page_number' not in st.session_state:
    st.session_state.page_number = 1

# ---------------------------------------------------------
# 1페이지: 개념 깊이 알아보기 및 생각 열기 질문
# ---------------------------------------------------------
if st.session_state.page_number == 1:
    st.title("🎲 시뮬레이션으로 만나는 큰 수의 법칙")
    
    st.markdown("---")
    st.subheader("📖 개념 깊이 알아보기")
    
    st.info(
        "우리는 주사위를 던졌을 때 특정 눈이 나올 확률이 **1/6** 이라는 것을 알고 있습니다. "
        "이처럼 머릿속으로 계산해 낸 이상적인 확률을 **'수학적 확률'**이라고 합니다.\n\n"
        "하지만 실제로 주사위를 6번 던진다고 해서 무조건 원하는 눈이 딱 1번만 나올까요? "
        "직접 실험해서 얻어낸 결과를 **'통계적 확률(상대도수)'**이라고 합니다. "
        "처음에는 이 둘이 서로 달라서 당황스러울 수 있어요."
    )
    
    st.success(
        "**💡 큰 수의 법칙이란?**\n\n"
        "실험을 하는 횟수(시행 횟수)를 100번, 1,000번, 10,000번으로 계속 늘려가면 어떻게 될까요? "
        "놀랍게도 우리가 직접 구한 **통계적 확률**이 이론적인 **수학적 확률**에 점점 가까워집니다. "
        "이것이 바로 확률과 통계에서 아주 중요한 **큰 수의 법칙**입니다!"
    )
    
    st.markdown("---")
    st.subheader("🤔 여기서 잠깐! 생각해볼 질문")
    st.warning(
        "친구가 동전을 **10번** 던졌는데 앞면이 **8번**이나 나왔습니다. "
        "친구는 *'이 동전은 앞면이 훨씬 잘 나오는 조작된 동전이야!'*라고 주장하고 있어요. "
        "친구의 주장이 맞을까요? \n\n"
        "만약 동전을 **10,000번** 던졌을 때 앞면이 **8,000번** 나왔다면 어떨까요?"
    )
    
    if st.button("정답 확인 및 시뮬레이션 하러 가기 🚀"):
        st.session_state.page_number = 2
        st.rerun()

# ---------------------------------------------------------
# 2페이지: 정답 해설 및 다양한 시뮬레이션
# ---------------------------------------------------------
elif st.session_state.page_number == 2:
    st.title("📊 직접 실험해보기")
    
    st.subheader("💡 질문에 대한 정답")
    st.write(
        "동전을 10번 던져서 앞면이 8번(80%) 나오는 것은 시행 횟수가 적어 우연히 일어날 수 있는 일입니다. "
        "하지만 10,000번처럼 횟수가 충분히 커지면 큰 수의 법칙에 의해 반드시 1/2 (50%)에 가까워져야 해요. "
        "따라서 10,000번 중 8,000번이 나왔다면 그 동전은 정말 조작됐을 가능성이 매우 높습니다!"
    )
    
    st.markdown("---")
    st.subheader("🎲 어떤 실험을 해볼까요?")
    
    exp_type = st.radio(
        "실험 도구를 선택해주세요.", 
        [
            "🪙 동전 던지기 (앞면이 나올 확률)", 
            "🎲 주사위 던지기 (숫자 1이 나올 확률)",
            "🌀 4색 팽이 돌리기 (빨간 면에 멈출 확률)"
        ]
    )
    
    if "동전" in exp_type:
        target_prob = 1/2
        prob_text = "1/2 (0.5)"
    elif "주사위" in exp_type:
        target_prob = 1/6
        prob_text = "1/6 (약 0.1667)"
    else:
        target_prob = 1/4
        prob_text = "1/4 (0.25)"

st.markdown("---")
    st.subheader("🤔 나의 예상 확률은?")
    
    # 1. 숫자 대신 텍스트로 입력받기 (분수, 소수 모두 가능)
    user_guess_str = st.text_input(
        "실험을 시작하기 전에, 이 사건이 일어날 확률을 입력해보세요! (예: 1/6, 1/2 또는 0.5)", 
        value="1/2"
    )
    
    # 2. 입력받은 글자를 컴퓨터가 계산할 수 있는 소수로 변환하는 과정
    user_guess = None
    try:
        if "/" in user_guess_str:
            num, denom = user_guess_str.split("/")
            user_guess = float(num) / float(denom)
        else:
            user_guess = float(user_guess_str)
            
        # 확률이 0과 1 사이가 아니면 에러 처리
        if not (0.0 <= user_guess <= 1.0):
            user_guess = None
    except:
        pass # 이상한 글자를 치면 user_guess는 계속 None 상태로 남음

    st.markdown("---")
    st.subheader("🚀 시뮬레이션 설정")
    trials = st.number_input(
        "몇 번 실험할까요? (최대 100만 번!)", 
        min_value=10, max_value=1000000, value=1000, step=100
    )
    
    # 3. 제대로 된 확률이 입력되었을 때만 실험 시작 버튼 활성화
    if user_guess is None:
        st.error("⚠️ 올바른 확률 값(0~1 사이의 소수 또는 분수)을 입력해주세요! (예: 1/6, 0.25)")
    else:
        if st.button("실험 시작!"):
            with st.spinner('열심히 시뮬레이션을 돌리는 중입니다...'):
                if "동전" in exp_type:
                    results = np.random.randint(0, 2, size=trials) 
                    success = (results == 0).astype(int) 
                elif "주사위" in exp_type:
                    results = np.random.randint(1, 7, size=trials) 
                    success = (results == 1).astype(int) 
                else:
                    results = np.random.randint(1, 5, size=trials)
                    success = (results == 1).astype(int)
                    
                cumulative_success = np.cumsum(success)
                trial_numbers = np.arange(1, trials + 1)
                relative_frequencies = cumulative_success / trial_numbers
                
                chart_data = pd.DataFrame({
                    "시행 횟수": trial_numbers,
                    "상대도수 (실제 결과)": relative_frequencies,
                    f"수학적 확률 ({frac_text})": target_prob,
                    "나의 예상 확률": user_guess
                })
                
                st.line_chart(
                    chart_data, 
                    x="시행 횟수", 
                    y=["상대도수 (실제 결과)", f"수학적 확률 ({frac_text})", "나의 예상 확률"]
                )
                
                final_rate = relative_frequencies[-1]
                st.success(
                    f"**총 {trials:,}번** 실험 완료! \n\n"
                    f"👉 **나의 예상:** {user_guess_str} (약 {user_guess:.4f}) \n"
                    f"👉 **실제 상대도수:** {final_rate:.4f} \n"
                    f"👉 **수학적 확률:** {frac_text} (약 {target_prob:.4f})"
                )
                
                st.info(
                    f"💡 **선생님의 꿀팁: 엄청 많이 던졌는데 왜 정확히 {frac_text}이 아닐까요?**\n\n"
                    f"수학적 확률인 **{frac_text}**은 주사위나 동전의 모양이 완벽하게 대칭이라는 가정하에 계산된 '이상적인 정답'이에요. "
                    "하지만 실제 실험에서는 늘 '우연'이 작용하죠. "
                    f"10,000번이 엄청 큰 숫자 같지만 무한대에 비하면 여전히 작은 숫자이기 때문에, {final_rate:.4f}처럼 미세한 오차가 남는 거랍니다. "
                    f"중요한 건, 횟수를 계속 늘려갈수록 이 우연의 오차들이 서로 깎여나가면서 결국 수학적 확률({frac_text})에 한없이 가까워진다는 사실이에요!"
                )
                
    st.markdown("---")
    if st.button("⬅️ 개념 페이지로 돌아가기"):
        st.session_state.page_number = 1
        st.rerun()
