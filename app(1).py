
import streamlit as st
import streamlit.components.v1 as components
import random
import time
import html

st.set_page_config(
    page_title="성지온 냄새 뽑기",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 기본 설정
# =========================================================

PULL_COST = 100
TEN_PULL_COST = 900
STARTING_CURRENCY = 300
PITY_INTERVAL = 100

RARITIES = ["F", "E", "D", "C", "B", "A", "S", "SS", "SSS"]

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
    "F": 0, "E": 1, "D": 2, "C": 3, "B": 4,
    "A": 5, "S": 6, "SS": 7, "SSS": 8
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
# 전체 CSS
# =========================================================

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% -12%, #30305a 0%, #18182d 30%, #0c0c18 58%, #050509 100%);
    color: #f5f5ff;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111120, #090911);
    border-right: 1px solid rgba(255,255,255,.07);
}

[data-testid="stSidebar"] * {
    color: #eeeeff;
}

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 1000;
    margin-bottom: 3px;
    background: linear-gradient(90deg, #ffffff, #b9c5ff, #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 18px rgba(160,170,255,.28));
}

.subtitle {
    text-align: center;
    font-size: 16px;
    color: rgba(230,232,255,.62);
    margin-bottom: 28px;
}

.status-panel {
    padding: 22px 24px;
    border-radius: 22px;
    background:
        radial-gradient(circle at 50% 0%, rgba(100,100,190,.11), transparent 55%),
        linear-gradient(145deg, rgba(26,26,49,.92), rgba(10,10,21,.96));
    border: 1px solid rgba(255,255,255,.09);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.035), 0 16px 45px rgba(0,0,0,.30);
    text-align: center;
    margin-bottom: 14px;
}

.status-title {
    color: rgba(235,237,255,.70);
    font-size: 14px;
    margin-bottom: 7px;
}

.status-value {
    font-size: 31px;
    font-weight: 1000;
    color: #ffffff;
}

.status-small {
    font-size: 13px;
    color: rgba(225,228,245,.50);
    margin-top: 5px;
}

.currency-panel {
    padding: 18px 20px;
    border-radius: 18px;
    background: linear-gradient(145deg, rgba(36,34,66,.95), rgba(12,12,24,.96));
    border: 1px solid rgba(200,190,255,.16);
    box-shadow: 0 12px 35px rgba(0,0,0,.25);
    text-align: center;
}

.currency-title {
    font-size: 13px;
    color: rgba(235,235,255,.62);
}

.currency-value {
    margin-top: 5px;
    font-size: 28px;
    font-weight: 1000;
}

.gacha-card {
    min-height: 220px;
    padding: 30px 27px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-radius: 24px;
    background:
        radial-gradient(circle at 50% 0%, rgba(105,105,180,.10), transparent 50%),
        linear-gradient(145deg, rgba(24,24,46,.98), rgba(8,8,17,.99));
    border: 1px solid rgba(255,255,255,.10);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.045), 0 18px 50px rgba(0,0,0,.33);
    transition: transform .25s ease, box-shadow .25s ease;
    margin: 8px 0 18px 0;
}

.gacha-card:hover {
    transform: translateY(-4px) scale(1.008);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.07), 0 22px 58px rgba(0,0,0,.40);
}

.card-name {
    text-align: center;
    color: #f5f5ff;
    font-size: 21px;
    line-height: 1.55;
    font-weight: 900;
    margin-bottom: 18px;
    word-break: keep-all;
}

.card-description {
    text-align: center;
    color: rgba(222,224,242,.68);
    font-size: 14px;
    line-height: 1.75;
    word-break: keep-all;
}

.r-F { border-color: rgba(160,160,170,.25); }
.r-E { border-color: rgba(183,138,94,.30); }
.r-D { border-color: rgba(90,220,130,.33); }
.r-C { border-color: rgba(76,174,255,.37); }
.r-B { border-color: rgba(170,100,255,.42); }
.r-A { border-color: rgba(255,91,177,.45); }
.r-S {
    border-color: rgba(255,220,75,.58);
    box-shadow: 0 0 24px rgba(255,220,75,.08), 0 18px 50px rgba(0,0,0,.34);
}
.r-SS {
    border-color: rgba(220,250,255,.72);
    box-shadow: 0 0 25px rgba(85,220,255,.13), 0 0 50px rgba(180,100,255,.07), 0 18px 50px rgba(0,0,0,.34);
}
.r-SSS {
    border-color: rgba(255,255,255,.88);
    animation: sss-card-glow 2.3s linear infinite;
}

@keyframes sss-card-glow {
    0% { box-shadow: 0 0 25px rgba(255,80,120,.18), 0 18px 50px rgba(0,0,0,.35); }
    33% { box-shadow: 0 0 28px rgba(80,220,255,.20), 0 18px 50px rgba(0,0,0,.35); }
    66% { box-shadow: 0 0 28px rgba(180,90,255,.22), 0 18px 50px rgba(0,0,0,.35); }
    100% { box-shadow: 0 0 25px rgba(255,80,120,.18), 0 18px 50px rgba(0,0,0,.35); }
}

