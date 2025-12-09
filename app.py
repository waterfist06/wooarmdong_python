# Flask에서 웹 앱을 만들기 위해 필요한 것들 불러오기
from flask import Flask, render_template, request, session
import os  # 파일/폴더 경로 확인, 생성 등에 사용

# 그래프(이미지)로 저장하기 위한 설정
import matplotlib
matplotlib.use('Agg')   # macOS에서 GUI 없이 그래프를 그릴 때 오류가 나는 걸 막아주는 설정

# Flask 앱 생성
app = Flask(__name__)
# 세션(session)을 사용하기 위한 비밀 키 (쿠키 암호화용)
app.secret_key = "wooarmdong"

# 1) 전공 / 성향 / 직업 데이터 정의

# 사용자에게 점수를 입력받을 "전공 과목" 리스트
all_majors = [
    "창의적공학설계", "기술경영개론", "객체지향프로그래밍", "경제성공학", "공급사슬관리",
    "데이터베이스", "기초경영과학", "생산운영관리", "실험계획법", "인간공학",
    "경영정보시스템", "경영과학응용", "설비관리", "의사결정론", "빅데이터분석",
    "캡스톤디자인", "제품개발론"
]

all_traits = [
    "분석적 성향", "논리적 사고", "시스템적 사고", "문제 해결 능력",
    "데이터 기반 의사결정", "창의적 사고", "대인 커뮤니케이션 및 협업",
    "실행력", "메이킹"
]

# 직업 추천에 사용할 데이터베이스(딕셔너리)
# key   : 직업 이름
# value : 그 직업과 관련된 전공(m), 성향(t), 자격증(c), 설명(r)
careers = {
    "경영 컨설턴트": {
        "m": ["경영과학응용", "의사결정론", "기술경영개론"],   
        "t": ["논리적 사고", "분석적 성향", "시스템적 사고"],  
        "c": ["ADsP", "경영지도사"],                         
        "r": "논리적 사고와 분석력이 뛰어나며 문제 해결 중심의 업무에 적합합니다."  
    },
    "물류 관리 전문가": {
        "m": ["공급사슬관리", "기초경영과학", "생산운영관리"],
        "t": ["시스템적 사고", "분석적 성향", "실행력"],
        "c": ["물류관리사", "CPIM"],
        "r": "공급망 전반을 이해하고 운영 효율을 개선하는 데에 강점이 있습니다."
    },
    "변리사": {
        "m": ["기술경영개론", "제품개발론", "경제성공학"],
        "t": ["논리적 사고", "창의적 사고", "분석적 성향"],
        "c": ["변리사 시험", "기술거래사"],
        "r": "기술과 법률을 융합하여 지식재산권을 다루는 직업에 적합합니다."
    },
    "산업공학기술자": {
        "m": ["생산운영관리", "인간공학", "설비관리"],
        "t": ["문제 해결 능력", "실행력", "메이킹"],
        "c": ["산업안전기사"],
        "r": "현장 개선, 공정 설계 등 실제 산업 문제를 해결하는 능력이 뛰어납니다."
    },
    "산업관리원": {
        "m": ["생산운영관리", "설비관리", "인간공학"],
        "t": ["시스템적 사고", "실행력", "대인 커뮤니케이션 및 협업"],
        "c": ["ERP 정보관리사(생산)"],
        "r": "현장의 운영 흐름을 조율하고 관리하는 역할에 적합합니다."
    },
    "생산관리사무원": {
        "m": ["생산운영관리", "기초경영과학", "공급사슬관리"],
        "t": ["분석적 성향", "논리적 사고", "문제 해결 능력"],
        "c": ["ERP 정보관리사(생산)"],
        "r": "생산 계획 수립과 운영 효율화에 강점을 보입니다."
    },
    "연구실 안전전문가": {
        "m": ["인간공학", "실험계획법"],
        "t": ["문제 해결 능력", "시스템적 사고"],
        "c": ["산업안전기사"],
        "r": "연구 환경의 위험 요소를 분석하고 안전 시스템을 구축하는 데 적합합니다."
    },
    "온실가스 인증심사원": {
        "m": ["경제성공학", "생산운영관리"],
        "t": ["분석적 성향", "데이터 기반 의사결정"],
        "c": ["온실가스 관리 산업기사"],
        "r": "환경 규제와 데이터 분석 기반의 평가 업무에 적합합니다."
    },
    "자재관리사무원": {
        "m": ["공급사슬관리", "생산운영관리", "데이터베이스"],
        "t": ["시스템적 사고", "실행력"],
        "c": ["물류관리사"],
        "r": "재고 및 자재 흐름을 체계적으로 관리하는 데에 강점이 있습니다."
    },
    "정보시스템운영자": {
        "m": ["경영정보시스템", "데이터베이스", "객체지향프로그래밍"],
        "t": ["논리적 사고", "분석적 성향"],
        "c": ["정보처리기사", "SQLD"],
        "r": "데이터와 시스템 운영에 관심이 많고 분석에 강합니다."
    },
    "컴퓨터시스템분석가": {
        "m": ["경영정보시스템", "빅데이터분석", "의사결정론"],
        "t": ["논리적 사고", "시스템적 사고"],
        "c": ["정보처리기사"],
        "r": "시스템 최적화와 데이터 분석을 기반으로 개선안을 도출하는 직무에 적합합니다."
    },
    "품질관리사무원": {
        "m": ["실험계획법", "생산운영관리"],
        "t": ["분석적 성향"],
        "c": ["품질경영기사"],
        "r": "데이터 기반 품질 분석과 공정 개선 업무에 잘 맞습니다."
    },
    "품질인증심사전문가": {
        "m": ["실험계획법", "생산운영관리", "의사결정론"],
        "t": ["논리적 사고", "시스템적 사고"],
        "c": ["ISO 9001 심사원"],
        "r": "품질 기준을 평가하고 인증하는 체계적인 업무에 적합합니다."
    },
}

