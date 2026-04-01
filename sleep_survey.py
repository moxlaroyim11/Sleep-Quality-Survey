"""
Sleep Quality and Well-being Survey
Fundamentals of Programming - Project 1
"""

import json
import csv
import re
import os
from datetime import datetime

# ─────────────────────────────────────────────
# SURVEY DATA (embedded in code + loaded from file)
# ─────────────────────────────────────────────

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
        "text": "Do you want to sleep more even if you slept more hours?",
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
        "text": "Do you have problems with memorization because of poor sleep?",
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

SCORING: list = [
    {"min": 0,  "max": 10, "label": "Excellent Sleep Quality",
     "description": "Your sleep habits are excellent. Your psychological and physical well-being is well-supported. No intervention needed."},
    {"min": 11, "max": 22, "label": "Good Sleep Quality",
     "description": "Your sleep is generally healthy with minor issues. Maintaining good sleep hygiene is recommended."},
    {"min": 23, "max": 34, "label": "Moderate Sleep Issues",
     "description": "You show moderate sleep disturbances that may be affecting your daily functioning. Consider improving your sleep routine."},
    {"min": 35, "max": 46, "label": "Poor Sleep Quality",
     "description": "Your sleep quality is poor and is likely impacting your mood, concentration, and energy. Lifestyle changes are advisable."},
    {"min": 47, "max": 58, "label": "Significant Sleep Disorder",
     "description": "You are experiencing significant sleep problems affecting your psychological well-being. Consulting a healthcare professional is recommended."},
    {"min": 59, "max": 66, "label": "Severe Sleep Deprivation",
     "description": "Your sleep deprivation is severe and poses a serious risk to your mental and physical health. Please seek professional medical advice promptly."},
    {"min": 67, "max": 72, "label": "Critical Sleep Crisis",
     "description": "You are in a critical state of sleep dysfunction. Immediate consultation with a medical or psychological professional is strongly advised."},
]

# ─────────────────────────────────────────────
# INPUT VALIDATION FUNCTIONS
# ─────────────────────────────────────────────

def validate_name(name: str) -> bool:
    """Validate that name contains only letters, hyphens, apostrophes, spaces."""
    pattern = r"^[a-zA-Z][a-zA-Z\s\-']*$"
    return bool(re.match(pattern, name.strip())) and len(name.strip()) >= 2


def validate_date_of_birth(dob: str) -> bool:
    """Validate date of birth in DD/MM/YYYY format."""
    try:
        date = datetime.strptime(dob.strip(), "%d/%m/%Y")
        # Must be in the past and not too far back
        if date >= datetime.now():
            return False
        if date.year < 1900:
            return False
        return True
    except ValueError:
        return False


def validate_student_id(student_id: str) -> bool:
    """Validate that student ID contains only digits."""
    return student_id.strip().isdigit() and len(student_id.strip()) >= 4


# ─────────────────────────────────────────────
# SURVEY LOGIC FUNCTIONS
# ─────────────────────────────────────────────

def get_result(total_score: int) -> dict:
    """Return the scoring band that matches the total score."""
    for band in SCORING:
        if band["min"] <= total_score <= band["max"]:
            return band
    return SCORING[-1]  # fallback to last band


