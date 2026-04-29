import { useState } from "react";
import { chatAI } from "../services/api";
import { useDispatch } from "react-redux";
import { setFormData } from "../features/interaction/interactionSlice";

export default function ChatPanel() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const dispatch = useDispatch();

  const formatAIResponse = (data) => {
    const fields = Object.keys(data);

    if (fields.length === 0) {
      return "No updates made.";
    }

    return `✅ Interaction updated successfully. Updated fields: ${fields.join(", ")}`;
  };

  const send = async () => {
    const res = await chatAI(input);

    if (res.data.error) {
      console.log("AI error:", res.data);
      return;
    }

    // clean data (important)
    const cleanData = Object.fromEntries(
      Object.entries(res.data).filter(([_, v]) => v !== "" && v !== null)
    );

    // update form (merge)
    dispatch(setFormData(cleanData));

    // update chat UI
    setMessages([
      ...messages,
      { role: "user", text: input },
      { role: "ai", text: formatAIResponse(cleanData) }
    ]);

    setInput("");
  };

  return (
    <div>
      <h3>AI Assistant</h3>

      <div className="chat-box">
        {messages.map((m, i) => (
          <div key={i} style={{
            marginBottom: 12
          }}>
            <div style={{
              background: m.role === "user" ? "#e6f0ff" : "#e6f4ea",
              borderLeft: m.role === "user"
                ? "4px solid #3b82f6"
                : "4px solid #22c55e",
              padding: "10px",
              borderRadius: "8px"
            }}>
              {m.text}
            </div>
          </div>
        ))}
      </div>

      <input
        placeholder="Describe interaction..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button onClick={send}>Log</button>
    </div>
  );
}