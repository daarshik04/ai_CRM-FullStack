import "./App.css";
import InteractionForm from "./components/InteractionForm";
import ChatPanel from "./components/ChatPanel";

function App() {
  return (
    <div className="container">
      <div className="left-panel">
        <InteractionForm />
      </div>

      <div className="right-panel">
        <ChatPanel />
      </div>
    </div>
  );
}

export default App;