# 2) 메인 페이지

@app.route('/', methods=['GET', 'POST'])  # '/' 주소로 GET/POST 요청 처리
def index():
    # 사용자가 폼을 제출했을 때 (POST 요청)
    if request.method == 'POST':
        # 1) 사용자가 설정한 가중치 가져오기 (문자열 → 정수 변환)
        w_major = int(request.form.get("weight_major"))      # 전공 가중치
        w_trait = int(request.form.get("weight_trait"))      # 성향 가중치
        w_a = int(request.form.get("weight_a_grade"))        # A0 가중치

        # 2) 각 전공별 선호도 점수 가져오기 (1~5점)
        #    예: {"공급사슬관리": 5, "인간공학": 3, ...}
        major_scores = {m: int(request.form.get(f"major_{m}")) for m in all_majors}

        # 3) 체크박스로 선택한 성향 & A0 받은 과목 리스트
        #    예: traits = ["논리적 사고", "실행력"]
        #        a_grade = ["생산운영관리", "실험계획법"]
        traits = request.form.getlist("traits")
        a_grade = request.form.getlist("a_grade")

        # 4) 직업별 점수 계산용 딕셔너리
        #    예: {"경영 컨설턴트": 123, "물류 관리 전문가": 98, ...}
        results = {}

        # 모든 직업에 대해 반복
        for job, info in careers.items():
            # 그 직업과 관련된 전공(m 리스트)에 대해
            # 사용자가 준 점수를 합산
            major_sum = sum(major_scores[m] for m in info["m"])

            # 그 직업이 요구하는 성향(t 리스트) 중
            # 사용자가 선택한 성향(traits)에 포함되는 개수
            trait_match = sum(t in traits for t in info["t"])

            # 사용자가 A0 받은 과목 중에서
            # 그 직업과 관련된 전공(info["m"])에 포함되는 개수
            a_match = sum(a in info["m"] for a in a_grade)

            # 최종 점수 = 전공합 * 전공가중치 + 성향일치수 * 성향가중치 + A0일치수 * A0가중치
            score = major_sum*w_major + trait_match*w_trait + a_match*w_a

            # 직업 이름을 key로, 계산한 점수를 value로 저장
            results[job] = score

        # 5) 가장 점수가 높은 직업 찾기
        best_job = max(results, key=results.get)  # 딕셔너리에서 value(점수)가 가장 큰 key(직업)
        best_info = careers[best_job]             # 그 직업의 상세 정보

        # 6) 상세 분석 페이지에서 다시 쓰기 위해 세션에 저장
        session["major_scores"] = major_scores
        session["traits"] = traits
        session["a_grade"] = a_grade
        session["weights"] = {"major": w_major, "trait": w_trait, "a_grade": w_a}
        session["best_job"] = best_job

        # 7) 직업 별 점수 결과를 점수 내림차순으로 정렬 (순위표용)
        #    sorted_results = [(직업명, 점수), ...] 형태의 리스트
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        # 8) index.html에 데이터 넘겨주기 (결과까지 포함)
        return render_template(
            "index.html",
            all_majors=all_majors,
            all_traits=all_traits,
            results=sorted_results,   # 직업별 점수 순위
            best_job=best_job,        # 1등 직업 이름
            best_info=best_info       # 1등 직업 상세 정보
        )

    # GET 요청이면 (처음 접속) → 아직 결과 없음
    return render_template(
        "index.html",
        all_majors=all_majors,
        all_traits=all_traits,
        results=None   # 결과를 표시하지 않도록 설정
    )


