import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { setFormData } from "../features/interaction/interactionSlice";
import "./InteractionForm.css";

export default function InteractionForm() {
  const dispatch = useDispatch();
  const form = useSelector((state) => state.interaction);

  const update = (field, value) => {
    dispatch(setFormData({ [field]: value }));
  };

  return (
    <div className="form-container">
      <h2 className="form-title">Log HCP Interaction</h2>

      <div className="form-grid">

        {/* HCP Name */}
        <div className="form-group">
          <label>HCP Name</label>
          <input
            type="text"
            value={form.hcp_name || ""}
            onChange={(e) => update("hcp_name", e.target.value)}
          />
        </div>

        {/* Interaction Type */}
        <div className="form-group">
          <label>Interaction Type</label>
          <select
            value={form.interaction_type || "Meeting"}
            onChange={(e) => update("interaction_type", e.target.value)}
          >
            <option>Meeting</option>
            <option>Call</option>
            <option>Email</option>
          </select>
        </div>

        {/* Date */}
        <div className="form-group">
          <label>Date</label>
          <input
            type="date"
            value={form.date || ""}
            onChange={(e) => update("date", e.target.value)}
          />
        </div>

        {/* Time */}
        <div className="form-group">
          <label>Time</label>
          <input
            type="time"
            value={form.time || ""}
            onChange={(e) => update("time", e.target.value)}
          />
        </div>

        {/* Topics */}
        <div className="form-group full">
          <label>Topics Discussed</label>
          <textarea
            value={form.topics || ""}
            onChange={(e) => update("topics", e.target.value)}
          />
        </div>

        {/* Materials */}
        <div className="form-group">
          <label>Materials Shared</label>
          <input
            type="text"
            value={form.materials || ""}
            onChange={(e) => update("materials", e.target.value)}
          />
        </div>

        {/* Samples */}
        <div className="form-group">
          <label>Samples Distributed</label>
          <input
            type="text"
            value={form.samples || ""}
            onChange={(e) => update("samples", e.target.value)}
          />
        </div>

        {/* Sentiment */}
        <div className="form-group full">
          <label>HCP Sentiment</label>
          <div className="radio-group">
            {["Positive", "Neutral", "Negative"].map((s) => (
              <label key={s}>
                <input
                  type="radio"
                  checked={form.sentiment === s}
                  onChange={() => update("sentiment", s)}
                />
                {s}
              </label>
            ))}
          </div>
        </div>

        {/* Outcomes */}
        <div className="form-group full">
          <label>Outcomes</label>
          <textarea
            value={form.outcomes || ""}
            onChange={(e) => update("outcomes", e.target.value)}
          />
        </div>

        {/* Follow-up */}
        <div className="form-group full">
          <label>Follow-up Actions</label>
          <textarea
            value={form.follow_up || ""}
            onChange={(e) => update("follow_up", e.target.value)}
          />
        </div>

      </div>
    </div>
  );
}