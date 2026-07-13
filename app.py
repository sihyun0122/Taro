import streamlit as st
import random
import time

# ---------------- 페이지 기본 설정 ----------------
st.set_page_config(page_title="🕯️ 저주받은 타로", page_icon="💀", layout="centered")

# ---------------- CSS 디자인 + 애니메이션 (공포 강화 버전) ----------------
st.markdown("""
    <style>
    /* 전체 배경 - 핏빛 어둠 */
    .stApp {
        background: linear-gradient(135deg, #0d0000 0%, #1a0000 50%, #000000 100%);
        color: #d9c2c2;
    }

    /* ⑤ 안개가 스멀스멀 흐르는 배경 오버레이 */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 200%; height: 100%;
        background: radial-gradient(circle at 30% 40%, rgba(80,0,0,0.15), transparent 40%),
                    radial-gradient(circle at 70% 60%, rgba(50,0,0,0.15), transparent 40%);
        animation: fogMove 25s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    @keyframes fogMove {
        from { transform: translateX(0); }
        to   { transform: translateX(-50%); }
    }

    /* ⑥ 제목이 미세하게 흔들리는 공포 효과 */
    @keyframes titleHaunt {
        0%, 100% { text-shadow: 0 0 12px rgba(255,0,0,0.7); transform: translateX(0); }
        25%      { text-shadow: 0 0 20px rgba(255,0,0,0.9); transform: translateX(-1px); }
        75%      { text-shadow: 0 0 8px rgba(150,0,0,0.6); transform: translateX(1px); }
    }
    h1 {
        color: #b30000 !important;
        text-align: center;
        letter-spacing: 3px;
        animation: titleHaunt 3s ease-in-out infinite;
    }
    h2, h3 {
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

    /* ② 화면 붉게 번쩍이는 글리치 효과 */
    @keyframes bloodFlash {
        0%   { background-color: rgba(150, 0, 0, 0); }
        20%  { background-color: rgba(180, 0, 0, 0.7); }
        40%  { background-color: rgba(150, 0, 0, 0); }
        60%  { background-color: rgba(200, 0, 0, 0.8); }
        100% { background-color: rgba(150, 0, 0, 0); }
    }
    .curse-flash {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 9999;
        animation: bloodFlash 2.5s ease-in-out;
    }

    /* ③ 저주 메시지 박스 */
    .curse-box {
        border: 3px solid #ff0000;
        background: #2a0000;
        color: #ff4444 !important;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        padding: 20px;
        border-radius: 8px;
        text-shadow: 0 0 15px rgba(255,0,0,0.9);
        animation: flicker 1s infinite;
    }

    /* ① 타이핑 효과용 커서 깜빡임 */
    @keyframes blinkCursor {
        50% { opacity: 0; }
    }
    .typing-cursor {
        display: inline-block;
        color: #ff0000;
        animation: blinkCursor 0.8s infinite;
    }

    /* ===== 추가 공포 연출: 눈 효과 대신 맥동하는 어둠/필름 노이즈 ===== */
    @keyframes abyssPulse {
        0%, 100% { box-shadow: inset 0 0 120px rgba(0,0,0,.88); }
        50% { box-shadow: inset 0 0 210px rgba(80,0,0,.72); }
    }
    @keyframes grainShift {
        0% { transform: translate(0,0); opacity:.13; }
        25% { transform: translate(-1%,1%); opacity:.18; }
        50% { transform: translate(1%,-1%); opacity:.10; }
        75% { transform: translate(1%,1%); opacity:.16; }
        100% { transform: translate(0,0); opacity:.13; }
    }
    @keyframes candleFlicker {
        0%, 100% { opacity:.88; text-shadow:0 0 8px #7a0000; }
        48% { opacity:.55; text-shadow:0 0 22px #d00000; }
        52% { opacity:.95; text-shadow:0 0 5px #430000; }
    }
    .stApp {
        animation: abyssPulse 7s ease-in-out infinite;
    }
    .stApp::after {
        content:"";
        position:fixed;
        inset:-12%;
        pointer-events:none;
        z-index:1;
        background-image:
            repeating-radial-gradient(circle at 20% 30%, rgba(255,255,255,.05) 0 1px, transparent 1px 4px),
            linear-gradient(115deg, transparent 0 45%, rgba(110,0,0,.08) 50%, transparent 55%);
        mix-blend-mode:overlay;
        animation:grainShift .28s steps(2) infinite;
    }
    [data-testid="stAppViewContainer"] > .main {
        position:relative;
        z-index:2;
    }
    .ritual-warning {
        margin: 8px auto 20px;
        max-width: 680px;
        text-align:center;
        color:#8e6767 !important;
        font-family: Georgia, serif;
        letter-spacing:2px;
        animation:candleFlicker 2.7s infinite;
    }
    .whisper {
        text-align:center;
        color:#6d4444 !important;
        font-size:13px;
        letter-spacing:4px;
        opacity:.8;
        animation:flicker 3.5s infinite;
    }


    /* ===== 좌우 심연 장식 ===== */
    .side-haunt {
        position: fixed;
        top: 0;
        width: 19vw;
        height: 100vh;
        z-index: 1;
        pointer-events: none;
        overflow: hidden;
        background:
            radial-gradient(circle at 50% 22%, rgba(120,0,0,.22), transparent 18%),
            repeating-linear-gradient(90deg, transparent 0 24px, rgba(90,0,0,.05) 25px 26px),
            linear-gradient(to bottom, #050000, #160000 48%, #000);
        box-shadow: inset 0 0 80px #000;
    }
    .side-haunt.left { left: 0; border-right: 1px solid rgba(120,0,0,.35); }
    .side-haunt.right { right: 0; border-left: 1px solid rgba(120,0,0,.35); }

    .side-haunt::before {
        content: "☾\A\A 𖤐\A\A †\A\A ◉\A\A 𖤐\A\A ☽";
        white-space: pre;
        position: absolute;
        width: 100%;
        top: 8%;
        text-align: center;
        color: rgba(125,0,0,.42);
        font-size: clamp(28px, 3.2vw, 58px);
        line-height: 1.45;
        text-shadow: 0 0 18px rgba(255,0,0,.35);
        animation: sideWhisper 7s ease-in-out infinite;
    }
    .side-haunt.right::before { animation-delay: -3.5s; transform: scaleX(-1); }

    .side-haunt::after {
        content: "";
        position: absolute;
        left: 15%;
        right: 15%;
        bottom: -12%;
        height: 52%;
        border-radius: 50% 50% 0 0;
        background:
            radial-gradient(ellipse at 35% 32%, rgba(180,0,0,.42) 0 2%, transparent 3%),
            radial-gradient(ellipse at 65% 32%, rgba(180,0,0,.42) 0 2%, transparent 3%),
            radial-gradient(ellipse at 50% 45%, rgba(0,0,0,.96) 0 24%, transparent 25%),
            radial-gradient(ellipse, rgba(35,0,0,.9), #000 70%);
        filter: blur(2px);
        opacity: .72;
        animation: shadowRise 9s ease-in-out infinite;
    }
    @keyframes sideWhisper {
        0%,100% { opacity:.28; transform:translateY(0); }
        50% { opacity:.7; transform:translateY(18px); }
    }
    @keyframes shadowRise {
        0%,100% { transform:translateY(18%); opacity:.38; }
        50% { transform:translateY(0); opacity:.8; }
    }

    /* ===== 카드 선택 직후 공포 리빌 ===== */
    @keyframes voidReveal {
        0% { background:#000; opacity:1; }
        42% { background:#000; opacity:1; }
        48% { background:#6d0000; opacity:.96; }
        51% { background:#000; opacity:1; }
        58% { background:#210000; opacity:.9; }
        100% { background:#000; opacity:0; visibility:hidden; }
    }
    @keyframes omenText {
        0%,30% { opacity:0; transform:scale(.6); filter:blur(8px); }
        43% { opacity:1; transform:scale(1.08); filter:blur(0); }
        55% { opacity:.15; transform:translateX(-7px); }
        60% { opacity:1; transform:translateX(6px); }
        78%,100% { opacity:0; transform:scale(1.3); }
    }
    .horror-reveal {
        position:fixed;
        inset:0;
        z-index:10000;
        pointer-events:none;
        animation:voidReveal 2.7s ease-out forwards;
    }
    .horror-reveal .omen {
        position:absolute;
        inset:0;
        display:flex;
        align-items:center;
        justify-content:center;
        color:#b60000;
        font-family:Georgia, serif;
        font-size:clamp(30px,6vw,88px);
        letter-spacing:8px;
        text-align:center;
        text-shadow:0 0 10px #ff0000, 0 0 35px #5c0000;
        animation:omenText 2.5s ease-in-out forwards;
    }
    .chosen-card {
        border:1px solid rgba(120,0,0,.6);
        background:linear-gradient(180deg, rgba(25,0,0,.7), rgba(0,0,0,.88));
        padding:14px 8px 18px;
        box-shadow:inset 0 0 35px #000, 0 0 22px rgba(120,0,0,.28);
        animation:cardPossessed 4s ease-in-out infinite;
    }
    @keyframes cardPossessed {
        0%,100% { transform:translateY(0); }
        48% { transform:translateY(-3px); }
        50% { transform:translate(-1px,-3px) rotate(-.25deg); }
        52% { transform:translate(1px,-3px) rotate(.25deg); }
    }
    @media (max-width: 1100px) {
        .side-haunt { width: 8vw; opacity:.55; }
        .side-haunt::before { font-size:24px; }
        .side-haunt::after { display:none; }
    }

    </style>
""", unsafe_allow_html=True)