.collection-card {
    padding: 20px 22px;
    margin-bottom: 12px;
    border-radius: 17px;
    background: linear-gradient(145deg, rgba(25,25,46,.86), rgba(10,10,19,.93));
    border: 1px solid rgba(255,255,255,.07);
}

.collection-name {
    font-weight: 850;
    font-size: 16px;
    color: #f3f3ff;
    line-height: 1.5;
}

.collection-description {
    margin-top: 9px;
    font-size: 13px;
    line-height: 1.65;
    color: rgba(222,224,242,.60);
}

.collection-count {
    margin-top: 10px;
    font-size: 12px;
    color: rgba(215,218,238,.42);
}

.history-item {
    padding: 15px 18px;
    border-radius: 14px;
    margin-bottom: 9px;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.055);
}

.history-rarity {
    font-size: 13px;
    font-weight: 900;
    color: rgba(200,205,255,.70);
    margin-bottom: 5px;
}

.history-name {
    font-size: 15px;
    font-weight: 750;
    color: #eeeeff;
    line-height: 1.5;
}

.game-panel {
    padding: 24px;
    border-radius: 20px;
    background:
        radial-gradient(circle at 50% 0%, rgba(120,100,210,.11), transparent 60%),
        linear-gradient(145deg, rgba(23,23,45,.95), rgba(9,9,18,.98));
    border: 1px solid rgba(255,255,255,.08);
    box-shadow: 0 16px 40px rgba(0,0,0,.28);
    margin-bottom: 16px;
}

.game-title {
    font-size: 22px;
    font-weight: 900;
    margin-bottom: 8px;
}

.game-desc {
    color: rgba(225,228,245,.65);
    line-height: 1.7;
    font-size: 14px;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,.03);
    padding: 15px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,.06);
}

div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #8787ff, #d5b3ff);
}

.stButton > button {
    border-radius: 14px;
    min-height: 48px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 카드 설명 생성
# =========================================================

def make_cards(names, rarity):
    descriptions = {
        "F": ["모든 전설과 미사여구가 시작되기 전의 가장 순수한 기본 형태다."],
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
        ],
    }

    cards = []
    for index, name in enumerate(names):
        cards.append({
            "name": name,
            "description": descriptions[rarity][index % len(descriptions[rarity])]
        })
    return cards

# =========================================================
# 카드 데이터
# =========================================================

CARDS = {}

CARDS["F"] = make_cards(["성지온"], "F")

CARDS["E"] = make_cards([
    "은은하게 감지되는 성지온의 냄새",
    "복도 끝에서 먼저 도착한 성지온의 냄새",
    "바람결에 살짝 실려 온 성지온의 냄새",
    "어딘가 익숙하게 느껴지는 성지온의 냄새",
    "조용히 존재감을 드러내는 성지온의 냄새",
], "E")

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
CARDS["C"] = make_cards([f"{a} {b}" for a in C_PREFIX for b in C_CORE], "C")

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
CARDS["B"] = make_cards([f"{a} {b}" for a in B_PREFIX for b in B_CORE], "B")

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
CARDS["A"] = make_cards([f"{a} {b}" for a in A_PREFIX for b in A_CORE], "A")

CARDS["S"] = make_cards([
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
], "S")

CARDS["SS"] = make_cards([
    "『천상천하 유아독존 · 억겁성광을 두른 성지온의 궁극초월신성 대냄새』",
    "『태초와 종말의 별들이 동시에 경배하는 성지온의 영겁무한천상 대냄새』",
    "『삼천세계와 구천은하를 관통하여 시공간 그 자체에 새겨진 성지온의 절대 대냄새』",
    "『일월성신과 천지만물이 일제히 찬송하는 성지온의 천상천하무쌍 대냄새』",
    "『우주의 시작과 끝을 목격하고도 끝내 사라지지 않은 성지온의 극광초월 대냄새』",
], "SS")

CARDS["SSS"] = make_cards(["그냥 성지온"], "SSS")

TOTAL_CARD_TYPES = sum(len(cards) for cards in CARDS.values())

# =========================================================
# 세션 상태
# =========================================================

DEFAULTS = {
    "total_pulls": 0,
    "history": [],
    "collection": {},
    "last_results": [],
    "currency": STARTING_CURRENCY,
    "memory_sequence": None,
    "memory_hidden": False,
    "memory_round": 0,
    "math_question": None,
    "math_answer": None,
    "math_round": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, (dict, list)) else value

# 이전 버전 데이터 보정
clean_history = []
for item in st.session_state.history:
    if not isinstance(item, dict):
        continue
    item.setdefault("pity", False)
    item.setdefault("pull_number", 0)
    item.setdefault("rarity", "F")
    item.setdefault("name", "알 수 없는 카드")
    item.setdefault("description", "")
    clean_history.append(item)
st.session_state.history = clean_history

# =========================================================
# 뽑기 로직
# =========================================================

def draw_one():
    next_pull = st.session_state.total_pulls + 1
    pity = (next_pull % PITY_INTERVAL == 0)

    if pity:
        rarity = "SS"
    else:
        rarity = random.choices(RARITIES, weights=PROBABILITIES, k=1)[0]

    selected_card = random.choice(CARDS[rarity])

    st.session_state.total_pulls = next_pull

    result = {
        "pull_number": next_pull,
        "rarity": rarity,
        "name": selected_card["name"],
        "description": selected_card["description"],
        "pity": pity,
    }

    st.session_state.history.insert(0, result)

    collection_key = f"{rarity}|{selected_card['name']}"
    st.session_state.collection[collection_key] = (
        st.session_state.collection.get(collection_key, 0) + 1
    )

    return result

