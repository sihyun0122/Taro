import streamlit as st
import random

# ---------------- 페이지 기본 설정 ----------------
st.set_page_config(page_title="🔮 신비의 타로", page_icon="🔮", layout="centered")

# ---------------- CSS 디자인 (신비로운 분위기) ----------------
st.markdown("""
    <style>
    /* 전체 배경 - 보라빛 밤하늘 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #1a0033 0%, #2d1b4e 50%, #0d001a 100%);
        color: #f0e6ff;
    }
    /* 제목 스타일 */
    h1, h2, h3 {
        color: #ffd700 !important;
        text-align: center;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    /* 일반 글씨 */
    p, label, .stMarkdown {
        color: #e6d9ff !important;
    }
    /* 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(90deg, #8e2de2, #4a00e0);
        color: white;
        border: 2px solid #ffd700;
        border-radius: 25px;
        padding: 10px 30px;
        font-size: 18px;
        font-weight: bold;
        display: block;
        margin: 0 auto;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ffd700, #ff8c00);
        color: #1a0033;
        transform: scale(1.05);
    }
    /* 카드 이미지 테두리 */
    .stImage img {
        border-radius: 15px;
        border: 3px solid #ffd700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- 타로 카드 데이터 (메이저 아르카나 22장) ----------------
tarot_cards = [
    {"name": "0. The Fool (바보)", "img": "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg",
     "up": "새로운 시작과 모험이 기다립니다.", "down": "무모한 행동은 잠시 멈추고 신중하세요."},
    {"name": "1. The Magician (마법사)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
     "up": "당신의 재능으로 원하는 것을 이룰 수 있어요.", "down": "자신감이 부족하거나 기회를 놓칠 수 있습니다."},
    {"name": "2. The High Priestess (여사제)", "img": "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg",
     "up": "직관을 믿으면 좋은 답을 찾습니다.", "down": "숨겨진 진실에 주의가 필요합니다."},
    {"name": "3. The Empress (여황제)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg",
     "up": "풍요와 사랑, 안정이 함께합니다.", "down": "자신을 돌보는 시간이 필요합니다."},
    {"name": "4. The Emperor (황제)", "img": "https://upload.wikimedia.org/wikipedia/commons/c/c3/RWS_Tarot_04_Emperor.jpg",
     "up": "리더십과 안정된 성취가 있습니다.", "down": "지나친 고집은 조심하세요."},
    {"name": "5. The Hierophant (교황)", "img": "https://upload.wikimedia.org/wikipedia/commons/8/8d/RWS_Tarot_05_Hierophant.jpg",
     "up": "전통과 배움에서 좋은 조언을 얻습니다.", "down": "관습에 얽매이지 말고 자신만의 길을 찾으세요."},
    {"name": "6. The Lovers (연인)", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3a/TheLovers.jpg",
     "up": "좋은 인연과 조화로운 관계가 기대됩니다.", "down": "선택 앞에서 신중해야 합니다."},
    {"name": "7. The Chariot (전차)", "img": "https://upload.wikimedia.org/wikipedia/commons/9/9b/RWS_Tarot_07_Chariot.jpg",
     "up": "의지와 추진력으로 승리합니다.", "down": "방향을 잃지 않도록 집중하세요."},
    {"name": "8. Strength (힘)", "img": "https://upload.wikimedia.org/wikipedia/commons/f/f5/RWS_Tarot_08_Strength.jpg",
     "up": "용기와 인내가 좋은 결과를 만듭니다.", "down": "자신감을 잃지 않도록 하세요."},
    {"name": "9. The Hermit (은둔자)", "img": "https://upload.wikimedia.org/wikipedia/commons/4/4d/RWS_Tarot_09_Hermit.jpg",
     "up": "혼자만의 성찰이 답을 줍니다.", "down": "너무 고립되지 않도록 주의하세요."},
    {"name": "10. Wheel of Fortune (운명의 수레바퀴)", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg",
     "up": "행운의 변화가 찾아옵니다.", "down": "예상치 못한 변수에 유연하게 대처하세요."},
    {"name": "11. Justice (정의)", "img": "https://upload.wikimedia.org/wikipedia/commons/e/e0/RWS_Tarot_11_Justice.jpg",
     "up": "공정한 결과와 균형이 찾아옵니다.", "down": "편견 없이 상황을 바라보세요."},
    {"name": "12. The Hanged Man (매달린 사람)", "img": "https://upload.wikimedia.org/wikipedia/commons/2/2b/RWS_Tarot_12_Hanged_Man.jpg",
     "up": "관점을 바꾸면 새로운 답이 보입니다.", "down": "정체된 상황에서 벗어날 때입니다."},
    {"name": "13. Death (죽음)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg",
     "up": "끝은 새로운 시작을 의미합니다.", "down": "변화를 두려워하지 마세요."},
    {"name": "14. Temperance (절제)", "img": "https://upload.wikimedia.org/wikipedia/commons/f/f8/RWS_Tarot_14_Temperance.jpg",
     "up": "조화와 균형이 평안을 줍니다.", "down": "인내심을 가지고 조절하세요."},
    {"name": "15. The Devil (악마)", "img": "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg",
     "up": "욕망을 직시하고 다스릴 때입니다.", "down": "속박에서 벗어날 기회가 옵니다."},
    {"name": "16. The Tower (탑)", "img": "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg",
     "up": "갑작스러운 변화가 오지만 성장의 계기입니다.", "down": "위기를 미리 대비하세요."},
    {"name": "17. The Star (별)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_17_Star.jpg",
     "up": "희망과 영감이 가득한 날입니다.", "down": "잠시 실망할 수 있지만 곧 회복됩니다."},
    {"name": "18. The Moon (달)", "img": "https://upload.wikimedia.org/wikipedia/commons/7/7f/RWS_Tarot_18_Moon.jpg",
     "up": "직감을 믿어보세요.", "down": "불안한 마음을 다스릴 필요가 있어요."},
    {"name": "19. The Sun (태양)", "img": "https://upload.wikimedia.org/wikipedia/commons/1/17/RWS_Tarot_19_Sun.jpg",
     "up": "성공과 기쁨이 함께합니다!", "down": "작은 오해가 생길 수 있으니 주의하세요."},
    {"name": "20. Judgement (심판)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/dd/RWS_Tarot_20_Judgement.jpg",
     "up": "새로운 깨달음과 부활의 시간입니다.", "down": "과거에 너무 얽매이지 마세요."},
    {"name": "21. The World (세계)", "img": "https://upload.wikimedia.org/wikipedia/commons/f/ff/RWS_Tarot_21_World.jpg",
     "up": "목표를 이루고 완성하는 날입니다.", "down": "마무리에 조금 더 신경 쓰세요."},
]

# 카드 뒷면 이미지
card_back = "https://upload.wikimedia.org/wikipedia/commons/9/9b/Tarot_card_back.jpg"

# ---------------- 상태 저장 (세션) ----------------
# 카드가 뽑혔는지 여부를 기억하기 위해 session_state 사용
if "drawn" not in st.session_state:
    st.session_state.drawn = False
if "result" not in st.session_state:
    st.session_state.result = []

# ---------------- 화면 구성 ----------------
st.title("🔮 신비의 타로 운세 🔮")
st.markdown("<p style='text-align:center;'>마음속으로 질문을 떠올리고, 카드를 뽑아보세요 ✨</p>", unsafe_allow_html=True)

name = st.text_input("🌙 이름을 입력하세요")
mode = st.radio("🃏 운세 방식을 선택하세요", ["원 카드 (오늘의 운세)", "쓰리 카드 (과거·현재·미래)"])

# 뽑기 전: 카드 뒷면 미리 보여주기
if not st.session_state.drawn:
    num = 1 if "원 카드" in mode else 3
    cols = st.columns(num)
    for i in range(num):
        with cols[i]:
            st.image(card_back, width=160, caption="???")

# ---------------- 카드 뽑기 버튼 ----------------
if st.button("✨ 카드 뽑기 ✨"):
    if name.strip() == "":
        st.warning("🌟 이름을 먼저 입력해주세요!")
    else:
        st.session_state.drawn = True
        num = 1 if "원 카드" in mode else 3
        # 중복 없이 카드 뽑기 + 방향 정하기
        picked = random.sample(tarot_cards, num)
        st.session_state.result = [
            (card, random.choice(["정방향", "역방향"])) for card in picked
        ]

# ---------------- 결과 표시 ----------------
if st.session_state.drawn and st.session_state.result:
    st.markdown(f"<h2>✨ {name}님의 타로 결과 ✨</h2>", unsafe_allow_html=True)

    positions = ["과거", "현재", "미래"] if len(st.session_state.result) == 3 else ["오늘의 운세"]
    cols = st.columns(len(st.session_state.result))

    for i, (card, direction) in enumerate(st.session_state.result):
        with cols[i]:
            st.markdown(f"### {positions[i]}")
            st.image(card["img"], width=180, caption=card["name"])
            st.markdown(f"**🔸 {direction}**")
            if direction == "정방향":
                st.success(card["up"])
            else:
                st.info(card["down"])

    st.balloons()

    # 다시 뽑기 버튼
    if st.button("🔄 다시 뽑기"):
        st.session_state.drawn = False
        st.session_state.result = []
        st.rerun()
