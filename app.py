# app.py

import streamlit as st
import random
import time

st.set_page_config(
    page_title="성지온 냄새 뽑기",
    page_icon="🎴",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top, #202040 0%, #0c0c16 50%, #050509 100%);
    color: white;
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    opacity: 0.75;
    margin-bottom: 30px;
}

.card {
    padding: 35px 25px;
    border-radius: 24px;
    text-align: center;
    margin: 25px 0;
    background: rgba(255,255,255,0.06);
    border: 3px solid white;
    box-shadow: 0 0 30px rgba(255,255,255,0.15);
}

.rarity {
    font-size: 52px;
    font-weight: 1000;
}

.card-name {
    font-size: 25px;
    font-weight: 800;
    margin-top: 15px;
    line-height: 1.5;
}

.F  { border-color:#888; box-shadow:0 0 25px #666; }
.E  { border-color:#9f7650; box-shadow:0 0 25px #9f7650; }
.D  { border-color:#57d957; box-shadow:0 0 30px #57d957; }
.C  { border-color:#48a9ff; box-shadow:0 0 35px #48a9ff; }
.B  { border-color:#b164ff; box-shadow:0 0 40px #b164ff; }
.A  { border-color:#ff4fa3; box-shadow:0 0 45px #ff4fa3; }
.S  { border-color:#ffd43b; box-shadow:0 0 60px #ffd43b; }
.SS {
    border-color:#ffffff;
    box-shadow:
        0 0 15px #fff,
        0 0 35px #5ee7ff,
        0 0 60px #cf5eff;
}
.SSS {
    border-color:#ffffff;
    animation: rainbow 1.5s infinite;
}

@keyframes rainbow {
    0%   {box-shadow:0 0 40px red;}
    16%  {box-shadow:0 0 50px orange;}
    33%  {box-shadow:0 0 60px yellow;}
    50%  {box-shadow:0 0 70px lime;}
    66%  {box-shadow:0 0 80px cyan;}
    83%  {box-shadow:0 0 90px violet;}
    100% {box-shadow:0 0 40px red;}
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 카드 이름
# =========================================================

CARDS = {
    "F": [
        "성지온"
    ],

    "E": [
        "은은하게 감지되는 성지온의 냄새",
        "복도 끝에서 먼저 도착한 성지온의 냄새",
        "바람결에 살짝 실려 온 성지온의 냄새",
        "어딘가 익숙한 성지온의 냄새",
        "조용히 존재감을 드러내는 성지온의 냄새",
    ],

    "D": [
        "바람을 타고 확산되는 성지온의 기묘한 냄새",
        "교실 한구석을 맴도는 성지온의 냄새",
        "새벽 공기를 가르며 등장한 성지온의 냄새",
        "구름 사이를 유영하는 성지온의 냄새",
        "미세한 기류를 뒤흔드는 성지온의 냄새",
        "문이 열리기 전부터 느껴지는 성지온의 냄새",
        "고요한 공간에 흔적을 남기는 성지온의 냄새",
        "바람의 방향을 알려주는 성지온의 냄새",
        "은근한 존재감을 발산하는 성지온의 냄새",
        "조용하지만 확실한 성지온의 냄새",
    ],

    "C": [
        "교실의 공기 흐름마저 바꾸는 성지온의 신비로운 냄새",
        "푸른 하늘 아래 장엄하게 퍼지는 성지온의 냄새",
        "은빛 달빛과 함께 깨어난 성지온의 냄새",
        "별빛 사이를 헤엄치는 성지온의 냄새",
        "운명의 바람을 타고 찾아온 성지온의 냄새",
        "시간이 흘러도 기억되는 성지온의 냄새",
        "천공의 기류에 새겨진 성지온의 냄새",
        "황혼과 새벽 사이에 머무는 성지온의 냄새",
        "미지의 공기층을 지배하는 성지온의 냄새",
        "구름이 갈라지며 나타난 성지온의 냄새",
        "바람의 정령들이 발견한 성지온의 냄새",
        "별자리마저 위치를 바꾸게 하는 성지온의 냄새",
        "찬란한 햇빛을 받아 각성한 성지온의 냄새",
        "천천히 그러나 확실하게 퍼지는 성지온의 냄새",
        "한밤중에도 존재감을 잃지 않는 성지온의 냄새",
        "공간에 새로운 분위기를 창조하는 성지온의 냄새",
        "하늘과 땅의 경계에서 발견된 성지온의 냄새",
        "초여름 바람을 점령한 성지온의 냄새",
        "은하의 기류를 타고 온 성지온의 냄새",
        "세상의 모든 바람이 기억하는 성지온의 냄새",
    ]
}


# =========================================================
# B 40장
# =========================================================

B_PREFIX = [
    "천공을 가르며 강림한",
    "황금빛 새벽을 등에 업은",
    "은하수의 별빛을 한몸에 두른",
    "운명의 바람과 함께 등장한",
    "찬란한 태양의 축복을 받은",
    "백은의 달빛 아래 각성한",
    "별들의 속삭임 속에서 탄생한",
    "천상의 구름을 가르며 내려온",
]

B_CORE = [
    "성지온의 장엄무쌍 냄새",
    "성지온의 천공진동 냄새",
    "성지온의 찬란광휘 냄새",
    "성지온의 신비절정 냄새",
    "성지온의 성운폭풍 냄새",
]

CARDS["B"] = [
    f"{prefix} {core}"
    for prefix in B_PREFIX
    for core in B_CORE
]


# =========================================================
# A 40장
# =========================================================

A_PREFIX = [
    "백만 별빛과 억겁의 세월을 머금은",
    "태초의 별들이 탄생하던 순간 예언된",
    "수천 개의 은하를 건너 마침내 도달한",
    "태양과 달이 동시에 경배하는",
    "시간과 공간의 경계를 뛰어넘은",
    "천공의 모든 별자리가 찬양하는",
    "운명의 수레바퀴를 직접 움직이는",
    "세상의 모든 바람을 지휘하는",
]

A_CORE = [
    "성지온의 초월적 냄새",
    "성지온의 영겁불멸 냄새",
    "성지온의 천상절정 냄새",
    "성지온의 무한성운 냄새",
    "성지온의 황금광휘 냄새",
]

CARDS["A"] = [
    f"{prefix} {core}"
    for prefix in A_PREFIX
    for core in A_CORE
]


# =========================================================
# S 15장
# =========================================================

CARDS["S"] = [
    "삼천세계를 진동시키며 차원의 경계를 초월한 성지온의 절대궁극 냄새",
    "태초의 별들이 탄생하던 순간부터 예언되어 온 성지온의 천상절대 냄새",
    "천공과 대지가 동시에 경배하는 성지온의 찬란무궁 냄새",
    "억겁의 시간을 넘어 마침내 강림한 성지온의 영원불멸 냄새",
    "수천 은하의 별빛을 왕관처럼 두른 성지온의 초월천상 냄새",
    "세상의 모든 새벽과 황혼을 지배하는 성지온의 절대 냄새",
    "운명의 별들마저 고개를 숙이게 한 성지온의 성역 냄새",
    "우주의 모든 별들이 일제히 합창하며 맞이한 성지온의 무한 냄새",
    "천상의 문이 열리고 광휘와 함께 내려온 성지온의 신성 냄새",
    "시간과 공간을 넘어 영원히 기억될 성지온의 초월 냄새",
    "별과 달과 태양이 하나 되어 탄생시킨 성지온의 삼위천상 냄새",
    "태초의 혼돈을 가르고 질서를 가져온 성지온의 창세 냄새",
    "백만 개의 별빛이 폭발하며 등장한 성지온의 황제 냄새",
    "천공의 모든 신비와 기적이 응축된 성지온의 절대찬란 냄새",
    "은하의 끝에서조차 전설로 전해지는 성지온의 무궁천상 냄새",
]


# =========================================================
# SS 5장
# =========================================================

CARDS["SS"] = [
    "『천상천하 유아독존 · 억겁성광을 두른 성지온의 궁극초월신성 대냄새』",
    "『태초와 종말의 별들이 동시에 경배하는 성지온의 영겁무한천상 대냄새』",
    "『삼천세계와 구천은하를 관통하여 시공간 그 자체에 새겨진 성지온의 절대 대냄새』",
    "『일월성신과 천지만물이 일제히 찬송하는 성지온의 천상천하무쌍 대냄새』",
    "『우주의 시작과 끝을 목격하고도 끝내 사라지지 않은 성지온의 극광초월 대냄새』",
]


# =========================================================
# SSS 1장
# =========================================================

CARDS["SSS"] = [
    "그냥 성지온"
]


# =========================================================
# 등급 확률
# =========================================================

RARITIES = [
    "F",
    "E",
    "D",
    "C",
    "B",
    "A",
    "S",
    "SS",
    "SSS"
]

PROBABILITIES = [
    42.0,   # F
    24.0,   # E
    14.0,   # D
    8.0,    # C
    5.0,    # B
    3.5,    # A
    2.0,    # S
    1.3,    # SS
    0.2     # SSS
]


# =========================================================
# 세션 상태
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "count" not in st.session_state:
    st.session_state.count = 0


# =========================================================
# 함수
# =========================================================

def draw_card():
    rarity = random.choices(
        RARITIES,
        weights=PROBABILITIES,
        k=1
    )[0]

    card = random.choice(CARDS[rarity])

    return rarity, card


def show_animation(rarity):

    placeholder = st.empty()

    if rarity in ["F", "E", "D"]:
        placeholder.markdown(
            "### 🎴 카드가 나타나고 있다..."
        )
        time.sleep(0.5)

    elif rarity in ["C", "B"]:
        placeholder.markdown(
            "## ✨ 뭔가 심상치 않다..."
        )
        time.sleep(0.7)

        placeholder.markdown(
            "## 💫 냄새의 기운이 모이고 있다..."
        )
        time.sleep(0.7)

    elif rarity == "A":
        placeholder.markdown(
            "# 🌟 고등급 반응 감지"
        )
        time.sleep(0.7)

        placeholder.markdown(
            "# ⚡ 공기가 진동한다..."
        )
        time.sleep(0.7)

        placeholder.markdown(
            "# 🌌 성지온의 냄새가 각성한다!"
        )
        time.sleep(0.8)

    elif rarity == "S":
        st.balloons()

        placeholder.markdown(
            "# ⭐ S급 반응 ⭐"
        )
        time.sleep(0.7)

        placeholder.markdown(
            "# 🌌 천공의 문이 열리고 있다..."
        )
        time.sleep(0.7)

        placeholder.markdown(
            "# ⚡ 전설급 냄새 출현 ⚡"
        )
        time.sleep(1)

    elif rarity == "SS":
        st.balloons()

        placeholder.markdown(
            "# 🚨 경고 🚨"
        )
        time.sleep(0.7)

        placeholder.markdown(
            "# 🌈 측정 불가능한 냄새 에너지 감지"
        )
        time.sleep(0.8)

        placeholder.markdown(
            "# 👑 SS급 강림 👑"
        )
        time.sleep(1)

    elif rarity == "SSS":

        placeholder.markdown(
            "# ⚠️ 시스템 오류 ⚠️"
        )
        time.sleep(0.8)

        placeholder.markdown(
            "# 냄새 측정기를 초과했다."
        )
        time.sleep(0.8)

        placeholder.markdown(
            "# 등급 판정을 다시 시도한다..."
        )
        time.sleep(0.8)

        placeholder.markdown(
            "# SSS"
        )
        time.sleep(1)

        st.balloons()
        st.snow()

    placeholder.empty()


# =========================================================
# 화면
# =========================================================

st.markdown(
    '<div class="main-title">🎴 성지온 냄새 뽑기 🎴</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">137종의 성지온 냄새 카드를 수집하라</div>',
    unsafe_allow_html=True
)


# =========================================================
# 뽑기
# =========================================================

if st.button(
    "🎲 냄새 카드 1회 뽑기",
    use_container_width=True,
    type="primary"
):

    rarity, card = draw_card()

    show_animation(rarity)

    st.session_state.count += 1
    st.session_state.history.insert(
        0,
        {
            "rarity": rarity,
            "card": card
        }
    )

    st.markdown(
        f"""
        <div class="card {rarity}">
            <div class="rarity">{rarity}</div>
            <div class="card-name">{card}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if rarity == "SSS":
        st.success(
            "🎉 축하한다. 모든 미사여구가 사라지고 본체가 등장했다."
        )

    elif rarity == "SS":
        st.success(
            "👑 SS급 냄새 카드를 획득했다."
        )

    elif rarity == "S":
        st.success(
            "⭐ S급 전설 냄새 카드를 획득했다."
        )


# =========================================================
# 통계
# =========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "총 뽑기 횟수",
        st.session_state.count
    )

with col2:
    unique_cards = len(
        set(
            item["card"]
            for item in st.session_state.history
        )
    )

    st.metric(
        "발견한 카드",
        f"{unique_cards} / 137"
    )


# =========================================================
# 도감
# =========================================================

with st.expander("📖 카드 도감"):

    collected = set(
        item["card"]
        for item in st.session_state.history
    )

    for rarity in RARITIES:

        st.subheader(
            f"{rarity} 등급 · {len(CARDS[rarity])}종"
        )

        for card in CARDS[rarity]:

            if card in collected:
                st.write(
                    f"✅ {card}"
                )

            else:
                st.write(
                    "❓ ???"
                )


# =========================================================
# 확률표
# =========================================================

with st.expander("📊 등급별 확률"):

    for rarity, probability in zip(
        RARITIES,
        PROBABILITIES
    ):

        st.write(
            f"**{rarity}** : {probability}%"
        )


# =========================================================
# 최근 뽑기 기록
# =========================================================

with st.expander("🕘 최근 뽑기 기록"):

    if not st.session_state.history:
        st.write(
            "아직 뽑은 카드가 없다."
        )

    else:

        for item in st.session_state.history[:20]:

            st.write(
                f"**[{item['rarity']}]** {item['card']}"
            )


# =========================================================
# 초기화
# =========================================================

st.divider()

if st.button(
    "🗑️ 기록 초기화"
):

    st.session_state.history = []
    st.session_state.count = 0
    st.rerun()