def draw_many(count):
    return [draw_one() for _ in range(count)]

# =========================================================
# 카드 HTML
# =========================================================

def result_card_html(result):
    rarity = html.escape(result.get("rarity", "F"))
    name = html.escape(result.get("name", ""))
    description = html.escape(result.get("description", ""))

    return (
        f'<div class="gacha-card r-{rarity}">'
        f'<div class="card-name">{name}</div>'
        f'<div class="card-description">{description}</div>'
        f'</div>'
    )

def collection_card_html(name, description, amount):
    safe_name = html.escape(name)
    safe_description = html.escape(description)

    return (
        '<div class="collection-card">'
        f'<div class="collection-name">{safe_name}</div>'
        f'<div class="collection-description">{safe_description}</div>'
        f'<div class="collection-count">보유 수량 {amount}장</div>'
        '</div>'
    )

def show_results(results):
    if len(results) == 1:
        st.markdown(result_card_html(results[0]), unsafe_allow_html=True)
        return

    for row in range(5):
        cols = st.columns(2)
        for col_idx in range(2):
            idx = row * 2 + col_idx
            with cols[col_idx]:
                st.markdown(result_card_html(results[idx]), unsafe_allow_html=True)

# =========================================================
# 화려한 애니메이션
# =========================================================

def summon_animation(rarity):
    final_color = RARITY_COLORS[rarity]
    rarity_level = RARITY_ORDER[rarity]

    animation_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    overflow: hidden;
    background: transparent;
    font-family: Arial, sans-serif;
}

.scene {
    position: relative;
    height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 1300px;
    overflow: hidden;
    background:
        radial-gradient(circle at 50% 48%, rgba(120,130,255,.11), transparent 24%),
        radial-gradient(circle at center, rgba(60,65,120,.08), transparent 70%);
}

.vortex {
    position: absolute;
    width: 390px;
    height: 390px;
    border-radius: 50%;
    background:
        conic-gradient(
            from 0deg,
            transparent,
            rgba(255,255,255,.12),
            transparent,
            rgba(160,150,255,.15),
            transparent
        );
    filter: blur(2px);
    animation: vortexSpin 1.3s linear infinite;
    opacity: .55;
}

@keyframes vortexSpin {
    from { transform: rotate(0deg) scale(.8); }
    to { transform: rotate(360deg) scale(1.1); }
}

.energy {
    position: absolute;
    width: 190px;
    height: 190px;
    border-radius: 50%;
    background:
        radial-gradient(circle, rgba(255,255,255,.80), rgba(135,145,255,.18), transparent 70%);
    filter: blur(30px);
    animation: energyPulse .45s ease-in-out infinite alternate;
}

@keyframes energyPulse {
    from { transform: scale(.45); opacity: .22; }
    to { transform: scale(1.45); opacity: .62; }
}

.orbit {
    position: absolute;
    width: 270px;
    height: 270px;
    border: 1px solid rgba(230,235,255,.40);
    border-radius: 50%;
    animation: orbitA .72s linear infinite;
}

.orbit.o2 {
    width: 215px;
    height: 215px;
    border-style: dashed;
    opacity: .70;
    animation: orbitB .50s linear infinite;
}

.orbit.o3 {
    width: 330px;
    height: 330px;
    opacity: .25;
    animation: orbitC 1.05s linear infinite;
}

.orbit.o4 {
    width: 375px;
    height: 160px;
    opacity: .20;
    animation: orbitD .80s linear infinite;
}

@keyframes orbitA {
    from { transform: rotateX(70deg) rotateZ(0deg); }
    to { transform: rotateX(70deg) rotateZ(360deg); }
}
@keyframes orbitB {
    from { transform: rotateY(72deg) rotateZ(360deg); }
    to { transform: rotateY(72deg) rotateZ(0deg); }
}
@keyframes orbitC {
    from { transform: rotateX(38deg) rotateY(55deg) rotateZ(0deg); }
    to { transform: rotateX(38deg) rotateY(55deg) rotateZ(360deg); }
}
@keyframes orbitD {
    from { transform: rotateX(72deg) rotateY(35deg) rotateZ(0deg); }
    to { transform: rotateX(72deg) rotateY(35deg) rotateZ(-360deg); }
}

.object {
    position: relative;
    width: 112px;
    height: 112px;
    transform-style: preserve-3d;
    z-index: 10;
    animation: chaos 4.6s cubic-bezier(.45,0,.55,1) forwards;
}

.face {
    position: absolute;
    width: 112px;
    height: 112px;
    border: 1px solid rgba(240,245,255,.78);
    background:
        linear-gradient(135deg, rgba(255,255,255,.28), rgba(120,130,220,.10));
    box-shadow:
        inset 0 0 32px rgba(175,185,255,.17),
        0 0 22px rgba(190,200,255,.16);
    backdrop-filter: blur(5px);
    transition: all .7s ease;
}

