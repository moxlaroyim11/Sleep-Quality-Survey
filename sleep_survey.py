import json
import csv
import os
import io
from datetime import datetime, date
import streamlit as st

ALLOWED_EXTENSIONS: tuple = ("txt", "csv", "json")
VALID_NAME_CHARS: frozenset = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'"
)
answered_ids: set = set()
MAX_SCORE: float = 72.0
loaded_from_file: bool = False

QUESTIONS: list = [
    {
        "id": 1,
        "text": "How often do you sleep enough (7-8 hours)?",
        "options": [
            {"label": "Never", "score": 4},
            {"label": "Rarely", "score": 3},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 1},
            {"label": "Always", "score": 0},
        ],
    },
    {
        "id": 2,
        "text": "How often do you go to bed late?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 3,
        "text": "How often do you use phone, computer, or other screens before sleeping?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 4,
        "text": "Do you fall asleep within 30 minutes after going to bed?",
        "options": [
            {"label": "Never", "score": 4},
            {"label": "Rarely", "score": 3},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 1},
            {"label": "Always", "score": 0},
        ],
    },
    {
        "id": 5,
        "text": "How often do you wake up while sleeping?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 6,
        "text": "Can you sleep easily after waking up?",
        "options": [
            {"label": "Never", "score": 4},
            {"label": "Rarely", "score": 3},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 1},
            {"label": "Always", "score": 0},
        ],
    },
    {
        "id": 7,
        "text": "Do you feel rested after waking up?",
        "options": [
            {"label": "Never", "score": 4},
            {"label": "Rarely", "score": 3},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 1},
            {"label": "Always", "score": 0},
        ],
    },
    {
        "id": 8,
        "text": "Do you want to sleep more even if you slept many hours?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 9,
        "text": "How often do you nap during the day?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 10,
        "text": "Do you have trouble concentrating during the day due to lack of sleep?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 11,
        "text": "Does lack of sleep make you irritated?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 12,
        "text": "Do you fall asleep quickly when sitting quietly (during lectures) or riding in a car?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 13,
        "text": "Do you have problems with memorisation because of poor sleep?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 14,
        "text": "Does poor sleep affect your ability to think properly?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 15,
        "text": "Do you have headaches after waking up or during the day?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 16,
        "text": "Has anyone ever noticed you snoring or gasping during sleep?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 17,
        "text": "Does anyone notice your arms or legs moving while you sleep?",
        "options": [
            {"label": "Never", "score": 0},
            {"label": "Rarely", "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often", "score": 3},
            {"label": "Always", "score": 4},
        ],
    },
    {
        "id": 18,
        "text": "How long have you had problems with your sleep?",
        "options": [
            {"label": "I have no sleep problems", "score": 0},
            {"label": "Less than 1 month", "score": 1},
            {"label": "1 to 6 months", "score": 2},
            {"label": "6 months to 1 year", "score": 3},
            {"label": "More than 1 year", "score": 4},
        ],
    },
]

SCORING: tuple = (
    {"min": 0, "max": 10, "label": "Excellent Sleep Quality", "emoji": "🌟", "description": "Your sleep habits are excellent."},
    {"min": 11, "max": 22, "label": "Good Sleep Quality", "emoji": "✅", "description": "Your sleep is generally healthy."},
    {"min": 23, "max": 34, "label": "Moderate Sleep Issues", "emoji": "🟡", "description": "Moderate sleep disturbances."},
    {"min": 35, "max": 46, "label": "Poor Sleep Quality", "emoji": "🟠", "description": "Poor sleep quality."},
    {"min": 47, "max": 58, "label": "Significant Sleep Disorder", "emoji": "🔴", "description": "Significant sleep problems."},
    {"min": 59, "max": 66, "label": "Severe Sleep Deprivation", "emoji": "⚠️", "description": "Severe sleep deprivation."},
    {"min": 67, "max": 72, "label": "Critical Sleep Crisis", "emoji": "🚨", "description": "Critical sleep dysfunction."},
)


def validate_name(name: str) -> bool:
    stripped: str = name.strip()
    if len(stripped) < 2:
        return False
    index: int = 0
    while index < len(stripped):
        char: str = stripped[index]
        if char not in VALID_NAME_CHARS:
            return False
        index += 1
    return True


def validate_student_id(student_id: str) -> bool:
    stripped: str = student_id.strip()
    return stripped.isdigit() and len(stripped) >= 4


