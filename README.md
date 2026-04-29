# 🧠 AI-First CRM (HCP Interaction Module)

This project is an AI-powered Customer Relationship Management (CRM) system focused on Healthcare Professionals (HCPs). It allows field representatives to log and edit interactions using natural language instead of manually filling forms.

The system follows an AI-first approach where a conversational interface drives the entire workflow.

---

## 🚀 Overview

Users can log interactions through chat, and the system automatically extracts structured data such as doctor name, topics, sentiment, and outcomes. The form is auto-filled instantly. Users can also modify any field using conversational inputs like “actually I met Dr. John” or “sentiment was negative”.

The system supports multi-step conversational editing and keeps the UI synced in real time.

---

## 🎯 Key Features

- Natural language interaction logging  
- Automatic form population using AI  
- Conversational editing of specific fields  
- Multi-step updates without manual input  
- LangGraph-based agent orchestration  
- Clean CRM-style UI with form + chat layout  

---

## 🏗️ Tech Stack

Frontend: React with Redux  
Backend: FastAPI (Python)  
AI Agent Framework: LangGraph  
LLM: Groq (Gemma / LLaMA models)  
Database: PostgreSQL  
Styling: CSS  

---

## 🧠 LangGraph Agent Architecture

The system uses a LangGraph agent to process user queries.

Flow:
User input → Intent Detection → Tool Selection → Tool Execution → Response → UI Update

The agent determines whether the user is creating a new interaction, editing an existing one, or requesting additional insights.

---

## 🛠️ LangGraph Tools

The system implements the required 5 tools:

1. Log Interaction Tool  
   Extracts structured data from natural language input and populates the CRM form.

2. Edit Interaction Tool  
   Updates only the fields mentioned by the user without affecting other data.

3. Summarize Tool  
   Generates a summary of the interaction.

4. Extract Entities Tool  
   Extracts key entities such as doctor name and discussion topics.

5. Follow-up Suggestion Tool  
   Suggests next steps based on the interaction.

---

## ⚙️ Setup Instructions

Clone the repository and navigate into the project folder.

Backend setup:
Go to the backend folder, create a virtual environment using uv, install dependencies, and start the FastAPI server.

Frontend setup:
Go to the frontend folder, install dependencies using npm, and start the React development server.

Backend runs on: http://127.0.0.1:8000  
Frontend runs on: http://localhost:3000  

---

## 🔐 Environment Variables

Create a .env file inside the backend folder and add:

GROQ_API_KEY=your_api_key_here  
DATABASE_URL=postgresql://user:password@localhost:5432/ai_crm  

---

## 🧪 Example Usage

User input:
Today I met Dr. Smith, discussed product X efficacy, positive sentiment

Result:
The system extracts structured data and auto-fills the form.

User input:
Actually I met Dr. John

Result:
Only the HCP name is updated.

User input:
Sentiment was negative

Result:
Only the sentiment field is updated.

---

## 📂 Project Structure

ai-crm/
│
├── frontend/
│   ├── src/
│   │   ├── features/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── agents/
│   │   ├── services/
│   │   └── db/
│
└── README.md

---

## 🎥 Demo Highlights

- Chat-based interaction logging  
- Automatic form filling  
- Conversational editing  
- LangGraph tool execution  
- Real-time UI updates  

---

## 🧠 Key Insight

This project demonstrates how AI can act as the primary interface for CRM systems, reducing manual work and improving usability for field representatives.

---

## 📌 Submission Coverage

React + Redux frontend  
FastAPI backend  
LangGraph agent  
Groq LLM integration  
PostgreSQL database  
5 LangGraph tools implemented  
Chat + Form dual interface  

---

## 👤 Author

Deep Gupta