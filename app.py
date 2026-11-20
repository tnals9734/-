import streamlit as st
from pathlib import Path

# ═════════════════════════════════════════════
# 기본 설정
# ═════════════════════════════════════════════
st.set_page_config(page_title="탄소중립도시", page_icon="🌱", layout="wide")

BASE_DIR = Path(__file__).parent  # 깃허브 저장소 최상위 폴더

ICONS = {".pdf": "📕", ".hwp": "📄", ".pptx": "📊", ".jpg": "🖼️", ".png": "🖼️"}


def download(label, name, key):
    """파일이 있으면 다운로드 버튼, 없으면 안내 문구를 보여줍니다."""
    p = BASE_DIR / name
    if p.exists():
        with open(p, "rb") as f:
            st.download_button(label, f, file_name=name, key=key, use_container_width=True)
    else:
        st.caption(f"⚠️ 파일을 찾을 수 없습니다: {name}")


def show_image(name):
    p = BASE_DIR / name
    if p.exists():
        st.image(str(p), use_container_width=True)
    else:
        st.caption(f"⚠️ 이미지를 찾을 수 없습니다: {name}")


def title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def card(icon, head, body):
    st.markdown(
        f'<div class="card"><div class="icon">{icon}</div><h3>{head}</h3><p>{body}</p></div>',
        unsafe_allow_html=True,
    )


def info_box(rows):
    """[('항목', '내용'), ...] 형태의 요약표"""
    html = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
    st.markdown(f'<table class="info">{html}</table>', unsafe_allow_html=True)


