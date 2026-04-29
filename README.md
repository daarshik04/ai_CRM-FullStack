🧠 AI-First CRM (HCP Interaction Module)

This project is an AI-powered Customer Relationship Management (CRM) system focused on Healthcare Professionals (HCPs). It allows users to log and edit interactions using natural language instead of manually filling forms. The system follows an AI-first approach where a conversational interface drives the entire workflow.

🚀 Overview

Users interact with the system through a chat panel, and the AI automatically extracts structured information such as HCP name, topics discussed, sentiment, materials shared, samples distributed, outcomes, and follow-up actions. The extracted data is instantly used to auto-fill a CRM form. Users can also modify specific fields using conversational inputs like “actually I met Dr. John” or “samples were 6 units,” and the system updates only those fields while preserving existing data.

🎯 Key Features
Natural language interaction logging
Automatic form population using AI
Conversational editing of specific fields
Multi-step updates without manual input
Context-aware AI responses
LangGraph-based multi-tool architecture
Clean CRM-style UI with form and chat layout
🏗️ Tech Stack

Frontend: React with Redux
Backend: FastAPI (Python)
AI Agent Framework: LangGraph with LangChain tools
LLM: Groq (Gemma / LLaMA models)
Database: PostgreSQL
Styling: CSS

🧠 LangGraph Agent Architecture

The system uses a LangGraph workflow to orchestrate different tools. The flow is:

User input → Tool routing → Tool execution → Response → UI update

A hybrid approach is used:

Rule-based routing ensures reliability for create and edit actions
LLM-powered tools handle extraction, summarization, and reasoning
🛠️ LangGraph Tools

The system implements the required five tools:

Log Interaction Tool
Extracts structured data from natural language and populates the CRM form.
Edit Interaction Tool
Updates only the fields mentioned by the user without affecting other data.
Summarize Tool
Generates a summary using stored interaction data from the database.
Extract Entities Tool
Extracts key entities such as doctor name and topics from the latest interaction.
Follow-up Suggestion Tool
Suggests next steps based on the interaction.
⚙️ Setup Instructions

Clone the repository and navigate into the project folder.

Backend setup:
Navigate to the backend folder, create a virtual environment using uv, install dependencies, and start the FastAPI server.

Frontend setup:
Navigate to the frontend folder, install dependencies using npm, and start the React development server.

Backend runs on: http://127.0.0.1:8000

Frontend runs on: http://localhost:3000

🔐 Environment Variables

Create a .env file inside the backend folder and add:

GROQ_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/ai_crm

🧪 Example Usage

User input:
Today I met Dr. Smith, discussed product X efficacy, shared brochure, distributed 3 samples, positive sentiment

Result:
The system extracts structured data and auto-fills the form.

User input:
Actually I met Dr. John

Result:
Only the HCP name is updated.

User input:
Samples were 6 units

Result:
Only the samples field is updated.

User input:
summarize this interaction

Result:
The system generates a contextual summary based on stored interaction data.

📂 Project Structure

ai-crm/
│
├── frontend/
│ ├── src/
│ │ ├── features/
│ │ ├── components/
│ │ ├── pages/
│ │ └── services/
│
├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── agents/
│ │ ├── models/
│ │ ├── services/
│ │ └── db/
│
└── README.md

🎥 Demo Highlights
Chat-based interaction logging
Automatic form filling
Conversational editing
LangGraph tool execution
Context-aware summarization and insights
🧠 Key Learnings

This project demonstrates how to build AI-first applications where natural language acts as the primary interface. It shows how to convert unstructured text into structured CRM data, orchestrate multiple tools using LangGraph, handle LLM inconsistencies, and maintain consistent application state across multiple interactions.

📌 Submission Coverage
React + Redux frontend
FastAPI backend
LangGraph agent workflow
Groq LLM integration
PostgreSQL database
Five LangGraph tools implemented
Chat and form dual interface
Context-aware AI system
👤 Author

Deep Gupta