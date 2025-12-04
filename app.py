from flask import Flask, render_template, request

app = Flask(__name__)

# ----- 데이터 정의 -----
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

careers = {
    "경영 컨설턴트": {
        "m": ["경영과학응용", "의사결정론", "기술경영개론"],
        "t": ["논리적 사고", "분석적 성향", "시스템적 사고"],
        "c": ["ADsP", "경영지도사"],
        "r": "논리적 사고와 분석적 성향이 뛰어나고, 의사결정 및 기술경영 과목에 높은 선호도를 보였습니다."
    },
    "물류 관리 전문가": {
        "m": ["공급사슬관리", "기초경영과학", "생산운영관리"],
        "t": ["시스템적 사고", "분석적 성향", "실행력"],
        "c": ["물류관리사", "CPIM(국제자격증)"],
        "r": "시스템적 사고력이 강하고 공급사슬관리 및 생산운영 관련 과목에 대한 선호도와 성취도가 높습니다."
    },
    "산업공학기술자": {
        "m": ["생산운영관리", "인간공학", "설비관리"],
        "t": ["문제 해결 능력", "실행력", "메이킹"],
        "c": ["산업안전기사", "공장관리기술사"],
        "r": "생산 공정 개선 및 설비 관리에 대한 선호도가 높으며, 실제 시스템을 만드는 실행력과 문제 해결 능력이 우수합니다."
    },
    "정보시스템운영자": {
        "m": ["경영정보시스템", "데이터베이스", "객체지향프로그래밍"],
        "t": ["논리적 사고", "데이터 기반 의사결정", "분석적 성향"],
        "c": ["정보처리기사", "SQLD"],
        "r": "IT 시스템, 데이터베이스, 프로그래밍에 관심이 많고, 논리적 분석을 통해 시스템을 안정적으로 운영하는 능력이 있습니다."
    },
    "품질관리사무원": {
        "m": ["실험계획법", "생산운영관리"],
        "t": ["분석적 성향", "논리적 사고", "데이터 기반 의사결정"],
        "c": ["품질경영기사", "6시그마 자격"],
        "r": "실험계획법을 비롯한 통계/분석 과목에 우수하며, 객관적인 데이터 기반으로 품질을 관리하는 능력이 탁월합니다."
    }
}


# -------------------------------------------------
# 메인 페이지
# -------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 중요도
        WEIGHT_MAJOR = int(request.form.get("weight_major"))
        WEIGHT_TRAIT = int(request.form.get("weight_trait"))
        WEIGHT_A_GRADE = int(request.form.get("weight_a_grade"))

        # 전공 선호도
        major_scores = {}
        for m in all_majors:
            major_scores[m] = int(request.form.get(f"major_{m}"))

        # 성향(여러 개 선택 가능)
        traits = request.form.getlist("traits")

        # A0 받은 과목(여러 개 선택 가능)
        a_grade = request.form.getlist("a_grade")

        # ----- 점수 계산 -----
        results = {}

        for job, info in careers.items():
            current_score = 0

            # 전공 점수 계산
            major_sum = sum(major_scores[m] for m in info["m"])
            current_score += major_sum * WEIGHT_MAJOR

            # 성향 점수 계산
            trait_match = sum(1 for t in info["t"] if t in traits)
            current_score += trait_match * WEIGHT_TRAIT

            # A0 과목 점수
            a_match = sum(1 for a in a_grade if a in info["m"])
            current_score += a_match * WEIGHT_A_GRADE

            results[job] = current_score

        # 최종 추천 직업 선택
        best_job = max(results, key=results.get)
        best_info = careers[best_job]

        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        return render_template("index.html",
                               all_majors=all_majors,
                               all_traits=all_traits,
                               results=sorted_results,
                               best_job=best_job,
                               best_info=best_info)

    return render_template("index.html",
                           all_majors=all_majors,
                           all_traits=all_traits,
                           results=None)


if __name__ == '__main__':
    app.run(debug=True)