# ═════════════════════════════════════════════
# 디자인 (CSS)
# ═════════════════════════════════════════════
st.markdown(
    """
    <style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {padding: 1.5rem 2rem; max-width: 100%;}

    /* 상단 배너 */
    .hero {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 45%, #43a047 100%);
        color: white; padding: 52px 48px; border-radius: 18px; margin-bottom: 20px;
    }
    .hero .eyebrow {font-size: 14px; opacity: .85; letter-spacing: 3px;}
    .hero h1 {color: white; font-size: 48px; margin: 8px 0 12px 0;}
    .hero p {font-size: 18px; opacity: .95; line-height: 1.6; margin: 0;}

    /* 메뉴 탭 */
    .stTabs [data-baseweb="tab-list"] {gap: 6px;}
    .stTabs [data-baseweb="tab"] {font-size: 17px; font-weight: 600; padding: 10px 18px;}
    .stTabs [aria-selected="true"] {color: #1b5e20 !important;}

    /* 카드 */
    .card {
        background: #f4f9f4; border: 1px solid #dcebdc; border-radius: 14px;
        padding: 24px; height: 100%; margin-bottom: 12px;
    }
    .card .icon {font-size: 32px;}
    .card h3 {color: #1b5e20; font-size: 20px; margin: 10px 0 8px 0;}
    .card p {color: #444; font-size: 15px; line-height: 1.65; margin: 0;}

    /* 제목 */
    .section-title {
        color: #1b5e20; font-size: 26px; font-weight: 700;
        border-left: 6px solid #43a047; padding-left: 12px; margin: 18px 0 18px 0;
    }

    /* 요약표 */
    table.info {width: 100%; border-collapse: collapse; margin: 8px 0 20px 0; font-size: 15px;}
    table.info th {
        width: 160px; background: #e8f5e9; color: #1b5e20; text-align: left;
        padding: 12px 16px; border-bottom: 1px solid #dcebdc;
    }
    table.info td {padding: 12px 16px; border-bottom: 1px solid #eee; color: #333;}

    .badge {
        display: inline-block; background: #e8f5e9; color: #1b5e20; border-radius: 20px;
        padding: 4px 12px; font-size: 13px; font-weight: 600; margin: 0 6px 6px 0;
    }
    .footer {
        margin-top: 48px; padding: 24px; text-align: center; color: #777;
        font-size: 13px; border-top: 1px solid #e5e5e5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ═════════════════════════════════════════════
# 상단 배너
# ═════════════════════════════════════════════
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">CARBON NEUTRAL CITY</div>
        <h1>🌱 탄소중립도시</h1>
        <p>도시에서 시작하는 2050 탄소중립<br>
        탄소중립도시 지원기구가 지역과 함께 만들어 갑니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ═════════════════════════════════════════════
# 메인 메뉴
# ═════════════════════════════════════════════
m1, m2, m3, m4, m5 = st.tabs(
    ["🌍 탄소중립", "🏙️ 탄소중립도시", "🏢 탄소중립 지원기구", "⚖️ 법체계 및 계획", "🔍 돋보기"]
)

# ─────────────────────────────────────────────
# 1. 탄소중립
# ─────────────────────────────────────────────
with m1:
    s1, s2 = st.tabs(["탄소중립 소개", "비전 및 전략"])

    with s1:
        title("탄소중립이란?")
        st.write(
            "탄소중립(Net-Zero)은 인간 활동으로 배출되는 온실가스를 최대한 줄이고, "
            "남은 배출량은 숲·습지 같은 흡수원이나 탄소포집 기술로 흡수·제거하여 "
            "실질적인 배출량을 '0'으로 만드는 것을 말합니다."
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            card("⬇️", "배출 줄이기", "에너지 전환, 건물 효율화, 친환경 수송 등으로 온실가스 배출 자체를 줄입니다.")
        with c2:
            card("🌳", "흡수 늘리기", "도시숲·공원·습지 등 탄소흡수원을 확충합니다.")
        with c3:
            card("⚖️", "순배출 0", "배출량과 흡수량이 같아져 실질 배출이 '0'이 되는 상태를 목표로 합니다.")

        title("왜 도시인가?")
        st.write(
            "도시는 사람과 경제 활동이 모이는 곳으로 에너지 소비와 온실가스 배출의 대부분이 "
            "도시에서 발생합니다. 따라서 도시별 배출 특성에 맞춘 감축 전략이 탄소중립 실현의 핵심입니다."
        )

    with s2:
        title("국가 비전")
        st.markdown(
            '<div class="card" style="text-align:center;"><div class="icon">🎯</div>'
            '<h3 style="font-size:24px;">2050 탄소중립 실현</h3>'
            "<p>탄소중립 사회로의 공정하고 질서 있는 전환</p></div>",
            unsafe_allow_html=True,
        )

        title("국가 온실가스 감축목표 (NDC)")
        n1, n2, n3 = st.columns(3)
        n1.metric("2030 감축목표", "40%", "2018년 대비")
        n2.metric("2035 감축목표", "53~61%", "2018년 대비 · 2025.11 확정")
        n3.metric("최종 목표", "2050년", "탄소중립")

        title("부문별 주요 감축 전략")
        c1, c2 = st.columns(2)
        with c1:
            card("⚡", "전력", "재생에너지 보급 확대와 석탄발전 감축")
            card("🏢", "건물", "제로에너지 건축과 그린 리모델링 확산, 열 공급의 전기화")
        with c2:
            card("🏭", "산업", "연료·원료의 탈탄소화와 저탄소 제품 생산")
            card("🚗", "수송", "전기·수소차 보급 확대 (신차 기준 2030년 40%, 2035년 70%)")

# ─────────────────────────────────────────────
# 2. 탄소중립도시
# ─────────────────────────────────────────────
with m2:
    s1, s2, s3 = st.tabs(["스마트 그린도시", "탄소중립 그린도시", "탄소중립 선도도시"])

    with s1:
        title("스마트 그린도시")
        st.write(
            "그린뉴딜 핵심 사업 중 하나로, 도시의 기후·환경 문제를 진단하고 "
            "맞춤형 해결책을 적용해 생활공간의 녹색전환을 이끄는 사업입니다."
        )
        info_box([
            ("추진 부처", "환경부"),
            ("시작", "2020년 공모 (그린뉴딜)"),
            ("대상", "공모로 선정된 25개 도시"),
            ("사업 기간", "2021년부터 2년간"),
            ("사업 규모", "총 약 2,900억 원"),
            ("목표", "도시의 기후변화 대응력 강화와 생활공간의 녹색전환"),
        ])

    with s2:
        title("탄소중립 그린도시")
        st.write(
            "스마트 그린도시 사업을 발전시킨 사업으로, 지역 중심의 탄소중립 이행 및 "
            "확산 체계를 구축하기 위해 추진되었습니다."
        )
        info_box([
            ("추진 부처", "환경부"),
            ("시작", "2022년 공모"),
            ("선정 도시", "경기 수원시, 충북 충주시"),
            ("사업 기간", "5년"),
            ("사업 규모", "한 곳당 400억 원"),
        ])
        c1, c2 = st.columns(2)
        with c1:
            card("🏙️", "경기 수원시", "고색동 일원 · 공공건물 태양광과 그린수소 등 에너지 전환, 국공유지 흡수원 확충, 폐기물 스마트 수거")
        with c2:
            card("🌲", "충북 충주시", "용전리 일원 · 수소모빌리티 스테이션, 탄소흡수 군집식재숲, 도시열섬 저감시스템")

    with s3:
        title("탄소중립 선도도시")
        st.write(
            "지역과 민간 중심의 탄소중립 이행 및 확산 기반을 마련하기 위해 "
            "환경부와 국토교통부가 공동으로 추진하는 사업입니다."
        )
        info_box([
            ("추진 부처", "환경부 · 국토교통부 공동"),
            ("선정", "2024년 10월 (1차 대상지 4곳)"),
            ("선정 도시", "충남 당진시, 제주특별자치도, 충남 보령시, 서울 노원구"),
            ("추진 계획", "2030년까지 총 10곳 조성 예정"),
        ])
        st.markdown(
            '<span class="badge">당진시</span><span class="badge">제주특별자치도</span>'
            '<span class="badge">보령시</span><span class="badge">노원구</span>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 서울특별시 노원구")
            show_image("노원.jpg")
            st.write("수도권 유일의 선도도시로, 공공건축물 제로에너지 등 건축 분야의 탄소중립 정책을 중심으로 도심형 탄소중립 모델을 추진합니다.")
            download("⬇️ 노원구 기본계획 (PDF)", "(노원구)01_탄소중립 선도도시 기본계획(260709)_최종.pdf", "nowon")
        with c2:
            st.markdown("### 충청남도 당진시")
            show_image("당진.jpg")
            st.write("배출 비중이 높은 에너지·산업 부문을 중심으로 재생에너지·그린수소 전환과 바이오에너지 순환체계 구축을 추진합니다.")
            download("⬇️ 당진시 기본계획 (PDF)", "(당진시)01_탄소중립 선도도시 기본계획(260707)_최종.pdf", "dangjin")

# ─────────────────────────────────────────────
# 3. 탄소중립 지원기구
# ─────────────────────────────────────────────
with m3:
    title("탄소중립도시 지원기구")
    # ✏️ 아래 소개 문구는 예시입니다. 실제 내용으로 바꿔 주세요.
    st.write(
        "탄소중립도시 지원기구는 탄소중립도시가 실효성 있는 계획을 세우고 "
        "이를 차질 없이 이행할 수 있도록 지원하는 전문 기관입니다."
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("📋", "계획 수립 지원", "도시별 탄소중립 기본계획 수립 컨설팅과 기술 자문")
    with c2:
        card("🤝", "협력체계 구축", "중앙정부·지자체·전문기관 간 협조체계 운영")
    with c3:
        card("📈", "이행 점검", "로드맵에 따른 추진 현황 점검과 성과 관리")
    with c4:
        card("📢", "성과 확산", "우수 사례 발굴과 전국 확산 지원")

    title("운영 자료")
    d1, d2 = st.columns(2)
    with d1:
        download("📄 지원기구 업무계획", "'23 탄소중립도시 지원기구 업무계획_최종f.hwp", "org1")
        download("📄 지원기구 운영계획", "'23 탄소중립도시 지원기구 운영계획_2.hwp", "org2")
        download("📄 지원기구 공모 참여계획(방침)", "지원기구 공모 참여계획(방침)_최종1.hwp", "org3")
    with d2:
        download("📊 지원기구 운영 로드맵", "'23년 지원기구 운영 로드맵.pptx", "org4")
        download("📊 지원기구 운영 로드맵 (그린도시)", "'23년 지원기구 운영 로드맵_그린도시.pptx", "org5")
        download("📄 협조체계 구축 계획(안)", "탄소중립도시 지원기구 협조체계 구축 계획(안).hwp", "org6")

# ─────────────────────────────────────────────
# 4. 법체계 및 계획
# ─────────────────────────────────────────────
with m4:
    title("법체계")
    info_box([
        ("근거 법률", "기후위기 대응을 위한 탄소중립·녹색성장 기본법 (약칭: 탄소중립기본법)"),
        ("시행", "2022년 3월 25일"),
        ("주요 내용", "2050 탄소중립 목표 법제화, 국가·지자체 탄소중립 계획 수립, 탄소중립도시 지정 근거 마련"),
    ])

    title("계획 체계")
    c1, c2, c3 = st.columns(3)
    with c1:
        card("🇰🇷", "국가 기본계획", "국가 탄소중립·녹색성장 기본계획 (20년 단위, 5년마다 수립)")
    with c2:
        card("🗺️", "지자체 기본계획", "광역·기초 지자체별 탄소중립·녹색성장 기본계획")
    with c3:
        card("🏙️", "도시 계획", "탄소중립도시별 기본계획 및 추진계획")

    title("관련 계획 자료")
    d1, d2 = st.columns(2)
    with d1:
        download("📄 탄소중립도시 추진계획(요약)", "탄소중립도시 추진계획(요약)_최종.hwp", "plan1")
    with d2:
        download("📄 탄소중립도시 추진계획", "탄소중립도시 추진계획_최종2.hwp", "plan2")

# ─────────────────────────────────────────────
# 5. 돋보기 (통합 검색 · 자료실)
# ─────────────────────────────────────────────
with m5:
    title("돋보기 · 통합 검색")
    keyword = st.text_input("🔍 찾고 싶은 내용을 입력하세요", placeholder="예: 노원, 로드맵, 기본계획")

    files = sorted(p for p in BASE_DIR.iterdir() if p.is_file() and p.suffix.lower() in ICONS)

    tab_all, tab_pdf, tab_hwp, tab_ppt, tab_img = st.tabs(["전체", "PDF", "한글", "PPT", "이미지"])
    groups = {
        tab_all: list(ICONS),
        tab_pdf: [".pdf"],
        tab_hwp: [".hwp"],
        tab_ppt: [".pptx"],
        tab_img: [".jpg", ".png"],
    }
    for t_idx, (tab, exts) in enumerate(groups.items()):
        with tab:
            shown = [p for p in files if p.suffix.lower() in exts and (not keyword or keyword in p.name)]
            st.caption(f"총 {len(shown)}건")
            for p in shown:
                left, right = st.columns([6, 1])
                left.markdown(f"{ICONS[p.suffix.lower()]} **{p.stem}** `{p.suffix[1:].upper()}`")
                with right:
                    with open(p, "rb") as f:
                        st.download_button(
                            "다운로드", f, file_name=p.name, key=f"search{t_idx}-{p.name}"
                        )
            if not shown:
                st.info("검색 결과가 없습니다.")

    title("관련 사이트")
    l1, l2, l3 = st.columns(3)
    with l1:
        st.link_button("🏛️ 기후에너지환경부", "https://www.me.go.kr", use_container_width=True)
    with l2:
        st.link_button("🌐 2050 탄소중립녹색성장위원회", "https://www.2050cnc.go.kr", use_container_width=True)
    with l3:
        st.link_button("⚖️ 국가법령정보센터", "https://www.law.go.kr", use_container_width=True)

# ═════════════════════════════════════════════
# 하단
# ═════════════════════════════════════════════
st.markdown(
    '<div class="footer">© 2026 탄소중립도시 지원기구 · All rights reserved.</div>',
    unsafe_allow_html=True,
)
