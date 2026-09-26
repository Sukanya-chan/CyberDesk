# Database Entities

User: id, username, email, password_hash, role, timestamps.
Category: id, name, description.
Course: id, category_id, title, description, difficulty, published, timestamps.
Lesson: id, course_id, title, content, order_index.
LessonProgress: id, user_id, lesson_id, completed_at.
Quiz: id, course_id, title, description.
Question: id, quiz_id, question_text, type.
QuestionOption: id, question_id, option_text, is_correct.
QuizAttempt: id, quiz_id, user_id, score, timestamps.
Challenge: id, title, description, difficulty, category, published.
ChallengeSubmission: id, challenge_id, user_id, result, submitted_at.

Exact schema evolves through documented decisions.
