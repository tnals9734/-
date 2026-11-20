import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ═════════════════════════════════════════════
# 기본 설정
# ═════════════════════════════════════════════
st.set_page_config(page_title="탄소중립도시", page_icon="🌱", layout="wide")

BASE_DIR = Path(__file__).parent          # 깃허브 저장소 최상위 폴더
GITHUB_RAW = "https://raw.githubusercontent.com/tnals9734/-/main/"  # 파일 다운로드 주소
PAGE_HEIGHT = 2600                        # 화면 높이(px). 아래가 잘리면 숫자를 키우세요.

# 스트림릿 기본 여백·메뉴 숨기기 → 화면 꽉 채우기
st.markdown(
    """
    <style>
    #MainMenu, footer, header, [data-testid="stToolbar"] {display: none !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    iframe {border: 0; display: block;}
    </style>
    """,
    unsafe_allow_html=True,
)


def image_data(name):
    """저장소의 이미지를 페이지에 바로 넣을 수 있는 형태로 바꿉니다."""
    p = BASE_DIR / name
    if not p.exists():
        return ""
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


# 저장소에 있는 자료 파일 목록 (돋보기 › 자료실)
FILE_TYPES = {".pdf": "PDF", ".hwp": "HWP", ".pptx": "PPT", ".jpg": "이미지", ".png": "이미지"}
files = [
    {"name": p.name, "stem": p.stem, "type": FILE_TYPES[p.suffix.lower()]}
    for p in sorted(BASE_DIR.iterdir())
    if p.is_file() and p.suffix.lower() in FILE_TYPES
]

