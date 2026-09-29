import { useState } from "react";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { AccountPage } from "../pages/AccountPage";
import { SignInPage } from "../pages/SignInPage";
import { SignUpPage } from "../pages/SignUpPage";
import { CourseCataloguePage } from "../pages/learn/CourseCataloguePage";
import { CourseDetailPage } from "../pages/learn/CourseDetailPage";
import { LessonPage } from "../pages/learn/LessonPage";
import { AdminContentPage } from "../pages/admin/AdminContentPage";

type View =
  | { kind: "account" }
  | { kind: "catalogue" }
  | { kind: "course"; slug: string }
  | { kind: "lesson"; courseSlug: string; lessonSlug: string }
  | { kind: "admin" };

export function App() {
  const [showSignUp, setShowSignUp] = useState(false);
  const [view, setView] = useState<View>({ kind: "account" });

  return (
    <ProtectedRoute
      fallback={
        <>
          {showSignUp ? <SignUpPage /> : <SignInPage />}
          <button type="button" onClick={() => setShowSignUp((prev) => !prev)}>
            {showSignUp ? "Already have an account? Sign in" : "New here? Sign up"}
          </button>
        </>
      }
    >
      {view.kind === "account" && (
        <AccountPage
          onLearn={() => setView({ kind: "catalogue" })}
          onAdmin={() => setView({ kind: "admin" })}
        />
      )}
      {view.kind === "catalogue" && (
        <CourseCataloguePage onCourse={(slug) => setView({ kind: "course", slug })} />
      )}
      {view.kind === "course" && (
        <CourseDetailPage
          slug={view.slug}
          onLesson={(lessonSlug) =>
            setView({ kind: "lesson", courseSlug: view.slug, lessonSlug })
          }
          onBack={() => setView({ kind: "catalogue" })}
        />
      )}
      {view.kind === "lesson" && (
        <LessonPage
          courseSlug={view.courseSlug}
          lessonSlug={view.lessonSlug}
          onBack={() => setView({ kind: "course", slug: view.courseSlug })}
        />
      )}
      {view.kind === "admin" && (
        <AdminContentPage onBack={() => setView({ kind: "account" })} />
      )}
    </ProtectedRoute>
  );
}
