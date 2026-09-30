import { useAuth, useClerk, UserButton } from "@clerk/react";
import { useEffect, useState } from "react";
import { fetchCurrentUser } from "../services/authFetch";
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

  useEffect(() => {
    let cancelled = false;
    fetchCurrentUser(getToken).then((data) => {
      if (!cancelled) { setUser(data); setState("success"); }
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
