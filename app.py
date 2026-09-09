import streamlit as st
import streamlit.components.v1 as components
import random
import time
import html

# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="성지온 냄새 뽑기",
    page_icon="🎴",
    layout="wide"
)

# =========================================================
# 전체 CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 50% -15%, #30305b 0%, #17172d 30%, #090912 65%, #040407 100%);
    color: white;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 1000;
    margin-bottom: 4px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #aebfff,
        #ffffff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    filter:
        drop-shadow(0 0 20px rgba(150,170,255,.32));
}

.subtitle {
    text-align: center;
    color: rgba(230,233,255,.68);
    font-size: 17px;
    margin-bottom: 28px;
}

/* --------------------------
   카드
-------------------------- */

.gacha-card {
    min-height: 235px;

    display: flex;
    flex-direction: column;
    justify-content: center;

    padding: 28px 24px;
    margin: 8px 0;

    border-radius: 24px;

    background:
        radial-gradient(
            circle at top,
            rgba(100,100,180,.13),
            transparent 50%
        ),
        linear-gradient(
            145deg,
            rgba(24,24,48,.97),
            rgba(8,8,18,.98)
        );

    border: 1px solid rgba(255,255,255,.10);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.05),
        0 15px 45px rgba(0,0,0,.32);

    transition:
        transform .25s ease,
        box-shadow .25s ease;
}

.gacha-card:hover {
    transform: translateY(-5px) scale(1.012);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.08),
        0 20px 55px rgba(0,0,0,.40);
}

.card-name {
    font-size: 21px;
    font-weight: 900;
    line-height: 1.5;

    text-align: center;

    color: #f4f5ff;

    margin-bottom: 18px;

    text-shadow:
        0 0 15px rgba(190,200,255,.12);
}

.card-description {
    font-size: 14px;
    line-height: 1.75;

    text-align: center;

    color: rgba(225,228,245,.70);
}

/* 카드 테두리 색 */

.r-F {
    border-color: rgba(160,160,170,.28);
}

.r-E {
    border-color: rgba(180,135,90,.35);
}

.r-D {
    border-color: rgba(90,220,130,.40);
}

.r-C {
    border-color: rgba(70,170,255,.44);
}

.r-B {
    border-color: rgba(165,95,255,.52);
}

.r-A {
    border-color: rgba(255,85,175,.55);
}

.r-S {
    border-color: rgba(255,215,60,.72);

    box-shadow:
        0 0 25px rgba(255,215,60,.13),
        0 15px 45px rgba(0,0,0,.34);
}

.r-SS {
    border-color: rgba(215,250,255,.85);

    box-shadow:
        0 0 30px rgba(90,220,255,.18),
        0 0 55px rgba(180,90,255,.10),
        0 15px 45px rgba(0,0,0,.35);
}

.r-SSS {
    border-color: rgba(255,255,255,.92);
    animation: sssGlow 2.4s linear infinite;
}

@keyframes sssGlow {

    0% {
        box-shadow:
            0 0 22px rgba(255,80,120,.22),
            0 15px 50px rgba(0,0,0,.35);
    }

    33% {
        box-shadow:
            0 0 28px rgba(70,220,255,.26),
            0 15px 50px rgba(0,0,0,.35);
    }

    66% {
        box-shadow:
            0 0 28px rgba(185,95,255,.28),
            0 15px 50px rgba(0,0,0,.35);
    }

    100% {
        box-shadow:
            0 0 22px rgba(255,80,120,.22),
            0 15px 50px rgba(0,0,0,.35);
    }
}


/* --------------------------
   천장 박스
-------------------------- */

.pity-box {
    padding: 18px 20px;

    border-radius: 18px;

    border:
        1px solid rgba(255,255,255,.11);

    background:
        rgba(255,255,255,.04);

    text-align: center;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.04);
}

.pity-big {
    font-size: 30px;
    font-weight: 1000;
}


/* --------------------------
   도감
-------------------------- */

