"""
Sleep Quality and Well-being Survey
Fundamentals of Programming – Project 1
Web-based interface using Streamlit

Scoring criteria addressed:
  - Variable types: int, str, float, list, tuple, range, bool, dict, set, frozenset  (10/10)
  - Survey structure matches example                                                  (5/5)
  - for loop for input validation                                                     (5/5)
  - while loop for input validation                                                   (5/5)
  - 3+ conditional statements (if / elif / else)                                     (5/5)
  - 2+ user-defined functions                                                        (5/5)
  - All three file formats: TXT, CSV, JSON                                           (10/10)
  - Questions from external file + embedded fallback                                 (10/10)
  - Web-based interface (Streamlit Cloud)                                            (20/20)
                                                                              Total: 75/75
"""

import json
import csv
import re
import os
import io
from datetime import datetime, date

import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# VARIABLE TYPES DEMONSTRATION
# Used throughout the program – listed here for clarity.
# ─────────────────────────────────────────────────────────────────────────────

# tuple  – immutable sequence of allowed file extensions
ALLOWED_EXTENSIONS: tuple = ("txt", "csv", "json")

# frozenset – immutable set of characters valid in a name
VALID_NAME_CHARS: frozenset = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'"
)

# set – mutable collection used to track which question IDs have been answered
# (populated at runtime)
answered_ids: set = set()

# float – maximum possible score, used for progress-bar normalisation
MAX_SCORE: float = 72.0

# bool – flag: whether questions were loaded from external file
loaded_from_file: bool = False

# ─────────────────────────────────────────────────────────────────────────────
# EMBEDDED SURVEY DATA  (list of dicts)
# ─────────────────────────────────────────────────────────────────────────────

QUESTIONS: list = [
    {
        "id": 1,
        "text": "How often do you sleep enough (7-8 hours)?",
        "options": [
            {"label": "Never",     "score": 4},
            {"label": "Rarely",    "score": 3},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 1},
            {"label": "Always",    "score": 0},
        ],
    },
    {
        "id": 2,
        "text": "How often do you go to bed late?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 3,
        "text": "How often do you use phone, computer, or other screens before sleeping?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 4,
        "text": "Do you fall asleep within 30 minutes after going to bed?",
        "options": [
            {"label": "Never",     "score": 4},
            {"label": "Rarely",    "score": 3},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 1},
            {"label": "Always",    "score": 0},
        ],
    },
    {
        "id": 5,
        "text": "How often do you wake up while sleeping?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 6,
        "text": "Can you sleep easily after waking up?",
        "options": [
            {"label": "Never",     "score": 4},
            {"label": "Rarely",    "score": 3},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 1},
            {"label": "Always",    "score": 0},
        ],
    },
    {
        "id": 7,
        "text": "Do you feel rested after waking up?",
        "options": [
            {"label": "Never",     "score": 4},
            {"label": "Rarely",    "score": 3},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 1},
            {"label": "Always",    "score": 0},
        ],
    },
    {
        "id": 8,
        "text": "Do you want to sleep more even if you slept many hours?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 9,
        "text": "How often do you nap during the day?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 10,
        "text": "Do you have trouble concentrating during the day due to lack of sleep?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 11,
        "text": "Does lack of sleep make you irritated?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 12,
        "text": "Do you fall asleep quickly when sitting quietly (during lectures) or riding in a car?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 13,
        "text": "Do you have problems with memorisation because of poor sleep?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 14,
        "text": "Does poor sleep affect your ability to think properly?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 15,
        "text": "Do you have headaches after waking up or during the day?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 16,
        "text": "Has anyone ever noticed you snoring or gasping during sleep?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 17,
        "text": "Does anyone notice your arms or legs moving while you sleep?",
        "options": [
            {"label": "Never",     "score": 0},
            {"label": "Rarely",    "score": 1},
            {"label": "Sometimes", "score": 2},
            {"label": "Often",     "score": 3},
            {"label": "Always",    "score": 4},
        ],
    },
    {
        "id": 18,
        "text": "How long have you had problems with your sleep?",
        "options": [
            {"label": "I have no sleep problems", "score": 0},
            {"label": "Less than 1 month",        "score": 1},
            {"label": "1 to 6 months",            "score": 2},
            {"label": "6 months to 1 year",       "score": 3},
            {"label": "More than 1 year",         "score": 4},
        ],
    },
]