# ---------------- ① 타이핑 효과 함수 ----------------
# 글자를 하나씩 화면에 그려서 스산하게 나타나게 한다.
def typing_effect(text, speed=0.04):
    placeholder = st.empty()   # 계속 덮어쓸 빈 공간
    shown = ""
    for ch in text:
        shown += ch
        placeholder.markdown(
            f"<p style='font-size:17px; line-height:1.8;'>{shown}"
            f"<span class='typing-cursor'>▊</span></p>",
            unsafe_allow_html=True
        )
        time.sleep(speed)
    # 마지막엔 커서 없이 완성된 문장 출력
    placeholder.markdown(
        f"<p style='font-size:17px; line-height:1.8;'>{shown}</p>",
        unsafe_allow_html=True
    )


# ---------------- 타로 카드 데이터 (메이저 22장 + 아래에서 마이너 56장 추가) ----------------
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


# ---------------- 마이너 아르카나 56장 추가 ----------------
# Wikimedia Commons의 동일한 Rider-Waite-Smith 78장 스캔 세트를 사용한다.
# 01~10 = Ace~Ten, 11~14 = Page, Knight, Queen, King
def commons_card(filename):
    from urllib.parse import quote
    return "https://commons.wikimedia.org/wiki/Special:Redirect/file/" + quote(filename)

