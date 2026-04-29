import { useState } from "react";
import { chatAI } from "../services/api";
import { useDispatch } from "react-redux";
import { setFormData } from "../features/interaction/interactionSlice";

export default function ChatPanel() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const dispatch = useDispatch();

  const formatAIResponse = (cleanData) => {
    const fields = Object.keys(cleanData);

    if (fields.length === 0) {
      return "No updates made.";
    }

    return `✅ Interaction updated successfully. Updated fields: ${fields.join(", ")}`;
  };

  const send = async () => {
  if (!input.trim()) return;

  console.log("Sending:", input);

  const res = await chatAI(input);

  if (res.data.error) {
    console.log("AI error:", res.data);
    return;
  }

  const cleanData = Object.fromEntries(
    Object.entries(res.data).filter(([_, v]) => v !== "" && v !== null)
  );

  dispatch(setFormData(cleanData));

  setMessages((prev) => [
    ...prev,
    { role: "user", text: input },
    {
      role: "ai",
      text: `✅ Interaction updated successfully. Updated fields: ${Object.keys(cleanData).join(", ")}`
    }
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