.collection-item {
    padding: 12px 15px;
    margin-bottom: 7px;

    border-radius: 12px;

    background:
        rgba(255,255,255,.025);

    border:
        1px solid rgba(255,255,255,.06);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 카드 생성 함수
# =========================================================

def make_cards(names, rarity):

    descriptions = {

        "F": [
            "수많은 수식어와 전설이 시작되기 전의 가장 순수한 기본형이다."
        ],

        "E": [
            "아직은 평범하지만 분명한 존재감을 남기는 냄새로 기록되어 있다.",
            "미세한 공기의 변화와 함께 감지된다는 관측 기록이 존재한다.",
            "누군가 지나간 뒤 남은 흔적처럼 은은하게 감지되는 형태다.",
            "본격적인 전설이 시작되기 전의 초기 단계로 분류된다.",
            "별도의 측정 장비 없이도 근거리에서 감지할 수 있다고 한다.",
        ],

        "D": [
            "주변 기류가 미세하게 흔들리는 현상이 함께 보고된 카드다.",
            "평범한 냄새와는 다른 묘한 존재감을 가진 것으로 기록되어 있다.",
            "복도와 교실을 넘나드는 이동성이 특징으로 알려져 있다.",
            "E등급보다 감지 범위가 눈에 띄게 넓어진 형태다.",
            "바람의 방향에 따라 체감되는 존재감이 달라진다고 전해진다.",
        ],

        "C": [
            "이 단계부터 냄새 자체에 하나의 서사가 붙기 시작한다.",
            "공기 중에서 독특한 분위기를 형성하는 카드로 분류된다.",
            "주변 공간의 분위기를 변화시킨다는 전설이 전해진다.",
            "단순한 냄새를 넘어 하나의 현상으로 기록되기 시작한 단계다.",
            "관측자마다 서로 다른 인상을 남기는 신비한 특성이 있다.",
        ],

        "B": [
            "천공과 대기의 움직임을 소재로 기록된 상급 냄새 카드다.",
            "장엄한 이름과 달리 근원은 여전히 성지온의 냄새다.",
            "이 등급부터 카드명이 지나치게 웅장해지는 특징이 있다.",
            "냄새 연구자들 사이에서 전설급 후보로 분류되기 시작한 단계다.",
            "주변 공기 자체가 하나의 배경 연출처럼 묘사되는 카드다.",
        ],

        "A": [
            "별과 은하까지 동원해야 설명할 수 있다는 초상급 냄새다.",
            "이름 하나를 전부 읽는 데 시간이 걸리는 것으로 유명하다.",
            "신화와 우주적 표현이 결합된 초월계 카드로 기록되어 있다.",
            "냄새 하나를 묘사하기 위해 시공간까지 등장하기 시작한다.",
            "평범함에서 매우 멀리 떨어진 초고등급 카드다.",
        ],

        "S": [
            "전설이라는 단어만으로는 설명하기 부족하다는 초희귀 카드다.",
            "삼천세계와 은하를 동원한 과장미가 절정에 도달한 형태다.",
            "등장 순간 화면 전체가 요란해지는 것으로 알려진 전설급 카드다.",
            "이쯤 되면 냄새보다 이름의 존재감이 더 강하다고 평가된다.",
            "현실적인 설명을 포기하고 신화의 영역으로 넘어간 카드다.",
        ],

        "SS": [
            "측정 장비가 오류를 표시한다는 설정을 가진 극희귀 카드다.",
            "천상천하와 시공간을 모두 끌어들인 최고급 미사여구를 자랑한다.",
            "카드 하나에 세계관 하나가 들어간 수준의 이름을 가진다.",
            "등장 순간 화면이 과도하게 발광하는 것으로 유명하다.",
            "SSS 바로 아래에 위치한 거의 최종 단계의 냄새 카드다.",
        ],

        "SSS": [
            "모든 미사여구를 끝까지 쌓은 뒤 다시 본체로 돌아온 최종 형태다."
        ]

    }

    result = []

    for i, name in enumerate(names):

        base = descriptions[rarity][
            i % len(descriptions[rarity])
        ]

        result.append({
            "name": name,
            "description": base
        })

    return result


# =========================================================
# 카드 데이터
# =========================================================

CARDS = {}


# F 1장

CARDS["F"] = make_cards([
    "성지온"
], "F")


# E 5장

CARDS["E"] = make_cards([

    "은은하게 감지되는 성지온의 냄새",

    "복도 끝에서 먼저 도착한 성지온의 냄새",

    "바람결에 살짝 실려 온 성지온의 냄새",

    "어딘가 익숙하게 느껴지는 성지온의 냄새",

    "조용히 존재감을 드러내는 성지온의 냄새",

], "E")


# D 10장

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


# C 20장

C_PREFIX = [
    "교실의 공기 흐름마저 바꾸는",
    "푸른 하늘 아래 장엄하게 퍼지는",
    "은빛 달빛과 함께 깨어난",
    "별빛 사이를 유영하는",
]

C_CORE = [
    "성지온의 신비로운 냄새",
    "성지온의 기류진동 냄새",
    "성지온의 미지관측 냄새",
    "성지온의 공간초월 냄새",
    "성지온의 황혼잔존 냄새",
]

C_NAMES = [
    f"{a} {b}"
    for a in C_PREFIX
    for b in C_CORE
]

CARDS["C"] = make_cards(
    C_NAMES,
    "C"
)


# B 40장

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
    f"{a} {b}"
    for a in B_PREFIX
    for b in B_CORE
]

