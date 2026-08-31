import React,{ useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { tickets } from "../api";
import StatusBadge from "../components/StatusBadge";
import { ArrowLeft, Send, Paperclip, Clock3 } from "lucide-react";
import { Link } from "react-router-dom";
export default function TicketDetail() {
  const { id } = useParams();
  const [t, setT] = useState(null),
    [comments, setComments] = useState([]),
    [text, setText] = useState("");
  const load = () =>
    Promise.all([tickets.get(id), tickets.comments(id)]).then(([a, b]) => {
      setT(a.data);
      setComments(b.data);
    });
  useEffect(load, [id]);
  if (!t) return <div className="loading">Loading ticket…</div>;
  const send = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    await tickets.addComment(id, { comment: text });
    setText("");
    load();
  };
  return (
    <>
      <Link className="back" to="/tickets">
        <ArrowLeft size={16} /> Back to tickets
      </Link>
      <div className="ticket-detail">
        <div>
          <div className="detail-top">
            <div>
              <span className="ticket-number">
                #{String(t.id).padStart(4, "0")}
              </span>
              <h2>{t.subject}</h2>
              <div className="badges">
                <StatusBadge value={t.priority} />
                <StatusBadge value={t.status} />
              </div>
            </div>
            <div className="sla-box">
              <Clock3 size={17} />
              <span>SLA deadline</span>
              <b>
                {t.sla_deadline
                  ? new Date(t.sla_deadline).toLocaleString()
                  : "—"}
              </b>
            </div>
          </div>
          <div className="description">
            <p>{t.description}</p>
          </div>
          <div className="comments">
            <h3>Conversation</h3>
            {comments.map((c) => (
              <div className="comment" key={c.id}>
                <div className="avatar">U</div>
                <div>
                  <div className="comment-meta">
                    <b>User #{c.user_id}</b>
                    <span>{new Date(c.created_at).toLocaleString()}</span>
                  </div>
                  <p>{c.comment}</p>
                </div>
              </div>
            ))}
            {!comments.length && (
              <div className="empty small">No comments yet.</div>
            )}
            <form className="comment-box" onSubmit={send}>
              <textarea
                placeholder="Write a reply…"
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
              <div>
                <button type="button" className="ghost">
                  <Paperclip size={16} /> Attach
                </button>
                <button className="primary">
                  <Send size={16} /> Send reply
                </button>
              </div>
            </form>
          </div>
        </div>
        <aside className="detail-side">
          <div>
            <span>Customer</span>
            <b>Customer #{t.customer_id}</b>
          </div>
          <div>
            <span>Assigned agent</span>
            <b>
              {t.assigned_agent_id
                ? `Agent #${t.assigned_agent_id}`
                : "Unassigned"}
            </b>
          </div>
          <div>
            <span>Category</span>
            <b>{t.category_id ? `Category #${t.category_id}` : "General"}</b>
          </div>
          <div>
            <span>Created</span>
            <b>{new Date(t.created_at).toLocaleString()}</b>
          </div>
        </aside>
      </div>
    </>
  );
}