def run_survey(questions: list) -> tuple:
    """
    Ask each survey question and collect answers.
    Returns (total_score, answers_list).
    """
    total_score: int = 0
    answers: list = []

    print("\n" + "=" * 60)
    print("       SLEEP QUALITY AND WELL-BEING SURVEY")
    print("=" * 60)
    print("For each question, enter the number of your answer.\n")

    for q in questions:
        print(f"\nQ{q['id']}. {q['text']}")
        opts = q["options"]
        for i, opt in enumerate(opts, start=1):
            print(f"  {i}. {opt['label']}")

        # While loop for input validation
        while True:
            choice = input("Your answer (enter number): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(opts):
                break
            print(f"  [!] Please enter a number between 1 and {len(opts)}.")

        chosen: dict = opts[int(choice) - 1]
        total_score += chosen["score"]
        answers.append({
            "question_id": q["id"],
            "question":    q["text"],
            "answer":      chosen["label"],
            "score":       chosen["score"],
        })

    return total_score, answers


def collect_user_info() -> dict:
    """Collect and validate user personal details."""
    print("\n--- Personal Information ---")

    # Surname - for loop used for retry counter feedback
    surname: str = ""
    for attempt in range(1, 6):
        surname = input("Enter your surname: ").strip()
        if validate_name(surname):
            break
        print(f"  [!] Invalid surname. Only letters, hyphens, apostrophes and spaces allowed. (Attempt {attempt}/5)")
    else:
        print("Too many invalid attempts. Exiting.")
        exit()

    # Given name
    given_name: str = ""
    for attempt in range(1, 6):
        given_name = input("Enter your given name: ").strip()
        if validate_name(given_name):
            break
        print(f"  [!] Invalid name. Only letters, hyphens, apostrophes and spaces allowed. (Attempt {attempt}/5)")
    else:
        print("Too many invalid attempts. Exiting.")
        exit()

    # Date of birth - while loop validation
    dob: str = ""
    while True:
        dob = input("Date of birth (DD/MM/YYYY): ").strip()
        if validate_date_of_birth(dob):
            break
        print("  [!] Invalid date. Use DD/MM/YYYY format and a valid past date.")

    # Student ID - while loop validation
    student_id: str = ""
    while True:
        student_id = input("Student ID (digits only): ").strip()
        if validate_student_id(student_id):
            break
        print("  [!] Invalid student ID. Only digits are allowed (minimum 4 digits).")

    return {
        "surname":    surname,
        "given_name": given_name,
        "dob":        dob,
        "student_id": student_id,
    }


# ─────────────────────────────────────────────
# FILE PERSISTENCE FUNCTIONS
# ─────────────────────────────────────────────

def save_results(user_info: dict, total_score: int, result: dict, answers: list) -> None:
    """Offer to save results in TXT, CSV, or JSON format."""
    print("\n--- Save Results ---")
    print("Would you like to save your results?")
    print("  1. TXT")
    print("  2. CSV")
    print("  3. JSON")
    print("  4. Do not save")

    choice: str = ""
    while True:
        choice = input("Choose (1-4): ").strip()
        if choice in {"1", "2", "3", "4"}:
            break
        print("  [!] Please enter 1, 2, 3, or 4.")

    if choice == "4":
        print("Results not saved.")
        return

    filename: str = f"{user_info['student_id']}_sleep_survey"
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Build a flat record dict for CSV/TXT
    record: dict = {
        "surname":    user_info["surname"],
        "given_name": user_info["given_name"],
        "dob":        user_info["dob"],
        "student_id": user_info["student_id"],
        "total_score": total_score,
        "result_label": result["label"],
        "result_description": result["description"],
        "timestamp": timestamp,
    }

    if choice == "1":
        filepath: str = f"{filename}.txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("SLEEP QUALITY AND WELL-BEING SURVEY - RESULTS\n")
            f.write("=" * 50 + "\n")
            f.write(f"Name:        {user_info['given_name']} {user_info['surname']}\n")
            f.write(f"Date of Birth: {user_info['dob']}\n")
            f.write(f"Student ID:  {user_info['student_id']}\n")
            f.write(f"Date/Time:   {timestamp}\n")
            f.write(f"Total Score: {total_score}\n")
            f.write(f"Result:      {result['label']}\n")
            f.write(f"Description: {result['description']}\n")
            f.write("\n--- Answers ---\n")
            for ans in answers:
                f.write(f"Q{ans['question_id']}. {ans['question']}\n")
                f.write(f"   Answer: {ans['answer']} (score: {ans['score']})\n")
        print(f"Results saved to '{filepath}'.")

    elif choice == "2":
        filepath: str = f"{filename}.csv"
        fieldnames: list = list(record.keys())
        # Check if file already exists to write header only once
        file_exists: bool = os.path.isfile(filepath)
        with open(filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(record)
        print(f"Results saved to '{filepath}'.")

    elif choice == "3":
        filepath: str = f"{filename}.json"
        full_record: dict = {**record, "answers": answers}
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(full_record, f, indent=2, ensure_ascii=False)
        print(f"Results saved to '{filepath}'.")


def load_results() -> None:
    """Load and display a previously saved result file."""
    filename: str = input("Enter the filename to load (with extension): ").strip()

    if not os.path.isfile(filename):
        print(f"  [!] File '{filename}' not found.")
        return

    ext: str = filename.lower().rsplit(".", 1)[-1]

    if ext == "txt":
        with open(filename, "r", encoding="utf-8") as f:
            print("\n" + f.read())

    elif ext == "csv":
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows: list = list(reader)
        if not rows:
            print("  [!] CSV file is empty.")
            return
        print("\n--- Survey Results (CSV) ---")
        for row in rows:
            for key, val in row.items():
                print(f"  {key}: {val}")
            print()

    elif ext == "json":
        with open(filename, "r", encoding="utf-8") as f:
            data: dict = json.load(f)
        print("\n--- Survey Results (JSON) ---")
        print(f"  Name:        {data.get('given_name')} {data.get('surname')}")
        print(f"  Student ID:  {data.get('student_id')}")
        print(f"  Total Score: {data.get('total_score')}")
        print(f"  Result:      {data.get('result_label')}")
        print(f"  Description: {data.get('result_description')}")
        answers: list = data.get("answers", [])
        if answers:
            print("\n  Answers:")
            for ans in answers:
                print(f"    Q{ans['question_id']}. {ans['answer']} (score: {ans['score']})")
    else:
        print("  [!] Unsupported file format. Use .txt, .csv, or .json.")


# ─────────────────────────────────────────────
# MAIN PROGRAM
# ─────────────────────────────────────────────

def main() -> None:
    """Main entry point: lets user start a new survey or load existing results."""
    print("\n" + "=" * 60)
    print("   SLEEP QUALITY AND WELL-BEING SURVEY SYSTEM")
    print("=" * 60)
    print("\nWhat would you like to do?")
    print("  1. Start a new survey")
    print("  2. Load existing results from a file")

    # While loop for menu selection validation
    choice: str = ""
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice in {"1", "2"}:
            break
        print("  [!] Please enter 1 or 2.")

    if choice == "2":
        load_results()
        return

    # --- NEW SURVEY ---
    # Try loading questions from external JSON file (bonus: both embedded + file)
    questions: list = QUESTIONS  # default: embedded
    json_file: str = "questions.json"
    if os.path.isfile(json_file):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data: dict = json.load(f)
            questions = data.get("questions", QUESTIONS)
            print(f"\n[Info] Questions loaded from '{json_file}'.")
        except (json.JSONDecodeError, KeyError):
            print(f"\n[Warning] Could not parse '{json_file}'. Using embedded questions.")
    else:
        print("\n[Info] Using embedded questions.")

    # Collect user info with validation
    user_info: dict = collect_user_info()

    # Run the survey
    total_score: int
    answers: list
    total_score, answers = run_survey(questions)

    # Determine result
    result: dict = get_result(total_score)

    # Display result
    print("\n" + "=" * 60)
    print("                   YOUR RESULT")
    print("=" * 60)
    print(f"  Name:        {user_info['given_name']} {user_info['surname']}")
    print(f"  Student ID:  {user_info['student_id']}")
    print(f"  Total Score: {total_score} / 72")
    print(f"  Result:      {result['label']}")
    print(f"\n  {result['description']}")
    print("=" * 60)

    # Offer to save
    save_results(user_info, total_score, result, answers)

    print("\nThank you for completing the survey. Goodbye!\n")


if __name__ == "__main__":
    main()
