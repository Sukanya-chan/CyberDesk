from app.db.session import SessionLocal
from app.models.category import Category
from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson


def seed():
    db = SessionLocal()

    try:
        # Category
        category = (
            db.query(Category)
            .filter(Category.name == "Cybersecurity Fundamentals")
            .first()
        )

        if not category:
            category = Category(
                name="Cybersecurity Fundamentals",
                description="Core concepts and foundations of cybersecurity.",
            )
            db.add(category)
            db.flush()

        # Course
        course = (
            db.query(Course)
            .filter(Course.slug == "cybersecurity-foundations")
            .first()
        )

        if not course:
            course = Course(
                category_id=category.id,
                slug="cybersecurity-foundations",
                title="Cybersecurity Foundations",
                description="A practical introduction to fundamental cybersecurity concepts.",
                status="published",
            )
            db.add(course)
            db.flush()
        else:
            course.status = "published"

        # Module 1
        module1 = (
            db.query(Module)
            .filter(
                Module.course_id == course.id,
                Module.title == "Security Foundations",
            )
            .first()
        )

        if not module1:
            module1 = Module(
                course_id=course.id,
                title="Security Foundations",
                position=1,
            )
            db.add(module1)
            db.flush()

        lessons = [
            {
                "slug": "what-is-cybersecurity",
                "title": "What Is Cybersecurity?",
                "position": 1,
                "content": """# What Is Cybersecurity?

Cybersecurity is the practice of protecting systems, networks, applications, devices, and data from unauthorized access, disruption, modification, or destruction.

A cybersecurity program typically focuses on:

- Confidentiality
- Integrity
- Availability
- Authentication
- Authorization
- Monitoring and incident response

The goal is not simply to prevent attacks, but also to detect, respond to, and recover from security incidents.""",
            },
            {
                "slug": "cia-triad",
                "title": "CIA Triad",
                "position": 2,
                "content": """# CIA Triad

The CIA triad is a foundational security model consisting of three objectives.

## Confidentiality

Information should only be accessible to authorized users.

## Integrity

Information should remain accurate and protected from unauthorized modification.

## Availability

Systems and information should be accessible when authorized users need them.

These three objectives are used when designing and evaluating security controls.""",
            },
            {
                "slug": "common-cyber-threats",
                "title": "Common Cyber Threats",
                "position": 3,
                "content": """# Common Cyber Threats

Common cybersecurity threats include:

- Phishing
- Malware
- Credential theft
- Denial-of-service attacks
- Web application vulnerabilities
- Social engineering
- Misconfiguration
- Unauthorized access

Understanding common attack categories helps security professionals identify appropriate defensive controls.""",
            },
        ]

        for item in lessons:
            lesson = (
                db.query(Lesson)
                .filter(
                    Lesson.course_id == course.id,
                    Lesson.slug == item["slug"],
                )
                .first()
            )

            if not lesson:
                lesson = Lesson(
                    module_id=module1.id,
                    course_id=course.id,
                    slug=item["slug"],
                    title=item["title"],
                    content=item["content"],
                    position=item["position"],
                    status="published",
                )
                db.add(lesson)
            else:
                lesson.module_id = module1.id
                lesson.course_id = course.id
                lesson.title = item["title"]
                lesson.content = item["content"]
                lesson.position = item["position"]
                lesson.status = "published"

        db.commit()

        print("Learning seed completed successfully.")
        print(f"Category : {category.name}")
        print(f"Course   : {course.title} [{course.status}]")
        print(f"Module   : {module1.title}")

        for lesson in (
            db.query(Lesson)
            .filter(Lesson.module_id == module1.id)
            .order_by(Lesson.position)
            .all()
        ):
            print(f"  Lesson : {lesson.title} [{lesson.status}]")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