CARDS["B"] = make_cards(
    B_NAMES,
    "B"
)


# A 40장

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
    f"{a} {b}"
    for a in A_PREFIX
    for b in A_CORE
]

CARDS["A"] = make_cards(
    A_NAMES,
    "A"
)


# S 15장

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

CARDS["S"] = make_cards(
    S_NAMES,
    "S"
)


# SS 5장

SS_NAMES = [

    "『천상천하 유아독존 · 억겁성광을 두른 성지온의 궁극초월신성 대냄새』",

    "『태초와 종말의 별들이 동시에 경배하는 성지온의 영겁무한천상 대냄새』",

    "『삼천세계와 구천은하를 관통하여 시공간 그 자체에 새겨진 성지온의 절대 대냄새』",

    "『일월성신과 천지만물이 일제히 찬송하는 성지온의 천상천하무쌍 대냄새』",

    "『우주의 시작과 끝을 목격하고도 끝내 사라지지 않은 성지온의 극광초월 대냄새』",

]

CARDS["SS"] = make_cards(
    SS_NAMES,
    "SS"
)


# SSS 1장

CARDS["SSS"] = make_cards([
    "그냥 성지온"
], "SSS")


# =========================================================
# 등급 / 확률
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
    "SSS",
]

# 총합 100
# F를 기존보다 낮췄다.

PROBABILITIES = [
    25.0,   # F
    24.0,   # E
    18.0,   # D
    11.0,   # C
    8.0,    # B
    6.0,    # A
    4.5,    # S
    2.8,    # SS
    0.7,    # SSS
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
    "SSS": 8,
}


RARITY_COLORS = {
    "F": "#aaaaaf",
    "E": "#b88a60",
    "D": "#61e78c",
    "C": "#5bbcff",
    "B": "#ab67ff",
    "A": "#ff63b5",
    "S": "#ffdb48",
    "SS": "#dffcff",
    "SSS": "#ffffff",
}


# =========================================================
# 세션 상태
# =========================================================

if "total_pulls" not in st.session_state:
    st.session_state.total_pulls = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "collection" not in st.session_state:
    st.session_state.collection = {}


# =========================================================
# 이전 버전 세션 자동 보정
# =========================================================

cleaned_history = []

for item in st.session_state.history:

    if not isinstance(
        item,
        dict
    ):
        continue

    item.setdefault(
        "pity",
        False
    )

    item.setdefault(
        "pull_number",
        0
    )

    item.setdefault(
        "rarity",
        "F"
    )

    item.setdefault(
        "name",
        "알 수 없는 카드"
    )

    item.setdefault(
        "description",
        ""
    )

    cleaned_history.append(
        item
    )

st.session_state.history = (
    cleaned_history
)


# =========================================================
# 뽑기 함수
# =========================================================

def draw_one():

    next_pull = (
        st.session_state.total_pulls
        + 1
    )

    # ---------------------------------------------
    # 100, 200, 300... 번째는 SS 확정이다.
    # SSS가 아니라 정확히 SS가 나온다.
    # ---------------------------------------------

    pity = (
        next_pull % 100 == 0
    )

    if pity:

        rarity = "SS"

    else:

        rarity = random.choices(
            RARITIES,
            weights=PROBABILITIES,
            k=1
        )[0]

    card = random.choice(
        CARDS[rarity]
    )

    st.session_state.total_pulls = (
        next_pull
    )

    result = {

        "pull_number":
            next_pull,

        "rarity":
            rarity,

        "name":
            card["name"],

        "description":
            card["description"],

        "pity":
            pity,

    }

    st.session_state.history.insert(
        0,
        result
    )

    key = (
        f'{rarity}|{card["name"]}'
    )

    st.session_state.collection[key] = (
        st.session_state.collection.get(
            key,
            0
        )
        + 1
    )

    return result


