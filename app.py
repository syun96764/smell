# app.py

import streamlit as st
import streamlit.components.v1 as components
import random
import time
import html

st.set_page_config(
    page_title="성지온 냄새 뽑기",
    page_icon="🎴",
    layout="wide"
)

# =========================================================
# 전체 디자인
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 50% -10%, #30305c 0%, #111122 38%, #050508 75%);
    color: white;
}

.block-container {
    max-width: 1250px;
}

.main-title {
    text-align:center;
    font-size:52px;
    font-weight:1000;
    margin-bottom:4px;
    text-shadow:
        0 0 12px rgba(255,255,255,.35),
        0 0 30px rgba(160,100,255,.25);
}

.subtitle {
    text-align:center;
    opacity:.72;
    margin-bottom:25px;
    font-size:18px;
}

/* 카드 */

.gacha-card {
    height: 100%;
    min-height: 260px;
    padding: 22px;
    border-radius: 22px;
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.10),
            rgba(255,255,255,.025)
        );
    border: 2px solid rgba(255,255,255,.3);
    box-shadow: 0 8px 30px rgba(0,0,0,.3);
    transition: .3s;
}

.gacha-card:hover {
    transform: translateY(-7px) scale(1.015);
}

.card-rarity {
    font-size: 38px;
    font-weight: 1000;
    margin-bottom: 12px;
}

.card-name {
    font-size: 19px;
    font-weight: 850;
    line-height: 1.45;
    margin-bottom: 16px;
}

.card-description {
    font-size: 14px;
    line-height: 1.65;
    opacity: .78;
}

/* 등급 색 */

.r-F {
    border-color:#888;
    box-shadow:0 0 18px rgba(150,150,150,.25);
}

.r-E {
    border-color:#9d7a55;
    box-shadow:0 0 20px rgba(157,122,85,.30);
}

.r-D {
    border-color:#59db78;
    box-shadow:0 0 22px rgba(89,219,120,.30);
}

.r-C {
    border-color:#4db8ff;
    box-shadow:0 0 25px rgba(77,184,255,.35);
}

.r-B {
    border-color:#a75cff;
    box-shadow:0 0 28px rgba(167,92,255,.40);
}

.r-A {
    border-color:#ff59ac;
    box-shadow:0 0 32px rgba(255,89,172,.45);
}

.r-S {
    border-color:#ffd84a;
    box-shadow:
        0 0 15px rgba(255,216,74,.7),
        0 0 40px rgba(255,216,74,.35);
}

.r-SS {
    border-color:white;
    box-shadow:
        0 0 12px white,
        0 0 35px #5ee7ff,
        0 0 55px #ba62ff;
}

.r-SSS {
    border-color:white;
    animation:sssrainbow 1.7s infinite linear;
}

@keyframes sssrainbow {
    0% {
        box-shadow:0 0 15px red, 0 0 40px orange;
    }
    25% {
        box-shadow:0 0 15px yellow, 0 0 45px lime;
    }
    50% {
        box-shadow:0 0 15px cyan, 0 0 50px blue;
    }
    75% {
        box-shadow:0 0 15px violet, 0 0 45px magenta;
    }
    100% {
        box-shadow:0 0 15px red, 0 0 40px orange;
    }
}

