/** Mirrors backend/app/schemas/user.py: AppUserResponse. */
export interface AppUser {
  id: number;
  clerk_user_id: string;
  role: "student" | "admin";
  created_at: string;
  updated_at: string;
}