def draw_many(amount):

    results = []

    for _ in range(amount):

        results.append(
            draw_one()
        )

    return results


# =========================================================
# 3D 소환 애니메이션
# =========================================================

def summon_animation(
    rarity,
    multi=False
):

    final_color = (
        RARITY_COLORS[rarity]
    )

    # 화면에는 마지막 순간까지 rarity를 쓰지 않는다.
    # JS에서 일정 시간이 지난 뒤에만 표시한다.

    animation_html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

* {{
    box-sizing:border-box;
}}

body {{
    margin:0;
    overflow:hidden;

    background:
        radial-gradient(
            circle at center,
            rgba(80,85,150,.10),
            transparent 65%
        );

    font-family:
        Arial,
        sans-serif;
}}


.scene {{

    height:430px;

    position:relative;

    display:flex;

    align-items:center;

    justify-content:center;

    perspective:1100px;

    overflow:hidden;
}}


/* ===========================================
   별 파티클
=========================================== */

.particle {{

    position:absolute;

    width:4px;
    height:4px;

    border-radius:50%;

    background:white;

    opacity:0;

    animation:
        fly
        2.1s
        linear
        infinite;
}}


@keyframes fly {{

    0% {{
        transform:
            translate(0,0)
            scale(.2);

        opacity:0;
    }}

    20% {{
        opacity:.65;
    }}

    100% {{
        transform:
            translate(
                var(--x),
                var(--y)
            )
            scale(1.7);

        opacity:0;
    }}
}}


/* ===========================================
   에너지 핵
=========================================== */

.energy {{

    position:absolute;

    width:180px;
    height:180px;

    border-radius:50%;

    background:
        radial-gradient(
            circle,
            rgba(240,240,255,.78),
            rgba(120,120,230,.18),
            transparent 70%
        );

    filter:blur(28px);

    animation:
        breathe
        .48s
        ease-in-out
        infinite alternate;
}}


@keyframes breathe {{

    from {{
        transform:scale(.55);
        opacity:.22;
    }}

    to {{
        transform:scale(1.35);
        opacity:.58;
    }}
}}


/* ===========================================
   회전 고리
=========================================== */

.orbit {{

    position:absolute;

    width:260px;
    height:260px;

    border:
        2px solid
        rgba(225,230,255,.38);

    border-radius:50%;

    animation:
        orbitA
        .75s
        linear
        infinite;
}}


.orbit.two {{

    width:205px;
    height:205px;

    border-style:dashed;

    opacity:.65;

    animation:
        orbitB
        .53s
        linear
        infinite;
}}


.orbit.three {{

    width:315px;
    height:315px;

    opacity:.25;

    animation:
        orbitC
        1.05s
        linear
        infinite;
}}


@keyframes orbitA {{

    from {{
        transform:
            rotateX(68deg)
            rotateZ(0deg);
    }}

    to {{
        transform:
            rotateX(68deg)
            rotateZ(360deg);
    }}
}}


@keyframes orbitB {{

    from {{
        transform:
            rotateY(70deg)
            rotateZ(360deg);
    }}

    to {{
        transform:
            rotateY(70deg)
            rotateZ(0deg);
    }}
}}


@keyframes orbitC {{

    from {{
        transform:
            rotateX(40deg)
            rotateY(55deg)
            rotateZ(0deg);
    }}

    to {{
        transform:
            rotateX(40deg)
            rotateY(55deg)
            rotateZ(360deg);
    }}
}}


/* ===========================================
   3D 오브젝트
=========================================== */

.object {{

    width:105px;
    height:105px;

    position:relative;

    transform-style:preserve-3d;

    z-index:5;

    animation:
        mutate
        4s
        cubic-bezier(.45,0,.55,1)
        forwards;
}}


.face {{

    position:absolute;

    width:105px;
    height:105px;

    border:
        1px solid
        rgba(235,240,255,.78);

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,.26),
            rgba(130,140,220,.10)
        );

    box-shadow:
        inset 0 0 28px
        rgba(170,180,255,.20),

        0 0 18px
        rgba(180,190,255,.20);

    backdrop-filter:
        blur(5px);

    transition:
        all .65s ease;
}}


.front {{
    transform:
        rotateY(0deg)
        translateZ(52px);
}}

.back {{
    transform:
        rotateY(180deg)
        translateZ(52px);
}}

.left {{
    transform:
        rotateY(-90deg)
        translateZ(52px);
}}