.front  { transform: rotateY(0deg) translateZ(56px); }
.back   { transform: rotateY(180deg) translateZ(56px); }
.left   { transform: rotateY(-90deg) translateZ(56px); }
.right  { transform: rotateY(90deg) translateZ(56px); }
.top    { transform: rotateX(90deg) translateZ(56px); }
.bottom { transform: rotateX(-90deg) translateZ(56px); }

.core {
    position: absolute;
    inset: 30px;
    border-radius: 50%;
    background: rgba(255,255,255,.86);
    box-shadow: 0 0 25px white;
    animation: coreBeat .35s ease-in-out infinite alternate;
    z-index: 20;
}

@keyframes coreBeat {
    from { transform: scale(.55); opacity: .55; }
    to { transform: scale(1.25); opacity: 1; }
}

@keyframes chaos {
    0%   { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale(.03); }
    8%   { transform: rotateX(160deg) rotateY(240deg) rotateZ(80deg) scale(1.25); }
    16%  { transform: rotateX(340deg) rotateY(500deg) rotateZ(180deg) scale(.52,1.55); }
    24%  { transform: rotateX(570deg) rotateY(760deg) rotateZ(320deg) scale(1.55,.50); }
    32%  { transform: rotateX(830deg) rotateY(1040deg) rotateZ(490deg) scale(.58) skewX(18deg); }
    40%  { transform: rotateX(1120deg) rotateY(1340deg) rotateZ(690deg) scale(1.70); }
    48%  { transform: rotateX(1380deg) rotateY(1660deg) rotateZ(880deg) scale(.55,1.42) skewY(-16deg); }
    56%  { transform: rotateX(1660deg) rotateY(1940deg) rotateZ(1050deg) scale(1.40,.62); }
    64%  { transform: rotateX(1900deg) rotateY(2190deg) rotateZ(1210deg) scale(.50); }
    72%  { transform: rotateX(2120deg) rotateY(2440deg) rotateZ(1370deg) scale(1.72); }
    80%  { transform: rotateX(2350deg) rotateY(2720deg) rotateZ(1510deg) scale(.62,1.45); }
    88%  { transform: rotateX(2560deg) rotateY(2980deg) rotateZ(1660deg) scale(1.50,.62); }
    95%  { transform: rotateX(2760deg) rotateY(3240deg) rotateZ(1800deg) scale(.55); }
    100% { transform: rotateX(25deg) rotateY(35deg) rotateZ(0deg) scale(1); }
}

.shard {
    position: absolute;
    width: 18px;
    height: 55px;
    background: linear-gradient(180deg, rgba(255,255,255,.7), rgba(170,180,255,.08));
    clip-path: polygon(50% 0%, 100% 55%, 50% 100%, 0% 55%);
    opacity: .42;
    transform-origin: 50% 220px;
    animation: shardSpin 1.8s linear infinite;
}

@keyframes shardSpin {
    from { transform: rotate(var(--r)) translateY(-165px) rotate(0deg) scale(.7); }
    to { transform: rotate(calc(var(--r) + 360deg)) translateY(-165px) rotate(360deg) scale(1.15); }
}

.wave {
    position: absolute;
    width: 80px;
    height: 80px;
    border: 2px solid rgba(235,240,255,.52);
    border-radius: 50%;
    opacity: 0;
    animation: shock 1.1s ease-out infinite;
}
.wave.w2 { animation-delay: .32s; }
.wave.w3 { animation-delay: .64s; }

@keyframes shock {
    0% { transform: scale(.2); opacity: .70; }
    100% { transform: scale(6); opacity: 0; }
}

.burst {
    position: absolute;
    width: 10px;
    height: 10px;
    opacity: 0;
    z-index: 16;
}

.burst::before,
.burst::after {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    background: white;
    transform-origin: center;
}
.burst::before {
    width: 300px;
    height: 3px;
    transform: translate(-50%,-50%);
}
.burst::after {
    width: 3px;
    height: 300px;
    transform: translate(-50%,-50%);
}

.burst.go {
    animation: burstAnim .6s ease-out;
}
@keyframes burstAnim {
    0% { opacity: 0; transform: scale(.2) rotate(0deg); }
    30% { opacity: .95; transform: scale(1.2) rotate(25deg); }
    100% { opacity: 0; transform: scale(1.8) rotate(45deg); }
}

.lightning {
    position: absolute;
    width: 4px;
    height: 170px;
    background: white;
    opacity: 0;
    filter: drop-shadow(0 0 10px white);
    clip-path: polygon(35% 0, 65% 0, 55% 42%, 90% 42%, 35% 100%, 48% 56%, 10% 56%);
    z-index: 17;
}
.lightning.l1 { transform: rotate(28deg) translateX(-140px); }
.lightning.l2 { transform: rotate(-32deg) translateX(140px); }

.lightning.go {
    animation: lightningFlash .55s steps(2,end) 2;
}
@keyframes lightningFlash {
    0%,100% { opacity: 0; }
    45%,55% { opacity: .95; }
}