RANKS = [
    ("Ace", "에이스"), ("Two", "2"), ("Three", "3"), ("Four", "4"),
    ("Five", "5"), ("Six", "6"), ("Seven", "7"), ("Eight", "8"),
    ("Nine", "9"), ("Ten", "10"), ("Page", "페이지"), ("Knight", "나이트"),
    ("Queen", "퀸"), ("King", "킹"),
]

SUITS = {
    "Cups": {
        "ko": "컵",
        "file": "Cups",
        "up": [
            "감정의 문이 열렸다. 그 너머의 속삭임까지 들으려 하지 마라.",
            "두 마음이 마주 본다. 그러나 하나의 그림자가 둘 사이에 서 있다.",
            "웃음소리가 번진다. 이상하게도 방 안에는 아무도 없다.",
            "익숙한 평온이 썩어 간다. 놓친 신호가 다시 문을 두드린다.",
            "잃어버린 것에 시선을 빼앗긴 사이, 뒤에서 무언가 다가온다.",
            "오래된 기억이 돌아온다. 기억 속 얼굴은 조금 달라져 있다.",
            "수많은 환영이 손짓한다. 가장 아름다운 것이 가장 위험할 수 있다.",
            "등을 돌릴 때가 왔다. 미련은 발목을 잡는 차가운 손이 된다.",
            "바라던 것이 가까워진다. 소원이 누구의 목소리였는지 기억하라.",
            "가득 찬 행복 뒤에 낯선 침묵이 눌러앉는다.",
            "어둠이 전한 소식이 감정을 흔든다. 첫 느낌을 무시하지 마라.",
            "감정이 폭주한다. 달콤한 약속을 너무 빨리 믿지 마라.",
            "고요한 직감이 경고한다. 말하지 않은 진실을 읽어라.",
            "감정을 다스리는 자가 나타난다. 그의 침묵에는 깊은 물이 고여 있다.",
        ],
        "down": [
            "메마른 마음 틈으로 불길한 집착이 스며든다.",
            "관계의 균열 속에서 오래 숨은 진실이 모습을 드러낸다.",
            "즐거움이 과해진 밤, 누군가의 가면이 벗겨진다.",
            "무관심이 문을 잠갔다. 그러나 바깥의 것은 떠나지 않았다.",
            "후회가 같은 장면을 반복한다. 과거에 너무 오래 머물지 마라.",
            "왜곡된 기억이 현재를 삼킨다. 그때의 목소리를 의심하라.",
            "환상이 썩어 내린다. 선택하지 못하면 선택당한다.",
            "떠나지 못한 마음이 폐허에 묶인다.",
            "욕망이 주인이 되었다. 만족 뒤의 공허가 더 크게 웃는다.",
            "가까운 곳의 균열을 외면하고 있다. 침묵이 길어질수록 깊어진다.",
            "감정적인 소식이 혼란을 부른다. 충동적인 답을 피하라.",
            "거짓된 낭만이 길을 흐린다. 달콤한 말 뒤를 살펴라.",
            "억눌린 감정이 차갑게 굳는다. 직감이 공포로 변하기 전에 마주하라.",
            "감정의 조종자가 실을 당긴다. 죄책감에 끌려가지 마라.",
        ],
    },
    "Pents": {
        "ko": "펜타클",
        "file": "Pents",
        "up": [
            "새로운 기회가 차가운 손바닥 위에 놓인다. 대가를 먼저 확인하라.",
            "두 운명을 동시에 돌린다. 하나를 놓치는 순간 균형이 깨진다.",
            "함께 쌓은 것이 형태를 얻는다. 벽 속의 빈 공간을 조심하라.",
            "쥔 것을 놓지 못한다. 소유가 사슬로 변하고 있다.",
            "추위와 결핍의 시간이 지나간다. 희미한 불빛을 따라가라.",
            "주고받는 손길 사이에 보이지 않는 빚이 남는다.",
            "기다림의 뿌리가 깊어진다. 썩은 가지는 잘라내야 한다.",
            "반복과 숙련이 힘이 된다. 같은 실수를 의식처럼 되풀이하지 마라.",
            "홀로 쌓은 성취가 빛난다. 정원의 그림자도 함께 자랐다.",
            "오래된 유산이 문을 연다. 그 집안의 침묵까지 물려받지 마라.",
            "현실적인 소식이 도착한다. 작은 징후를 기록하라.",
            "느리지만 확실한 발걸음이다. 멈춰 선 자국이 없는지 뒤를 보라.",
            "차가운 현실 감각이 당신을 지킨다. 감정보다 증거를 보라.",
            "단단한 권력이 자리를 지킨다. 안전해 보여도 출구를 기억하라.",
        ],
        "down": [
            "기회가 손가락 사이로 새어 나간다. 탐욕이 시야를 가린다.",
            "균형이 무너진다. 감당할 수 없는 것을 동시에 붙잡고 있다.",
            "엇갈린 손들이 탑을 비뚤게 쌓는다. 기초부터 확인하라.",
            "집착이 금고를 관으로 바꾼다. 놓아야 살아남는다.",
            "고립감이 문을 닫는다. 도움의 불빛을 일부러 외면하지 마라.",
            "불공정한 거래가 흔적을 남긴다. 조건 없는 호의를 경계하라.",
            "기다림이 집착으로 변한다. 죽은 땅에 계속 물을 붓고 있다.",
            "대충 넘긴 반복이 균열을 만든다. 작은 오류가 커지고 있다.",
            "겉의 풍요가 안의 불안을 숨긴다. 혼자 버티는 척하지 마라.",
            "오래된 갈등이 다시 깨어난다. 물려받은 문제를 그대로 반복하지 마라.",
            "계획 없는 욕심이 발을 묶는다. 현실을 확인하라.",
            "멈춘 발걸음 아래에서 땅이 갈라진다. 고집을 속도라 착각하지 마라.",
            "차가운 통제가 주변을 얼린다. 계산만으로는 읽히지 않는 것이 있다.",
            "권력과 소유욕이 문을 잠근다. 가진 것이 당신을 소유하고 있다.",
        ],
    },
    "Swords": {
        "ko": "소드",
        "file": "Swords",
        "up": [
            "날카로운 진실이 어둠을 가른다. 본 것을 다시 못 본 척할 수 없다.",
            "두 선택이 침묵 속에서 맞선다. 오래 미룰수록 칼끝이 가까워진다.",
            "아픈 진실이 모습을 드러낸다. 상처보다 거짓이 오래 남는다.",
            "고요한 휴식이 필요하다. 침묵 속 소리에 너무 깊이 귀 기울이지 마라.",
            "승리 뒤에 차가운 시선이 남는다. 이긴 것이 정말 당신인지 묻는다.",
            "어두운 물을 건넌다. 떠난 곳의 그림자가 배를 따라온다.",
            "숨겨진 움직임이 있다. 사라진 조각과 발자국을 확인하라.",
            "스스로 만든 경계에 갇혔다. 눈앞의 두려움이 벽을 더 높인다.",
            "밤의 생각이 문을 긁는다. 상상이 사실인 것처럼 자라게 두지 마라.",
            "끝을 알리는 침묵이 내려앉는다. 이제 낡은 흐름은 끝나야 한다.",
            "불안한 소식과 날카로운 호기심이 문을 연다. 너무 멀리 들여다보지 마라.",
            "거침없는 결단이 폭풍처럼 달린다. 방향을 잃으면 자신도 베인다.",
            "차가운 판단이 안개를 걷어낸다. 진실을 말하되 잔혹함을 즐기지 마라.",
            "명령과 이성이 어둠을 정리한다. 감춰진 모순을 찾아라.",
        ],
        "down": [
            "혼란스러운 생각이 스스로를 베고 있다. 확신 없는 결론을 멈춰라.",
            "외면한 선택이 스스로 움직이기 시작한다. 침묵도 선택이다.",
            "오래된 아픔이 왜곡되어 돌아온다. 상처의 목소리를 사실과 구분하라.",
            "쉬지 못한 정신이 환영을 만든다. 지친 판단을 믿지 마라.",
            "원한이 승리의 얼굴을 쓴다. 복수는 끝난 뒤에도 방에 남는다.",
            "과거가 배 밑을 붙잡는다. 떠나려면 짐을 줄여야 한다.",
            "거짓이 흔적을 남겼다. 숨긴 자보다 사라진 사실을 찾아라.",
            "두려움이 눈가리개를 조인다. 실제 출구를 차분히 확인하라.",
            "불안이 현실을 먹어 치운다. 혼자 만든 최악의 결말을 예언으로 믿지 마라.",
            "끝나지 않은 문제가 다시 꿈틀거린다. 미룬 결말을 정리하라.",
            "소문과 의심이 칼날처럼 번진다. 확인되지 않은 말을 믿지 마라.",
            "충동적인 돌진이 모든 것을 어지럽힌다. 멈추지 않으면 길을 잃는다.",
            "냉혹한 말이 관계를 얼린다. 진실과 공격을 구분하라.",
            "권위가 진실을 왜곡한다. 명령보다 근거를 확인하라.",
        ],
    },
    "Wands": {
        "ko": "완드",
        "file": "Wands",
        "up": [
            "불씨가 살아난다. 누가 처음 불을 붙였는지는 묻지 마라.",
            "두 갈래 길 너머에서 붉은 빛이 흔들린다. 선택의 시간이 온다.",
            "멀리 보낸 신호에 답이 온다. 답장을 보낸 존재는 아직 보이지 않는다.",
            "잠깐의 평온과 축하가 찾아온다. 문밖의 발소리만 아니었다면.",
            "충돌하는 기운이 방 안을 가득 채운다. 혼란 속 중심을 지켜라.",
            "승리의 소식이 퍼진다. 환호하는 얼굴들 사이 낯선 표정을 찾아라.",
            "자리를 지켜야 한다. 어둠은 약해 보이는 틈부터 두드린다.",
            "일이 너무 빠르게 움직인다. 날아오는 신호를 놓치지 마라.",
            "지친 경계가 마지막 시험을 맞는다. 한 번만 더 버텨라.",
            "너무 많은 짐이 등을 누른다. 그중 몇 개는 원래 당신 것이 아니다.",
            "작은 불꽃이 호기심을 깨운다. 금지된 문 앞에서는 멈춰라.",
            "뜨거운 추진력이 밤을 가른다. 불길이 번질 방향을 먼저 보라.",
            "강한 의지가 주변을 밝힌다. 그 빛에 끌려오는 것도 있다.",
            "지배적인 불의 기운이 길을 연다. 자신감과 오만의 경계를 지켜라.",
        ],
        "down": [
            "불씨가 꺼지거나 엉뚱한 곳에 번진다. 시작을 서두르지 마라.",
            "결정하지 못한 사이 길이 스스로 닫힌다.",
            "기다린 소식이 늦어진다. 멀리 보이는 형체를 성급히 부르지 마라.",
            "안전해 보이던 장소에 균열이 생긴다. 기초를 다시 확인하라.",
            "사소한 충돌이 소란으로 커진다. 자존심이 불쏘시개가 된다.",
            "인정에 대한 집착이 그림자를 키운다. 박수 소리에 취하지 마라.",
            "방어가 무너지고 있다. 모든 적을 혼자 상대하려 하지 마라.",
            "지연과 혼선이 신호를 뒤틀어 놓는다. 잘못 도착한 메시지를 조심하라.",
            "의심이 경계를 집착으로 바꾼다. 모든 소리를 위협으로 만들지 마라.",
            "짐이 한계를 넘었다. 내려놓지 않으면 길에서 멈춘다.",
            "충동적인 불꽃이 금기를 건드린다. 호기심만으로 문을 열지 마라.",
            "성급한 행동이 화를 키운다. 분노가 방향을 정하게 두지 마라.",
            "질투와 불안이 불길을 탁하게 만든다. 타인의 빛과 비교하지 마라.",
            "고집 센 권력이 주변을 태운다. 통제하려 할수록 손에서 벗어난다.",
        ],
    },
}

