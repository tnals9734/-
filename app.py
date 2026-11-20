import streamlit as st
from pathlib import Path

# ─────────────────────────────────────────────
# 기본 설정
# ─────────────────────────────────────────────
st.set_page_config(page_title="탄소중립도시", page_icon="🌱", layout="wide")

BASE_DIR = Path(__file__).parent  # 깃허브 저장소 최상위 폴더


def file_path(name):
    """저장소 안의 파일 경로를 돌려줍니다."""
    return BASE_DIR / name


def download(label, name, key):
    """파일이 있으면 다운로드 버튼을, 없으면 안내 문구를 보여줍니다."""
    p = file_path(name)
    if p.exists():
        with open(p, "rb") as f:
            st.download_button(label, f, file_name=name, key=key, use_container_width=True)
    else:
        st.caption(f"⚠️ 파일을 찾을 수 없습니다: {name}")


def show_image(name):
    p = file_path(name)
    if p.exists():
        st.image(str(p), use_container_width=True)
    else:
        st.caption(f"⚠️ 이미지를 찾을 수 없습니다: {name}")


# ─────────────────────────────────────────────
# 디자인 (CSS)
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {padding: 1.5rem 2rem; max-width: 100%;}

    .hero {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 45%, #43a047 100%);
        color: white;
        padding: 56px 48px;
        border-radius: 18px;
        margin-bottom: 28px;
    }
    .hero .eyebrow {font-size: 15px; opacity: .85; letter-spacing: 2px;}
    .hero h1 {color: white; font-size: 46px; margin: 8px 0 12px 0;}
    .hero p {font-size: 18px; opacity: .95; line-height: 1.6; margin: 0;}

    .card {
        background: #f4f9f4;
        border: 1px solid #dcebdc;
        border-radius: 14px;
        padding: 24px;
        height: 100%;
    }
    .card .icon {font-size: 32px;}
    .card h3 {color: #1b5e20; font-size: 20px; margin: 10px 0 8px 0;}
    .card p {color: #444; font-size: 15px; line-height: 1.6; margin: 0;}

    .section-title {
        color: #1b5e20;
        font-size: 26px;
        font-weight: 700;
        border-left: 6px solid #43a047;
        padding-left: 12px;
        margin: 12px 0 18px 0;
    }
    .footer {
        margin-top: 48px;
        padding: 24px;
        text-align: center;
        color: #777;
        font-size: 13px;
        border-top: 1px solid #e5e5e5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# 상단 배너
# ─────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">CARBON NEUTRAL CITY SUPPORT CENTER</div>
        <h1>🌱 탄소중립도시</h1>
        <p>탄소중립도시 지원기구는 선도도시의 계획 수립부터 이행까지<br>
        지자체와 함께 2050 탄소중립을 실현합니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# 메뉴 (탭)
# ─────────────────────────────────────────────
home, about, cities, library, contact = st.tabs(
    ["🏠 홈", "🏢 기구 소개", "🏙️ 선도도시", "📂 자료실", "✉️ 문의"]
)

# ── 홈 ───────────────────────────────────────
with home:
    st.markdown('<div class="section-title">주요 사업</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    cards = [
        ("📋", "계획 수립 지원", "선도도시별 탄소중립 기본계획 수립을 위한 컨설팅과 기술 자문을 제공합니다."),
        ("🤝", "협력체계 구축", "중앙정부·지자체·전문기관이 함께하는 협조체계를 운영합니다."),
        ("📈", "이행 점검", "로드맵에 따라 사업 추진 현황을 점검하고 성과를 관리합니다."),
    ]
    for col, (icon, title, text) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(
                f'<div class="card"><div class="icon">{icon}</div><h3>{title}</h3><p>{text}</p></div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title" style="margin-top:36px;">선도도시 현황</div>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("지원 선도도시", "2곳", "노원구 · 당진시")
    m2.metric("기본계획 수립", "2건", "2026년 7월 완료")
    m3.metric("목표 연도", "2050년", "탄소중립")

# ── 기구 소개 ─────────────────────────────────
with about:
    st.markdown('<div class="section-title">탄소중립도시 지원기구</div>', unsafe_allow_html=True)
    st.write(
        "탄소중립도시 지원기구는 탄소중립 선도도시가 실효성 있는 계획을 세우고 "
        "이를 차질 없이 이행할 수 있도록 지원하는 전문 기관입니다."
    )
    a1, a2 = st.columns(2)
    with a1:
        st.markdown("#### 🎯 비전")
        st.info("지역이 주도하는 2050 탄소중립도시 실현")
    with a2:
        st.markdown("#### 🧭 추진 전략")
        st.success("계획 수립 지원 · 협력체계 구축 · 이행 점검 · 성과 확산")

    st.markdown("#### 📑 운영 관련 자료")
    d1, d2 = st.columns(2)
    with d1:
        download("📄 지원기구 업무계획", "'23 탄소중립도시 지원기구 업무계획_최종f.hwp", "about1")
        download("📄 지원기구 운영계획", "'23 탄소중립도시 지원기구 운영계획_2.hwp", "about2")
    with d2:
        download("📊 지원기구 운영 로드맵", "'23년 지원기구 운영 로드맵.pptx", "about3")
        download("📄 협조체계 구축 계획(안)", "탄소중립도시 지원기구 협조체계 구축 계획(안).hwp", "about4")

# ── 선도도시 ─────────────────────────────────
with cities:
    st.markdown('<div class="section-title">탄소중립 선도도시</div>', unsafe_allow_html=True)
    nowon, dangjin = st.columns(2)

    with nowon:
        st.markdown("### 서울특별시 노원구")
        show_image("노원.jpg")
        st.write("도시형 탄소중립 모델을 만들어 가는 선도도시입니다.")
        download(
            "⬇️ 노원구 기본계획 (PDF)",
            "(노원구)01_탄소중립 선도도시 기본계획(260709)_최종.pdf",
            "nowon",
        )

    with dangjin:
        st.markdown("### 충청남도 당진시")
        show_image("당진.jpg")
        st.write("산업·에너지 전환을 이끄는 선도도시입니다.")
        download(
            "⬇️ 당진시 기본계획 (PDF)",
            "(당진시)01_탄소중립 선도도시 기본계획(260707)_최종.pdf",
            "dangjin",
        )

# ── 자료실 ───────────────────────────────────
with library:
    st.markdown('<div class="section-title">자료실</div>', unsafe_allow_html=True)

    icons = {".pdf": "📕", ".hwp": "📄", ".pptx": "📊", ".jpg": "🖼️", ".png": "🖼️"}
    files = sorted(
        p for p in BASE_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in icons
    )

    keyword = st.text_input("🔍 자료 검색", placeholder="파일 이름으로 검색하세요")
    if keyword:
        files = [p for p in files if keyword in p.name]

    st.caption(f"총 {len(files)}건")
    for i, p in enumerate(files):
        left, right = st.columns([5, 1])
        left.markdown(f"{icons[p.suffix.lower()]} **{p.stem}**  `{p.suffix[1:].upper()}`")
        with right:
            with open(p, "rb") as f:
                st.download_button("다운로드", f, file_name=p.name, key=f"lib{i}")

# ── 문의 ─────────────────────────────────────
with contact:
    st.markdown('<div class="section-title">문의하기</div>', unsafe_allow_html=True)
    with st.form("contact_form"):
        name = st.text_input("이름")
        org = st.text_input("소속 기관")
        email = st.text_input("이메일")
        message = st.text_area("문의 내용", height=150)
        sent = st.form_submit_button("보내기")
    if sent:
        if name and message:
            st.success(f"{name}님, 문의가 접수되었습니다. 빠르게 답변드리겠습니다.")
        else:
            st.warning("이름과 문의 내용을 입력해 주세요.")

# ─────────────────────────────────────────────
# 하단
# ─────────────────────────────────────────────
st.markdown(
    '<div class="footer">© 2026 탄소중립도시 지원기구 · All rights reserved.</div>',
    unsafe_allow_html=True,
)