.flash {
    position: absolute;
    inset: 0;
    background: white;
    opacity: 0;
    z-index: 18;
    pointer-events: none;
}
.flash.go { animation: flashAnim .55s ease-out; }
@keyframes flashAnim {
    0% { opacity: 0; }
    28% { opacity: .88; }
    100% { opacity: 0; }
}

.grade {
    position: absolute;
    bottom: 18px;
    width: 100%;
    text-align: center;
    font-size: 62px;
    font-weight: 1000;
    letter-spacing: 10px;
    opacity: 0;
    transform: scale(.25) translateY(32px);
    z-index: 25;
}
.grade.show {
    animation: gradeShow .70s cubic-bezier(.12,.85,.25,1.3) forwards;
}
@keyframes gradeShow {
    0% { opacity: 0; transform: scale(.25) translateY(32px); }
    70% { opacity: 1; transform: scale(1.28) translateY(0); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

.particle {
    position: absolute;
    left: 50%;
    top: 50%;
    width: var(--size);
    height: var(--size);
    border-radius: 50%;
    background: white;
    opacity: 0;
    animation: particleFly var(--speed) linear infinite;
}

@keyframes particleFly {
    0% { transform: translate(0,0) scale(.2); opacity: 0; }
    20% { opacity: .65; }
    100% { transform: translate(var(--x), var(--y)) scale(1.6); opacity: 0; }
}

.scene.high .vortex { opacity: .85; filter: blur(0); }
.scene.high .orbit { border-width: 2px; }

.scene.sss {
    animation: rainbowScene 1.2s linear infinite;
}
@keyframes rainbowScene {
    0% { filter: hue-rotate(0deg) brightness(1.05); }
    100% { filter: hue-rotate(360deg) brightness(1.18); }
}
</style>
</head>

<body>
<div class="scene" id="scene">
    <div class="vortex" id="vortex"></div>
    <div class="energy" id="energy"></div>

    <div class="orbit" id="orbit1"></div>
    <div class="orbit o2" id="orbit2"></div>
    <div class="orbit o3" id="orbit3"></div>
    <div class="orbit o4" id="orbit4"></div>

    <div class="wave"></div>
    <div class="wave w2"></div>
    <div class="wave w3"></div>

    <div class="object" id="object">
        <div class="face front"></div>
        <div class="face back"></div>
        <div class="face left"></div>
        <div class="face right"></div>
        <div class="face top"></div>
        <div class="face bottom"></div>
        <div class="core" id="core"></div>
    </div>

    <div class="burst" id="burst"></div>
    <div class="lightning l1" id="l1"></div>
    <div class="lightning l2" id="l2"></div>
    <div class="flash" id="flash"></div>
    <div class="grade" id="grade"></div>
</div>

<script>
const rarity = "__RARITY__";
const finalColor = "__FINAL_COLOR__";
const level = Number("__RARITY_LEVEL__");

const scene = document.getElementById("scene");
const object = document.getElementById("object");
const faces = document.querySelectorAll(".face");
const energy = document.getElementById("energy");
const vortex = document.getElementById("vortex");
const orbit1 = document.getElementById("orbit1");
const orbit2 = document.getElementById("orbit2");
const orbit3 = document.getElementById("orbit3");
const orbit4 = document.getElementById("orbit4");
const flash = document.getElementById("flash");
const burst = document.getElementById("burst");
const l1 = document.getElementById("l1");
const l2 = document.getElementById("l2");
const grade = document.getElementById("grade");
const core = document.getElementById("core");

if (level >= 6) scene.classList.add("high");
if (rarity === "SSS") scene.classList.add("sss");

// 파티클
const particleCount = 46 + level * 7;
for (let i = 0; i < particleCount; i++) {
    const p = document.createElement("div");
    p.className = "particle";

    const angle = Math.random() * Math.PI * 2;
    const distance = 150 + Math.random() * (170 + level * 20);
    const x = Math.cos(angle) * distance;
    const y = Math.sin(angle) * distance;

    p.style.setProperty("--x", x + "px");
    p.style.setProperty("--y", y + "px");
    p.style.setProperty("--size", (2 + Math.random() * 4) + "px");
    p.style.setProperty("--speed", (1.1 + Math.random() * 1.7) + "s");
    p.style.animationDelay = (Math.random() * 1.8) + "s";
    scene.appendChild(p);
}

// 조각
const shardCount = 8 + Math.max(0, level - 3) * 2;
for (let i = 0; i < shardCount; i++) {
    const s = document.createElement("div");
    s.className = "shard";
    s.style.setProperty("--r", (i * (360 / shardCount)) + "deg");
    s.style.animationDelay = (i * 0.06) + "s";
    scene.appendChild(s);
}

// 중간 단계 연출 1
setTimeout(() => {
    vortex.style.transform = "scale(1.25)";
    energy.style.filter = "blur(18px)";
}, 1500);

// 중간 단계 연출 2
setTimeout(() => {
    orbit1.style.animationDuration = ".38s";
    orbit2.style.animationDuration = ".30s";
    orbit3.style.animationDuration = ".55s";
    orbit4.style.animationDuration = ".42s";
}, 2800);

// 고등급이면 결과 직전 번개
setTimeout(() => {
    if (level >= 6) {
        l1.classList.add("go");
        l2.classList.add("go");
    }
}, 3900);

// 결과 형태로 정지
setTimeout(() => {
    flash.classList.add("go");
    burst.classList.add("go");
    object.style.animation = "none";

    if (rarity === "F") {
        object.style.transform = "rotateX(12deg) rotateY(28deg) scale(.82)";
    } else if (rarity === "E") {
        object.style.transform = "rotateX(22deg) rotateY(35deg) rotateZ(10deg) scale(.90)";
    } else if (rarity === "D") {
        object.style.transform = "rotateX(45deg) rotateY(45deg) rotateZ(45deg) scale(.98)";
    } else if (rarity === "C") {
        object.style.transform = "rotateX(40deg) rotateY(45deg) rotateZ(45deg) scale(1.05,1.18)";
    } else if (rarity === "B") {
        object.style.transform = "rotateX(30deg) rotateY(45deg) rotateZ(45deg) scale(1.17,1.32)";
    } else if (rarity === "A") {
        object.style.transform = "rotateX(25deg) rotateY(45deg) rotateZ(45deg) scale(1.28,1.42)";
    } else if (rarity === "S") {
        object.style.transform = "rotateX(45deg) rotateY(45deg) rotateZ(45deg) scale(1.45)";
    } else if (rarity === "SS") {
        object.style.transform = "rotateX(25deg) rotateY(45deg) scale(1.62)";
    } else {
        object.style.transform = "rotateX(45deg) rotateY(45deg) rotateZ(45deg) scale(1.82)";
    }

    faces.forEach(face => {
        face.style.borderColor = finalColor;
        face.style.background =
            "linear-gradient(135deg," + finalColor + "88," + finalColor + "12)";
        face.style.boxShadow =
            "inset 0 0 " + (35 + level * 4) + "px " + finalColor +
            ", 0 0 " + (45 + level * 7) + "px " + finalColor;
    });

    core.style.background = finalColor;
    core.style.boxShadow =
        "0 0 25px " + finalColor +
        ", 0 0 55px " + finalColor +
        ", 0 0 95px " + finalColor;

    energy.style.background =
        "radial-gradient(circle," + finalColor + "," + finalColor + "55,transparent 70%)";

    [orbit1, orbit2, orbit3, orbit4].forEach(o => {
        o.style.borderColor = finalColor;
        o.style.boxShadow = "0 0 " + (18 + level * 4) + "px " + finalColor;
    });

    vortex.style.background =
        "conic-gradient(from 0deg,transparent," + finalColor +
        ",transparent," + finalColor + "88,transparent)";
}, 4600);

// 결과 공개
setTimeout(() => {
    grade.innerText = rarity;
    grade.style.color = finalColor;
    grade.style.textShadow =
        "0 0 10px " + finalColor +
        ",0 0 30px " + finalColor +
        ",0 0 70px " + finalColor;
    grade.classList.add("show");
}, 5200);
</script>
</body>
</html>
"""

    animation_html = animation_html.replace("__RARITY__", rarity)
    animation_html = animation_html.replace("__FINAL_COLOR__", final_color)
    animation_html = animation_html.replace("__RARITY_LEVEL__", str(rarity_level))

    components.html(animation_html, height=510, scrolling=False)
    time.sleep(5.9)

# =========================================================
# 미니게임
# =========================================================

def new_memory_game():
    symbols = ["◆", "●", "▲", "■", "★", "✦", "⬟", "⬢"]
    length = 4 + min(st.session_state.memory_round // 3, 4)
    st.session_state.memory_sequence = " ".join(random.choices(symbols, k=length))
    st.session_state.memory_hidden = False

def new_math_game():
    difficulty = min(st.session_state.math_round // 4, 3)
    if difficulty == 0:
        a, b = random.randint(10, 40), random.randint(5, 30)
        op = random.choice(["+", "-"])
    elif difficulty == 1:
        a, b = random.randint(15, 60), random.randint(2, 12)
        op = random.choice(["+", "-", "×"])
    else:
        a, b = random.randint(20, 90), random.randint(3, 15)
        op = random.choice(["+", "-", "×"])

    if op == "+":
        answer = a + b
    elif op == "-":
        answer = a - b
    else:
        answer = a * b

    st.session_state.math_question = f"{a} {op} {b}"
    st.session_state.math_answer = answer

# =========================================================
# 사이드바
# =========================================================

st.sidebar.markdown("## 🎴 성지온 냄새 뽑기")
st.sidebar.caption("실제 결제 없이 미니게임 재화만 사용하는 버전이다.")

page = st.sidebar.radio(
    "메뉴",
    ["🎲 뽑기", "🎮 미니게임", "📚 카드 목록", "🕘 뽑기 기록"],
    label_visibility="collapsed",
)

st.sidebar.divider()
st.sidebar.metric("냄새 결정", f"{st.session_state.currency:,}")
st.sidebar.metric("총 뽑기", st.session_state.total_pulls)
st.sidebar.metric("수집 카드", f"{len(st.session_state.collection)} / {TOTAL_CARD_TYPES}")

# =========================================================
# 뽑기 페이지
# =========================================================

if page == "🎲 뽑기":
    st.markdown('<div class="main-title">🎴 성지온 냄새 뽑기 🎴</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">미니게임으로 냄새 결정을 모아 137종의 카드를 수집한다.</div>', unsafe_allow_html=True)

    top1, top2 = st.columns(2)

    pity_progress = st.session_state.total_pulls % PITY_INTERVAL
    remaining = PITY_INTERVAL - pity_progress

    with top1:
        st.markdown(
            (
                '<div class="currency-panel">'
                '<div class="currency-title">💎 보유 냄새 결정</div>'
                f'<div class="currency-value">{st.session_state.currency:,}</div>'
                f'<div class="status-small">1회 {PULL_COST} · 10회 {TEN_PULL_COST}</div>'
                '</div>'
            ),
            unsafe_allow_html=True
        )

    with top2:
        st.markdown(
            (
                '<div class="status-panel">'
                '<div class="status-title">👑 SS 확정 천장</div>'
                f'<div class="status-value">{remaining}회</div>'
                f'<div class="status-small">{PITY_INTERVAL}번째마다 SS 등급이 확정된다.</div>'
                '</div>'
            ),
            unsafe_allow_html=True
        )

    st.progress(pity_progress / PITY_INTERVAL)

    st.write("")
    button_1, button_10 = st.columns(2)

    with button_1:
        single = st.button(
            f"🎲 1회 뽑기 · {PULL_COST} 결정",
            type="primary",
            use_container_width=True
        )

    with button_10:
        multi = st.button(
            f"🔥 10회 뽑기 · {TEN_PULL_COST} 결정",
            use_container_width=True
        )

    if single:
        if st.session_state.currency < PULL_COST:
            st.error("냄새 결정이 부족하다. 미니게임에서 재화를 얻어야 한다.")
        else:
            st.session_state.currency -= PULL_COST
            result = draw_one()
            st.session_state.last_results = [result]
            summon_animation(result["rarity"])

            if result.get("pity", False):
                st.toast("100회 천장으로 SS가 등장했다.", icon="👑")
            if result["rarity"] in ["SS", "SSS"]:
                st.balloons()

    if multi:
        if st.session_state.currency < TEN_PULL_COST:
            st.error("냄새 결정이 부족하다. 미니게임에서 재화를 얻어야 한다.")
        else:
            st.session_state.currency -= TEN_PULL_COST
            results = draw_many(10)
            st.session_state.last_results = results

            highest = max(results, key=lambda r: RARITY_ORDER[r["rarity"]])
            summon_animation(highest["rarity"])

            if any(r.get("pity", False) for r in results):
                st.toast("이번 10연차에서 SS 천장이 발동했다.", icon="👑")
            if any(r["rarity"] in ["SS", "SSS"] for r in results):
                st.balloons()

    if st.session_state.last_results:
        st.divider()
        st.markdown("### 최근 뽑기 결과")
        show_results(st.session_state.last_results)

    st.divider()
    s1, s2, s3 = st.columns(3)

    with s1:
        st.metric("총 뽑기", st.session_state.total_pulls)
    with s2:
        st.metric("수집 카드", f"{len(st.session_state.collection)} / {TOTAL_CARD_TYPES}")
    with s3:
        if st.session_state.history:
            best = max(
                (r.get("rarity", "F") for r in st.session_state.history),
                key=lambda r: RARITY_ORDER.get(r, 0)
            )
        else:
            best = "-"
        st.metric("최고 등급", best)

    with st.expander("📊 등급별 기본 확률"):
        st.caption("천장 뽑기는 아래 확률을 무시하고 SS가 확정된다.")
        for rarity, probability in zip(RARITIES, PROBABILITIES):
            st.write(f"**{rarity}** · {probability}% · {len(CARDS[rarity])}종")

# =========================================================
# 미니게임 페이지
# =========================================================

elif page == "🎮 미니게임":
    st.title("🎮 냄새 결정 채굴장")
    st.caption("실제 돈이나 결제는 없고, 미니게임으로만 뽑기 재화를 얻는다.")

    st.markdown(
        (
            '<div class="currency-panel">'
            '<div class="currency-title">현재 보유 냄새 결정</div>'
            f'<div class="currency-value">{st.session_state.currency:,}</div>'
            '</div>'
        ),
        unsafe_allow_html=True
    )

    st.write("")
    memory_tab, math_tab = st.tabs(["🧠 순간 암기", "⚡ 빠른 계산"])

    # -----------------------------
    # 순간 암기
    # -----------------------------
    with memory_tab:
        st.markdown(
            (
                '<div class="game-panel">'
                '<div class="game-title">🧠 순간 암기</div>'
                '<div class="game-desc">'
                '기호 순서를 외운 뒤 그대로 입력하면 된다. '
                '정답이면 40 결정을 얻고, 연속 라운드가 올라갈수록 기호 수가 늘어난다.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True
        )

        if st.session_state.memory_sequence is None:
            if st.button("새 암기 게임 시작", use_container_width=True, key="memory_start"):
                new_memory_game()
                st.rerun()
        else:
            if not st.session_state.memory_hidden:
                st.info(f"외울 순서:  {st.session_state.memory_sequence}")
                if st.button("외웠다", use_container_width=True, key="memory_hide"):
                    st.session_state.memory_hidden = True
                    st.rerun()
            else:
                answer = st.text_input(
                    "기호 사이를 한 칸씩 띄워 입력한다.",
                    key="memory_answer_input",
                    placeholder="예: ◆ ● ★ ■"
                )

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("정답 확인", use_container_width=True, key="memory_check"):
                        normalized = " ".join(answer.split())
                        if normalized == st.session_state.memory_sequence:
                            st.session_state.currency += 40
                            st.session_state.memory_round += 1
                            st.success("정답이다. 냄새 결정 40개를 획득했다.")
                            st.session_state.memory_sequence = None
                            st.session_state.memory_hidden = False
                        else:
                            st.error("틀렸다. 순서를 다시 확인해야 한다.")
                            st.session_state.memory_sequence = None
                            st.session_state.memory_hidden = False
                with c2:
                    if st.button("포기", use_container_width=True, key="memory_giveup"):
                        st.session_state.memory_sequence = None
                        st.session_state.memory_hidden = False
                        st.rerun()

        st.caption(f"완료한 암기 라운드: {st.session_state.memory_round}")

    # -----------------------------
    # 빠른 계산
    # -----------------------------
    with math_tab:
        st.markdown(
            (
                '<div class="game-panel">'
                '<div class="game-title">⚡ 빠른 계산</div>'
                '<div class="game-desc">'
                '제시된 계산 문제를 맞히면 25 결정을 얻는다. '
                '라운드가 올라가면 곱셈도 등장한다.'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True
        )

        if st.session_state.math_question is None:
            if st.button("새 계산 문제", use_container_width=True, key="math_start"):
                new_math_game()
                st.rerun()
        else:
            st.markdown(f"## {st.session_state.math_question} = ?")

            math_input = st.number_input(
                "정답",
                step=1,
                value=0,
                key="math_answer_input"
            )

            c1, c2 = st.columns(2)

            with c1:
                if st.button("제출", use_container_width=True, key="math_submit"):
                    if int(math_input) == int(st.session_state.math_answer):
                        st.session_state.currency += 25
                        st.session_state.math_round += 1
                        st.success("정답이다. 냄새 결정 25개를 획득했다.")
                    else:
                        st.error(f"오답이다. 정답은 {st.session_state.math_answer}였다.")

                    st.session_state.math_question = None
                    st.session_state.math_answer = None

            with c2:
                if st.button("다른 문제", use_container_width=True, key="math_skip"):
                    st.session_state.math_question = None
                    st.session_state.math_answer = None
                    st.rerun()

        st.caption(f"완료한 계산 라운드: {st.session_state.math_round}")

# =========================================================
# 카드 목록 페이지
# =========================================================

elif page == "📚 카드 목록":
    st.title("📚 카드 목록")
    st.caption(
        f"전체 {TOTAL_CARD_TYPES}종 중 {len(st.session_state.collection)}종을 발견했다."
    )

    tabs = st.tabs(RARITIES)

    for tab, rarity in zip(tabs, RARITIES):
        with tab:
            st.subheader(f"{rarity} 등급")
            st.caption(f"총 {len(CARDS[rarity])}종")

            collected = 0
            for card in CARDS[rarity]:
                key = f"{rarity}|{card['name']}"
                amount = st.session_state.collection.get(key, 0)

                if amount > 0:
                    collected += 1
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
                            '<div class="collection-name" style="opacity:.36;">'
                            '❓ 아직 발견하지 못한 카드'
                            '</div>'
                            '</div>'
                        ),
                        unsafe_allow_html=True
                    )

            st.caption(f"{collected} / {len(CARDS[rarity])}종 수집")

# =========================================================
# 뽑기 기록 페이지
# =========================================================

elif page == "🕘 뽑기 기록":
    st.title("🕘 뽑기 기록")

    if not st.session_state.history:
        st.info("아직 뽑기 기록이 없다.")
    else:
        filter_rarity = st.selectbox(
            "등급 필터",
            ["전체"] + RARITIES
        )

        if filter_rarity == "전체":
            filtered = st.session_state.history
        else:
            filtered = [
                r for r in st.session_state.history
                if r.get("rarity") == filter_rarity
            ]

        st.caption(f"{len(filtered)}개의 기록을 표시한다.")

        for result in filtered[:200]:
            rarity = html.escape(result.get("rarity", "?"))
            name = html.escape(result.get("name", "알 수 없는 카드"))
            number = result.get("pull_number", "?")
            pity_text = " · 천장" if result.get("pity", False) else ""

            st.markdown(
                (
                    '<div class="history-item">'
                    f'<div class="history-rarity">#{number} · {rarity}{pity_text}</div>'
                    f'<div class="history-name">{name}</div>'
                    '</div>'
                ),
                unsafe_allow_html=True
            )

        st.divider()

        if st.button("🗑️ 모든 진행 상황 초기화", type="secondary"):
            st.session_state.total_pulls = 0
            st.session_state.history = []
            st.session_state.collection = {}
            st.session_state.last_results = []
            st.session_state.currency = STARTING_CURRENCY
            st.session_state.memory_sequence = None
            st.session_state.memory_hidden = False
            st.session_state.memory_round = 0
            st.session_state.math_question = None
            st.session_state.math_answer = None
            st.session_state.math_round = 0
            st.rerun()