# ═════════════════════════════════════════════
# 홈페이지 (HTML · CSS · JavaScript)
# ═════════════════════════════════════════════
PAGE = r"""
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:'Noto Sans KR',sans-serif;color:#13263A;background:#F4F7FA}
a{color:#00539A;text-decoration:none}a:hover{color:#0B7BC9}
button{font-family:inherit}

/* 헤더 */
header{position:relative;z-index:30;background:#fff;border-bottom:1px solid #D5DEE8}
.top{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;padding:14px 48px}
.brand{display:flex;align-items:center;gap:16px;cursor:pointer}
.mark{width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#00539A,#20B9F0);display:flex;align-items:center;justify-content:center}
.brand .name{font-size:24px;font-weight:900;color:#00539A;letter-spacing:-.5px}
.brand .sub{font-size:13px;color:#4A6076;margin-top:2px}
.search{display:flex;gap:8px;flex:0 1 400px;min-width:240px}
.search .box{position:relative;flex:1;display:flex}
.search input{flex:1;width:100%;height:44px;padding:0 52px 0 18px;border:1px solid #9FB4C9;border-radius:22px;font-size:15px;font-family:inherit;color:#13263A}
.search .go{position:absolute;right:6px;top:5px;width:34px;height:34px;border:0;border-radius:50%;background:none;cursor:pointer;display:flex;align-items:center;justify-content:center}
.pill{height:44px;padding:0 18px;border:1px solid #9FB4C9;border-radius:22px;background:#fff;color:#00539A;font-size:14px;cursor:pointer}
.bar{height:4px;background:linear-gradient(90deg,#00539A 0%,#1B8FD6 60%,#20B9F0 100%)}

/* 메뉴 */
nav{position:relative;background:#fff;border-top:1px solid #E3EAF1}
.navgrid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));max-width:1280px;margin:0 auto}
.nt{height:62px;padding:0 8px;background:none;border:0;border-bottom:3px solid transparent;font-size:17px;font-weight:700;color:#13263A;cursor:pointer}
.nt.on{border-bottom-color:#00539A;color:#00539A;font-weight:900}
.mega{display:none;position:absolute;left:0;right:0;top:100%;z-index:60;background:#fff;box-shadow:0 14px 26px rgba(19,38,58,.16);border-top:1px solid #E3EAF1;border-bottom:1px solid #D5DEE8}
nav.open .mega{display:block}
.col{border-left:1px solid #E3EAF1;padding:18px 10px 22px;display:flex;flex-direction:column;gap:2px;min-height:130px}
.mi{background:none;border:0;padding:9px 6px;font-size:15px;line-height:1.5;color:#13263A;cursor:pointer;word-break:keep-all}
.mi:hover{color:#00539A;font-weight:700}

/* 메인 배너 */
.hero{position:relative;overflow:hidden;background:linear-gradient(115deg,#062C52 0%,#00539A 62%,#0B7BC9 100%);color:#fff;padding:84px 48px}
.hero .c1{position:absolute;right:-120px;top:-160px;width:560px;height:560px;border-radius:50%;background:rgba(32,185,240,.14)}
.hero .c2{position:absolute;right:160px;bottom:-220px;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,.05)}
.hero .in{position:relative;max-width:900px}
.eyebrow{display:flex;align-items:center;gap:12px;font-size:13px;font-weight:700;letter-spacing:2px;color:#9ED8F5}
.eyebrow span{width:36px;height:3px;background:#F08A00;display:block}
.hero h1{margin:18px 0;font-size:50px;line-height:1.25;font-weight:900;letter-spacing:-1px}
.hero p{margin:0;font-size:18px;line-height:1.8;color:#DCEBF7}

/* 본문 */
main{padding:36px 48px 64px;max-width:1440px;margin:0 auto}
.crumb{font-size:14px;color:#4A6076;margin-bottom:6px}
.ptitle{font-size:30px;font-weight:900;margin:0 0 20px}
.subs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px}
.sb{padding:10px 20px;border-radius:6px;font-size:15px;font-weight:500;cursor:pointer;background:#fff;color:#00539A;border:1px solid #B5C8DC}
.sb.on{font-weight:700;background:#DCEBF7;border:2px solid #00539A}
.panel{background:#fff;border-top:2px solid #00539A;margin-bottom:24px}
.row{display:flex;gap:32px;flex-wrap:wrap;padding:24px 28px;border-bottom:1px solid #DCE4EC}
.row .tag{flex:0 0 180px;font-size:15px;font-weight:700;color:#00539A;line-height:1.6}
.row .body{flex:1 1 420px;min-width:0}
.row h3{margin:0 0 8px;font-size:19px;font-weight:700;line-height:1.5}
.row p{margin:0;font-size:16px;line-height:1.85;color:#31475C;white-space:pre-line}
.lbl{font-size:15px;font-weight:700;color:#00539A;margin:12px 0 4px}
.gomenu{margin-top:12px;height:36px;padding:0 16px;border:1px solid #00539A;border-radius:18px;background:#fff;color:#00539A;font-size:14px;cursor:pointer}

/* 홈 바로가기 카드 */
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-bottom:28px}
.card{display:flex;flex-direction:column;justify-content:flex-start;background:#fff;border:1px solid #DCE4EC;border-top:3px solid #00539A;border-radius:6px;padding:24px;cursor:pointer;text-align:left}
.card:hover{box-shadow:0 8px 20px rgba(19,38,58,.10)}
.card .k{font-size:13px;font-weight:700;color:#F08A00;letter-spacing:1px}
.card h3{margin:8px 0;font-size:20px;font-weight:900;color:#13263A}
.card p{margin:0;font-size:14px;line-height:1.7;color:#4A6076}
.sec{font-size:22px;font-weight:900;margin:8px 0 14px}

/* 추진경위 타임라인 */
.tl{background:#fff;border-top:2px solid #00539A;padding:36px 24px 16px}
.tlhead{display:flex;justify-content:center;margin-bottom:36px}
.tlhead div{background:#00539A;color:#fff;font-size:19px;font-weight:900;padding:10px 44px;border-radius:6px}
.tr{display:flex}
.tr.rev{flex-direction:row-reverse}
.tc{flex:1;min-width:0;padding:0 8px 36px;display:flex;flex-direction:column;align-items:flex-end}
.tr.rev .tc{align-items:flex-start}
.ban{min-height:40px;display:flex;align-items:center;max-width:100%;background:#00539A;color:#fff;font-size:17px;line-height:1.4;padding:6px 34px 6px 22px;clip-path:polygon(0 0,calc(100% - 16px) 0,100% 50%,calc(100% - 16px) 100%,0 100%)}
.tr.rev .ban{padding:6px 22px 6px 34px;clip-path:polygon(16px 0,100% 0,100% 100%,16px 100%,0 50%)}
.ban b{color:#FFD84D;margin-right:10px}
.tbox{margin-top:10px;width:100%;max-width:560px;border:1px solid #B5C8DC;border-radius:8px;padding:14px 18px;font-size:15px;line-height:1.8;color:#31475C;white-space:pre-line;background:#fff}
.tm{flex:0 0 72px;position:relative;display:flex;justify-content:center}
.line{position:absolute;left:50%;margin-left:-2px;width:4px;background:#00539A;top:0;bottom:0}
.tr:first-child .line{top:20px}.tr:last-child .line{bottom:calc(100% - 20px)}
.dot{position:relative;z-index:1;width:40px;height:40px;border-radius:50%;background:#00539A;color:#fff;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:900;box-shadow:0 0 0 4px #fff}

/* 선도도시 */
.cities{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 18px}
.cb{height:44px;padding:0 20px;border-radius:22px;font-size:15px;font-weight:700;cursor:pointer;background:#fff;color:#00539A;border:1px solid #00539A}
.cb.on{background:#F08A00;border-color:#F08A00;color:#fff}
.city{background:#fff;border-top:2px solid #00539A;padding:28px 32px;display:flex;gap:32px;flex-wrap:wrap}
.city .info{flex:1 1 420px;min-width:0}
.city .pic{flex:1 1 420px;min-width:0}
.city .pic img{width:100%;height:auto;border:1px solid #DCE4EC;border-radius:6px;display:block}
.city h3{margin:0 0 14px;font-size:26px;font-weight:900}
.vision{font-size:19px;font-weight:700;line-height:1.6;margin-bottom:18px}
table.it{width:100%;border-collapse:collapse;font-size:15px;margin-bottom:18px}
table.it th{width:110px;text-align:left;background:#EEF5FB;color:#00539A;padding:10px 14px;border-bottom:1px solid #DCE4EC;vertical-align:top}
table.it td{padding:10px 14px;border-bottom:1px solid #DCE4EC;line-height:1.7;color:#31475C}
.dl{display:inline-flex;align-items:center;gap:8px;height:44px;padding:0 20px;border-radius:22px;background:#00539A;color:#fff !important;font-size:15px;font-weight:700}
.dl:hover{background:#0B7BC9}
.empty{padding:28px;border:1px dashed #9FB4C9;border-radius:8px;font-size:16px;color:#4A6076;background:#fff}

/* 자료실 */
.frow{display:flex;align-items:center;gap:16px;padding:16px 28px;border-bottom:1px solid #DCE4EC}
.ft{flex:0 0 70px;text-align:center;font-size:12px;font-weight:700;padding:4px 0;border-radius:4px;background:#EEF5FB;color:#00539A}
.fn{flex:1;font-size:16px;min-width:0;word-break:break-all}
.fd{height:36px;padding:0 16px;border:1px solid #00539A;border-radius:18px;color:#00539A;font-size:14px;display:inline-flex;align-items:center}

/* 계산기 */
.calc{background:#fff;border-top:2px solid #00539A;padding:28px 40px 32px;margin-bottom:24px}
.calc label{display:flex;flex-direction:column;gap:6px;font-size:14px;font-weight:700;color:#31475C}
.calc input{width:180px;height:44px;padding:0 14px;border:1px solid #9FB4C9;border-radius:6px;font-size:16px;font-family:inherit}
.cr{display:flex;gap:20px;align-items:center;flex-wrap:wrap;margin-top:14px}
.cr .n{flex:0 0 190px;font-size:16px;font-weight:700}
.cr .n small{display:block;font-size:12px;font-weight:400;color:#4A6076}
.cr .track{flex:1 1 280px;min-width:200px;height:22px;background:#E8EEF4;border-radius:4px;overflow:hidden}
.cr .fill{height:100%;border-radius:4px}
.cr .v{flex:0 0 250px;font-size:15px}
.msg{margin-top:22px;padding:16px 20px;background:#EEF5FB;border-left:4px solid #F08A00;font-size:16px;line-height:1.8}
.note{margin-top:14px;font-size:13px;line-height:1.7;color:#4A6076}

footer{margin:0 48px;padding:24px 0 40px;border-top:1px solid #D5DEE8;font-size:14px;color:#4A6076}

@media (max-width:760px){
  .top,main,.hero{padding-left:20px;padding-right:20px}
  .navgrid{grid-template-columns:repeat(3,1fr)}
  .hero h1{font-size:34px}
  .tr,.tr.rev{flex-direction:row}.tc,.tr.rev .tc{align-items:flex-start}.tr>div:last-child{display:none}
}
</style>
</head>
<body>
<header>
  <div class="top">
    <div class="brand" onclick="go('home')">
      <div class="mark"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c4-2 7-6 7-11a7 7 0 0 0-14 0c0 5 3 9 7 11z"/><path d="M12 22V10"/><path d="M12 14l3-3"/></svg></div>
      <div><div class="name">탄소중립도시</div><div class="sub">국가 탄소중립도시 지원기구 · K-water</div></div>
    </div>
    <div class="search">
      <div class="box">
        <input id="q" type="search" placeholder="검색 (예: 당진, 기본계획, 제29조)" oninput="onSearch(this.value)" aria-label="검색">
        <button class="go" aria-label="검색" onclick="document.getElementById('q').focus()"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00539A" stroke-width="2.4" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg></button>
      </div>
      <button class="pill" id="clr" style="display:none" onclick="clearSearch()">지우기</button>
    </div>
  </div>
  <div class="bar"></div>
  <nav id="nav" onmouseleave="this.classList.remove('open')">
    <div class="navgrid" id="navtop"></div>
    <div class="mega"><div class="navgrid" id="navcols"></div></div>
  </nav>
</header>
<div id="hero"></div>
<main id="main"></main>
<footer>© 국가 탄소중립도시 지원기구 K-water. All rights reserved.</footer>

<script>
const FILES = __FILES__;
const IMG = {nowon: "__IMG_NOWON__", dangjin: "__IMG_DANGJIN__"};
const RAW = "__RAW__";
const fileUrl = (n) => RAW + encodeURIComponent(n);

/* ───── 메뉴 구성 ───── */
const MENU = [
  ["home","홈",[]],
  ["cn","탄소중립",[["intro","탄소중립 소개"],["vision","비전 및 전략"]]],
  ["city","탄소중립도시",[["smart","스마트 그린도시"],["green","탄소중립 그린도시"],["pilot","탄소중립 선도도시"]]],
  ["org","탄소중립 지원기구",[["about","기구 소개"],["history","추진경위"],["docs","운영 자료"]]],
  ["law","법체계 및 계획",[["act","탄소중립기본법"],["decree","시행령"],["plan","관련 계획"]]],
  ["look","돋보기",[["files","자료실"],["policy","국내외 정책 동향"],["faq","탄소중립 궁금증"]]]
];
const ML = {}, SL = {};
MENU.forEach(m => { ML[m[0]] = m[1]; m[2].forEach(s => SL[m[0]+":"+s[0]] = s[1]); });

/* ───── 내용 데이터: [메뉴, 하위메뉴, 구분, 제목, 내용, 주요사업, 위탁내용] ───── */
const D = [
["cn","intro","개념","탄소중립이란?","사람의 활동으로 배출한 온실가스의 양과 숲·기술 등으로 흡수·제거한 양을 같게 만들어 순배출을 0(Net-Zero)으로 하는 것입니다."],
["cn","intro","용어","온실가스에는 어떤 것이 있을까?","이산화탄소(CO₂), 메탄(CH₄), 아산화질소(N₂O), 수소불화탄소(HFCs), 과불화탄소(PFCs), 육불화황(SF₆) 6가지를 6대 온실가스라고 하며, 이산화탄소 환산량(CO₂eq)으로 합산해 관리합니다."],
["cn","intro","도시","왜 도시인가?","사람과 경제 활동이 모이는 도시에서 에너지 소비와 온실가스 배출 대부분이 발생합니다.\n도시별 배출 특성에 맞춘 감축 전략이 탄소중립 실현의 핵심입니다."],
["cn","intro","탄소중립도시","탄소중립도시란?","탄소중립 관련 계획 및 기술 등을 적극 활용하여 탄소중립을 공간적으로 구현하는 도시입니다(탄소중립기본법 제29조)."],

["cn","vision","비전","2050 탄소중립 실현","2020년 10월 2050 탄소중립을 선언했고, 탄소중립기본법(2022.3 시행)으로 법적 목표가 되었습니다."],
["cn","vision","2030 목표","2030 국가 온실가스 감축목표(NDC)","2018년 대비 40% 감축(시행령 제3조)"],
["cn","vision","2035 목표","2035 국가 온실가스 감축목표(NDC)","2018년 대비 53~61% 감축(2025.11 국무회의 의결)"],
["cn","vision","전략 · 전력","재생에너지 확대","재생에너지 보급 확대와 석탄발전 감축"],
["cn","vision","전략 · 산업","산업 탈탄소화","연료·원료의 탈탄소화와 저탄소 제품 생산"],
["cn","vision","전략 · 건물","제로에너지 건축","제로에너지 건축과 그린 리모델링 확산, 열 공급의 전기화"],
["cn","vision","전략 · 수송","무공해차 전환","전기·수소차 보급 확대(신차 기준 2030년 40%, 2035년 70%)"],
["cn","vision","전략 · 도시","탄소중립도시 조성","스마트 그린도시 → 탄소중립 그린도시 → 탄소중립 선도도시 3단계로 도시 단위 감축 모델 확산"],

["city","smart","개요","스마트 그린도시","환경질 및 기후회복력 개선을 목적으로 환경기술과 스마트기술을 더하여 도시의 환경체질을 개선하는 미래지향적 환경도시 조성"],
["city","smart","선정 지역","종합선도형·문제해결형 25개 도시","종합선도형 5곳(상주, 화성, 김해, 전주, 강진, 도시별 167억원), 문제해결형 20곳(도시별 100억원) 선정"],
["city","smart","K-water 설계 및 공사 시행","상주","","생태계류, 소규모 메가스테이션, 클린로드, 쿨링포그 등","전체 사업의 설계 및 시공 (167억원, 수변기획처 및 구미사업단)"],
["city","smart","K-water 설계 및 공사 시행","장흥","","수열네트워크 구축 및 공공시설 공급, 수생태계 모니터링","수열 네트워크(하우스시범단지 및 공공시설) 설계·시공 (47억원, 영섬본부)"],
["city","smart","K-water 설계 및 공사 시행","장수","","ICT 기반 탄소저감 아울숲 및 스마트 쉘터 조성","스마트 수질 측정시스템 및 스마트 미터링 구축 설계·시공 (44억원, 동화권지사)"],
["city","green","개요","탄소중립 그린도시","2050 탄소중립 사회로의 전환에 맞춰 탄소중립도시 선도모델을 제시하고 지역 중심의 이행·확산 기반 마련\n에너지전환, 흡수원 확충, 순환경제 촉진 등 탄소중립 정책을 공간적으로 계획·구현하는 도시"],
["city","green","추진현황","수원·충주","’22.4 공모선정(수원, 충주), 사업기간 ’22~’26, 각 400억원(국고 60%, 지방비 40%)\n’22.11 시행계획 수립용역 착수 → ’23.7 중간보고회 → ’24.3~ 사업계획 승인, 기본·실시설계 진행"],
["city","green","공모 제안 기준","환경부 공모 제안 사업내용","① 탄소중립 기반구축: 에너지전환, 흡수원 확대, 자원순환 촉진, 기후변화 적응\n② 사회전환 프로그램: 조례·지침 제·개정, 주민협약, 리빙랩 등 생활행태 개선\n③ 연계사업의 발굴·연계: 지자체 및 중앙부처 사업과 연계"],
["city","pilot","개념","탄소중립 선도도시","탄소중립 기술을 기반으로 탄소를 저감·흡수하여 효율적으로 탄소중립을 구현 또는 지향하도록 선도적으로 조성하는 도시\n개별 감축사업의 집합이 아니라, 지역 내 계획된 모든 사업(정부지원·지자체·민간협력)의 연계성을 극대화하고 누락된 사업을 발굴해 추가 감축 효과 창출"],
["city","pilot","추진경위","선도도시 추진경위","’23 예비후보지 선정(39개소)\n’24 공모·선정(10개소)\n’25 제주, 노원, 당진, 보령 4개소 기본계획 수립\n’26 4개소 실시설계 및 1개소(구미) 기본계획 수립 추진 중"],
["city","pilot","도시 유형","유형별 선도모델","노후주거지 효율화(노원구) · 탈석탄 전환(당진·보령) · 풍부한 재생에너지(제주) · 노후산단(구미)\n건물, 수송, 농축산, 폐기물, 흡수원 등 지자체 관리권한 부문 위주 구성(관리권한 배출량은 전국 평균 약 43.5%)"],

["org","about","2022.12","국가 탄소중립도시 지원기구 지정","탄소중립기본법 제29조에 따라 K-water는 2022년 12월 국가 탄소중립도시 지원기구로 지정되었습니다.\n선도도시 사업 등 탄소중립도시 관련 국가 정책지원 업무를 수행하고 있습니다."],
["org","about","지정 현황","7개 지원기구","K-water(한국수자원공사) · 한국임업진흥원 · 국토연구원 · 건축공간연구원 · 한국건설기술연구원 · 한국국토정보공사(LX) · 한국환경연구원"],
["org","about","주요 역할","정부사업 전 주기 지원","• 스마트 그린도시(1단계)·탄소중립 그린도시(2단계) 성과평가, 사업비 정산, 사업계획 변경 검토\n• 탄소중립 선도도시(3단계) 선정 절차, 대상지 기본계획 수립\n• 주요 사항 의결 및 효율적 사업 추진을 위한 민관협의체 운영·관리"],
["org","about","3단계 시범사업","스마트 그린도시 → 탄소중립 그린도시 → 탄소중립 선도도시","1단계 스마트 그린도시(’21~): 도시 기후변화 대응, 대상지별 100~167억원, 아파트 단지 규모\n2단계 탄소중립 그린도시(’22~’25): 근린단위 탄소감축 이행체계 구축, 대상지별 400억원, 인구 1~2만 근린생활권\n3단계 탄소중립 도시(’26~): 도시단위 탄소감축 본격 이행, 대상지별 1천억원 이상, 도시 단위"],

["org","history","2022.12","지원기구 지정","K-water 국가 탄소중립도시 지원기구 지정, 3단계 시범사업 전 주기 지원 착수"],
["org","history","2022.12~","그린도시 정부 업무 지원","스마트 그린도시·탄소중립 그린도시 성과평가, 사업비 정산, 사업계획 변경 검토 등 정부 부처 업무 지원"],
["org","history","2023 ~ 2024.12","선도도시 민관협의체 운영","환경부에서 추진중인 탄소중립 선도도시 사업의 실효성 제고 및 전문성 강화 등을 위해 구성된 민관협의체의 원활한 운영·관리 수행"],
["org","history","2024.12","선도도시(당진, 제주) 기본계획 수립 위탁","기후부↔K-water 계약 체결, 기본계획 수립 착수"],
["org","history","2025.3","선도도시(보령, 노원) 기본계획 수립 위탁","3.5. 기본계획(보령·노원) 위탁용역 계약, 3.7~ ’25년 민관협의체 위탁계약 체결\n스마트 그린도시 25개 중 12개 지자체 정산 완료(’25.3 기준)"],
["org","history","2026.1","당진·제주 기본계획 수립 완료","’25.4.18.~’26.1.31. 지자체 제안사업 분석, 최종 사업계획 확정"],
["org","history","2026.3","보령·노원 기본계획 수립 완료","’25.6.13.~’26.3.31. 1기 4개소 선도도시 기본계획 수립 완료(’26.3)"],
["org","history","2026.4~","선도도시(구미) 기본계획 수립 위탁","4.27. 위탁용역 계약(기후부↔K-water, 2.9억원), 7.13. 외주용역 착수(~’27.5.8)"],
["org","history","~2030","선도도시 조성 완료 목표","2030년까지 선도도시 10개소 조성 목표, 이후 성과 확산"],

["law","act","대상 법률","기후위기 대응을 위한 탄소중립ㆍ녹색성장 기본법","법률 제18469호(2021.9.24. 공포). 제5장 온실가스 감축 시책 중 탄소중립도시 지원기구 관련 조항"],
["law","act","제29조 제1항","탄소중립도시 조성 정책 수립·시행","국가와 지방자치단체는 탄소중립 관련 계획 및 기술 등을 적극 활용하여 탄소중립을 공간적으로 구현하는 도시(탄소중립도시)를 조성하기 위한 정책을 수립·시행하여야 한다."],
["law","act","제29조 제2항","탄소중립도시의 지정","정부는 각 호의 사업을 시행하고자 하는 도시를 직접 또는 지방자치단체의 장의 요청을 받아 탄소중립도시로 지정할 수 있다."],
["law","act","제29조 제3항","사업 계획의 수립·시행","제2항에 따라 지정된 탄소중립도시를 관할하는 지방자치단체의 장은 탄소중립도시 조성 사업 계획을 수립·시행하여야 한다."],
["law","act","제29조 제4항","비용 보조","정부는 탄소중립도시 조성 사업의 시행을 위하여 필요한 비용의 전부 또는 일부를 보조할 수 있다."],
["law","act","제29조 제5항","지원기구의 지정","정부는 제3항에 따른 사업 계획의 수립·시행 및 이행점검, 조사·연구 등을 수행하기 위하여 공공기관 중 대통령령으로 정하는 기관을 지원기구로 지정할 수 있다."],
["law","act","제29조 제6항","탄소중립도시 지정 취소","정부는 제2항에 따라 지정된 탄소중립도시가 대통령령으로 정하는 지정기준에 맞지 아니하게 된 경우에는 그 지정을 취소할 수 있다."],
["law","act","제29조 제7항","대통령령 위임","제2항부터 제6항까지의 규정에 따른 탄소중립도시의 지정 및 지정취소, 조성 사업 계획의 수립·시행, 지원기구의 지정 및 지정취소 등에 관하여 필요한 사항은 대통령령으로 정한다."],
["law","act","제80조 제2호","청문(지원기구 지정취소)","제29조제7항에 따른 지원기구의 지정취소를 하려는 경우에는 청문을 하여야 한다."],

["law","decree","기준","시행령 조문 기준","2023.5.23. 개정본(대통령령 제33479호) 기준이며 이후 개정으로 부처명(환경부→기후에너지환경부) 등이 달라질 수 있음. 최신 조문은 국가법령정보센터에서 확인"],
["law","decree","제28조 제1항","공동 지정","환경부장관과 국토교통부장관은 법 제29조제2항에 따라 탄소중립도시를 공동으로 지정할 수 있다."],
["law","decree","제28조 제2항","의견 청취","직접 지정하려는 경우 관할 지방자치단체의 장 및 관계 중앙행정기관의 장의 의견을, 지방자치단체의 장 요청에 따라 지정하려는 경우 관계 중앙행정기관의 장의 의견을 들어야 한다."],
["law","decree","제28조 제3항","지정요청서","지정을 요청하려는 지방자치단체의 장은 ① 지정의 필요성과 조성목표 ② 시행 예정 사업 및 분야별 추진계획 ③ 관할구역의 여건 및 인프라 구축계획 ④ 재원조달계획 ⑤ 토지이용 등 도시계획에 관한 사항을 포함한 요청서를 두 장관에게 각각 제출해야 한다."],
["law","decree","제28조 제4항","지정 통보와 공고","지정한 경우 위원회에 보고한 후 지방자치단체의 장 및 관계 중앙행정기관의 장에게 지체 없이 통보하고, 사업 규모, 지정 사유, 사업 내용 및 추진기간을 두 부처 인터넷 홈페이지에 공고해야 한다."],
["law","decree","제28조 제5항","조성 사업 계획 포함사항","① 사업의 목표와 기간 ② 관련 여건 분석 ③ 탄소중립시·도계획 및 시·군·구계획과의 연계방안 ④ 광역도시계획·도시·군기본계획·도시·군관리계획과의 연계방안 ⑤ 재원조달방안"],
["law","decree","제28조 제6항","주민 의견 청취","지방자치단체의 장은 조성 사업 계획을 수립·시행하는 경우 미리 해당 지역 주민의 의견을 들어야 한다."],
["law","decree","제28조 제7항","지원기구 지정 대상 기관","한국수자원공사, 한국환경공단, 한국환경산업기술원, 국토교통과학기술진흥원, 한국토지주택공사, 한국국토정보공사, 한국임업진흥원, 정부출연연구기관, 과학기술분야 정부출연연구기관"],
["law","decree","제28조 제8항","지원기구 경비 지원","환경부장관과 국토교통부장관은 법 제29조제5항에 따라 지정된 지원기구의 업무 수행에 필요한 경비를 예산의 범위에서 지원할 수 있다."],
["law","decree","제28조 제9항","탄소중립도시 지정기준","① 법 제29조제2항 각 호의 사업 시행 추진 ② 탄소중립시·도계획 및 시·군·구계획과 사업의 연계성 확보 ③ 구체적이고 실현가능한 사업계획으로 감축목표 달성에 기여"],
["law","decree","제28조 제10·11항","지정 취소 절차","지정을 취소하려는 경우 미리 지방자치단체의 장 의견을 듣고, 취소 후 위원회 보고, 통보 및 홈페이지 공고(취소 사유, 지정일·취소일, 조성 위치와 사업 내용)"],
["law","decree","제28조 제12항","세부사항 고시","지정·지정취소와 조성 사업 계획의 수립·시행에 필요한 사항은 두 장관이 공동으로 정하여 고시한다."],
["law","decree","제74조 제20항","지원기구에 위탁하는 업무","법 제81조제2항에 따라 탄소중립도시의 지정 및 지정취소를 위한 조사·분석 및 검토 업무를 지원기구에 위탁하며, 수탁자와 위탁업무의 내용은 두 장관이 공동으로 고시한다."],

["law","plan","2023","제1차 국가 탄소중립 녹색성장 기본계획","2030 NDC 달성을 위한 부문별·연도별 감축 대책을 담은 법정 계획"],
["law","plan","2022.12 ~ 2030","탄소중립도시 조성","‘신성장 4.0 추진전략’(2022.12)에 따라 탄소중립도시 10개소 조성 추진\n2030년까지 선도도시 조성 목표"],
["law","plan","2024.8","헌법재판소 헌법불합치 결정","탄소중립기본법이 2031~2049년 감축목표를 규정하지 않은 점에 대해 헌법불합치 결정"],
["law","plan","2026.7 ~ 8","탄소중립기본법 개정안(범위형 목표)","2031~2049년 감축목표를 5년 단위 범위로 설정(2018년 대비): 2035년 53~61%, 2040년 69~80%, 2045년 84~90%\n구체적 수치는 대통령령으로 정하며, 2026.8 국회 기후특위 의결(본회의 통과·공포 여부는 확인 필요)"],

["look","policy","국내 · 2020.10","2050 탄소중립 선언","2020년 10월 2050 탄소중립 목표 선언"],
["look","policy","국내 · 2021.9","탄소중립기본법 제정·시행","기후위기 대응을 위한 탄소중립·녹색성장 기본법 제정(2021.9.24, 법률 제18469호), 2022.3 시행\n제29조에 탄소중립도시 지정 및 지원기구 지정 근거 마련"],
["look","policy","국내 · 2025.11","2035 NDC 확정","2035년 국가 온실가스 감축목표 2018년 대비 53~61%(2025.11 국무회의 의결)"],
["look","policy","국외 · 2015.12","파리협정 채택","지구 평균기온 상승을 산업화 이전 대비 2℃보다 훨씬 낮게 유지하고 1.5℃ 달성을 위해 노력, 각국은 5년 주기로 국가결정기여(NDC) 제출"],
["look","policy","EU · 2026.3","유럽 기후법 2040 목표","2040년 순배출량 1990년 대비 90% 감축을 법제화(2026.3 이사회 최종 승인)\n90% 중 국내 감축 85%, 국제 탄소배출권은 최대 5%까지 활용"],
["look","policy","EU · 2026","탄소국경조정제도(CBAM)","수입품에 내재된 탄소배출에 비용을 부과하는 제도로 2026년부터 본격 시행"],
["look","policy","EU · 2030","기후중립·스마트 도시 미션","2030년까지 유럽 100개 기후중립·스마트 도시 조성(2022.4 대상 도시 선정)"],
["look","policy","일본 · 2025.2","2035·2040 감축목표","2013년 대비 2035년 60%, 2040년 73% 감축(2025.2.18 발표)"],
["look","policy","중국","2060 탄소중립 목표","2030년 이전 탄소배출 정점, 2060년 이전 탄소중립 달성을 선언(2020.9)"],
["look","policy","미국","파리협정 탈퇴","2025.1 파리협정 탈퇴 의사를 통보했으며, 탈퇴는 통보 1년 후 발효"],
["look","policy","안내","자료 기준","2026.11 기준 정리한 내용이며 해외 정책과 개정 법령은 변경될 수 있어 공식 원문 확인 필요"],

["look","faq","수송","휘발유차를 전기차·수소차로 바꾸면?","위 계산기로 내 차 기준 연간 감축량을 확인해 볼 수 있습니다.\n• 전기차: 주행 중 배출은 없지만 충전하는 전기를 만드는 과정에서 배출이 발생하며, 전력 구성에 따라 감축 폭이 달라집니다.\n• 수소차: 주행 중 배출은 물뿐이지만 수소를 만드는 방식(그레이·블루·그린)에 따라 배출이 크게 달라집니다."],
["look","faq","수송","대중교통·자전거·도보로 바꾸면?","같은 거리를 이동할 때 승용차보다 1인당 배출량이 낮으며, 가까운 거리일수록 감축 효과가 뚜렷합니다."],
["look","faq","전기","전기를 아끼면 탄소가 얼마나 줄까?","전기 1kWh를 쓸 때 대략 0.4~0.5kg의 이산화탄소가 배출되는 수준으로 알려져 있습니다(전력 구성에 따라 변동)."],
["look","faq","숲","나무 한 그루는 탄소를 얼마나 흡수할까?","수종·수령에 따라 다르지만 30년생 소나무 1그루가 연간 약 6.6kg의 이산화탄소를 흡수하는 것으로 자주 인용됩니다."],
["look","faq","소비","일회용품·음식물 쓰레기는 왜 탄소와 관련될까?","제품의 생산·운송·폐기 전 과정에서 온실가스가 배출되며, 음식물 쓰레기는 매립·부패 과정에서 메탄이 발생합니다."],
["look","faq","안내","자료 안내","계산기와 설명의 수치는 이해를 돕기 위한 참고용 가정값이며, 정확한 수치는 관계기관 발표 자료를 확인해야 합니다."]
].map(d => ({m:d[0], s:d[1], tag:d[2], h:d[3], p:d[4]||"", a:d[5]||"", b:d[6]||""}));

/* ───── 선도도시 ───── */
const CITIES = [
 {id:"nowon",name:"서울 노원구",img:IMG.nowon,pdf:"(노원구)01_탄소중립 선도도시 기본계획(260709)_최종.pdf",vision:"82%를 뒤집는 도시, 인프라 없이 사람으로 줄이는 탄소",items:[["유형","노후주거지 효율화"],["중점 분야","건축물·수송: 건축물 에너지효율 개선 및 친환경 수송 확대"],["총사업비","1,084억원 · 30개 사업(신규 14개)"],["주요 사업","노원에너지제로주택 운영, 건물 에너지 통합관리 플랫폼 ‘제로빌’, 스마트 자전거도로, 도시형 태양광"]]},
 {id:"dangjin",name:"충남 당진",img:IMG.dangjin,pdf:"(당진시)01_탄소중립 선도도시 기본계획(260707)_최종.pdf",vision:"4,000MW를 끄고 90만 톤을 켜는 탄소중립도시, 당진",items:[["유형","탈석탄 전환"],["중점 분야","에너지·산업공정: 신재생에너지 전환을 통한 산업구조 개선"],["총사업비","3조 5,468억원 · 64개 사업(신규 19개)"],["주요 사업","염해지 태양광 조성, 석문 풍력발전단지, 수소도시 조성, 친환경 수산종합단지"]]},
 {id:"boryeong",name:"충남 보령",img:"",pdf:"",vision:"1.3GW로 부는 탄소중립의 바람",items:[["유형","탈석탄 전환"],["중점 분야","에너지: 신재생에너지 생산 및 활용 고도화"],["총사업비","4조 9,765억원 · 44개 사업(신규 18개)"],["주요 사업","해상풍력 집적화단지, 청정블루수소플랜트, 갯벌생태계 복원, 탄소중립 힐링파크"]]},
 {id:"jeju",name:"제주특별자치도",img:"",pdf:"",vision:"자연으로 채우는 에너지, 관광으로 덜어내는 탄소, 기후중립 섬 제주",items:[["유형","풍부한 재생에너지"],["중점 분야","건축물·수송: 건축물 에너지효율 개선 및 친환경 수송체계 구축"],["총사업비","8조 9,905억원 · 74개 사업(신규 8개)"],["주요 사업","전기자동차 보급, 곶자왈 보호, 공공주도 육해상 풍력자원 개발, 탄소흡수지도 DB 구축"]]},
 {id:"gumi",name:"경북 구미",img:"",pdf:"",vision:"기본계획 수립 중(’26.4~’27.3)",items:[["유형","노후산단"],["구분","’26 신규 대상지"],["기본계획","’26.4.27 위탁용역 계약(기후부↔K-water, 2.9억원), ’26.7.13 외주용역 착수(~’27.5.8)"]]}
];

/* ───── 운영·계획 자료 (파일 이름은 저장소와 똑같아야 합니다) ───── */
const ORG_DOCS = [
 ["지원기구 업무계획","'23 탄소중립도시 지원기구 업무계획_최종f.hwp"],
 ["지원기구 운영계획","'23 탄소중립도시 지원기구 운영계획_2.hwp"],
 ["지원기구 운영 로드맵","'23년 지원기구 운영 로드맵.pptx"],
 ["지원기구 운영 로드맵 (그린도시)","'23년 지원기구 운영 로드맵_그린도시.pptx"],
 ["지원기구 공모 참여계획(방침)","지원기구 공모 참여계획(방침)_최종1.hwp"],
 ["협조체계 구축 계획(안)","탄소중립도시 지원기구 협조체계 구축 계획(안).hwp"]
];
const PLAN_DOCS = [
 ["탄소중립도시 추진계획(요약)","탄소중립도시 추진계획(요약)_최종.hwp"],
 ["탄소중립도시 추진계획","탄소중립도시 추진계획_최종2.hwp"]
];

/* ───── 상태 ───── */
const S = {m:"home", s:"", q:"", city:"nowon", ftype:"전체", km:"12000", eff:"12"};
const firstSub = (m) => { const x = MENU.find(t => t[0] === m); return x && x[2].length ? x[2][0][0] : ""; };
function go(m, s){ S.m = m; S.s = s || firstSub(m); S.q = ""; document.getElementById("q").value = ""; document.getElementById("nav").classList.remove("open"); render(); window.scrollTo(0,0); }
function onSearch(v){ S.q = v; render(); }
function clearSearch(){ S.q = ""; document.getElementById("q").value = ""; render(); }

/* ───── 화면 그리기 ───── */
const fmt = (n) => Math.round(n).toLocaleString("ko-KR");
function rowHTML(r, withGo){
  return `<div class="row"><div class="tag">${r.tag}</div><div class="body">
    <h3>${r.h}</h3>${r.p ? `<p>${r.p}</p>` : ""}
    ${r.a ? `<div class="lbl">주요 사업내용</div><p>${r.a}</p>` : ""}
    ${r.b ? `<div class="lbl">K-water 위탁내용</div><p>${r.b}</p>` : ""}
    ${withGo ? `<button class="gomenu" onclick="go('${r.m}','${r.s}')">해당 메뉴로 이동</button>` : ""}
  </div></div>`;
}
const list = (m, s) => `<div class="panel">${D.filter(r => r.m === m && r.s === s).map(r => rowHTML(r)).join("")}</div>`;
const docList = (docs) => `<div class="panel">${docs.map(d => `<div class="frow"><span class="ft">${d[1].split(".").pop().toUpperCase()}</span><span class="fn">${d[0]}</span><a class="fd" href="${fileUrl(d[1])}" target="_blank" rel="noopener">다운로드</a></div>`).join("")}</div>`;

function homeHTML(){
  const cards = MENU.slice(1).map(m => `<button class="card" onclick="go('${m[0]}')"><div class="k">MENU</div><h3>${m[1]}</h3><p>${m[2].map(s => s[1]).join(" · ")}</p></button>`).join("");
  return `<div class="sec">바로가기</div><div class="cards">${cards}</div>
    <div class="sec">국가 탄소중립도시 지원기구</div>${list("org","about")}`;
}

function timelineHTML(){
  const rows = D.filter(r => r.m === "org" && r.s === "history");
  return `<div class="tl"><div class="tlhead"><div>K-water 탄소중립도시 지원기구 추진경위</div></div>
    <div>${rows.map((r, i) => `<div class="tr ${i % 2 ? "rev" : ""}">
      <div class="tc"><div class="ban"><b>${r.tag}</b>${r.h}</div><div class="tbox">${r.p}</div></div>
      <div class="tm"><div class="line"></div><div class="dot">${i + 1}</div></div><div style="flex:1;padding:0 8px"></div></div>`).join("")}</div>
  </div>`;
}

function pilotHTML(){
  const c = CITIES.find(x => x.id === S.city) || CITIES[0];
  return list("city","pilot") +
    `<div class="sec">선도도시 둘러보기</div>
    <div class="cities">${CITIES.map(x => `<button class="cb ${x.id === c.id ? "on" : ""}" onclick="S.city='${x.id}';render()">${x.name}</button>`).join("")}</div>
    <div class="city"><div class="info">
      <h3>${c.name}</h3><div class="lbl">비전</div><div class="vision">${c.vision}</div>
      <table class="it">${c.items.map(i => `<tr><th>${i[0]}</th><td>${i[1]}</td></tr>`).join("")}</table>
      ${c.pdf ? `<a class="dl" href="${fileUrl(c.pdf)}" target="_blank" rel="noopener">⬇ 기본계획 PDF 받기</a>` : ""}
    </div>${c.img ? `<div class="pic"><img src="${c.img}" alt="${c.name} 선도도시 구상도"></div>` : ""}</div>`;
}

function filesHTML(){
  const types = ["전체","PDF","HWP","PPT","이미지"];
  const shown = FILES.filter(f => S.ftype === "전체" || f.type === S.ftype);
  return `<div class="subs">${types.map(t => `<button class="sb ${S.ftype === t ? "on" : ""}" onclick="S.ftype='${t}';render()">${t}</button>`).join("")}</div>
    <div class="panel">${shown.length ? shown.map(f => `<div class="frow"><span class="ft">${f.type}</span><span class="fn">${f.stem}</span><a class="fd" href="${fileUrl(f.name)}" target="_blank" rel="noopener">다운로드</a></div>`).join("") : `<div class="frow">자료가 없습니다.</div>`}</div>`;
}

function calcHTML(){
  const km = Math.max(0, Number(S.km) || 0), eff = Math.max(1, Number(S.eff) || 12);
  const gas = km / eff * 2.3, ev = km / 5 * 0.43, h2 = km / 100 * 10;
  const bar = (kg, color, name, note) => `<div class="cr"><div class="n">${name}<small>${note}</small></div>
    <div class="track"><div class="fill" style="background:${color};width:${gas > 0 ? Math.min(100, kg / gas * 100) : 0}%"></div></div>
    <div class="v"><b style="font-size:18px">${fmt(kg)}</b> kg CO₂/년 <span style="color:#00539A;font-weight:700">${kg === gas || gas <= 0 ? "" : "▼ " + Math.round((1 - kg / gas) * 100) + "% 감축"}</span></div></div>`;
  return `<div class="calc">
    <div style="font-size:14px;font-weight:700;color:#00539A;letter-spacing:1px;margin-bottom:6px">탄소 감축 계산기</div>
    <h3 style="margin:0 0 18px;font-size:24px;font-weight:900">내 차를 바꾸면 1년에 탄소가 얼마나 줄까?</h3>
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:12px">
      <label>연간 주행거리 (km)<input type="number" min="0" value="${S.km}" onchange="S.km=this.value;render()"></label>
      <label>현재 휘발유차 연비 (km/L)<input type="number" min="1" step="0.5" value="${S.eff}" onchange="S.eff=this.value;render()"></label>
    </div>
    ${bar(gas,"#7C8DA0","휘발유차","현재 차량")}${bar(ev,"#00539A","전기차","국내 전력 평균 가정")}${bar(h2,"#20B9F0","수소차","그레이 수소 가정")}
    <div class="msg">${gas > 0 ? `전기차로 바꾸면 연간 약 ${fmt(gas - ev)}kg, 수소차(그레이 수소)로 바꾸면 약 ${fmt(gas - h2)}kg의 이산화탄소를 줄일 수 있습니다. 전기차 기준 감축량은 30년생 소나무 약 ${fmt((gas - ev) / 6.6)}그루가 1년간 흡수하는 양과 비슷합니다.` : "주행거리를 입력해 주세요."}</div>
    <div class="note">계산 가정(참고용): 휘발유 1L당 2.3kg CO₂, 전기차 전비 5km/kWh, 전력 1kWh당 0.43kg CO₂, 수소차 100km/kg, 수소(그레이) 1kg당 10kg CO₂, 소나무 1그루 연 6.6kg 흡수. 주행 단계만 계산했습니다.</div>
  </div>`;
}

function contentHTML(){
  const k = S.m + ":" + S.s;
  if (S.m === "home") return homeHTML();
  if (k === "city:pilot") return pilotHTML();
  if (k === "org:history") return timelineHTML();
  if (k === "org:docs") return docList(ORG_DOCS);
  if (k === "law:plan") return list("law","plan") + `<div class="sec">관련 계획 자료</div>` + docList(PLAN_DOCS);
  if (k === "look:files") return filesHTML();
  if (k === "look:faq") return calcHTML() + list("look","faq");
  return list(S.m, S.s);
}

function searchHTML(q){
  const key = q.toLowerCase();
  const pool = D.concat(CITIES.map(c => ({m:"city", s:"pilot", tag:"선도도시", h:c.name, p:"비전: " + c.vision + "\n" + c.items.map(i => i[0] + ": " + i[1]).join("\n")})));
  const hits = pool.filter(r => [ML[r.m], SL[r.m+":"+r.s], r.tag, r.h, r.p, r.a, r.b].join(" ").toLowerCase().includes(key));
  const fileHits = FILES.filter(f => f.name.toLowerCase().includes(key));
  let html = `<div class="crumb">통합 검색</div><h2 class="ptitle">‘${q}’ 검색 결과 ${hits.length + fileHits.length}건</h2>`;
  if (hits.length) html += `<div class="panel">${hits.map(r => rowHTML(Object.assign({}, r, {tag: ML[r.m] + " › " + SL[r.m+":"+r.s] + "<br>" + r.tag}), true)).join("")}</div>`;
  if (fileHits.length) html += `<div class="sec">자료</div><div class="panel">${fileHits.map(f => `<div class="frow"><span class="ft">${f.type}</span><span class="fn">${f.stem}</span><a class="fd" href="${fileUrl(f.name)}" target="_blank" rel="noopener">다운로드</a></div>`).join("")}</div>`;
  if (!hits.length && !fileHits.length) html += `<div class="empty">일치하는 내용이 없습니다. 다른 검색어를 입력해 보세요.</div>`;
  return html;
}

function render(){
  const q = S.q.trim(), searching = q.length > 0;
  document.getElementById("clr").style.display = searching ? "" : "none";

  document.getElementById("navtop").innerHTML = MENU.map(m =>
    `<button class="nt ${!searching && S.m === m[0] ? "on" : ""}" onmouseenter="document.getElementById('nav').classList.add('open')" onclick="go('${m[0]}')">${m[1]}</button>`).join("");
  document.getElementById("navcols").innerHTML = MENU.map(m =>
    `<div class="col">${m[2].map(s => `<button class="mi" onclick="go('${m[0]}','${s[0]}')">${s[1]}</button>`).join("")}</div>`).join("");

  document.getElementById("hero").innerHTML = (S.m === "home" && !searching) ? `
    <section class="hero"><div class="c1"></div><div class="c2"></div><div class="in">
      <div class="eyebrow"><span></span>KOREA CENTER FOR NET-ZERO CITIES</div>
      <h1>탄소중립을 도시공간에 구현하는<br>탄소중립도시</h1>
      <p>국가 탄소중립도시 지원기구 K-water가 탄소중립 선도도시를 비롯한 탄소중립도시 정책을 지원합니다.<br>상단 메뉴에서 탄소중립, 탄소중립도시, 지원기구, 법체계 및 계획을 확인해 보세요.</p>
    </div></section>` : "";

  const main = document.getElementById("main");
  if (searching) { main.innerHTML = searchHTML(q); return; }
  if (S.m === "home") { main.innerHTML = homeHTML(); return; }
  const menu = MENU.find(m => m[0] === S.m);
  main.innerHTML = `<div class="crumb">홈 › ${menu[1]} › ${SL[S.m + ":" + S.s]}</div>
    <h2 class="ptitle">${SL[S.m + ":" + S.s]}</h2>
    <div class="subs">${menu[2].map(s => `<button class="sb ${S.s === s[0] ? "on" : ""}" onclick="go('${S.m}','${s[0]}')">${s[1]}</button>`).join("")}</div>
    ${contentHTML()}`;
}
render();
</script>
</body>
</html>
"""

page = (
    PAGE.replace("__FILES__", json.dumps(files, ensure_ascii=False))
    .replace("__IMG_NOWON__", image_data("노원.jpg"))
    .replace("__IMG_DANGJIN__", image_data("당진.jpg"))
    .replace("__RAW__", GITHUB_RAW)
)

components.html(page, height=PAGE_HEIGHT, scrolling=True)
