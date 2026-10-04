"""Seed CyberDesk Phase 6-8 demo data.

Run from backend/:
    python seed_phase6_8.py

The script is idempotent:
- creates missing database tables
- ensures the Phase 3 learning seed exists
- creates/publishes one 5-question assessment
- creates/publishes three safe flag-based challenges
- does not delete existing data
- stores challenge flags only as SHA-256 hashes

Demo challenge flags are intentionally simple and are printed after seeding so
the student can verify the challenge-submit flow locally.
"""

from __future__ import annotations

import os

from app.db.session import Base, SessionLocal, engine
from app.models import AppUser, Challenge, Course, Question, QuestionOption, Quiz
from app.services.challenges import flag_hash
from seed_learning import seed as seed_learning


QUIZ_TITLE = "Cybersecurity Foundations — Assessment"

QUIZ_DESCRIPTION = (
    "A short assessment covering the CIA triad, authentication, phishing, "
    "least privilege, and basic defensive security."
)

QUIZ_QUESTIONS = [
    {
        "text": "Which CIA triad objective protects information from unauthorized disclosure?",
        "options": [
            ("Confidentiality", True),
            ("Integrity", False),
            ("Availability", False),
            ("Non-repudiation", False),
        ],
    },
    {
        "text": "Which statement best describes authentication?",
        "options": [
            ("Verifying who a user or system is", True),
            ("Determining what an authenticated user may access", False),
            ("Encrypting every file on a computer", False),
            ("Recording every network packet", False),
        ],
    },
    {
        "text": "Which is the clearest example of phishing?",
        "options": [
            ("A deceptive message designed to trick a user into revealing credentials", True),
            ("A scheduled operating-system update", False),
            ("A backup copied to offline storage", False),
            ("A firewall rule blocking an unused port", False),
        ],
    },
    {
        "text": "What does the principle of least privilege require?",
        "options": [
            ("Give users and processes only the access they need", True),
            ("Give every user administrator access", False),
            ("Disable authentication for internal systems", False),
            ("Allow permanent access to every available resource", False),
        ],
    },
    {
        "text": "Which control most directly helps detect suspicious activity after an event occurs?",
        "options": [
            ("Security logging and monitoring", True),
            ("Removing all system logs", False),
            ("Sharing administrator passwords", False),
            ("Disabling access controls", False),
        ],
    },
]

CHALLENGES = [
    {
        "slug": "cia-triad-classifier",
        "title": "CIA Triad Classifier",
        "description": (
            "Identify the CIA triad objective represented by a short security "
            "scenario. This is a knowledge-based challenge with no code execution."
        ),
        "instructions": (
            "Scenario: A security control prevents an unauthorized person from "
            "reading confidential customer records. Identify the CIA objective "
            "and submit the provided flag format."
        ),
        "hint": "Think about which CIA objective deals with unauthorized disclosure.",
        "difficulty": "easy",
        "category": "Fundamentals",
        "points": 50,
        "flag": "CYBERDESK{confidentiality}",
    },
    {
        "slug": "least-privilege",
        "title": "Least Privilege",
        "description": (
            "Recognize the defensive principle that limits a user's permissions "
            "to the minimum required for the task."
        ),
        "instructions": (
            "A student account only receives permissions required to complete "
            "coursework. Submit the flag associated with this principle."
        ),
        "hint": "The principle minimizes unnecessary permissions.",
        "difficulty": "easy",
        "category": "Access Control",
        "points": 75,
        "flag": "CYBERDESK{least_privilege}",
    },
    {
        "slug": "phishing-defense",
        "title": "Phishing Defense",
        "description": (
            "Classify a social-engineering scenario and identify the defensive "
            "concept that should be applied."
        ),
        "instructions": (
            "A message impersonates a trusted service and asks the recipient "
            "to enter a password through an unfamiliar link. Identify the "
            "attack category and submit the challenge flag."
        ),
        "hint": "The attack relies on deception rather than exploiting a server directly.",
        "difficulty": "medium",
        "category": "Social Engineering",
        "points": 100,
        "flag": "CYBERDESK{phishing}",
    },
]


def get_or_create_quiz(db, course: Course) -> Quiz:
    quiz = db.query(Quiz).filter(Quiz.title == QUIZ_TITLE).first()

    if quiz is None:
        quiz = Quiz(
            course_id=course.id,
            title=QUIZ_TITLE,
            description=QUIZ_DESCRIPTION,
            status="published",
        )
        db.add(quiz)
        db.flush()
    else:
        quiz.course_id = course.id
        quiz.description = QUIZ_DESCRIPTION
        quiz.status = "published"

    return quiz