.right {{
    transform:
        rotateY(90deg)
        translateZ(52px);
}}

.top {{
    transform:
        rotateX(90deg)
        translateZ(52px);
}}

.bottom {{
    transform:
        rotateX(-90deg)
        translateZ(52px);
}}


/* 계속 형태가 변하도록 만든다. */

@keyframes mutate {{

    0% {{
        transform:
            rotateX(0deg)
            rotateY(0deg)
            rotateZ(0deg)
            scale(.05);
    }}

    10% {{
        transform:
            rotateX(160deg)
            rotateY(250deg)
            rotateZ(80deg)
            scale(1.45);
    }}

    20% {{
        transform:
            rotateX(380deg)
            rotateY(540deg)
            rotateZ(220deg)
            scale(.55,1.60);
    }}

    30% {{
        transform:
            rotateX(650deg)
            rotateY(860deg)
            rotateZ(390deg)
            scale(1.60,.52);
    }}

    42% {{
        transform:
            rotateX(980deg)
            rotateY(1180deg)
            rotateZ(650deg)
            scale(.50)
            skewX(15deg);
    }}

    55% {{
        transform:
            rotateX(1280deg)
            rotateY(1540deg)
            rotateZ(860deg)
            scale(1.65);
    }}

    66% {{
        transform:
            rotateX(1570deg)
            rotateY(1920deg)
            rotateZ(1040deg)
            scale(.65,1.48)
            skewY(-12deg);
    }}

    77% {{
        transform:
            rotateX(1810deg)
            rotateY(2200deg)
            rotateZ(1280deg)
            scale(1.45,.65);
    }}

    88% {{
        transform:
            rotateX(2070deg)
            rotateY(2440deg)
            rotateZ(1390deg)
            scale(.60);
    }}

    96% {{
        transform:
            rotateX(2160deg)
            rotateY(2520deg)
            rotateZ(1440deg)
            scale(1.55);
    }}

    100% {{
        transform:
            rotateX(25deg)
            rotateY(35deg)
            rotateZ(0deg)
            scale(1);
    }}

}}


/* ===========================================
   충격파
=========================================== */

.wave {{

    position:absolute;

    width:80px;
    height:80px;

    border:
        2px solid
        rgba(230,235,255,.5);

    border-radius:50%;

    opacity:0;

    animation:
        shock
        1.1s
        ease-out
        infinite;
}}


.wave.w2 {{
    animation-delay:.35s;
}}

.wave.w3 {{
    animation-delay:.7s;
}}


@keyframes shock {{

    0% {{
        transform:scale(.2);
        opacity:.65;
    }}

    100% {{
        transform:scale(5.5);
        opacity:0;
    }}

}}


/* ===========================================
   최종 등급 텍스트
=========================================== */

.grade {{

    position:absolute;

    bottom:20px;

    width:100%;

    text-align:center;

    font-size:54px;

    font-weight:1000;

    letter-spacing:8px;

    opacity:0;

    transform:
        scale(.25)
        translateY(30px);

    z-index:20;
}}


.grade.show {{

    animation:
        gradeShow
        .65s
        cubic-bezier(.12,.85,.25,1.3)
        forwards;
}}


@keyframes gradeShow {{

    0% {{
        opacity:0;

        transform:
            scale(.25)
            translateY(30px);
    }}

    70% {{
        opacity:1;

        transform:
            scale(1.25)
            translateY(0);
    }}

    100% {{
        opacity:1;

        transform:
            scale(1)
            translateY(0);
    }}

}}


/* ===========================================
   플래시
=========================================== */

.flash {{

    position:absolute;

    inset:0;

    background:white;

    opacity:0;

    pointer-events:none;

    z-index:15;
}}


.flash.go {{

    animation:
        flashAnim
        .48s
        ease-out;
}}


@keyframes flashAnim {{

    0% {{
        opacity:0;
    }}

    30% {{
        opacity:.85;
    }}

    100% {{
        opacity:0;
    }}

}}

</style>

</head>


<body>


<div class="scene">

    <div
        class="energy"
        id="energy">
    </div>

    <div
        class="orbit"
        id="orbit1">
    </div>

    <div
        class="orbit two"
        id="orbit2">
    </div>

    <div
        class="orbit three"
        id="orbit3">
    </div>


    <div class="wave"></div>
    <div class="wave w2"></div>
    <div class="wave w3"></div>


    <div
        class="object"
        id="object">

        <div class="face front"></div>
        <div class="face back"></div>
        <div class="face left"></div>
        <div class="face right"></div>
        <div class="face top"></div>
        <div class="face bottom"></div>

    </div>


    <div
        class="flash"
        id="flash">
    </div>


    <div
        class="grade"
        id="grade">
    </div>