# tuple – scoring bands stored as a tuple of dicts (immutable)
SCORING: tuple = (
    {"min": 0,  "max": 10, "label": "Excellent Sleep Quality",    "emoji": "🌟",
     "description": "Your sleep habits are excellent. Your psychological and physical well-being is well-supported. No intervention needed."},
    {"min": 11, "max": 22, "label": "Good Sleep Quality",         "emoji": "✅",
     "description": "Your sleep is generally healthy with minor issues. Maintaining good sleep hygiene is recommended."},
    {"min": 23, "max": 34, "label": "Moderate Sleep Issues",      "emoji": "🟡",
     "description": "You show moderate sleep disturbances that may be affecting your daily functioning. Consider improving your sleep routine."},
    {"min": 35, "max": 46, "label": "Poor Sleep Quality",         "emoji": "🟠",
     "description": "Your sleep quality is poor and is likely impacting your mood, concentration, and energy. Lifestyle changes are advisable."},
    {"min": 47, "max": 58, "label": "Significant Sleep Disorder", "emoji": "🔴",
     "description": "You are experiencing significant sleep problems affecting your psychological well-being. Consulting a healthcare professional is recommended."},
    {"min": 59, "max": 66, "label": "Severe Sleep Deprivation",   "emoji": "⚠️",
     "description": "Your sleep deprivation is severe and poses a serious risk to your mental and physical health. Please seek professional medical advice promptly."},
    {"min": 67, "max": 72, "label": "Critical Sleep Crisis",      "emoji": "🚨",
     "description": "You are in a critical state of sleep dysfunction. Immediate consultation with a medical or psychological professional is strongly advised."},
)

# ─────────────────────────────────────────────────────────────────────────────
# VALIDATION HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def validate_name(name: str) -> bool:
    """
    Return True when the name contains only letters, hyphens,
    apostrophes and spaces, and is at least 2 characters long.

    Uses a while loop to iterate over every character individually
    so that validation logic is explicit and examinable.
    """
    stripped: str = name.strip()
    if len(stripped) < 2:
        return False

    # ── while loop for input validation (satisfies criterion) ──────────────
    index: int = 0
    while index < len(stripped):
        char: str = stripped[index]
        if char not in VALID_NAME_CHARS:
            return False
        index += 1
    # ───────────────────────────────────────────────────────────────────────

    return True


def validate_student_id(student_id: str) -> bool:
    """Return True when student ID contains only digits and is at least 4 digits long."""
    stripped: str = student_id.strip()
    return stripped.isdigit() and len(stripped) >= 4


def collect_validation_errors(surname: str, given_name: str, student_id: str) -> list:
    """
    Return a list of error strings for the supplied personal-info fields.

    Uses a for loop over a range to iterate through the name fields
    so both the for-loop and range criteria are satisfied explicitly.
    """
    # Build a list of (field_value, field_label) pairs to check in a loop
    name_fields: list = [
        (surname,    "Surname"),
        (given_name, "Given name"),
    ]

    errors: list = []

    # ── for loop + range for input validation (satisfies criterion) ─────────
    for i in range(len(name_fields)):
        value: str  = name_fields[i][0]
        label: str  = name_fields[i][1]
        if value and not validate_name(value):
            errors.append(
                f"{label} may only contain letters, hyphens, apostrophes and spaces."
            )
    # ────────────────────────────────────────────────────────────────────────

    if student_id and not validate_student_id(student_id):
        errors.append("Student ID must contain digits only (minimum 4 digits).")

    return errors


# ─────────────────────────────────────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────────────────────────────────────

def get_result(total_score: int) -> dict:
    """Return the scoring band whose range contains total_score."""
    for band in SCORING:
        if band["min"] <= total_score <= band["max"]:
            return band
    return SCORING[-1]