.pity-box {
    padding:16px 20px;
    border:1px solid rgba(255,255,255,.18);
    border-radius:16px;
    background:rgba(255,255,255,.05);
    text-align:center;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 카드 생성 함수
# =========================================================

def make_cards(names, rarity):

    rarity_lore = {

        "F": [
            "별다른 수식어가 필요 없는 기본형이다."
        ],

        "E": [
            "아직은 평범하지만 분명한 존재감을 남긴다.",
            "미세한 공기의 변화와 함께 등장한다고 전해진다.",
            "누군가 지나간 뒤 남은 흔적처럼 은은하게 감지된다.",
            "본격적인 전설이 시작되기 전의 초기 형태다.",
            "관측 장비 없이도 가까이에서는 감지할 수 있다고 한다.",
        ],

        "D": [
            "주변의 기류가 아주 조금 흔들리는 현상이 보고됐다.",
            "평범한 냄새와는 다른 묘한 존재감을 가진 카드다.",
            "복도와 교실을 넘나드는 이동성이 특징이다.",
            "감지 범위가 E등급보다 눈에 띄게 확장됐다.",
            "바람의 방향에 따라 위력이 달라진다는 소문이 있다.",
        ],

        "C": [
            "이 단계부터 냄새에 서사가 붙기 시작한다.",
            "공기 중에서 독특한 존재감을 형성하는 카드다.",
            "주변 공간의 분위기를 바꾼다는 전설이 전해진다.",
            "단순한 냄새를 넘어 하나의 현상으로 분류되기 시작했다.",
            "관측자에 따라 전혀 다른 느낌으로 기록되는 신비한 카드다.",
        ],

        "B": [
            "천공과 대기의 움직임을 소재로 기록된 상급 냄새 카드다.",
            "장엄한 이름과 달리 정체는 여전히 성지온의 냄새다.",
            "이 등급부터 카드명이 지나치게 웅장해지는 특징이 있다.",
            "냄새 연구자들 사이에서 본격적인 전설급 후보로 분류된다.",
            "주변 공기마저 배경 연출로 사용한다는 설정을 가진 카드다.",
        ],

        "A": [
            "수많은 별과 은하를 동원해야 설명할 수 있다는 최상급 냄새다.",
            "이름 하나를 읽는 데 상당한 시간이 걸리는 것으로 유명하다.",
            "신화와 우주적 표현이 결합된 초월계 냄새 카드다.",
            "냄새 하나를 설명하기 위해 시공간까지 등장하기 시작한다.",
            "평범함에서 너무 멀리 와 버린 초고등급 카드다.",
        ],

        "S": [
            "전설이라는 단어조차 부족하다는 설정의 초희귀 카드다.",
            "삼천세계와 은하가 동원되는 과장미의 절정을 보여준다.",
            "등장 순간 뽑기 화면 전체가 요란해지는 전설급 카드다.",
            "이쯤 되면 냄새보다 카드명의 위력이 더 강하다고 평가된다.",
            "현실적인 설명을 포기하고 신화의 영역으로 진입한 카드다.",
        ],

        "SS": [
            "측정 장비가 오류를 표시한다는 설정의 극희귀 카드다.",
            "천상천하와 시공간을 모두 끌어들인 최고급 미사여구를 자랑한다.",
            "카드 하나에 세계관 하나가 들어간 수준의 이름을 가진다.",
            "등장 순간 화면이 과도하게 빛나는 것으로 유명하다.",
            "SSS 바로 아래에 위치한 거의 최종 단계의 냄새 카드다.",
        ],

        "SSS": [
            "수많은 미사여구를 모두 초월한 끝에 결국 본체로 돌아왔다."
        ]
    }

    result = []

    for i, name in enumerate(names):

        lore = rarity_lore[rarity][i % len(rarity_lore[rarity])]

        description = (
            f"{lore} "
            f"공식 도감에서는 「{name}」이라는 이름으로 기록되어 있다."
        )

        result.append({
            "name": name,
            "description": description
        })

    return result


# =========================================================
# F 1장
# =========================================================

CARDS = {}

CARDS["F"] = make_cards([
    "성지온"
], "F")


# =========================================================
# E 5장
# =========================================================

CARDS["E"] = make_cards([

    "은은하게 감지되는 성지온의 냄새",

    "복도 끝에서 먼저 도착한 성지온의 냄새",

    "바람결에 살짝 실려 온 성지온의 냄새",

    "어딘가 익숙하게 느껴지는 성지온의 냄새",

    "조용히 존재감을 드러내는 성지온의 냄새",

], "E")


# =========================================================
# D 10장
# =========================================================

CARDS["D"] = make_cards([

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

], "D")


# =========================================================
# C 20장
# =========================================================

C_PREFIX = [
    "교실의 공기 흐름마저 바꾸는",
    "푸른 하늘 아래 장엄하게 퍼지는",
    "은빛 달빛과 함께 깨어난",
    "별빛 사이를 유영하는"
]

C_CORE = [
    "성지온의 신비로운 냄새",
    "성지온의 기류진동 냄새",
    "성지온의 미지관측 냄새",
    "성지온의 공간초월 냄새",
    "성지온의 황혼잔존 냄새"
]

C_NAMES = [
    f"{prefix} {core}"
    for prefix in C_PREFIX
    for core in C_CORE
]

CARDS["C"] = make_cards(C_NAMES, "C")


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

B_NAMES = [
    f"{prefix} {core}"
    for prefix in B_PREFIX
    for core in B_CORE
]

CARDS["B"] = make_cards(B_NAMES, "B")


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

A_NAMES = [
    f"{prefix} {core}"
    for prefix in A_PREFIX
    for core in A_CORE
]

CARDS["A"] = make_cards(A_NAMES, "A")


# =========================================================
# S 15장
# =========================================================

S_NAMES = [

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

CARDS["S"] = make_cards(S_NAMES, "S")


# =========================================================
# SS 5장
# =========================================================

SS_NAMES = [

    "『천상천하 유아독존 · 억겁성광을 두른 성지온의 궁극초월신성 대냄새』",

    "『태초와 종말의 별들이 동시에 경배하는 성지온의 영겁무한천상 대냄새』",

    "『삼천세계와 구천은하를 관통하여 시공간 그 자체에 새겨진 성지온의 절대 대냄새』",

    "『일월성신과 천지만물이 일제히 찬송하는 성지온의 천상천하무쌍 대냄새』",

    "『우주의 시작과 끝을 목격하고도 끝내 사라지지 않은 성지온의 극광초월 대냄새』",

]

CARDS["SS"] = make_cards(SS_NAMES, "SS")


# =========================================================
# SSS 1장
# =========================================================

CARDS["SSS"] = make_cards([
    "그냥 성지온"
], "SSS")


# =========================================================
# 등급과 기본 확률
# 천장 뽑기는 아래 확률과 별도로 SS가 확정된다.
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
    30.0,   # F
    25.0,   # E
    17.0,   # D
    10.0,   # C
    7.0,    # B
    5.0,    # A
    3.5,    # S
    2.0,    # SS
    0.5,    # SSS
]

RARITY_ORDER = {
    "F": 0,
    "E": 1,
    "D": 2,
    "C": 3,
    "B": 4,
    "A": 5,
    "S": 6,
    "SS": 7,
    "SSS": 8
}


# =========================================================
# 세션
# =========================================================

if "total_pulls" not in st.session_state:
    st.session_state.total_pulls = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "collection" not in st.session_state:
    st.session_state.collection = {}


# =========================================================
# 뽑기 함수
# =========================================================

def draw_one():

    next_pull = st.session_state.total_pulls + 1

    # -------------------------------------
    # 100, 200, 300... 번째는 SS 확정
    # -------------------------------------

    pity = (next_pull % 100 == 0)

    if pity:
        rarity = "SS"

    else:
        rarity = random.choices(
            RARITIES,
            weights=PROBABILITIES,
            k=1
        )[0]

    card = random.choice(CARDS[rarity])

    st.session_state.total_pulls = next_pull

    result = {
        "pull_number": next_pull,
        "rarity": rarity,
        "name": card["name"],
        "description": card["description"],
        "pity": pity
    }

    st.session_state.history.insert(0, result)

    key = card["name"]

    if key not in st.session_state.collection:
        st.session_state.collection[key] = 0

    st.session_state.collection[key] += 1

    return result


def draw_many(amount):

    results = []

    for _ in range(amount):
        results.append(draw_one())

    return results


# =========================================================
# 3D 소환 연출
# =========================================================

RARITY_COLORS = {

    "F": "#999999",
    "E": "#a67a52",
    "D": "#55e479",
    "C": "#55baff",
    "B": "#ab64ff",
    "A": "#ff5aac",
    "S": "#ffda42",
    "SS": "#e8ffff",
    "SSS": "#ffffff",

}


def summon_animation(rarity, multi=False):

    color = RARITY_COLORS[rarity]

    intensity = RARITY_ORDER[rarity]

    if intensity <= 2:
        speed = "1.5s"
        glow = 20

    elif intensity <= 4:
        speed = "1.1s"
        glow = 35

    elif intensity <= 6:
        speed = ".8s"
        glow = 55

    else:
        speed = ".55s"
        glow = 80

    label = (
        f"10연차 최고 등급 : {rarity}"
        if multi
        else f"{rarity} 등급 반응 감지"
    )

    animation = f"""
    <!DOCTYPE html>
    <html>
    <head>

    <style>

    * {{
        box-sizing:border-box;
    }}

    body {{
        margin:0;
        overflow:hidden;
        background:
            radial-gradient(circle, {color}22 0%, transparent 65%);
        font-family:Arial, sans-serif;
    }}

    .scene {{

        position:relative;

        height:360px;

        display:flex;

        justify-content:center;

        align-items:center;

        perspective:900px;

        overflow:hidden;

    }}

    /* 뒷쪽 발광 */

    .energy {{

        position:absolute;

        width:190px;
        height:190px;

        border-radius:50%;

        background:{color};

        filter:blur(55px);

        opacity:.45;

        animation:
            energyPulse .7s infinite alternate,
            energyGrow 2s ease-out;

    }}

    /* 회전 링 */

    .ring {{

        position:absolute;

        width:230px;
        height:230px;

        border:3px solid {color};

        border-radius:50%;

        box-shadow:
            0 0 {glow}px {color},
            inset 0 0 {glow}px {color};

        animation: ringSpin 1.2s linear infinite;

    }}

    .ring2 {{

        position:absolute;

        width:175px;
        height:175px;

        border:2px dashed white;

        border-radius:50%;

        opacity:.7;

        transform:rotateX(68deg);

        animation:ringReverse .8s linear infinite;

    }}

    /* 3D 큐브 */

    .cube {{

        width:100px;
        height:100px;

        position:relative;

        transform-style:preserve-3d;

        animation:
            cubeSpin {speed} linear infinite,
            summonScale 2s cubic-bezier(.2,.8,.2,1);

    }}

    .face {{

        position:absolute;

        width:100px;
        height:100px;

        border:2px solid white;

        background:{color}55;

        box-shadow:
            inset 0 0 30px {color},
            0 0 {glow}px {color};

        backdrop-filter:blur(4px);

    }}

    .front {{
        transform:rotateY(0deg) translateZ(50px);
    }}

    .back {{
        transform:rotateY(180deg) translateZ(50px);
    }}

    .right {{
        transform:rotateY(90deg) translateZ(50px);
    }}

    .left {{
        transform:rotateY(-90deg) translateZ(50px);
    }}

    .top {{
        transform:rotateX(90deg) translateZ(50px);
    }}

    .bottom {{
        transform:rotateX(-90deg) translateZ(50px);
    }}

    /* 충격파 */

    .shockwave {{

        position:absolute;

        width:60px;
        height:60px;

        border:4px solid {color};

        border-radius:50%;

        opacity:0;

        animation:shock 1.4s ease-out infinite;

    }}

    .shockwave.second {{
        animation-delay:.45s;
    }}

    .text {{

        position:absolute;

        bottom:15px;

        width:100%;

        text-align:center;

        color:white;

        font-size:24px;

        font-weight:900;

        text-shadow:
            0 0 8px {color},
            0 0 20px {color};

        animation:textPulse .65s infinite alternate;

    }}

    @keyframes cubeSpin {{

        from {{
            transform:
                rotateX(0deg)
                rotateY(0deg)
                rotateZ(0deg);
        }}

        to {{
            transform:
                rotateX(360deg)
                rotateY(720deg)
                rotateZ(360deg);
        }}

    }}

    @keyframes summonScale {{

        0% {{
            scale:.05;
            opacity:0;
        }}

        25% {{
            scale:1.45;
            opacity:1;
        }}

        45% {{
            scale:.8;
        }}

        65% {{
            scale:1.25;
        }}

        100% {{
            scale:1;
        }}

    }}

    @keyframes ringSpin {{

        from {{
            transform:
                rotateX(65deg)
                rotateZ(0deg)
                scale(.6);
        }}

        to {{
            transform:
                rotateX(65deg)
                rotateZ(360deg)
                scale(1.1);
        }}

    }}

    @keyframes ringReverse {{

        from {{
            transform:
                rotateY(65deg)
                rotateZ(360deg);
        }}

        to {{
            transform:
                rotateY(65deg)
                rotateZ(0deg);
        }}

    }}

    @keyframes energyPulse {{

        from {{
            transform:scale(.65);
            opacity:.25;
        }}

        to {{
            transform:scale(1.4);
            opacity:.65;
        }}

    }}

    @keyframes energyGrow {{

        from {{
            scale:.2;
        }}

        to {{
            scale:1.6;
        }}

    }}

    @keyframes shock {{

        0% {{
            transform:scale(.2);
            opacity:.9;
        }}

        100% {{
            transform:scale(6);
            opacity:0;
        }}

    }}

    @keyframes textPulse {{

        from {{
            transform:scale(.96);
        }}

        to {{
            transform:scale(1.07);
        }}

    }}

    </style>

    </head>

    <body>

    <div class="scene">

        <div class="energy"></div>

        <div class="shockwave"></div>
        <div class="shockwave second"></div>

        <div class="ring"></div>
        <div class="ring2"></div>

        <div class="cube">

            <div class="face front"></div>
            <div class="face back"></div>
            <div class="face right"></div>
            <div class="face left"></div>
            <div class="face top"></div>
            <div class="face bottom"></div>

        </div>

        <div class="text">
            ✦ {label} ✦
        </div>

    </div>

    </body>
    </html>
    """

    components.html(
        animation,
        height=370
    )

    time.sleep(1.9)


# =========================================================
# 카드 표시
# =========================================================

def card_html(result):

    rarity = result["rarity"]

    name = html.escape(result["name"])

    description = html.escape(result["description"])

    pity_badge = ""

    if result["pity"]:

        pity_badge = """
        <div style="
            display:inline-block;
            background:#ffcb35;
            color:#111;
            padding:5px 9px;
            border-radius:999px;
            font-weight:900;
            margin-bottom:10px;
        ">
            👑 100회 천장
        </div>
        """

    return f"""
    <div class="gacha-card r-{rarity}">

        {pity_badge}

        <div class="card-rarity">
            {rarity}
        </div>

        <div class="card-name">
            {name}
        </div>

        <div class="card-description">
            {description}
        </div>

        <div style="
            margin-top:15px;
            opacity:.48;
            font-size:12px;
        ">
            #{result["pull_number"]} 번째 뽑기
        </div>

    </div>
    """


def show_results(results):

    # 10연차는 5장씩 2줄
    if len(results) == 10:

        for row in range(2):

            cols = st.columns(5)

            for i in range(5):

                index = row * 5 + i

                with cols[i]:

                    st.markdown(
                        card_html(results[index]),
                        unsafe_allow_html=True
                    )

    else:

        st.markdown(
            card_html(results[0]),
            unsafe_allow_html=True
        )


# =========================================================
# 제목
# =========================================================

st.markdown(
    '<div class="main-title">🎴 성지온 냄새 뽑기 🎴</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">137종의 전설적인 성지온 냄새 카드를 수집하라</div>',
    unsafe_allow_html=True
)


# =========================================================
# 천장 상태
# =========================================================

current_cycle = st.session_state.total_pulls % 100

until_pity = 100 - current_cycle

if current_cycle == 0 and st.session_state.total_pulls > 0:
    until_pity = 100


st.markdown(
    f"""
    <div class="pity-box">
        👑 <b>SS 확정 천장</b><br><br>
        다음 확정 SS까지
        <span style="
            font-size:30px;
            font-weight:1000;
        ">
            {until_pity}
        </span>
        회
    </div>
    """,
    unsafe_allow_html=True
)

st.progress(current_cycle / 100)


# =========================================================
# 뽑기 버튼
# =========================================================

st.write("")

left, right = st.columns(2)


# =========================================================
# 1회 뽑기
# =========================================================

with left:

    single = st.button(
        "🎲 1회 뽑기",
        use_container_width=True,
        type="primary"
    )


# =========================================================
# 10회 뽑기
# =========================================================

with right:

    multi = st.button(
        "🔥 10회 뽑기",
        use_container_width=True
    )


# =========================================================
# 1회 결과
# =========================================================

if single:

    result = draw_one()

    summon_animation(
        result["rarity"],
        multi=False
    )

    show_results([result])

    if result["pity"]:

        st.success(
            "👑 100회 천장 발동 — SS 등급이 확정 등장했다."
        )

    elif result["rarity"] == "SSS":

        st.balloons()

        st.success(
            "🌈 SSS 등장 — 모든 미사여구를 초월하고 그냥 성지온이 등장했다."
        )

    elif result["rarity"] == "SS":

        st.balloons()

        st.success(
            "👑 SS 초희귀 카드가 등장했다."
        )

    elif result["rarity"] == "S":

        st.success(
            "⭐ S 전설 카드가 등장했다."
        )


# =========================================================
# 10연차 결과
# =========================================================

if multi:

    results = draw_many(10)

    highest = max(
        results,
        key=lambda x: RARITY_ORDER[x["rarity"]]
    )

    summon_animation(
        highest["rarity"],
        multi=True
    )

    show_results(results)

    pity_cards = [
        r
        for r in results
        if r["pity"]
    ]

    ss_or_higher = [
        r
        for r in results
        if RARITY_ORDER[r["rarity"]] >= RARITY_ORDER["SS"]
    ]

    if pity_cards:

        st.success(
            "👑 이번 10연차에서 100회 천장이 발동해 SS가 확정 등장했다."
        )

    if any(r["rarity"] == "SSS" for r in results):

        st.balloons()

        st.success(
            "🌈 10연차에서 SSS가 등장했다. 그냥 성지온이다."
        )

    elif ss_or_higher:

        st.balloons()


# =========================================================
# 통계
# =========================================================

st.divider()

total_cards = sum(
    len(cards)
    for cards in CARDS.values()
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "총 뽑기",
        st.session_state.total_pulls
    )

with col2:

    st.metric(
        "수집 카드",
        f"{len(st.session_state.collection)} / {total_cards}"
    )

with col3:

    if st.session_state.total_pulls == 0:

        best = "-"

    else:

        best = max(
            (
                result["rarity"]
                for result in st.session_state.history
            ),
            key=lambda rarity: RARITY_ORDER[rarity]
        )

    st.metric(
        "최고 등급",
        best
    )

with col4:

    ss_count = sum(
        1
        for x in st.session_state.history
        if x["rarity"] == "SS"
    )

    st.metric(
        "SS 획득",
        ss_count
    )


# =========================================================
# 확률표
# =========================================================

with st.expander("📊 등급별 기본 확률"):

    st.caption(
        "100번째, 200번째, 300번째… 뽑기는 아래 확률 계산을 생략하고 SS가 확정된다."
    )

    for rarity, probability in zip(
        RARITIES,
        PROBABILITIES
    ):

        st.write(
            f"**{rarity}** — {probability}% "
            f"({len(CARDS[rarity])}종)"
        )


# =========================================================
# 도감
# =========================================================

with st.expander("📚 냄새 카드 도감"):

    for rarity in RARITIES:

        st.subheader(
            f"{rarity} 등급 · {len(CARDS[rarity])}종"
        )

        for card in CARDS[rarity]:

            count = st.session_state.collection.get(
                card["name"],
                0
            )

            if count > 0:

                st.markdown(
                    f"""
                    **✅ {card["name"]}**

                    {card["description"]}

                    보유 수량: **{count}장**
                    """
                )

            else:

                st.write(
                    "❓ 아직 발견하지 못한 카드"
                )

        st.divider()


# =========================================================
# 최근 기록
# =========================================================

with st.expander("🕘 최근 뽑기 기록"):

    if not st.session_state.history:

        st.write(
            "아직 뽑기 기록이 없다."
        )

    else:

        for result in st.session_state.history[:50]:

            pity_text = (
                " 👑 천장"
                if result["pity"]
                else ""
            )

            st.write(
                f'#{result["pull_number"]} '
                f'**[{result["rarity"]}]** '
                f'{result["name"]}'
                f'{pity_text}'
            )


# =========================================================
# 초기화
# =========================================================

st.divider()

if st.button(
    "🗑️ 모든 기록 초기화"
):

    st.session_state.total_pulls = 0
    st.session_state.history = []
    st.session_state.collection = {}

    st.rerun()