</div>


<script>

const rarity = "{rarity}";
const finalColor = "{final_color}";

const object =
    document.getElementById("object");

const faces =
    document.querySelectorAll(".face");

const energy =
    document.getElementById("energy");

const orbit1 =
    document.getElementById("orbit1");

const orbit2 =
    document.getElementById("orbit2");

const orbit3 =
    document.getElementById("orbit3");

const flash =
    document.getElementById("flash");

const grade =
    document.getElementById("grade");


/* -------------------------------------------
   파티클 생성
------------------------------------------- */

const scene =
    document.querySelector(".scene");

for (
    let i = 0;
    i < 38;
    i++
) {{

    const particle =
        document.createElement("div");

    particle.className =
        "particle";

    const angle =
        Math.random()
        * Math.PI
        * 2;

    const distance =
        150
        + Math.random()
        * 210;

    const x =
        Math.cos(angle)
        * distance;

    const y =
        Math.sin(angle)
        * distance;

    particle.style.setProperty(
        "--x",
        x + "px"
    );

    particle.style.setProperty(
        "--y",
        y + "px"
    );

    particle.style.left =
        "50%";

    particle.style.top =
        "50%";

    particle.style.animationDelay =
        (
            Math.random()
            * 2
        )
        + "s";

    scene.appendChild(
        particle
    );

}}


/* -------------------------------------------
   약 4초 동안 결과를 숨긴 채 변형한다.
------------------------------------------- */

setTimeout(() => {{

    flash.classList.add(
        "go"
    );

    /* 변형 애니메이션 정지 */

    object.style.animation =
        "none";


    /* 등급에 따라 최종 형태가 달라진다. */

    if (
        rarity === "F"
    ) {{

        object.style.transform =
            "rotateX(12deg) rotateY(28deg) scale(.85)";

    }}

    else if (
        rarity === "E"
    ) {{

        object.style.transform =
            "rotateX(22deg) rotateY(35deg) rotateZ(10deg) scale(.92)";

    }}

    else if (
        rarity === "D"
    ) {{

        object.style.transform =
            "rotateX(45deg) rotateY(45deg) rotateZ(45deg) scale(.98)";

    }}

    else if (
        rarity === "C"
    ) {{

        object.style.transform =
            "rotateX(40deg) rotateY(45deg) rotateZ(45deg) scale(1.05,1.2)";

    }}

    else if (
        rarity === "B"
    ) {{

        object.style.transform =
            "rotateX(30deg) rotateY(45deg) rotateZ(45deg) scale(1.18,1.34)";

    }}

    else if (
        rarity === "A"
    ) {{

        object.style.transform =
            "rotateX(25deg) rotateY(45deg) rotateZ(45deg) scale(1.28,1.42)";

    }}

    else if (
        rarity === "S"
    ) {{

        object.style.transform =
            "rotateX(45deg) rotateY(45deg) rotateZ(45deg) scale(1.42)";

    }}

    else if (
        rarity === "SS"
    ) {{

        object.style.transform =
            "rotateX(25deg) rotateY(45deg) scale(1.58)";

    }}

    else {{

        object.style.transform =
            "rotateX(45deg) rotateY(45deg) rotateZ(45deg) scale(1.78)";

    }}


    /* 결과 등급 색은 이 순간 처음 적용한다. */

    faces.forEach(
        face => {{

            face.style.borderColor =
                finalColor;

            face.style.background =
                `linear-gradient(
                    135deg,
                    ${{finalColor}}88,
                    ${{finalColor}}12
                )`;

            face.style.boxShadow =
                `
                inset 0 0 38px ${{finalColor}},
                0 0 48px ${{finalColor}}
                `;

        }}
    );


    energy.style.background =
        `radial-gradient(
            circle,
            ${{finalColor}},
            ${{finalColor}}55,
            transparent 70%
        )`;

    energy.style.filter =
        "blur(34px)";


    orbit1.style.borderColor =
        finalColor;

    orbit2.style.borderColor =
        finalColor;

    orbit3.style.borderColor =
        finalColor;


    orbit1.style.boxShadow =
        `0 0 32px ${{finalColor}}`;

    orbit2.style.boxShadow =
        `0 0 25px ${{finalColor}}`;

}}, 4000);