def seed_quiz(db, course: Course) -> Quiz:
    quiz = get_or_create_quiz(db, course)

    # Make reruns deterministic without duplicating questions.
    existing = {
        q.question_text: q
        for q in db.query(Question)
        .filter(Question.quiz_id == quiz.id)
        .all()
    }

    for position, item in enumerate(QUIZ_QUESTIONS, start=1):
        question = existing.get(item["text"])

        if question is None:
            question = Question(
                quiz_id=quiz.id,
                question_text=item["text"],
                type="mcq",
                position=position,
            )
            db.add(question)
            db.flush()
        else:
            question.position = position
            question.type = "mcq"

            # Rebuild options on rerun so the demo data stays deterministic.
            for option in list(question.options):
                db.delete(option)
            db.flush()

        for option_position, (text, is_correct) in enumerate(
            item["options"], start=1
        ):
            db.add(
                QuestionOption(
                    question_id=question.id,
                    option_text=text,
                    position=option_position,
                    is_correct=is_correct,
                )
            )

    return quiz


def seed_challenges(db) -> list[Challenge]:
    seeded: list[Challenge] = []

    for item in CHALLENGES:
        challenge = (
            db.query(Challenge)
            .filter(Challenge.slug == item["slug"])
            .first()
        )

        if challenge is None:
            challenge = Challenge(
                slug=item["slug"],
                title=item["title"],
                description=item["description"],
                instructions=item["instructions"],
                hint=item["hint"],
                difficulty=item["difficulty"],
                category=item["category"],
                points=item["points"],
                flag_hash=flag_hash(item["flag"]),
                status="published",
            )
            db.add(challenge)
        else:
            challenge.title = item["title"]
            challenge.description = item["description"]
            challenge.instructions = item["instructions"]
            challenge.hint = item["hint"]
            challenge.difficulty = item["difficulty"]
            challenge.category = item["category"]
            challenge.points = item["points"]
            challenge.flag_hash = flag_hash(item["flag"])
            challenge.status = "published"

        seeded.append(challenge)

    return seeded


def ensure_admin_user(db) -> None:
    """Promote the configured Clerk user to admin, if that AppUser exists.

    Set ADMIN_CLERK_USER_ID in the deployment environment. The user must have
    signed in at least once so Clerk authentication has created the AppUser row.
    """
    clerk_user_id = os.getenv("ADMIN_CLERK_USER_ID", "").strip()
    if not clerk_user_id:
        print("ADMIN_CLERK_USER_ID not set; skipping admin promotion.")
        return

    user = (
        db.query(AppUser)
        .filter(AppUser.clerk_user_id == clerk_user_id)
        .first()
    )
    if user is None:
        print(
            "Configured admin Clerk user is not registered in app_users yet; "
            "skipping admin promotion until that account signs in."
        )
        return

    if user.role != "admin":
        user.role = "admin"
        db.commit()
        print(f"Promoted configured Clerk user to admin: {clerk_user_id}")
    else:
        print(f"Configured admin already has admin role: {clerk_user_id}")


def seed() -> None:
    # Safe for the already-created isolated DB and also works on a fresh one.
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # Reuse the existing Phase 3 learning seed so this script can bootstrap
    # the complete demo database instead of depending on execution order.
    seed_learning()

    db = SessionLocal()

    try:
        course = (
            db.query(Course)
            .filter(Course.slug == "cybersecurity-foundations")
            .first()
        )

        if course is None:
            raise RuntimeError(
                "Expected cybersecurity-foundations course after learning seed."
            )

        course.status = "published"

        quiz = seed_quiz(db, course)
        challenges = seed_challenges(db)

        db.commit()

        ensure_admin_user(db)

        # Refresh after commit for reliable IDs in the output.
        db.refresh(quiz)
        for challenge in challenges:
            db.refresh(challenge)

        print("\nPhase 6-8 seed completed successfully.")
        print(f"Course      : {course.title} [published]")
        print(
            f"Assessment  : {quiz.id} — {quiz.title} "
            f"[published, {len(QUIZ_QUESTIONS)} questions]"
        )
        print("Challenges  :")
        for challenge, source in zip(challenges, CHALLENGES):
            print(
                f"  {challenge.id} — {challenge.title} "
                f"[published, {challenge.points} pts]"
            )
            print(f"    Demo flag: {source['flag']}")

        print("\nExpected public content:")
        print(f"  GET /api/quizzes -> quiz {quiz.id}")
        print(f"  GET /api/challenges -> {len(challenges)} challenges")

        print(
            "\nCore progress remains server-derived: quiz attempts and "
            "successful challenge submissions are recorded only through "
            "their authenticated APIs."
        )

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
