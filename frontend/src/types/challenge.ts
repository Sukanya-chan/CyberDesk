export interface Challenge {
  id: number;
  slug: string;
  title: string;
  description: string;
  instructions: string | null;
  hint: string | null;
  difficulty: string;
  category: string;
  points: number;
  status: string;
}

export interface ChallengeProgress {
  solved: boolean;
  points_earned: number;
}

export interface ChallengeSubmissionResponse {
  correct: boolean;
  points_awarded: number;
  total_points: number;
  message: string;
}