for suit, info in SUITS.items():
    for number, ((rank_en, rank_ko), up_text, down_text) in enumerate(
        zip(RANKS, info["up"], info["down"]), start=1
    ):
        tarot_cards.append({
            "name": f"{rank_en} of {suit} ({info['ko']} {rank_ko})",
            "img": commons_card(f"{info['file']}{number:02d}.jpg"),
            "up": up_text,
            "down": down_text,
        })


# ---------------- ③ 저주 이벤트 메시지 ----------------
CURSE_MESSAGES = [
    "🩸 {name}... 네 이름을 부르는 목소리가 들리는가. 오늘 밤, 그것이 너를 찾아온다.",
    "💀 거울을 보지 마라, {name}. 그 안에 있는 것은 더 이상 네가 아니다.",
    "🕯️ {name}, 세 번째 촛불이 꺼지는 순간 뒤를 돌아보지 말지어다.",
    "⚰️ {name}의 그림자가 하나 더 늘었다. 그것은 결코 네 것이 아니다.",
]
# 히든 키워드 전용 특별 메시지
SECRET_KEYWORD = "이건몰랐지ㅋㅋ"
SECRET_CURSE_MSG = "😈 이건 몰랐지...? 너는 이미 선택받았다. 이 화면을 끄더라도 소용없어. ㅋㅋㅋ"

