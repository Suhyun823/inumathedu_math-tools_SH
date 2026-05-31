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
    
    # 1. 예시 추가: 동전, 주사위에 이어 4색 팽이 추가
    exp_type = st.radio(
        "실험 도구를 선택해주세요.", 
        [
            "🪙 동전 던지기 (앞면이 나올 확률)", 
            "🎲 주사위 던지기 (숫자 1이 나올 확률)",
            "🌀 4색 팽이 돌리기 (빨간 면에 멈출 확률)"
        ]
    )
    
    # 선택된 실험에 따른 수학적 확률 세팅
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
    # 2. 학생의 예상 확률 입력받기
    user_guess = st.number_input(
        "실험을 시작하기 전에, 이 사건이 일어날 확률을 소수(0~1 사이)로 입력해보세요!", 
        min_value=0.0, max_value=1.0, value=0.5, step=0.05
    )
    
    st.markdown("---")
    st.subheader("🚀 시뮬레이션 설정")
    # 3. 한도를 크게 늘린 시행 횟수 입력 (최대 100만 번)
    trials = st.number_input(
        "몇 번 실험할까요? (직접 숫자를 입력하세요. 최대 100만 번!)", 
        min_value=10, max_value=1000000, value=1000, step=100
    )
    
    if st.button("실험 시작!"):
        with st.spinner('열심히 시뮬레이션을 돌리는 중입니다...'):
            if "동전" in exp_type:
                results = np.random.randint(0, 2, size=trials) 
                success = (results == 0).astype(int) 
            elif "주사위" in exp_type:
                results = np.random.randint(1, 7, size=trials) 
                success = (results == 1).astype(int) 
            else:
                # 4색 팽이 (1~4 중 1을 빨간색으로 간주)
                results = np.random.randint(1, 5, size=trials)
                success = (results == 1).astype(int)
                
            cumulative_success = np.cumsum(success)
            trial_numbers = np.arange(1, trials + 1)
            relative_frequencies = cumulative_success / trial_numbers
            
            # 그래프 데이터 정리 (나의 예상 확률 선 추가!)
            chart_data = pd.DataFrame({
                "시행 횟수": trial_numbers,
                "상대도수 (실제 결과)": relative_frequencies,
                f"수학적 확률 ({prob_text})": target_prob,
                "나의 예상 확률": user_guess
            })
            
            st.line_chart(
                chart_data, 
                x="시행 횟수", 
                y=["상대도수 (실제 결과)", f"수학적 확률 ({prob_text})", "나의 예상 확률"]
            )
            
            final_rate = relative_frequencies[-1]
            st.success(
                f"**총 {trials:,}번** 실험 완료! \n\n"
                f"👉 **나의 예상:** {user_guess:.4f} \n"
                f"👉 **실제 상대도수:** {final_rate:.4f} \n"
                f"👉 **수학적 확률:** {target_prob:.4f} \n\n"
                f"그래프를 보세요! 처음에는 결과가 요동치지만, 결국 수학적 확률({prob_text})을 향해 뻗어가는 것을 확인할 수 있죠?"
            )
    
    st.markdown("---")
    if st.button("⬅️ 개념 페이지로 돌아가기"):
        st.session_state.page_number = 1
        st.rerun()