# --------------------------------
# 3) 상세 결과 페이지
# --------------------------------
@app.route('/details')
def details():

    # index()에서 세션에 저장했던 값들을 가져오기
    major_scores = session.get("major_scores")
    traits = session.get("traits")
    a_grade = session.get("a_grade")
    weights = session.get("weights")
    best_job = session.get("best_job")

    # 만약 세션에 결과가 없다면 (바로 /details로 들어온 경우 등)
    if not major_scores:
        return "결과가 없습니다. 먼저 테스트를 진행하세요."

    # 레이더 차트 그리기 준비 
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import math

    # macOS에서 사용할 한글 폰트 경로 중 존재하는 것을 하나 선택(무시해도됨 나때메 만듦)
    font_path = next((f for f in [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/AppleSDGothicNeo-Regular.otf"
    ] if os.path.exists(f)), None)

    # 폰트가 실제로 있으면 matplotlib에 등록(무시해도됨 나때메 만듦)
    if font_path:
        font = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font.get_name()

    # 레이더 차트의 축 이름(라벨) = 전공 과목 이름
    labels = list(major_scores.keys())
    # 레이더 차트의 값 = 각 전공의 점수
    values = list(major_scores.values())

    # 레이더 차트는 원형 그래프라서 각도를 0~2π로 나눠서 사용
    angles = np.linspace(0, 2*math.pi, len(labels), endpoint=False).tolist()
    # 마지막 점과 처음 점을 연결하기 위해 맨 앞 값을 한 번 더 붙여줌
    angles += angles[:1]
    values += values[:1]

    # 레이더 차트 도화지 준비
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)  # polar=True가 원형 그래프

    # 선그리고 안쪽 그림 채우는거임
    ax.plot(angles, values, color="cyan")
    ax.fill(angles, values, color="cyan", alpha=0.25)

    # 축마다 전공 이름 넣는거
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)

    # y축(반지름 방향) 숫자들은 숨기기
    ax.set_yticklabels([])

    # static 폴더가 없으면 만들기
    os.makedirs("static", exist_ok=True)
    # 그래프 이미지를 파일로 저장
    chart_path = "static/major_chart.png"
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close()

    # 적합도 기여도 계산 

    # best_job(1등 직업)의 정보 가져오기
    info = careers[best_job]

    # 1) 전공 기여도: 관련 전공 점수 합 × 전공 가중치 
    major_sum = sum(major_scores[m] for m in info["m"])

    # 2) 성향 기여도: 직업에 필요한 성향 중 사용자가 가진 성향 개수 × 성향 가중치
    trait_match = sum(t in traits for t in info["t"])

    # 3) A0 기여도: 해당 직업 관련 전공 중 A0 받은 과목 개수 × A0 가중치
    a_match = sum(a in info["m"] for a in a_grade)

    # 각 항목별 점수 계산, 상세 분석 페이지 아래에 점수 기여 컨텐츠 추가해서 계산 코드 만듦
    summary = {
        "major": major_sum * weights["major"],    # 전공 점수 기여
        "trait": trait_match * weights["trait"],  # 성향 일치 기여
        "a_grade": a_match * weights["a_grade"],  # A0 과목 기여
    }
    # 총합 점수
    summary["total"] = sum(summary.values())

    # 상세 결과 페이지 렌더링
    # details.html에서:
    # - chart : 레이더 차트 이미지 파일 이름
    # - scores : 전공별 점수
    # - best_job : 추천 직업 이름
    # - best_info : 추천 직업 설명/관련 전공/성향/자격증
    # - summary : 전공/성향/A0 기여도와 총합 점수
    return render_template(
        "details.html",
        chart="major_chart.png",
        scores=major_scores,
        best_job=best_job,
        best_info=info,
        summary=summary
    )

# 4) 직업 소개 페이지

@app.route('/careers')
def career_info():
    # careers 딕셔너리 전체를 careers.html로 넘겨서
    # 직업 카드 형태로 쭉 보여주는 페이지
    return render_template("careers.html", careers=careers)

# 서버 실행
if __name__ == '__main__':
    # 개발 모드(debug=True)로 서버 실행
    # 코드 변경 시 자동 재시작 + 에러 메시지 자세히 표시
    app.run(debug=True)