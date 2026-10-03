export type CourseProgress = {
  course_id: number;
  course_slug: string;
  title: string;
  completed_lessons: number;
  total_lessons: number;
  percent: number;
};

export type DashboardProgress = {
  completed_lessons: number;
  total_lessons: number;
  lesson_percent: number;
  quiz_attempts: number;
  best_quiz_score: number | null;
  solved_challenges: number;
  challenge_points: number;
  courses: CourseProgress[];
  recent_course_slug: string | null;
};

export type LessonProgress = {
  lesson_id: number;
  completed: boolean;
  completed_at: string | null;
};
