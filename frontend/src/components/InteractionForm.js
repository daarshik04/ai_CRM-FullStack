import { useDispatch, useSelector } from "react-redux";
import { setFormData } from "../features/interaction/interactionSlice";
import { logInteraction } from "../services/api";

export default function InteractionForm() {
  const dispatch = useDispatch();
  const form = useSelector((state) => state.interaction.form);

  const update = (key, value) => {
    dispatch(setFormData({ [key]: value }));
  };

  const handleSubmit = async () => {
    await logInteraction({
      hcp_name: form.hcp_name,
      notes: form.topics
    });
    alert("Interaction saved!");
  };

  return (
    <div className="card">
      <h2>Log HCP Interaction</h2>

      <label>HCP Name</label>
      <input
        placeholder="Search or select HCP..."
        value={form.hcp_name}
        onChange={(e) => update("hcp_name", e.target.value)}
      />

      <label>Interaction Type</label>
      <select>
        <option>Meeting</option>
        <option>Call</option>
      </select>

      <label>Date</label>
      <input
  type="date"
  value={form.date || ""}
  onChange={(e) => update("date", e.target.value)}
/>

      <label>Time</label>
      <input
  type="time"
  value={form.time || ""}
  onChange={(e) => update("time", e.target.value)}
/>

      <label>Topics Discussed</label>
      <textarea
        placeholder="Enter key discussion points..."
        value={form.topics}
        onChange={(e) => update("topics", e.target.value)}
      />

      <label>Sentiment</label>
      <select
        value={form.sentiment}
        onChange={(e) => update("sentiment", e.target.value)}
      >
        <option>Positive</option>
        <option>Neutral</option>
        <option>Negative</option>
      </select>

      <label>Outcomes</label>
      <textarea
        value={form.outcomes}
        onChange={(e) => update("outcomes", e.target.value)}
      />

      <label>Follow-up Actions</label>
      <textarea
        value={form.follow_up}
        onChange={(e) => update("follow_up", e.target.value)}
      />

      {/* AI suggestions */}
      <div className="ai-suggestions">
        • Schedule follow-up in 2 weeks  
        • Send product brochure  
      </div>

      <button onClick={handleSubmit}>Save Interaction</button>
    </div>
  );
}