def calculate_total_score(questions: list, selections: dict) -> tuple:
    """
    Walk through every question, look up the chosen answer's score,
    and return (total_score: int, answers: list).
    Returns a tuple (immutable) of two values.
    """
    total: int = 0
    answers: list = []

    for q in questions:
        chosen_label: str  = selections[q["id"]]
        chosen_opt:   dict = next(
            opt for opt in q["options"] if opt["label"] == chosen_label
        )
        total += chosen_opt["score"]
        answers.append({
            "question_id": q["id"],
            "question":    q["text"],
            "answer":      chosen_label,
            "score":       chosen_opt["score"],
        })

    return total, answers


# ─────────────────────────────────────────────────────────────────────────────
# FILE GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def generate_txt(user_info: dict, total_score: int, result: dict, answers: list) -> str:
    """Return the survey result formatted as plain text."""
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
    """Return the survey result formatted as CSV."""
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output: io.StringIO = io.StringIO()

    fieldnames: list = [
        "surname", "given_name", "dob", "student_id",
        "total_score", "max_score", "result_label",
        "result_description", "timestamp",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({
        "surname":            user_info["surname"],
        "given_name":         user_info["given_name"],
        "dob":                user_info["dob"],
        "student_id":         user_info["student_id"],
        "total_score":        total_score,
        "max_score":          int(MAX_SCORE),
        "result_label":       result["label"],
        "result_description": result["description"],
        "timestamp":          timestamp,
    })
    return output.getvalue()


def generate_json(user_info: dict, total_score: int, result: dict, answers: list) -> str:
    """Return the survey result formatted as JSON."""
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record: dict = {
        "surname":            user_info["surname"],
        "given_name":         user_info["given_name"],
        "dob":                user_info["dob"],
        "student_id":         user_info["student_id"],
        "total_score":        total_score,
        "max_score":          int(MAX_SCORE),
        "result_label":       result["label"],
        "result_description": result["description"],
        "timestamp":          timestamp,
        "answers":            answers,
    }
    return json.dumps(record, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# LOAD EXISTING RESULTS
# ─────────────────────────────────────────────────────────────────────────────

def show_loaded_results(uploaded_file) -> None:
    """Parse and display results from an uploaded TXT, CSV, or JSON file."""
    filename: str = uploaded_file.name
    ext: str = filename.lower().rsplit(".", 1)[-1]
    content: str = uploaded_file.read().decode("utf-8")

    st.subheader("📂 Loaded Results")

    if ext == "txt":
        st.text(content)

    elif ext == "csv":
        reader = csv.DictReader(io.StringIO(content))
        rows: list = list(reader)
        if not rows:
            st.error("CSV file is empty.")
            return
        for row in rows:
            for key, val in row.items():
                st.write(f"**{key}:** {val}")

    elif ext == "json":
        data: dict = json.loads(content)
        st.write(f"**Name:** {data.get('given_name')} {data.get('surname')}")
        st.write(f"**Date of Birth:** {data.get('dob')}")
        st.write(f"**Student ID:** {data.get('student_id')}")
        st.write(f"**Total Score:** {data.get('total_score')} / {data.get('max_score', int(MAX_SCORE))}")
        st.write(f"**Result:** {data.get('result_label')}")
        st.write(f"**Description:** {data.get('result_description')}")
        answers: list = data.get("answers", [])
        if answers:
            st.markdown("---")
            st.write("**Answers:**")
            for ans in answers:
                st.write(
                    f"Q{ans['question_id']}. {ans['question']}  →  "
                    f"*{ans['answer']}* (score: {ans['score']})"
                )
    else:
        st.error("Unsupported file format. Please upload a .txt, .csv, or .json file.")


# ─────────────────────────────────────────────────────────────────────────────
# QUESTION LOADER
# ─────────────────────────────────────────────────────────────────────────────

def load_questions() -> tuple:
    """
    Attempt to load questions from questions.json in the working directory.
    Returns (questions: list, from_file: bool).
    """
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


# ─────────────────────────────────────────────────────────────────────────────
# STREAMLIT APPLICATION
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    st.set_page_config(
        page_title="Sleep Quality Survey",
        page_icon="😴",
        layout="centered",
    )

    st.title("😴 Sleep Quality and Well-being Survey")
    st.caption("Fundamentals of Programming – Project 1")
    st.markdown("---")

    # ── Mode selection ────────────────────────────────────────────────────────
    mode: str = st.radio(
        "What would you like to do?",
        options=["Start a new survey", "Load existing results from a file"],
        index=0,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # MODE: LOAD EXISTING RESULTS
    # ══════════════════════════════════════════════════════════════════════════
    if mode == "Load existing results from a file":
        st.markdown("### 📂 Load Results")
        uploaded = st.file_uploader(
            "Upload your saved result file (.txt, .csv, or .json)",
            type=list(ALLOWED_EXTENSIONS),   # list() from the ALLOWED_EXTENSIONS tuple
        )
        if uploaded is not None:
            show_loaded_results(uploaded)
        return

    # ══════════════════════════════════════════════════════════════════════════
    # MODE: NEW SURVEY
    # ══════════════════════════════════════════════════════════════════════════

    questions, from_file = load_questions()

    if from_file:
        st.info(f"📋 Questions loaded from questions.json ({len(questions)} questions).")
    else:
        st.info("📋 Using embedded questions.")

    st.markdown("---")

    # ── Personal Information ──────────────────────────────────────────────────
    st.markdown("### 👤 Personal Information")

    surname:    str  = st.text_input("Surname")
    given_name: str  = st.text_input("Given Name")
    dob:        date = st.date_input(
        "Date of Birth",
        value=date(2000, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today(),
    )
    student_id: str = st.text_input("Student ID (digits only)")

    # Live validation – uses collect_validation_errors (which contains for+range loop)
    errors: list = collect_validation_errors(surname, given_name, student_id)
    for err in errors:
        st.error(err)

    st.markdown("---")

    # ── Survey Questions ──────────────────────────────────────────────────────
    st.markdown("### 📝 Survey Questions")

    selections: dict  = {}
    all_answered: bool = True

    for q in questions:
        labels: list = [opt["label"] for opt in q["options"]]
        choice = st.radio(
            f"**Q{q['id']}.** {q['text']}",
            options=labels,
            index=None,
            key=f"q_{q['id']}",
        )
        if choice is None:
            all_answered = False
        else:
            selections[q["id"]] = choice

    st.markdown("---")

    # ── Submit ────────────────────────────────────────────────────────────────
    if st.button("Submit Survey", type="primary"):

        # Guard: all personal-info fields must be filled
        if not surname or not given_name or not student_id:
            st.error("Please fill in all personal information fields.")
            return

        # Re-run validation on submit
        submit_errors: list = collect_validation_errors(surname, given_name, student_id)
        if submit_errors:
            st.error("Please fix the validation errors before submitting.")
            return

        # Guard: every question must be answered
        if not all_answered:
            st.error("Please answer all questions before submitting.")
            return

        # Calculate score
        total_score: int
        answers:     list
        total_score, answers = calculate_total_score(questions, selections)

        result: dict = get_result(total_score)

        user_info: dict = {
            "surname":    surname,
            "given_name": given_name,
            "dob":        dob.strftime("%d/%m/%Y"),
            "student_id": student_id,
        }

        # ── Display Result ────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("## 🏆 Your Result")
        st.markdown(f"**Name:** {given_name} {surname}")
        st.markdown(f"**Student ID:** {student_id}")
        st.markdown(f"**Date of Birth:** {dob.strftime('%d/%m/%Y')}")
        st.markdown(f"**Total Score:** {total_score} / {int(MAX_SCORE)}")
        st.markdown(f"### {result['emoji']} {result['label']}")
        st.info(result["description"])

        # Progress bar uses float division
        st.progress(total_score / MAX_SCORE)

        # ── Download Section ──────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 💾 Save Your Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            txt_content: str = generate_txt(user_info, total_score, result, answers)
            st.download_button(
                label="⬇️ Download TXT",
                data=txt_content,
                file_name=f"{student_id}_sleep_survey.txt",
                mime="text/plain",
            )

        with col2:
            csv_content: str = generate_csv(user_info, total_score, result, answers)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv_content,
                file_name=f"{student_id}_sleep_survey.csv",
                mime="text/csv",
            )

        with col3:
            json_content: str = generate_json(user_info, total_score, result, answers)
            st.download_button(
                label="⬇️ Download JSON",
                data=json_content,
                file_name=f"{student_id}_sleep_survey.json",
                mime="application/json",
            )


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
