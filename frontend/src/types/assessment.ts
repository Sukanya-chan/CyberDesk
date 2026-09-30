export interface QuizSummary {
  id: number;
  course_id: number;
  title: string;
  description: string | null;
  status: string;
}

export interface QuizOption {
  id: number;
  option_text: string;
  position: number;
}

export interface QuizQuestion {
  id: number;
  question_text: string;
  position: number;
  options: QuizOption[];
}

export interface QuizDetail extends QuizSummary {
  questions: QuizQuestion[];
}

export interface QuizAnswerResult {
  question_id: number;
  selected_option_id: number | null;
  is_correct: boolean;
}

export interface QuizAttemptResponse {
  id: number;
  quiz_id: number;
  score: number;
  total_questions: number;
  submitted_at: string;
  answers: QuizAnswerResult[];
}

export interface AttemptSummary {
  id: number;
  quiz_id: number;
  score: number;
  total_questions: number;
  submitted_at: string;
}
