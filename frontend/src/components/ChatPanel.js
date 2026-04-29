import React, { useState } from "react";
import axios from "axios";
import { useDispatch } from "react-redux";
import { setFormData } from "../features/interaction/interactionSlice";

export default function ChatPanel() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const dispatch = useDispatch();

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;

    // add user message
    setMessages((prev) => [...prev, { role: "user", text: userMessage }]);
    setInput("");

    try {
      console.log("Sending:", userMessage);

      const res = await axios.post(
        "http://127.0.0.1:8000/api/v1/ai/chat",
        null,
        {
          params: { query: userMessage }
        }
      );

      const data = res.data;
      console.log("AI RESPONSE:", data);

      // 🧠 CASE 1 — TEXT RESPONSE (summarize / extract / followup)
      if (data.message) {
        setMessages((prev) => [
          ...prev,
          { role: "ai", text: data.message }
        ]);
        return;
      }

      // 🧠 CASE 2 — STRUCTURED FORM DATA
      Object.keys(data).forEach((key) => {
        if (data[key] !== "" && data[key] !== null && key !== "date" && key !== "time") {
          dispatch(setFormData({ [key]: data[key] }));
        }
      });

      // always update date/time
      if (data.date) dispatch(setFormData({ date: data.date }));
      if (data.time) dispatch(setFormData({ time: data.time }));

      // 🧠 CLEAN AI RESPONSE MESSAGE (better UX)
      const updatedFields = Object.keys(data).filter(
        (k) => k !== "date" && k !== "time"
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text:
            updatedFields.length > 0
              ? `Updated: ${updatedFields.join(", ")}`
              : "No changes detected"
        }
      ]);

    } catch (error) {
      console.error("AI error:", error.response?.data || error.message);

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "❌ Error processing request"
        }
      ]);
    }
  };

  return (
    <div style={{
      border: "1px solid #ccc",
      padding: 10,
      height: "500px",
      display: "flex",
      flexDirection: "column"
    }}>

      <div style={{ flex: 1, overflowY: "auto", marginBottom: 10 }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ marginBottom: 8 }}>
            <b>{msg.role === "user" ? "You" : "AI"}:</b> {msg.text}
          </div>
        ))}
      </div>

      <div style={{ display: "flex" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ flex: 1, padding: 8 }}
          placeholder="Type your interaction..."
        />
        <button onClick={sendMessage} style={{ padding: "8px 12px" }}>
          Send
        </button>
      </div>

    </div>
  );
}