/* -------------------------------------------
   도형이 정지한 뒤 등급 공개
------------------------------------------- */

setTimeout(() => {{

    grade.innerText =
        rarity;

    grade.style.color =
        finalColor;

    grade.style.textShadow =
        `
        0 0 10px ${{finalColor}},
        0 0 28px ${{finalColor}},
        0 0 60px ${{finalColor}}
        `;

    grade.classList.add(
        "show"
    );

}}, 4550);


</script>

</body>

</html>
"""

    components.html(
        animation_html,
        height=440,
        scrolling=False
    )

    # 결과 카드가 애니메이션보다 먼저 표시되지 않도록 기다린다.
    time.sleep(5.25)


# =========================================================
# 카드 HTML
# =========================================================

def card_html(result):

    rarity = html.escape(
        result.get(
            "rarity",
            "F"
        )
    )

    name = html.escape(
        result.get(
            "name",
            "알 수 없는 카드"
        )
    )

    description = html.escape(
        result.get(
            "description",
            ""
        )
    )

    return f"""
    <div class="gacha-card r-{rarity}">

        <div class="card-name">
            {name}
        </div>

        <div class="card-description">
            {description}
        </div>

    </div>
    """


def show_results(results):

    # 1회 뽑기
    if len(results) == 1:

        st.markdown(
            card_html(
                results[0]
            ),
            unsafe_allow_html=True
        )

        return


    # 10연차
    # 화면이 너무 좁아지는 것을 방지하기 위해 2장씩 5줄로 표시한다.
    for row in range(5):

        cols = st.columns(2)

        for col_index in range(2):

            result_index = (
                row * 2
                + col_index
            )

            with cols[col_index]:

                st.markdown(
                    card_html(
                        results[
                            result_index
                        ]
                    ),
                    unsafe_allow_html=True
                )


# =========================================================
# 제목
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🎴 성지온 냄새 뽑기 🎴
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        137종의 성지온 냄새 카드를 수집하라
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 전체 카드 수
# =========================================================

TOTAL_CARD_TYPES = sum(
    len(cards)
    for cards in CARDS.values()
)


# =========================================================
# 천장 상태
# =========================================================

current_pity_progress = (
    st.session_state.total_pulls
    % 100
)

remaining = (
    100
    - current_pity_progress
)

if (
    current_pity_progress == 0
    and
    st.session_state.total_pulls > 0
):

    remaining = 100


st.markdown(
    f"""
    <div class="pity-box">

        👑 <b>100회 SS 확정 천장</b>

        <br><br>

        다음 SS 확정까지

        <span class="pity-big">
            {remaining}
        </span>

        회다.

    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

st.progress(
    current_pity_progress
    / 100
)


# =========================================================
# 뽑기 버튼
# =========================================================

st.write("")

button_left, button_right = (
    st.columns(2)
)

with button_left:

    single_button = st.button(
        "🎲 1회 뽑기",
        use_container_width=True,
        type="primary"
    )

with button_right:

    ten_button = st.button(
        "🔥 10회 뽑기",
        use_container_width=True
    )


# =========================================================
# 1회 뽑기
# =========================================================

if single_button:

    result = draw_one()

    # 결과 카드보다 연출이 먼저 나온다.
    summon_animation(
        result["rarity"],
        multi=False
    )

    show_results(
        [result]
    )

    if result.get(
        "pity",
        False
    ):

        st.success(
            "👑 100회 천장이 발동해 SS 등급이 확정 등장했다."
        )

    elif result["rarity"] == "SSS":

        st.balloons()

        st.success(
            "🌈 SSS 등급이 등장했다. 모든 미사여구의 끝은 그냥 성지온이다."
        )

    elif result["rarity"] == "SS":

        st.balloons()

        st.success(
            "👑 SS 등급이 등장했다."
        )

    elif result["rarity"] == "S":

        st.success(
            "⭐ S 등급이 등장했다."
        )


# =========================================================
# 10회 뽑기
# =========================================================