# ---------------- 이미지 안전 표시 함수 ----------------
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
if "cursed" not in st.session_state:
    st.session_state.cursed = False
if "curse_msg" not in st.session_state:
    st.session_state.curse_msg = ""

# ---------------- 화면 구성 ----------------
# ---------------- 좌우 심연 장식 ----------------
st.markdown(
    "<div class='side-haunt left'></div><div class='side-haunt right'></div>",
    unsafe_allow_html=True
)

st.title("🕯️ 심연의 타로 🕯️")
st.markdown("<p style='text-align:center;'>어둠 속에서 질문을 떠올리고... 운명의 카드를 뒤집어라 💀</p>", unsafe_allow_html=True)
st.markdown(
    "<div class='ritual-warning'>빛을 낮추고, 질문을 하나만 떠올려라.<br>"
    "카드는 78장. 같은 밤은 두 번 오지 않는다.</div>",
    unsafe_allow_html=True
)
st.markdown("<div class='whisper'>… 듣고 있다 …</div>", unsafe_allow_html=True)

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
        # ④ 긴장감 로딩 연출
        with st.spinner("🕯️ 영혼이 어둠 속에서 카드를 고르는 중..."):
            progress = st.progress(0)
            for pct in range(100):
                time.sleep(0.015)
                progress.progress(pct + 1)
            progress.empty()

        st.session_state.drawn = True
        num = 1 if "원 카드" in mode else 3
        picked = random.sample(tarot_cards, num)
        st.session_state.result = [
            (card, random.choice(["정방향", "역방향"])) for card in picked
        ]

        # ③ 저주 발동 판정 (히든 키워드 or 10% 확률)
        if name.strip() == SECRET_KEYWORD:
            st.session_state.cursed = True
            st.session_state.curse_msg = SECRET_CURSE_MSG
        elif random.random() < 0.10:
            st.session_state.cursed = True
            st.session_state.curse_msg = random.choice(CURSE_MESSAGES).format(name=name)
        else:
            st.session_state.cursed = False
            st.session_state.curse_msg = ""

        st.rerun()

