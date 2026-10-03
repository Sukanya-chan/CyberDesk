import { useState } from "react";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { AccountPage } from "../pages/AccountPage";
import { SignInPage } from "../pages/SignInPage";
import { SignUpPage } from "../pages/SignUpPage";
import { CourseCataloguePage } from "../pages/learn/CourseCataloguePage";
import { CourseDetailPage } from "../pages/learn/CourseDetailPage";
import { LessonPage } from "../pages/learn/LessonPage";
import { AdminContentPage } from "../pages/admin/AdminContentPage";
import { AssessmentCataloguePage } from "../pages/assessments/AssessmentCataloguePage";
import { QuizPage } from "../pages/assessments/QuizPage";
import { ChallengeCataloguePage } from "../pages/challenges/ChallengeCataloguePage";
import { ChallengePage } from "../pages/challenges/ChallengePage";
import { AIAssistantPage } from "../pages/AIAssistantPage";

type View =
  | { kind: "account" } | { kind: "catalogue" } | { kind: "course"; slug: string }
  | { kind: "lesson"; courseSlug: string; lessonSlug: string } | { kind: "admin" }
  | { kind: "assessments" } | { kind: "quiz"; id: number }
  | { kind: "challenges" } | { kind: "challenge"; id: number } | { kind: "ai" };

export function App() {
  const [showSignUp, setShowSignUp] = useState(false);
  const [view, setView] = useState<View>({ kind: "account" });

  const signedInContent = (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">SECURITY LEARNING // 01</div>
          <h2>CyberDesk</h2>
        </div>
        <nav className="nav-stack" aria-label="Main navigation">
          <button className={`nav-btn ${view.kind === "account" ? "active" : ""}`} onClick={() => setView({kind:"account"})}>⌂ Dashboard</button>
          <button className={`nav-btn ${["catalogue","course","lesson"].includes(view.kind) ? "active" : ""}`} onClick={() => setView({kind:"catalogue"})}>◇ Learning</button>
          <button className={`nav-btn ${["assessments","quiz"].includes(view.kind) ? "active" : ""}`} onClick={() => setView({kind:"assessments"})}>◈ Assessments</button>
          <button className={`nav-btn ${["challenges","challenge"].includes(view.kind) ? "active" : ""}`} onClick={() => setView({kind:"challenges"})}>⚡ Challenges</button>
          <button className={`nav-btn ${view.kind === "ai" ? "active" : ""}`} onClick={() => setView({kind:"ai"})}>✦ AI Tutor</button>
        </nav>
        <div className="sidebar-foot">Safe labs · Flag-based practice<br />Local-first student workspace</div>
      </aside>
      <div className="workspace">
        <header className="topbar">
          <span className="status-dot">System online</span>
          <span className="muted">CyberDesk / {view.kind}</span>
        </header>
        <div className="content">
          {view.kind === "account" && <AccountPage
            onLearn={() => setView({kind:"catalogue"})}
            onAdmin={() => setView({kind:"admin"})}
            onAssessments={() => setView({kind:"assessments"})}
            onChallenges={() => setView({kind:"challenges"})}
          />}
          {view.kind === "catalogue" && <CourseCataloguePage onCourse={(slug) => setView({kind:"course",slug})} />}
          {view.kind === "course" && <CourseDetailPage slug={view.slug} onLesson={(lessonSlug) => setView({kind:"lesson",courseSlug:view.slug,lessonSlug})} onBack={() => setView({kind:"catalogue"})} />}
          {view.kind === "lesson" && <LessonPage courseSlug={view.courseSlug} lessonSlug={view.lessonSlug} onBack={() => setView({kind:"course",slug:view.courseSlug})} />}
          {view.kind === "admin" && <AdminContentPage onBack={() => setView({kind:"account"})} />}
          {view.kind === "assessments" && <AssessmentCataloguePage onQuiz={(id) => setView({kind:"quiz",id})} onBack={() => setView({kind:"account"})} />}
          {view.kind === "quiz" && <QuizPage quizId={view.id} onBack={() => setView({kind:"assessments"})} />}
          {view.kind === "challenges" && <ChallengeCataloguePage onChallenge={(id) => setView({kind:"challenge",id})} onBack={() => setView({kind:"account"})} />}
          {view.kind === "challenge" && <ChallengePage challengeId={view.id} onBack={() => setView({kind:"challenges"})} />}
          {view.kind === "ai" && <AIAssistantPage />}
        </div>
      </div>
    </div>
  );

  return <ProtectedRoute
    fallback={
      <div className="auth-page">
        <div>
          {showSignUp ? <SignUpPage /> : <SignInPage />}
          <button className="auth-toggle" type="button" onClick={() => setShowSignUp((prev) => !prev)}>
            {showSignUp ? "Already have an account? Sign in" : "New here? Sign up"}
          </button>
        </div>
      </div>
    }
  >{signedInContent}</ProtectedRoute>;
}
