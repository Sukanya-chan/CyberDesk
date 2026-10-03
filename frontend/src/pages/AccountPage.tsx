import { useAuth, useClerk, UserButton } from "@clerk/react";
import { useEffect, useState } from "react";
import { fetchCurrentUser } from "../services/authFetch";
import { fetchDashboardProgress } from "../services/progress";
import type { DashboardProgress } from "../types/progress";
import type { AppUser } from "../types/user";

type LoadState = "loading" | "success" | "error";

export function AccountPage({
  onLearn, onAdmin, onAssessments, onChallenges,
}: {
  onLearn: () => void; onAdmin: () => void; onAssessments: () => void; onChallenges: () => void;
}) {
  const { getToken } = useAuth();
  const { signOut } = useClerk();
  const [state, setState] = useState<LoadState>("loading");
  const [user, setUser] = useState<AppUser | null>(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [progress, setProgress] = useState<DashboardProgress | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([fetchCurrentUser(getToken), fetchDashboardProgress(getToken)]).then(([data, progressData]) => {
      if (!cancelled) { setUser(data); setProgress(progressData); setState("success"); }
    }).catch((error: unknown) => {
      if (!cancelled) { setErrorMessage(error instanceof Error ? error.message : "Unknown error"); setState("error"); }
    });
    return () => { cancelled = true; };
  }, [getToken]);

  return (
    <main>
      <section className="hero">
        <div className="eyebrow">CYBERDESK / COMMAND CENTER</div>
        <h1 className="page-title">Build your security edge.</h1>
        <p className="page-subtitle">Learn the fundamentals, test your knowledge, and solve safe cybersecurity challenges from one focused workspace.</p>
        {state === "loading" && <p className="loading" role="status">Syncing your account…</p>}
        {state === "error" && <p className="alert" role="alert">Could not load account: {errorMessage}</p>}
        {state === "success" && user && (
          <div className="card-action">
            <span className="tag">ROLE: {user.role}</span>
            <div style={{display:"flex",gap:8,alignItems:"center"}}>
              <UserButton />
              <button type="button" onClick={() => signOut()}>Sign out</button>
            </div>
          </div>
        )}
      </section>

      {state === "success" && progress && (
        <>
          <div className="section-head"><h2>Progress</h2><span className="muted">Authoritative server-side learning state</span></div>
          <section className="grid grid-4">
            <div className="card"><span className="muted">Lessons</span><div className="metric">{progress.completed_lessons}/{progress.total_lessons}</div></div>
            <div className="card"><span className="muted">Completion</span><div className="metric">{progress.lesson_percent}%</div></div>
            <div className="card"><span className="muted">Quiz attempts</span><div className="metric">{progress.quiz_attempts}</div></div>
            <div className="card"><span className="muted">Challenge points</span><div className="metric">{progress.challenge_points}</div></div>
          </section>
          <section className="grid grid-2 progress-courses">
            {progress.courses.map(course => <article className="card" key={course.course_id}>
              <div className="card-action"><span className="eyebrow">COURSE</span><span className="tag">{course.percent}%</span></div>
              <h3>{course.title}</h3>
              <div className="progress-track" aria-label={`${course.percent}% complete`}><span style={{width:`${course.percent}%`}} /></div>
              <p className="muted">{course.completed_lessons} of {course.total_lessons} published lessons completed.</p>
              <button onClick={() => onLearn()}>Continue →</button>
            </article>)}
            {!progress.courses.length && <div className="card"><h3>No published courses yet.</h3><p className="muted">Ask an admin to publish learning content.</p></div>}
          </section>
        </>
      )}

      <div className="section-head"><h2>Workspace</h2><span className="muted">Choose your next operation</span></div>
      <section className="grid grid-3">
        <article className="card"><div className="eyebrow">01 / Learn</div><h2>Learning</h2><p>Work through published cybersecurity courses, modules, and lessons.</p><div className="card-action"><span className="tag">KNOWLEDGE</span><button className="primary" onClick={onLearn}>Open →</button></div></article>
        <article className="card"><div className="eyebrow">02 / Test</div><h2>Assessments</h2><p>Challenge your understanding with scored multiple-choice assessments.</p><div className="card-action"><span className="tag">SCORED</span><button className="primary" onClick={onAssessments}>Start →</button></div></article>
        <article className="card"><div className="eyebrow">03 / Practice</div><h2>Challenges</h2><p>Apply concepts through safe, flag-based cybersecurity challenges.</p><div className="card-action"><span className="tag">CTF LAB</span><button className="primary" onClick={onChallenges}>Enter →</button></div></article>
      </section>

      {state === "success" && user?.role === "admin" && (
        <section className="section-head">
          <div><h2>Administration</h2><span className="muted">Manage published learning content.</span></div>
          <button onClick={onAdmin}>Open content console →</button>
        </section>
      )}

      <section className="section-head"><h2>System status</h2></section>
      <section className="grid grid-3">
        <div className="card"><span className="muted">Authentication</span><div className="metric">ACTIVE</div></div>
        <div className="card"><span className="muted">Learning API</span><div className="metric">READY</div></div>
        <div className="card"><span className="muted">Challenge mode</span><div className="metric">SAFE</div></div>
      </section>
    </main>
  );
}
