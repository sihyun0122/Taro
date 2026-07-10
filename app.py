import streamlit as st
import random

# ---------------- 페이지 기본 설정 ----------------
st.set_page_config(page_title="🕯️ 저주받은 타로", page_icon="💀", layout="centered")

# ---------------- CSS 디자인 + 애니메이션 (공포 버전) ----------------
st.markdown("""
    <style>
    /* 전체 배경 - 핏빛 어둠 */
    .stApp {
        background: linear-gradient(135deg, #0d0000 0%, #1a0000 50%, #000000 100%);
        color: #d9c2c2;
    }
    h1, h2, h3 {
        color: #b30000 !important;
        text-align: center;
        text-shadow: 0 0 12px rgba(255, 0, 0, 0.7);
        letter-spacing: 2px;
    }
    p, label, .stMarkdown {
        color: #cfa8a8 !important;
    }
    /* 버튼 - 핏빛 */
    .stButton>button {
        background: linear-gradient(90deg, #4a0000, #800000);
        color: #e0d0d0;
        border: 2px solid #b30000;
        border-radius: 5px;
        padding: 10px 30px;
        font-size: 18px;
        font-weight: bold;
        display: block;
        margin: 0 auto;
        transition: 0.3s;
        text-shadow: 0 0 8px rgba(255,0,0,0.6);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #800000, #ff0000);
        color: #000000;
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(255, 0, 0, 0.8);
    }
    /* 카드 이미지 테두리 - 붉은 핏빛 */
    .stImage img {
        border-radius: 8px;
        border: 3px solid #800000;
        box-shadow: 0 0 25px rgba(200, 0, 0, 0.6);
        filter: brightness(0.85) contrast(1.1);
    }

    /* 뒷면 카드가 불안하게 떨리는 애니메이션 */
    @keyframes shake {
        0%   { transform: translate(0, 0) rotate(0deg); }
        25%  { transform: translate(-2px, 1px) rotate(-1deg); }
        50%  { transform: translate(2px, -1px) rotate(1deg); }
        75%  { transform: translate(-1px, 2px) rotate(-1deg); }
        100% { transform: translate(0, 0) rotate(0deg); }
    }
    /* 촛불처럼 깜빡이는 효과 */
    @keyframes flicker {
        0%, 100% { opacity: 1; }
        45%      { opacity: 0.6; }
        50%      { opacity: 0.85; }
        55%      { opacity: 0.5; }
    }
    .floating-card {
        animation: shake 0.6s ease-in-out infinite, flicker 2s infinite;
        font-size: 90px;
        text-align: center;
        border: 3px solid #800000;
        border-radius: 8px;
        padding: 25px 10px;
        background: #1a0000;
        box-shadow: 0 0 25px rgba(200, 0, 0, 0.6);
    }

    /* 결과 카드가 스멀스멀 나타나는 효과 */
    @keyframes creepIn {
        from { opacity: 0; transform: translateY(30px) scale(0.9); filter: blur(4px); }
        to   { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }
    .stImage {
        animation: creepIn 1.5s ease;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- 타로 카드 데이터 (메이저 아르카나 22장) ----------------
# ✅ 모든 URL을 위키미디어 표준 형식(RWS_Tarot_XX_이름.jpg)으로 통일했습니다.
tarot_cards = [
    {"name": "0. The Fool (바보)", "img": "https://upload.wikimedia.org/wikipedia/commons/9/90/RWS_Tarot_00_Fool.jpg",
     "up": "새로운 시작이지만... 그 끝은 아무도 모른다.", "down": "무모한 발걸음이 당신을 낭떠러지로 이끈다."},
    {"name": "1. The Magician (마법사)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg",
     "up": "당신의 재능이 어둠 속에서 깨어난다.", "down": "잘못된 주문이 당신을 삼킬 것이다."},
    {"name": "2. The High Priestess (여사제)", "img": "https://upload.wikimedia.org/wikipedia/commons/8/88/RWS_Tarot_02_High_Priestess.jpg",
     "up": "숨겨진 비밀이 당신을 부른다.", "down": "알아서는 안 될 진실이 다가온다."},
    {"name": "3. The Empress (여황제)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/d2/RWS_Tarot_03_Empress.jpg",
     "up": "풍요 뒤에 도사린 그림자를 보라.", "down": "잃어버린 것들이 밤마다 찾아온다."},
    {"name": "4. The Emperor (황제)", "img": "https://upload.wikimedia.org/wikipedia/commons/c/c3/RWS_Tarot_04_Emperor.jpg",
     "up": "차가운 권력이 당신을 지배한다.", "down": "고집이 당신을 파멸로 몰아간다."},
    {"name": "5. The Hierophant (교황)", "img": "https://upload.wikimedia.org/wikipedia/commons/8/8d/RWS_Tarot_05_Hierophant.jpg",
     "up": "오래된 규율이 당신을 옭아맨다.", "down": "금기를 어긴 자에게 벌이 내린다."},
    # ✅ 여기가 수정된 부분! TheLovers.jpg → RWS_Tarot_06_Lovers.jpg
    {"name": "6. The Lovers (연인)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_06_Lovers.jpg",
     "up": "운명의 인연... 혹은 저주받은 만남.", "down": "잘못된 선택이 파국을 부른다."},
    {"name": "7. The Chariot (전차)", "img": "https://upload.wikimedia.org/wikipedia/commons/9/9b/RWS_Tarot_07_Chariot.jpg",
     "up": "멈출 수 없는 폭주가 시작된다.", "down": "방향을 잃은 채 어둠 속을 달린다."},
    {"name": "8. Strength (힘)", "img": "https://upload.wikimedia.org/wikipedia/commons/f/f5/RWS_Tarot_08_Strength.jpg",
     "up": "짐승 같은 본능을 억누르는 밤.", "down": "내면의 괴물이 고개를 든다."},
    {"name": "9. The Hermit (은둔자)", "img": "https://upload.wikimedia.org/wikipedia/commons/4/4d/RWS_Tarot_09_Hermit.jpg",
     "up": "홀로 남겨진 자만이 진실을 본다.", "down": "끝없는 고독이 당신을 갉아먹는다."},
    {"name": "10. Wheel of Fortune (운명의 수레바퀴)", "img": "https://upload.wikimedia.org/wikipedia/commons/3/3c/RWS_Tarot_10_Wheel_of_Fortune.jpg",
     "up": "운명의 수레바퀴가 불길하게 돌아간다.", "down": "피할 수 없는 저주가 다가온다."},
    {"name": "11. Justice (정의)", "img": "https://upload.wikimedia.org/wikipedia/commons/e/e0/RWS_Tarot_11_Justice.jpg",
     "up": "심판의 저울이 당신을 가리킨다.", "down": "지난 죄가 대가를 요구한다."},
    {"name": "12. The Hanged Man (매달린 사람)", "img": "https://upload.wikimedia.org/wikipedia/commons/2/2b/RWS_Tarot_12_Hanged_Man.jpg",
     "up": "거꾸로 매달린 채 세상을 본다.", "down": "빠져나올 수 없는 정체 속에 갇힌다."},
    {"name": "13. Death (죽음)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/d7/RWS_Tarot_13_Death.jpg",
     "up": "끝이 다가온다... 무언가가 죽는다.", "down": "죽음마저 거부당한 자의 고통."},
    {"name": "14. Temperance (절제)", "img": "https://upload.wikimedia.org/wikipedia/commons/f/f8/RWS_Tarot_14_Temperance.jpg",
     "up": "위태로운 균형 위에 서 있다.", "down": "무너지는 평온, 다가오는 혼돈."},
    {"name": "15. The Devil (악마)", "img": "https://upload.wikimedia.org/wikipedia/commons/5/55/RWS_Tarot_15_Devil.jpg",
     "up": "악마가 당신의 이름을 속삭인다.", "down": "사슬에 묶인 영혼이 절규한다."},
    {"name": "16. The Tower (탑)", "img": "https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg",
     "up": "모든 것이 무너져 내리는 밤.", "down": "재앙이 예고 없이 들이닥친다."},
    {"name": "17. The Star (별)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/db/RWS_Tarot_17_Star.jpg",
     "up": "희미한 빛조차 곧 꺼질 것이다.", "down": "꺼져버린 희망, 남겨진 어둠."},
    {"name": "18. The Moon (달)", "img": "https://upload.wikimedia.org/wikipedia/commons/7/7f/RWS_Tarot_18_Moon.jpg",
     "up": "핏빛 달 아래 진실이 숨는다.", "down": "환영과 광기가 당신을 잠식한다."},
    {"name": "19. The Sun (태양)", "img": "https://upload.wikimedia.org/wikipedia/commons/1/17/RWS_Tarot_19_Sun.jpg",
     "up": "빛조차 이곳에선 창백하다.", "down": "밝음 뒤에 숨은 거짓을 조심하라."},
    {"name": "20. Judgement (심판)", "img": "https://upload.wikimedia.org/wikipedia/commons/d/dd/RWS_Tarot_20_Judgement.jpg",
     "up": "무덤에서 무언가가 깨어난다.", "down": "과거의 망령이 당신을 붙잡는다."},
    {"name": "21. The World (세계)", "img": "https://upload.wikimedia.org/wikipedia/commons/f/ff/RWS_Tarot_21_World.jpg",
     "up": "완성... 그러나 대가가 따른다.", "down": "닫히지 않는 순환의 굴레."},
]

# ---------------- 이미지 안전 표시 함수 ----------------
# ✅ 이미지 로딩 실패 시 카드 뒷면 이모지로 대체하는 함수
def show_card_image(card):
    try:
        st.image(card["img"], width=180, caption=card["name"])
    except Exception:
        st.markdown(
            f"<div style='text-align:center; font-size:70px; "
            f"border:3px solid #800000; border-radius:8px; padding:20px; "
            f"background:#1a0000; box-shadow:0 0 25px rgba(200,0,0,0.6);'>🂠</div>",
            unsafe_allow_html=True
        )
        st.markdown(f"<p style='text-align:center;'>{card['name']}</p>", unsafe_allow_html=True)

# ---------------- 상태 저장 (세션) ----------------
if "drawn" not in st.session_state:
    st.session_state.drawn = False
if "result" not in st.session_state:
    st.session_state.result = []

# ---------------- 화면 구성 ----------------
st.title("🕯️ 저주받은 타로 🕯️")
st.markdown("<p style='text-align:center;'>어둠 속에서 질문을 떠올리고... 운명의 카드를 뒤집어라 💀</p>", unsafe_allow_html=True)

name = st.text_input("🩸 당신의 이름을 새겨라")
mode = st.radio("🃏 어떤 운명을 확인하겠는가", ["원 카드 (오늘의 저주)", "쓰리 카드 (과거·현재·미래)"])

# 뽑기 전: 떨리는 카드 뒷면 표시
if not st.session_state.drawn:
    num = 1 if "원 카드" in mode else 3
    cols = st.columns(num)
    for i in range(num):
        with cols[i]:
            st.markdown("<div class='floating-card'>🂠</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;'>. . .</p>", unsafe_allow_html=True)

# ---------------- 카드 뽑기 버튼 ----------------
if st.button("💀 운명을 뒤집어라 💀"):
    if name.strip() == "":
        st.warning("🩸 먼저 당신의 이름을 새겨라...")
    else:
        st.session_state.drawn = True
        num = 1 if "원 카드" in mode else 3
        picked = random.sample(tarot_cards, num)
        st.session_state.result = [
            (card, random.choice(["정방향", "역방향"])) for card in picked
        ]
        st.rerun()

# ---------------- 결과 표시 ----------------
if st.session_state.drawn and st.session_state.result:
    st.markdown(f"<h2>🕯️ {name}의 운명 🕯️</h2>", unsafe_allow_html=True)

    positions = ["과거", "현재", "미래"] if len(st.session_state.result) == 3 else ["오늘의 저주"]
    cols = st.columns(len(st.session_state.result))

    # 정방향 개수 세기 (전체 분위기 판단용)
    up_count = 0

    for i, (card, direction) in enumerate(st.session_state.result):
        with cols[i]:
            st.markdown(f"### {positions[i]}")
            show_card_image(card)   # ✅ 안전 표시 함수 사용
            st.markdown(f"**🔻 {direction}**")
            if direction == "정방향":
                st.error(card["up"])
                up_count += 1
            else:
                st.error(card["down"])

    # 스산한 눈 내리는 효과
    st.snow()

       # ---------------- 🕯️ 종합 해석 ----------------
    st.markdown("---")
    st.markdown("<h2>🕯️ 운명의 속삭임 🕯️</h2>", unsafe_allow_html=True)

    total = len(st.session_state.result)

    def key(item):
        """카드의 방향에 맞는 해석 문구를 반환"""
        card, direction = item
        return card["up"] if direction == "정방향" else card["down"]

    # ===== 쓰리 카드: 과거→현재→미래 흐름 해석 (8가지 경우) =====
    if total == 3:
        past, now, future = st.session_state.result

        # 1) 흐름 문장 (이야기 엮기)
        flow = (
            f"**{name}**의 지난날은 『{past[0]['name']}』의 그림자 속에서, "
            f"{key(past)} "
            f"지금 이 순간 『{now[0]['name']}』가 속삭인다... {key(now)} "
            f"그리고 다가올 어둠 속에서 『{future[0]['name']}』가 예언하길, {key(future)}"
        )
        st.markdown(f"<p style='font-size:17px; line-height:1.8;'>{flow}</p>", unsafe_allow_html=True)

        # 2) 세 카드의 방향을 하나의 '패턴 코드'로 만든다
        #    정방향 = "U"(Up), 역방향 = "D"(Down)
        pattern = "".join(
            "U" if d == "정방향" else "D"
            for _, d in st.session_state.result
        )

        # 3) 8가지 패턴별 해석 사전
        flow_readings = {
            "UUU": (
                "🌕 세 개의 촛불이 모두 흔들림 없이 타오른다. "
                "과거의 씨앗이 현재에 뿌리내리고, 미래에 활짝 피어날 흐름이다. "
                "어둠 속에서도 당신의 길은 또렷하게 빛나고 있다."
            ),
            "UUD": (
                "🌗 밝게 시작된 여정이 끝에 이르러 흐려진다. "
                "과거와 현재는 순조로웠으나, 미래에 방심이 화를 부를 수 있다. "
                "마무리에 각별히 신경 쓰지 않으면 애써 쌓은 것이 무너진다."
            ),
            "UDU": (
                "🌓 잠시 촛불이 꺼졌다 다시 타오른다. "
                "좋았던 과거 뒤에 현재의 시련이 닥쳤지만, 이는 지나갈 어둠일 뿐. "
                "지금의 고비만 넘기면 미래의 빛이 당신을 기다린다."
            ),
            "UDD": (
                "🌘 밝던 하늘에 서서히 먹구름이 몰려든다. "
                "좋았던 과거에서 점점 멀어져 어둠이 짙어지는 흐름이다. "
                "지금 흐름을 끊어낼 결단을 내리지 않으면 내리막이 계속된다."
            ),
            "DUU": (
                "🌒 긴 어둠을 뚫고 마침내 여명이 밝아온다. "
                "고통스러운 과거를 딛고 현재부터 상승세를 타는 흐름이다. "
                "당신은 이미 최악을 지나왔다. 이제 앞으로 나아가면 된다."
            ),
            "DUD": (
                "⚡ 어둠 속에서 잠시 번쩍인 섬광, 그러나 곧 사라진다. "
                "현재의 반짝임에 취해선 안 된다. 미래에 다시 그림자가 드리운다. "
                "지금 이 순간의 기회를 놓치면 다시 어둠에 갇힐 것이다."
            ),
            "DDU": (
                "🕯️ 오래도록 이어진 어둠 끝에, 저 멀리 한 줄기 빛이 보인다. "
                "과거도 현재도 힘겨웠으나, 미래에는 반드시 반전이 온다. "
                "지금의 인내가 곧 보상으로 돌아올 것이니 견뎌내라."
            ),
            "DDD": (
                "⚰️ 세 개의 촛불이 모두 꺼졌다. 짙은 어둠이 사방을 덮는다. "
                "과거·현재·미래 모두 불길한 기운에 잠겨 있다. "
                "무리한 시도는 파멸을 부를 뿐. 지금은 숨죽여 때를 기다려라."
            ),
        }

        st.markdown("### 🔮 운명의 흐름 풀이")
        st.markdown(
            f"<p style='font-size:17px; line-height:1.8;'>{flow_readings[pattern]}</p>",
            unsafe_allow_html=True
        )

        # 4) 흐름을 한눈에 보여주는 시각 표시 (⭕ / ❌)
        symbol = "".join("⭕" if c == "U" else "❌" for c in pattern)
        st.markdown(
            f"<p style='text-align:center; font-size:24px;'>"
            f"과거 {symbol[0]} → 현재 {symbol[1]} → 미래 {symbol[2]}</p>",
            unsafe_allow_html=True
        )

    # ===== 원 카드: 한 장의 카드 풀이 (2가지 경우) =====
    else:
        card, direction = st.session_state.result[0]
        st.markdown(
            f"<p style='font-size:17px; line-height:1.8;'>"
            f"오늘 **{name}**에게 드리운 카드는 『{card['name']}』... "
            f"{key((card, direction))}</p>",
            unsafe_allow_html=True
        )

        st.markdown("### 🌑 운명이 건네는 조언")
        if direction == "정방향":
            advice = (
                f"『{card['name']}』가 바로 선 채 당신을 향한다. "
                "카드가 전하는 기운을 믿고 오늘 하루를 나아가라. 당신 편이다."
            )
        else:
            advice = (
                f"『{card['name']}』가 뒤집힌 채 나타났다. "
                "이는 경고의 신호. 서두르지 말고 주변을 살피며 신중히 움직여라."
            )
        st.error(advice)
