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
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 전체 CSS
# =========================================================

st.markdown(
    """
<style>

html,
body,
[class*="css"] {
    font-family:
        Pretendard,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}


/* ==========================================
   전체 배경
========================================== */

.stApp {
    background:
        radial-gradient(
            circle at 50% -15%,
            #2b2b50 0%,
            #17172c 28%,
            #0c0c18 58%,
            #050509 100%
        );

    color: #f5f5ff;
}


.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ==========================================
   사이드바
========================================== */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #111120,
            #090911
        );

    border-right:
        1px solid rgba(255,255,255,.07);
}


[data-testid="stSidebar"] * {
    color: #eeeeff;
}


/* ==========================================
   제목
========================================== */

.main-title {
    text-align: center;

    font-size: 52px;
    font-weight: 1000;

    margin-bottom: 3px;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #b9c5ff,
            #ffffff
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    filter:
        drop-shadow(
            0 0 18px
            rgba(160,170,255,.28)
        );
}


.subtitle {
    text-align: center;

    font-size: 16px;

    color:
        rgba(230,232,255,.62);

    margin-bottom: 28px;
}


/* ==========================================
   상태 패널
========================================== */

.status-panel {

    padding:
        22px 24px;

    border-radius:
        22px;

    background:
        linear-gradient(
            145deg,
            rgba(26,26,49,.92),
            rgba(10,10,21,.96)
        );

    border:
        1px solid
        rgba(255,255,255,.09);

    box-shadow:
        inset 0 1px 0
        rgba(255,255,255,.035),

        0 16px 45px
        rgba(0,0,0,.30);

    text-align:
        center;

    margin-bottom:
        14px;
}


.status-title {

    color:
        rgba(235,237,255,.70);

    font-size:
        14px;

    margin-bottom:
        7px;
}


.status-value {

    font-size:
        31px;

    font-weight:
        1000;

    color:
        #ffffff;
}


.status-small {

    font-size:
        13px;

    color:
        rgba(225,228,245,.50);

    margin-top:
        5px;
}


/* ==========================================
   결과 카드
========================================== */

.gacha-card {

    min-height:
        220px;

    padding:
        30px 27px;

    display:
        flex;

    flex-direction:
        column;

    justify-content:
        center;

    border-radius:
        24px;

    background:

        radial-gradient(
            circle at 50% 0%,
            rgba(105,105,180,.10),
            transparent 50%
        ),

        linear-gradient(
            145deg,
            rgba(24,24,46,.98),
            rgba(8,8,17,.99)
        );

    border:
        1px solid
        rgba(255,255,255,.10);

    box-shadow:

        inset 0 1px 0
        rgba(255,255,255,.045),

        0 18px 50px
        rgba(0,0,0,.33);

    transition:
        transform .25s ease,
        box-shadow .25s ease;

    margin:
        8px 0 18px 0;
}


.gacha-card:hover {

    transform:
        translateY(-4px)
        scale(1.008);

    box-shadow:

        inset 0 1px 0
        rgba(255,255,255,.07),

        0 22px 58px
        rgba(0,0,0,.40);
}


.card-name {

    text-align:
        center;

    color:
        #f5f5ff;

    font-size:
        21px;

    line-height:
        1.55;

    font-weight:
        900;

    margin-bottom:
        18px;

    word-break:
        keep-all;
}


.card-description {

    text-align:
        center;

    color:
        rgba(222,224,242,.68);

    font-size:
        14px;

    line-height:
        1.75;

    word-break:
        keep-all;
}


/* ==========================================
   등급별 미세 테두리
========================================== */

.r-F {
    border-color:
        rgba(160,160,170,.25);
}

.r-E {
    border-color:
        rgba(183,138,94,.30);
}

.r-D {
    border-color:
        rgba(90,220,130,.33);
}

.r-C {
    border-color:
        rgba(76,174,255,.37);
}

.r-B {
    border-color:
        rgba(170,100,255,.42);
}

.r-A {
    border-color:
        rgba(255,91,177,.45);
}

.r-S {

    border-color:
        rgba(255,220,75,.58);

    box-shadow:

        0 0 24px
        rgba(255,220,75,.08),

        0 18px 50px
        rgba(0,0,0,.34);
}

.r-SS {

    border-color:
        rgba(220,250,255,.72);

    box-shadow:

        0 0 25px
        rgba(85,220,255,.13),

        0 0 50px
        rgba(180,100,255,.07),

        0 18px 50px
        rgba(0,0,0,.34);
}

.r-SSS {

    border-color:
        rgba(255,255,255,.88);

    animation:
        sss-card-glow
        2.3s
        linear
        infinite;
}


@keyframes sss-card-glow {

    0% {

        box-shadow:
            0 0 25px
            rgba(255,80,120,.18),

            0 18px 50px
            rgba(0,0,0,.35);
    }

    33% {

        box-shadow:
            0 0 28px
            rgba(80,220,255,.20),

            0 18px 50px
            rgba(0,0,0,.35);
    }

    66% {

        box-shadow:
            0 0 28px
            rgba(180,90,255,.22),

            0 18px 50px
            rgba(0,0,0,.35);
    }

    100% {

        box-shadow:
            0 0 25px
            rgba(255,80,120,.18),

            0 18px 50px
            rgba(0,0,0,.35);
    }
}


/* ==========================================
   카드 목록
========================================== */

.collection-card {

    padding:
        20px 22px;

    margin-bottom:
        12px;

    border-radius:
        17px;

    background:

        linear-gradient(
            145deg,
            rgba(25,25,46,.86),
            rgba(10,10,19,.93)
        );

    border:
        1px solid
        rgba(255,255,255,.07);
}


.collection-name {

    font-weight:
        850;

    font-size:
        16px;

    color:
        #f3f3ff;

    line-height:
        1.5;
}


.collection-description {

    margin-top:
        9px;

    font-size:
        13px;

    line-height:
        1.65;

    color:
        rgba(222,224,242,.60);
}


.collection-count {

    margin-top:
        10px;

    font-size:
        12px;

    color:
        rgba(215,218,238,.42);
}


/* ==========================================
   기록
========================================== */

.history-item {

    padding:
        15px 18px;

    border-radius:
        14px;

    margin-bottom:
        9px;

    background:
        rgba(255,255,255,.025);

    border:
        1px solid
        rgba(255,255,255,.055);
}


.history-rarity {

    font-size:
        13px;

    font-weight:
        900;

    color:
        rgba(200,205,255,.70);

    margin-bottom:
        5px;
}


.history-name {

    font-size:
        15px;

    font-weight:
        750;

    color:
        #eeeeff;

    line-height:
        1.5;
}


/* ==========================================
   Streamlit 기본 요소
========================================== */

[data-testid="stMetric"] {

    background:
        rgba(255,255,255,.03);

    padding:
        15px;

    border-radius:
        14px;

    border:
        1px solid
        rgba(255,255,255,.06);
}


div[data-testid="stProgress"] > div > div {

    background:
        linear-gradient(
            90deg,
            #8787ff,
            #d5b3ff
        );
}


.stButton > button {

    border-radius:
        14px;

    min-height:
        48px;

    font-weight:
        800;
}


</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# 카드 설명 생성
# =========================================================

def make_cards(names, rarity):

    descriptions = {

        "F": [
            "모든 전설과 미사여구가 시작되기 전의 가장 순수한 기본 형태다."
        ],

        "E": [
            "아직은 평범하지만 분명한 존재감을 남기는 초기 냄새 카드다.",
            "미세한 공기의 변화와 함께 관측되는 것으로 기록되어 있다.",
            "누군가 지나간 뒤 남은 흔적처럼 은은하게 감지되는 형태다.",
            "본격적인 전설이 시작되기 직전의 단계로 분류된다.",
            "별도의 관측 장비 없이도 가까이에서는 존재를 확인할 수 있다.",
        ],

        "D": [
            "주변 기류가 미세하게 흔들리는 현상이 함께 보고된 카드다.",
            "평범함을 살짝 벗어나기 시작한 묘한 존재감을 지닌다.",
            "복도와 교실을 넘나드는 이동성이 특징으로 기록되어 있다.",
            "E등급보다 감지 범위가 눈에 띄게 넓어진 형태다.",
            "바람의 방향에 따라 체감되는 존재감이 달라진다고 전해진다.",
        ],

        "C": [
            "이 단계부터 냄새 자체에 본격적인 서사가 붙기 시작한다.",
            "주변 공간에 독특한 분위기를 만드는 것으로 기록되어 있다.",
            "단순한 냄새를 넘어 하나의 현상처럼 취급되기 시작한 단계다.",
            "관측자마다 서로 다른 인상을 남긴다는 기록이 존재한다.",
            "점차 평범한 설명만으로 표현하기 어려워지기 시작한다.",
        ],

        "B": [
            "천공과 대기의 움직임을 소재로 기록된 상급 냄새 카드다.",
            "장엄한 이름과 달리 근원은 여전히 성지온의 냄새다.",
            "이 단계부터 카드명이 지나치게 웅장해지는 특징이 나타난다.",
            "전설급 후보로 분류되기 시작한 본격적인 상위 단계다.",
            "주변 공기 자체가 하나의 연출처럼 묘사되는 카드다.",
        ],

        "A": [
            "별과 은하까지 동원해야 설명할 수 있다는 초상급 냄새 카드다.",
            "이름 하나를 끝까지 읽는 것부터 쉽지 않은 단계다.",
            "신화적 표현과 우주적 미사여구가 결합된 초월계 카드다.",
            "냄새 하나를 묘사하기 위해 시공간까지 등장하기 시작한다.",
            "평범함에서 매우 멀리 떨어진 초고등급 카드다.",
        ],

        "S": [
            "전설이라는 단어만으로는 부족하다는 초희귀 냄새 카드다.",
            "삼천세계와 은하를 동원한 과장미가 절정에 도달한 형태다.",
            "등장 자체가 하나의 이벤트처럼 취급되는 전설급 카드다.",
            "이쯤 되면 냄새보다 이름의 존재감이 더 강하다고 평가된다.",
            "현실적인 묘사를 포기하고 신화의 영역으로 넘어간 카드다.",
        ],

        "SS": [
            "일반적인 측정 범위를 벗어났다는 설정의 극희귀 카드다.",
            "천상천하와 시공간을 모두 끌어들인 최고급 미사여구를 자랑한다.",
            "카드 하나에 세계관 하나가 들어간 수준의 이름을 가진다.",
            "등장 순간 주변 연출이 가장 강하게 변화하는 카드 중 하나다.",
            "SSS 바로 아래에 존재하는 사실상 최종 단계의 냄새 카드다.",
        ],

        "SSS": [
            "끝없는 미사여구를 모두 초월한 뒤 결국 본체 그 자체로 돌아온 최종 카드다."
        ]
    }

    cards = []

    for index, name in enumerate(names):

        description = descriptions[rarity][
            index % len(descriptions[rarity])
        ]

        cards.append(
            {
                "name": name,
                "description": description
            }
        )

    return cards


# =========================================================
# 카드 데이터
# =========================================================

CARDS = {}


# =========================================================
# F - 1종
# =========================================================

CARDS["F"] = make_cards(
    [
        "성지온"
    ],
    "F"
)


# =========================================================
# E - 5종
# =========================================================

CARDS["E"] = make_cards(
    [
        "은은하게 감지되는 성지온의 냄새",
        "복도 끝에서 먼저 도착한 성지온의 냄새",
        "바람결에 살짝 실려 온 성지온의 냄새",
        "어딘가 익숙하게 느껴지는 성지온의 냄새",
        "조용히 존재감을 드러내는 성지온의 냄새",
    ],
    "E"
)


# =========================================================
# D - 10종
# =========================================================

CARDS["D"] = make_cards(
    [
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
    "D"
)


# =========================================================
# C - 20종
# =========================================================

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
    f"{prefix} {core}"
    for prefix in C_PREFIX
    for core in C_CORE
]

CARDS["C"] = make_cards(
    C_NAMES,
    "C"
)


# =========================================================
# B - 40종
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

CARDS["B"] = make_cards(
    B_NAMES,
    "B"
)


# =========================================================
# A - 40종
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

CARDS["A"] = make_cards(
    A_NAMES,
    "A"
)


# =========================================================
# S - 15종
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

CARDS["S"] = make_cards(
    S_NAMES,
    "S"
)


# =========================================================
# SS - 5종
# =========================================================

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


# =========================================================
# SSS - 1종
# =========================================================

CARDS["SSS"] = make_cards(
    [
        "그냥 성지온"
    ],
    "SSS"
)


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


PROBABILITIES = [
    25.0,  # F
    24.0,  # E
    18.0,  # D
    11.0,  # C
    8.0,   # B
    6.0,   # A
    4.5,   # S
    2.8,   # SS
    0.7,   # SSS
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
    "F": "#a8a8ad",
    "E": "#b88a61",
    "D": "#61e78b",
    "C": "#5abaff",
    "B": "#aa67ff",
    "A": "#ff63b4",
    "S": "#ffda45",
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

if "last_results" not in st.session_state:
    st.session_state.last_results = []


# =========================================================
# 이전 버전 데이터 보정
# =========================================================

clean_history = []

for item in st.session_state.history:

    if not isinstance(item, dict):
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

    clean_history.append(
        item
    )

st.session_state.history = clean_history


# =========================================================
# 카드 총 개수
# =========================================================

TOTAL_CARD_TYPES = sum(
    len(cards)
    for cards in CARDS.values()
)


# =========================================================
# 뽑기
# =========================================================

def draw_one():

    next_pull = (
        st.session_state.total_pulls
        + 1
    )

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

    selected_card = random.choice(
        CARDS[rarity]
    )

    st.session_state.total_pulls = (
        next_pull
    )

    result = {
        "pull_number": next_pull,
        "rarity": rarity,
        "name": selected_card["name"],
        "description": selected_card["description"],
        "pity": pity,
    }

    st.session_state.history.insert(
        0,
        result
    )

    collection_key = (
        f"{rarity}|{selected_card['name']}"
    )

    st.session_state.collection[
        collection_key
    ] = (
        st.session_state.collection.get(
            collection_key,
            0
        )
        + 1
    )

    return result


def draw_many(count):

    results = []

    for _ in range(count):

        results.append(
            draw_one()
        )

    return results


# =========================================================
# 카드 HTML
#
# 중요:
# 들여쓰기된 HTML을 Markdown에 넣으면 코드블록처럼
# 출력될 수 있으므로 문자열을 한 줄씩 붙인다.
# =========================================================

def result_card_html(result):

    rarity = html.escape(
        result.get(
            "rarity",
            "F"
        )
    )

    name = html.escape(
        result.get(
            "name",
            ""
        )
    )

    description = html.escape(
        result.get(
            "description",
            ""
        )
    )

    return (
        f'<div class="gacha-card r-{rarity}">'
        f'<div class="card-name">{name}</div>'
        f'<div class="card-description">{description}</div>'
        f'</div>'
    )


def collection_card_html(
    name,
    description,
    amount
):

    safe_name = html.escape(
        name
    )

    safe_description = html.escape(
        description
    )

    return (
        '<div class="collection-card">'
        f'<div class="collection-name">{safe_name}</div>'
        f'<div class="collection-description">{safe_description}</div>'
        f'<div class="collection-count">보유 수량 {amount}장</div>'
        '</div>'
    )


# =========================================================
# 결과 카드 표시
# =========================================================

def show_results(results):

    if len(results) == 1:

        st.markdown(
            result_card_html(
                results[0]
            ),
            unsafe_allow_html=True
        )

        return

    # 10연차는 화면 가독성을 위해 2열 × 5줄이다.

    for row in range(5):

        columns = st.columns(
            2
        )

        for column_index in range(2):

            index = (
                row * 2
                + column_index
            )

            with columns[
                column_index
            ]:

                st.markdown(
                    result_card_html(
                        results[index]
                    ),
                    unsafe_allow_html=True
                )


# =========================================================
# 3D 뽑기 애니메이션
# =========================================================

def summon_animation(rarity):

    final_color = RARITY_COLORS[rarity]

    animation_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    overflow: hidden;
    background: transparent;

    font-family:
        Arial,
        sans-serif;
}

.scene {
    position: relative;

    height: 440px;

    display: flex;
    align-items: center;
    justify-content: center;

    perspective: 1200px;

    overflow: hidden;

    background:
        radial-gradient(
            circle at center,
            rgba(100,105,190,.10),
            rgba(25,25,50,.04) 35%,
            transparent 68%
        );
}


/* ======================================================
   에너지
====================================================== */

.energy {
    position: absolute;

    width: 170px;
    height: 170px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(235,238,255,.75),
            rgba(130,135,230,.16),
            transparent 70%
        );

    filter: blur(28px);

    animation:
        energy-pulse
        .50s
        ease-in-out
        infinite
        alternate;
}

@keyframes energy-pulse {

    from {
        transform: scale(.48);
        opacity: .20;
    }

    to {
        transform: scale(1.35);
        opacity: .52;
    }
}


/* ======================================================
   회전 궤도
====================================================== */

.orbit {
    position: absolute;

    width: 260px;
    height: 260px;

    border:
        1px solid
        rgba(225,230,255,.42);

    border-radius: 50%;

    animation:
        orbit-a
        .72s
        linear
        infinite;
}


.orbit.two {
    width: 205px;
    height: 205px;

    border-style: dashed;

    opacity: .65;

    animation:
        orbit-b
        .52s
        linear
        infinite;
}


.orbit.three {
    width: 320px;
    height: 320px;

    opacity: .23;

    animation:
        orbit-c
        1.1s
        linear
        infinite;
}


@keyframes orbit-a {

    from {
        transform:
            rotateX(68deg)
            rotateZ(0deg);
    }

    to {
        transform:
            rotateX(68deg)
            rotateZ(360deg);
    }
}


@keyframes orbit-b {

    from {
        transform:
            rotateY(72deg)
            rotateZ(360deg);
    }

    to {
        transform:
            rotateY(72deg)
            rotateZ(0deg);
    }
}


@keyframes orbit-c {

    from {
        transform:
            rotateX(40deg)
            rotateY(55deg)
            rotateZ(0deg);
    }

    to {
        transform:
            rotateX(40deg)
            rotateY(55deg)
            rotateZ(360deg);
    }
}


/* ======================================================
   3D 오브젝트
====================================================== */

.object {
    position: relative;

    width: 110px;
    height: 110px;

    transform-style: preserve-3d;

    z-index: 5;

    animation:
        chaos
        4s
        cubic-bezier(.45,0,.55,1)
        forwards;
}


.face {
    position: absolute;

    width: 110px;
    height: 110px;

    border:
        1px solid
        rgba(235,240,255,.75);

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,.26),
            rgba(120,130,210,.10)
        );

    box-shadow:
        inset 0 0 30px
        rgba(175,185,255,.16),

        0 0 20px
        rgba(180,190,255,.15);

    backdrop-filter:
        blur(5px);

    transition:
        all .65s ease;
}


.front {
    transform:
        rotateY(0deg)
        translateZ(55px);
}

.back {
    transform:
        rotateY(180deg)
        translateZ(55px);
}

.left {
    transform:
        rotateY(-90deg)
        translateZ(55px);
}

.right {
    transform:
        rotateY(90deg)
        translateZ(55px);
}

.top {
    transform:
        rotateX(90deg)
        translateZ(55px);
}

.bottom {
    transform:
        rotateX(-90deg)
        translateZ(55px);
}


/* ======================================================
   뽑기 중 형태 변환
====================================================== */

@keyframes chaos {

    0% {
        transform:
            rotateX(0deg)
            rotateY(0deg)
            rotateZ(0deg)
            scale(.05);
    }

    10% {
        transform:
            rotateX(160deg)
            rotateY(240deg)
            rotateZ(80deg)
            scale(1.35);
    }

    20% {
        transform:
            rotateX(390deg)
            rotateY(560deg)
            rotateZ(220deg)
            scale(.55, 1.55);
    }

    31% {
        transform:
            rotateX(650deg)
            rotateY(850deg)
            rotateZ(410deg)
            scale(1.55, .52);
    }

    42% {
        transform:
            rotateX(970deg)
            rotateY(1180deg)
            rotateZ(630deg)
            scale(.48)
            skewX(15deg);
    }

    54% {
        transform:
            rotateX(1280deg)
            rotateY(1540deg)
            rotateZ(840deg)
            scale(1.65);
    }

    66% {
        transform:
            rotateX(1570deg)
            rotateY(1900deg)
            rotateZ(1060deg)
            scale(.62, 1.45)
            skewY(-13deg);
    }

    78% {
        transform:
            rotateX(1830deg)
            rotateY(2200deg)
            rotateZ(1260deg)
            scale(1.45, .63);
    }

    89% {
        transform:
            rotateX(2070deg)
            rotateY(2440deg)
            rotateZ(1390deg)
            scale(.55);
    }

    96% {
        transform:
            rotateX(2160deg)
            rotateY(2520deg)
            rotateZ(1440deg)
            scale(1.58);
    }

    100% {
        transform:
            rotateX(25deg)
            rotateY(35deg)
            rotateZ(0deg)
            scale(1);
    }
}


/* ======================================================
   충격파
====================================================== */

.wave {
    position: absolute;

    width: 80px;
    height: 80px;

    border:
        2px solid
        rgba(230,235,255,.48);

    border-radius: 50%;

    opacity: 0;

    animation:
        shockwave
        1.05s
        ease-out
        infinite;
}


.wave.two {
    animation-delay: .34s;
}

.wave.three {
    animation-delay: .68s;
}


@keyframes shockwave {

    0% {
        transform: scale(.20);
        opacity: .62;
    }

    100% {
        transform: scale(5.5);
        opacity: 0;
    }
}


/* ======================================================
   등급 텍스트
====================================================== */

.grade {
    position: absolute;

    bottom: 22px;

    width: 100%;

    text-align: center;

    font-size: 56px;
    font-weight: 1000;

    letter-spacing: 9px;

    opacity: 0;

    transform:
        scale(.25)
        translateY(30px);

    z-index: 20;
}


.grade.show {
    animation:
        show-grade
        .65s
        cubic-bezier(.12,.85,.25,1.3)
        forwards;
}


@keyframes show-grade {

    0% {
        opacity: 0;

        transform:
            scale(.25)
            translateY(30px);
    }

    70% {
        opacity: 1;

        transform:
            scale(1.24)
            translateY(0);
    }

    100% {
        opacity: 1;

        transform:
            scale(1)
            translateY(0);
    }
}


/* ======================================================
   플래시
====================================================== */

.flash {
    position: absolute;

    inset: 0;

    background: white;

    opacity: 0;

    pointer-events: none;

    z-index: 15;
}


.flash.go {
    animation:
        flash-animation
        .46s
        ease-out;
}


@keyframes flash-animation {

    0% {
        opacity: 0;
    }

    30% {
        opacity: .82;
    }

    100% {
        opacity: 0;
    }
}


/* ======================================================
   파티클
====================================================== */

.particle {
    position: absolute;

    left: 50%;
    top: 50%;

    width: 4px;
    height: 4px;

    border-radius: 50%;

    background: white;

    opacity: 0;

    animation:
        particle-animation
        2s
        linear
        infinite;
}


@keyframes particle-animation {

    0% {
        transform:
            translate(0,0)
            scale(.2);

        opacity: 0;
    }

    20% {
        opacity: .60;
    }

    100% {
        transform:
            translate(
                var(--x),
                var(--y)
            )
            scale(1.7);

        opacity: 0;
    }
}

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
    <div class="wave two"></div>
    <div class="wave three"></div>

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

const rarity =
    "__RARITY__";

const finalColor =
    "__FINAL_COLOR__";


const object =
    document.getElementById(
        "object"
    );

const faces =
    document.querySelectorAll(
        ".face"
    );

const energy =
    document.getElementById(
        "energy"
    );

const orbit1 =
    document.getElementById(
        "orbit1"
    );

const orbit2 =
    document.getElementById(
        "orbit2"
    );

const orbit3 =
    document.getElementById(
        "orbit3"
    );

const flash =
    document.getElementById(
        "flash"
    );

const grade =
    document.getElementById(
        "grade"
    );

const scene =
    document.querySelector(
        ".scene"
    );


/* ======================================================
   파티클 생성
====================================================== */

for (
    let i = 0;
    i < 40;
    i++
) {

    const particle =
        document.createElement(
            "div"
        );

    particle.className =
        "particle";

    const angle =
        Math.random()
        * Math.PI
        * 2;

    const distance =
        150
        + Math.random()
        * 220;

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

    particle.style.animationDelay =
        (
            Math.random()
            * 2
        )
        + "s";

    scene.appendChild(
        particle
    );
}


/* ======================================================
   4초 후 결과 형태로 정지
====================================================== */

setTimeout(
    () => {

        flash.classList.add(
            "go"
        );

        object.style.animation =
            "none";


        if (
            rarity === "F"
        ) {

            object.style.transform =
                "rotateX(12deg) rotateY(28deg) scale(.82)";
        }

        else if (
            rarity === "E"
        ) {

            object.style.transform =
                "rotateX(22deg) rotateY(35deg) rotateZ(10deg) scale(.90)";
        }

        else if (
            rarity === "D"
        ) {

            object.style.transform =
                "rotateX(45deg) rotateY(45deg) rotateZ(45deg) scale(.98)";
        }

        else if (
            rarity === "C"
        ) {

            object.style.transform =
                "rotateX(40deg) rotateY(45deg) rotateZ(45deg) scale(1.05,1.18)";
        }

        else if (
            rarity === "B"
        ) {

            object.style.transform =
                "rotateX(30deg) rotateY(45deg) rotateZ(45deg) scale(1.17,1.32)";
        }

        else if (
            rarity === "A"
        ) {

            object.style.transform =
                "rotateX(25deg) rotateY(45deg) rotateZ(45deg) scale(1.28,1.42)";
        }

        else if (
            rarity === "S"
        ) {

            object.style.transform =
                "rotateX(45deg) rotateY(45deg) rotateZ(45deg) scale(1.42)";
        }

        else if (
            rarity === "SS"
        ) {

            object.style.transform =
                "rotateX(25deg) rotateY(45deg) scale(1.58)";
        }

        else {

            object.style.transform =
                "rotateX(45deg) rotateY(45deg) rotateZ(45deg) scale(1.78)";
        }


        faces.forEach(
            face => {

                face.style.borderColor =
                    finalColor;

                face.style.background =
                    "linear-gradient("
                    + "135deg,"
                    + finalColor
                    + "88,"
                    + finalColor
                    + "12"
                    + ")";

                face.style.boxShadow =
                    "inset 0 0 38px "
                    + finalColor
                    + ", 0 0 50px "
                    + finalColor;

            }
        );


        energy.style.background =
            "radial-gradient("
            + "circle,"
            + finalColor
            + ","
            + finalColor
            + "50,"
            + "transparent 70%"
            + ")";


        orbit1.style.borderColor =
            finalColor;

        orbit2.style.borderColor =
            finalColor;

        orbit3.style.borderColor =
            finalColor;


        orbit1.style.boxShadow =
            "0 0 32px "
            + finalColor;

        orbit2.style.boxShadow =
            "0 0 25px "
            + finalColor;

    },
    4000
);


/* ======================================================
   도형이 멈춘 뒤 등급 공개
====================================================== */

setTimeout(
    () => {

        grade.innerText =
            rarity;

        grade.style.color =
            finalColor;

        grade.style.textShadow =
            "0 0 10px "
            + finalColor
            + ", 0 0 28px "
            + finalColor
            + ", 0 0 60px "
            + finalColor;

        grade.classList.add(
            "show"
        );

    },
    4550
);

</script>

</body>
</html>
"""

    # f-string을 사용하지 않고 필요한 값만 치환한다.
    animation_html = animation_html.replace(
        "__RARITY__",
        rarity
    )

    animation_html = animation_html.replace(
        "__FINAL_COLOR__",
        final_color
    )

    components.html(
        animation_html,
        height=450,
        scrolling=False
    )

    # 애니메이션 종료 뒤 카드가 나오게 한다.
    time.sleep(5.15)
# =========================================================
# 사이드바
# =========================================================

st.sidebar.markdown(
    "## 🎴 성지온 냄새 뽑기"
)

st.sidebar.caption(
    "메뉴를 선택하면 해당 화면만 표시된다."
)

page = st.sidebar.radio(
    "메뉴",
    [
        "🎲 뽑기",
        "📚 카드 목록",
        "🕘 뽑기 기록",
    ],
    label_visibility="collapsed"
)


st.sidebar.divider()


st.sidebar.metric(
    "총 뽑기",
    st.session_state.total_pulls
)


st.sidebar.metric(
    "수집 카드",
    f"{len(st.session_state.collection)} / {TOTAL_CARD_TYPES}"
)


# =========================================================
# 뽑기 페이지
# =========================================================

if page == "🎲 뽑기":

    st.markdown(
        '<div class="main-title">🎴 성지온 냄새 뽑기 🎴</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">137종의 성지온 냄새 카드를 수집하라</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # 천장
    # =====================================================

    pity_progress = (
        st.session_state.total_pulls
        % 100
    )

    remaining = (
        100
        - pity_progress
    )


    st.markdown(
        (
            '<div class="status-panel">'
            '<div class="status-title">👑 SS 확정 천장</div>'
            f'<div class="status-value">{remaining}회</div>'
            '<div class="status-small">100번째마다 SS 등급이 확정된다.</div>'
            '</div>'
        ),
        unsafe_allow_html=True
    )


    st.progress(
        pity_progress
        / 100
    )


    # =====================================================
    # 버튼
    # =====================================================

    st.write("")

    button_1,
    button_10 = st.columns(
        2
    )


    with button_1:

        single = st.button(
            "🎲 1회 뽑기",
            type="primary",
            use_container_width=True
        )


    with button_10:

        multi = st.button(
            "🔥 10회 뽑기",
            use_container_width=True
        )


    # =====================================================
    # 1회 뽑기
    # =====================================================

    if single:

        result = draw_one()

        st.session_state.last_results = [
            result
        ]

        summon_animation(
            result["rarity"]
        )


        if result.get(
            "pity",
            False
        ):

            st.toast(
                "100회 천장으로 SS가 등장했다.",
                icon="👑"
            )


        if result["rarity"] in [
            "SS",
            "SSS"
        ]:

            st.balloons()


    # =====================================================
    # 10회 뽑기
    # =====================================================

    if multi:

        results = draw_many(
            10
        )

        st.session_state.last_results = (
            results
        )


        highest = max(
            results,
            key=lambda result:
                RARITY_ORDER[
                    result["rarity"]
                ]
        )


        summon_animation(
            highest["rarity"]
        )


        if any(
            result.get(
                "pity",
                False
            )
            for result
            in results
        ):

            st.toast(
                "이번 10연차에서 SS 천장이 발동했다.",
                icon="👑"
            )


        if any(
            result["rarity"]
            in ["SS", "SSS"]
            for result
            in results
        ):

            st.balloons()


    # =====================================================
    # 가장 최근 결과
    # =====================================================

    if st.session_state.last_results:

        st.divider()

        st.markdown(
            "### 최근 뽑기 결과"
        )

        show_results(
            st.session_state.last_results
        )


    # =====================================================
    # 하단 간단 통계
    # =====================================================

    st.divider()

    stat1,
    stat2,
    stat3 = st.columns(
        3
    )


    with stat1:

        st.metric(
            "총 뽑기",
            st.session_state.total_pulls
        )


    with stat2:

        st.metric(
            "수집 카드",
            f"{len(st.session_state.collection)} / {TOTAL_CARD_TYPES}"
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


    # =====================================================
    # 확률
    # =====================================================

    with st.expander(
        "📊 등급별 확률"
    ):

        for rarity, probability in zip(
            RARITIES,
            PROBABILITIES
        ):

            st.write(
                f"**{rarity}** · "
                f"{probability}% · "
                f"{len(CARDS[rarity])}종"
            )


# =========================================================
# 카드 목록 페이지
# =========================================================

elif page == "📚 카드 목록":

    st.title(
        "📚 카드 목록"
    )

    st.caption(
        f"전체 {TOTAL_CARD_TYPES}종 중 "
        f"{len(st.session_state.collection)}종을 발견했다."
    )


    rarity_tabs = st.tabs(
        RARITIES
    )


    for tab, rarity in zip(
        rarity_tabs,
        RARITIES
    ):

        with tab:

            st.subheader(
                f"{rarity} 등급"
            )

            st.caption(
                f"총 {len(CARDS[rarity])}종"
            )


            collected_in_rarity = 0

            for card in CARDS[
                rarity
            ]:

                key = (
                    f"{rarity}|"
                    f"{card['name']}"
                )

                amount = (
                    st.session_state.collection.get(
                        key,
                        0
                    )
                )

                if amount > 0:

                    collected_in_rarity += 1

                    st.markdown(
                        collection_card_html(
                            card["name"],
                            card["description"],
                            amount
                        ),
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        (
                            '<div class="collection-card">'
                            '<div class="collection-name" '
                            'style="opacity:.36;">'
                            '❓ 아직 발견하지 못한 카드'
                            '</div>'
                            '</div>'
                        ),
                        unsafe_allow_html=True
                    )


            st.caption(
                f"{collected_in_rarity} / "
                f"{len(CARDS[rarity])}종 수집"
            )


# =========================================================
# 뽑기 기록 페이지
# =========================================================

elif page == "🕘 뽑기 기록":

    st.title(
        "🕘 뽑기 기록"
    )


    if not (
        st.session_state.history
    ):

        st.info(
            "아직 뽑기 기록이 없다."
        )

    else:

        filter_rarity = st.selectbox(
            "등급 필터",
            [
                "전체"
            ]
            + RARITIES
        )


        if filter_rarity == "전체":

            filtered_history = (
                st.session_state.history
            )

        else:

            filtered_history = [

                result

                for result
                in st.session_state.history

                if result.get(
                    "rarity"
                )
                == filter_rarity

            ]


        st.caption(
            f"{len(filtered_history)}개의 기록을 표시한다."
        )


        for result in (
            filtered_history[:200]
        ):

            rarity = html.escape(
                result.get(
                    "rarity",
                    "?"
                )
            )

            name = html.escape(
                result.get(
                    "name",
                    "알 수 없는 카드"
                )
            )

            number = (
                result.get(
                    "pull_number",
                    "?"
                )
            )

            pity_text = (
                " · 천장"
                if result.get(
                    "pity",
                    False
                )
                else ""
            )


            st.markdown(
                (
                    '<div class="history-item">'
                    f'<div class="history-rarity">'
                    f'#{number} · {rarity}{pity_text}'
                    '</div>'
                    f'<div class="history-name">'
                    f'{name}'
                    '</div>'
                    '</div>'
                ),
                unsafe_allow_html=True
            )


        st.divider()


        if st.button(
            "🗑️ 모든 뽑기 기록 초기화",
            type="secondary"
        ):

            st.session_state.total_pulls = 0

            st.session_state.history = []

            st.session_state.collection = {}

            st.session_state.last_results = []

            st.rerun()
