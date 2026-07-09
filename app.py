import streamlit as st
import random

# 타로 카드 데이터 (이름, 이미지 URL, 정방향 의미, 역방향 의미)
tarot_cards = [
    {
        "name": "The Fool (바보)",
        "img": "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg",
        "up": "새로운 시작과 모험이 기다립니다.",
        "down": "무모한 행동은 잠시 멈추고 신중하세요."
    },
    {
        "name": "The Magician (마법사)",
        "img": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
        "up": "당신의 재능으로 원하는 것을 이룰 수 있어요.",
        "down": "자신감이 부족하거나 기회를 놓칠 수 있습니다."
    },
    {
        "name": "The High Priestess (여사제)",
        "img": "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg",
        "up": "직관을 믿으면 좋은 답을 찾습니다.",
        "down": "숨겨진 진실에 주의가 필요합니다."
    },
    {
        "name": "The Empress (여황제)",
        "img": "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg",
        "up": "풍요와 사랑, 안정이 함께합니다.",
        "down": "자신을 돌보는 시간이 필요합니다."
    },
    {
        "name": "The Emperor (황제)",
        "img": "https://upload.wikimedia.org/wikipedia/commons/c/c3/RWS_Tarot_04_Emperor.jpg",
        "up": "리더십과 안정된 성취가 있습니다.",
        "down": "지나친 고집은 조심하세요."
    },
    {
        "name": "The Lovers (연인)",
        "img": "https://upload.wikimedia.org/wikipedia/commons/3/3a/TheLovers.jpg",
        "up": "좋은 인연과 조화로운 관계가 기대됩니다.",
        "down": "선택 앞에서 신중해야 합니다."
    },
    {
        "name": "The Wheel of Fortune (운명의 수레바퀴)",
        "img": "https://upload.wikimedia.org/wikipedia/commons/3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg",
        "up": "행운의 변화가 찾아옵니다.",
        "down": "예상치 못한 변수에 유연하게 대처하세요."
    },
    {
        "name": "The Star (별)",
        "img": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_17_Star.jpg",
        "up": "희망과 영감이 가득한 날입니다.",
        "down": "잠시 실망할 수 있지만 곧 회복됩니다."
    },
    {
        "name": "The Sun (태양)",
        "img": "https://upload.wikimedia.org/wikipedia/commons/1/17/RWS_Tarot_19_Sun.jpg",
        "up": "성공과 기쁨이 함께합니다!",
        "down": "작은 오해가 생길 수 있으니 주의하세요."
    },
    {
        "name": "The World (세계)",
        "img": "https://upload.wikimedia.org/wikipedia/commons/f/ff/RWS_Tarot_21_World.jpg",
        "up": "목표를 이루고 완성하는 날입니다.",
        "down": "마무리에 조금 더 신경 쓰세요."
    },
]

# 카드 뒷면 이미지 URL
card_back = "https://upload.wikimedia.org/wikipedia/commons/9/9b/Tarot_card_back.jpg"

# ---------------- 앱 화면 ----------------
st.title("🔮 오늘의 타로 운세")
st.write("마음속으로 질문을 떠올리고, 카드를 뽑아보세요!")

# 사용자 이름 입력
name = st.text_input("이름을 입력하세요")

# 스프레드 선택
mode = st.radio("운세 방식을 선택하세요", ["원 카드 (오늘의 운세)", "쓰리 카드 (과거·현재·미래)"])

# 버튼 클릭
if st.button("🃏 카드 뽑기"):
    if name.strip() == "":
        st.warning("이름을 먼저 입력해주세요!")
    else:
        st.subheader(f"✨ {name}님의 타로 결과 ✨")

        if mode == "원 카드 (오늘의 운세)":
            card = random.choice(tarot_cards)
            direction = random.choice(["정방향", "역방향"])

            st.image(card["img"], width=250, caption=card["name"])
            st.write(f"**방향: {direction}**")
            if direction == "정방향":
                st.success(card["up"])
            else:
                st.info(card["down"])
            st.balloons()

        else:  # 쓰리 카드
            # 중복 없이 3장 뽑기
            picked = random.sample(tarot_cards, 3)
            positions = ["과거", "현재", "미래"]

            cols = st.columns(3)  # 3칸으로 나누기
            for i in range(3):
                card = picked[i]
                direction = random.choice(["정방향", "역방향"])
                with cols[i]:
                    st.markdown(f"### {positions[i]}")
                    st.image(card["img"], width=180, caption=card["name"])
                    st.write(f"**{direction}**")
                    if direction == "정방향":
                        st.success(card["up"])
                    else:
                        st.info(card["down"])
            st.balloons()