# ---------------- 결과 표시 ----------------
if st.session_state.drawn and st.session_state.result:
    st.markdown(
        "<div class='horror-reveal'><div class='omen'>선택은 끝났다</div></div>",
        unsafe_allow_html=True
    )

    # ② 저주 발동 시 화면 붉게 번쩍 + 저주 메시지
    if st.session_state.cursed:
        st.markdown("<div class='curse-flash'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='curse-box'>{st.session_state.curse_msg}</div>",
            unsafe_allow_html=True
        )

    st.markdown(f"<h2>🕯️ {name}의 운명 🕯️</h2>", unsafe_allow_html=True)

    positions = ["과거", "현재", "미래"] if len(st.session_state.result) == 3 else ["오늘의 저주"]
    cols = st.columns(len(st.session_state.result))

    up_count = 0
    for i, (card, direction) in enumerate(st.session_state.result):
        with cols[i]:
            st.markdown("<div class='chosen-card'>", unsafe_allow_html=True)
            st.markdown(f"### {positions[i]}")
            show_card_image(card)
            st.markdown(f"**🔻 {direction}**")
            if direction == "정방향":
                st.error(card["up"])
                up_count += 1
            else:
                st.error(card["down"])


    # ---------------- 🕯️ 종합 해석 ----------------
    st.markdown("---")
    st.markdown("<h2>🕯️ 운명의 속삭임 🕯️</h2>", unsafe_allow_html=True)

    total = len(st.session_state.result)

    def key(item):
        card, direction = item
        return card["up"] if direction == "정방향" else card["down"]

    # ===== 쓰리 카드 =====
    if total == 3:
        past, now, future = st.session_state.result

        flow = (
            f"{name}의 지난날은 『{past[0]['name']}』의 그림자 속에서, "
            f"{key(past)} "
            f"지금 이 순간 『{now[0]['name']}』가 속삭인다... {key(now)} "
            f"그리고 다가올 어둠 속에서 『{future[0]['name']}』가 예언하길, {key(future)}"
        )
        # ① 흐름 문장을 타이핑 효과로 출력
        typing_effect(flow, speed=0.03)

        pattern = "".join("U" if d == "정방향" else "D" for _, d in st.session_state.result)

        flow_readings = {
            "UUU": "🌕 세 개의 촛불이 모두 흔들림 없이 타오른다. 과거의 씨앗이 현재에 뿌리내리고, 미래에 활짝 피어날 흐름이다. 어둠 속에서도 당신의 길은 또렷하게 빛나고 있다.",
            "UUD": "🌗 밝게 시작된 여정이 끝에 이르러 흐려진다. 과거와 현재는 순조로웠으나, 미래에 방심이 화를 부를 수 있다. 마무리에 각별히 신경 쓰지 않으면 애써 쌓은 것이 무너진다.",
            "UDU": "🌓 잠시 촛불이 꺼졌다 다시 타오른다. 좋았던 과거 뒤에 현재의 시련이 닥쳤지만, 이는 지나갈 어둠일 뿐. 지금의 고비만 넘기면 미래의 빛이 당신을 기다린다.",
            "UDD": "🌘 밝던 하늘에 서서히 먹구름이 몰려든다. 좋았던 과거에서 점점 멀어져 어둠이 짙어지는 흐름이다. 지금 흐름을 끊어낼 결단을 내리지 않으면 내리막이 계속된다.",
            "DUU": "🌒 긴 어둠을 뚫고 마침내 여명이 밝아온다. 고통스러운 과거를 딛고 현재부터 상승세를 타는 흐름이다. 당신은 이미 최악을 지나왔다. 이제 앞으로 나아가면 된다.",
            "DUD": "⚡ 어둠 속에서 잠시 번쩍인 섬광, 그러나 곧 사라진다. 현재의 반짝임에 취해선 안 된다. 미래에 다시 그림자가 드리운다. 지금 이 순간의 기회를 놓치면 다시 어둠에 갇힐 것이다.",
            "DDU": "🕯️ 오래도록 이어진 어둠 끝에, 저 멀리 한 줄기 빛이 보인다. 과거도 현재도 힘겨웠으나, 미래에는 반드시 반전이 온다. 지금의 인내가 곧 보상으로 돌아올 것이니 견뎌내라.",
            "DDD": "⚰️ 세 개의 촛불이 모두 꺼졌다. 짙은 어둠이 사방을 덮는다. 과거·현재·미래 모두 불길한 기운에 잠겨 있다. 무리한 시도는 파멸을 부를 뿐. 지금은 숨죽여 때를 기다려라.",
        }

        st.markdown("### 🔮 운명의 흐름 풀이")
        st.markdown(f"<p style='font-size:17px; line-height:1.8;'>{flow_readings[pattern]}</p>", unsafe_allow_html=True)

        symbol = "".join("⭕" if c == "U" else "❌" for c in pattern)
        st.markdown(
            f"<p style='text-align:center; font-size:24px;'>"
            f"과거 {symbol[0]} → 현재 {symbol[1]} → 미래 {symbol[2]}</p>",
            unsafe_allow_html=True
        )

    # ===== 원 카드 =====
    else:
        card, direction = st.session_state.result[0]
        one_text = f"오늘 {name}에게 드리운 카드는 『{card['name']}』... {key((card, direction))}"
        # ① 타이핑 효과로 출력
        typing_effect(one_text, speed=0.03)

        st.markdown("### 🌑 운명이 건네는 조언")
        if direction == "정방향":
            advice = f"『{card['name']}』가 바로 선 채 당신을 향한다. 카드가 전하는 기운을 믿고 오늘 하루를 나아가라. 당신 편이다."
        else:
            advice = f"『{card['name']}』가 뒤집힌 채 나타났다. 이는 경고의 신호. 서두르지 말고 주변을 살피며 신중히 움직여라."
        st.error(advice)