if ten_button:

    results = draw_many(
        10
    )

    highest = max(
        results,
        key=lambda item:
            RARITY_ORDER[
                item["rarity"]
            ]
    )

    # 가장 높은 등급을 기준으로 연출하되,
    # 화면에는 마지막 순간까지 무엇인지 보이지 않는다.
    summon_animation(
        highest["rarity"],
        multi=True
    )

    show_results(
        results
    )


    pity_result_exists = any(
        result.get(
            "pity",
            False
        )
        for result in results
    )


    if pity_result_exists:

        st.success(
            "👑 이번 10연차에서 100회 SS 확정 천장이 발동했다."
        )


    if any(
        result["rarity"] == "SSS"
        for result in results
    ):

        st.balloons()

        st.success(
            "🌈 10연차에서 SSS가 등장했다. 그냥 성지온이다."
        )


    elif any(
        RARITY_ORDER[
            result["rarity"]
        ]
        >=
        RARITY_ORDER["SS"]

        for result in results
    ):

        st.balloons()


# =========================================================
# 통계
# =========================================================

st.divider()

stat1, stat2, stat3, stat4 = (
    st.columns(4)
)

with stat1:

    st.metric(
        "총 뽑기",
        st.session_state.total_pulls
    )


with stat2:

    collected_count = len(
        st.session_state.collection
    )

    st.metric(
        "수집한 카드",
        f"{collected_count} / {TOTAL_CARD_TYPES}"
    )


with stat3:

    if (
        st.session_state.history
    ):

        best_rarity = max(
            (
                result.get(
                    "rarity",
                    "F"
                )
                for result
                in st.session_state.history
            ),

            key=lambda rarity:
                RARITY_ORDER.get(
                    rarity,
                    0
                )
        )

    else:

        best_rarity = "-"

    st.metric(
        "최고 등급",
        best_rarity
    )


with stat4:

    ss_count = sum(

        1

        for result
        in st.session_state.history

        if result.get(
            "rarity"
        )
        in [
            "SS",
            "SSS"
        ]
    )

    st.metric(
        "SS 이상 획득",
        ss_count
    )


# =========================================================
# 확률
# =========================================================

with st.expander(
    "📊 등급별 기본 확률"
):

    st.caption(
        "100번째, 200번째, 300번째처럼 100의 배수가 되는 뽑기는 기본 확률을 무시하고 SS가 확정된다."
    )

    for rarity, probability in zip(
        RARITIES,
        PROBABILITIES
    ):

        st.write(
            f"**{rarity}** — "
            f"{probability}% / "
            f"{len(CARDS[rarity])}종"
        )


# =========================================================
# 카드 도감
# =========================================================

with st.expander(
    "📚 냄새 카드 도감"
):

    for rarity in RARITIES:

        st.subheader(
            f"{rarity} 등급 · "
            f"{len(CARDS[rarity])}종"
        )

        for card in CARDS[rarity]:

            key = (
                f'{rarity}|{card["name"]}'
            )

            amount = (
                st.session_state.collection.get(
                    key,
                    0
                )
            )

            if amount > 0:

                safe_name = (
                    html.escape(
                        card["name"]
                    )
                )

                safe_description = (
                    html.escape(
                        card["description"]
                    )
                )

                st.markdown(
                    f"""
                    <div class="collection-item">

                        <b>
                            ✅ {safe_name}
                        </b>

                        <br><br>

                        <span style="
                            opacity:.70;
                        ">
                            {safe_description}
                        </span>

                        <br><br>

                        <span style="
                            opacity:.55;
                            font-size:12px;
                        ">
                            보유 수량: {amount}장
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="collection-item">

                        <span style="
                            opacity:.45;
                        ">
                            ❓ 아직 발견하지 못한 카드
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# 최근 기록
# =========================================================

with st.expander(
    "🕘 최근 뽑기 기록"
):

    if not (
        st.session_state.history
    ):

        st.write(
            "아직 뽑기 기록이 없다."
        )

    else:

        for result in (
            st.session_state.history[:50]
        ):

            pity_text = (
                " 👑 천장"
                if result.get(
                    "pity",
                    False
                )
                else ""
            )

            pull_number = (
                result.get(
                    "pull_number",
                    "?"
                )
            )

            rarity = (
                result.get(
                    "rarity",
                    "?"
                )
            )

            name = (
                result.get(
                    "name",
                    "알 수 없는 카드"
                )
            )

            st.write(
                f"#{pull_number} "
                f"**[{rarity}]** "
                f"{name}"
                f"{pity_text}"
            )


# =========================================================
# 초기화
# =========================================================

st.divider()

if st.button(
    "🗑️ 모든 뽑기 기록 초기화"
):

    st.session_state.total_pulls = 0

    st.session_state.history = []

    st.session_state.collection = {}

    st.rerun()