def collect_validation_errors(surname: str, given_name: str, student_id: str) -> list:
    name_fields: list = [(surname, "Surname"), (given_name, "Given name")]
    errors: list = []
    for i in range(len(name_fields)):
        value: str = name_fields[i][0]
        label: str = name_fields[i][1]
        if value and not validate_name(value):
            errors.append(f"{label} may only contain letters, hyphens, apostrophes and spaces.")
    if student_id and not validate_student_id(student_id):
        errors.append("Student ID must contain digits only (minimum 4 digits).")
    return errors


def get_result(total_score: int) -> dict:
    for band in SCORING:
        if band["min"] <= total_score <= band["max"]:
            return band
    return SCORING[-1]


def calculate_total_score(questions: list, selections: dict) -> tuple:
    total: int = 0
    answers: list = []
    for q in questions:
        chosen_label: str = selections[q["id"]]
        chosen_opt: dict = next(opt for opt in q["options"] if opt["label"] == chosen_label)
        total += chosen_opt["score"]
        answers.append({
            "question_id": q["id"],
            "question": q["text"],
            "answer": chosen_label,
            "score": chosen_opt["score"],
        })
    return total, answers


def generate_txt(user_info: dict, total_score: int, result: dict, answers: list) -> str:
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list = [
        "SLEEP QUALITY AND WELL-BEING SURVEY - RESULTS",
        "=" * 50,
        f"Name:          {user_info['given_name']} {user_info['surname']}",
        f"Date of Birth: {user_info['dob']}",
        f"Student ID:    {user_info['student_id']}",
        f"Date/Time:     {timestamp}",
        f"Total Score:   {total_score} / {int(MAX_SCORE)}",
        f"Result:        {result['label']}",
        f"Description:   {result['description']}",
        "",
        "--- Answers ---",
    ]
    for ans in answers:
        lines.append(f"Q{ans['question_id']}. {ans['question']}")
        lines.append(f"   Answer: {ans['answer']} (score: {ans['score']})")
    return "\n".join(lines)


def generate_csv(user_info: dict, total_score: int, result: dict, answers: list) -> str:
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output: io.StringIO = io.StringIO()
    fieldnames: list = ["surname", "given_name", "dob", "student_id", "total_score", "max_score", "result_label", "result_description", "timestamp"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({
        "surname": user_info["surname"],
        "given_name": user_info["given_name"],
        "dob": user_info["dob"],
        "student_id": user_info["student_id"],
        "total_score": total_score,
        "max_score": int(MAX_SCORE),
        "result_label": result["label"],
        "result_description": result["description"],
        "timestamp": timestamp,
    })
    return output.getvalue()


def generate_json(user_info: dict, total_score: int, result: dict, answers: list) -> str:
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return json.dumps({
        "surname": user_info["surname"],
        "given_name": user_info["given_name"],
        "dob": user_info["dob"],
        "student_id": user_info["student_id"],
        "total_score": total_score,
        "max_score": int(MAX_SCORE),
        "result_label": result["label"],
        "result_description": result["description"],
        "timestamp": timestamp,
        "answers": answers,
    }, indent=2, ensure_ascii=False)


def load_questions() -> tuple:
    json_path: str = os.path.join(os.getcwd(), "questions.json")
    if os.path.isfile(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data: dict = json.load(f)
            qs: list = data.get("questions", [])
            if qs:
                return qs, True
        except (json.JSONDecodeError, KeyError):
            pass
    return QUESTIONS, False


def main() -> None:
    st.set_page_config(page_title="Sleep Quality Survey", page_icon="😴", layout="centered")
    st.title("😴 Sleep Quality and Well-being Survey")
    questions, from_file = load_questions()
    surname: str = st.text_input("Surname")
    given_name: str = st.text_input("Given Name")
    dob: date = st.date_input("Date of Birth", value=date(2000, 1, 1), min_value=date(1900, 1, 1), max_value=date.today())
    student_id: str = st.text_input("Student ID (digits only)")
    errors: list = collect_validation_errors(surname, given_name, student_id)
    for err in errors:
        st.error(err)
    selections: dict = {}
    all_answered: bool = True
    for q in questions:
        labels: list = [opt["label"] for opt in q["options"]]
        choice = st.radio(f"**Q{q['id']}.** {q['text']}", options=labels, index=None, key=f"q_{q['id']}")
        if choice is None:
            all_answered = False
        else:
            selections[q["id"]] = choice
    if st.button("Submit Survey", type="primary"):
        if not surname or not given_name or not student_id or not all_answered:
            st.error("Please complete all fields and questions.")
            return
        total_score, answers = calculate_total_score(questions, selections)
        result = get_result(total_score)
        st.markdown(f"### {result['emoji']} {result['label']}")
        st.info(result["description"])
        st.progress(total_score / MAX_SCORE)


if __name__ == "__main__":
    main()

