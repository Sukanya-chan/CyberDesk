export type Course = {
  id: number;
  category_id: number;
  category_name: string;
  slug: string;
  title: string;
  description: string | null;
};

export type Category = {
  id: number;
  name: string;
  description: string | null;
};

export type LessonSummary = {
  id: number;
  slug: string;
  title: string;
  position: number;
};

export type Module = {
  id: number;
  course_id: number;
  title: string;
  position: number;
  lessons: LessonSummary[];
};

export type CourseDetail = Course & { modules: Module[] };

export type Lesson = {
  id: number;
  course_id: number;
  module_id: number;
  slug: string;
  title: string;
  content: string;
  position: number;
  status: "draft" | "published";
};

export type AdminModule = {
  id: number;
  course_id: number;
  title: string;
  position: number;
};

export type AdminLesson = Lesson;
