import React, { useEffect, useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

export default function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);

  useEffect(() => {
    loadConversations();
    newChat();
  }, []);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userQuestion = message;
    setMessage("");
    setLoading(true);

    try {
      const { data } = await axios.post("http://127.0.0.1:8000/chat", {
        message: userQuestion,
        conversation_id: conversationId,
      });

      if (!conversationId && data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      setMessages((prev) => [
        ...prev,
        { question: userQuestion, answer: data.response },
      ]);

      await loadConversations();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const newChat = async () => {
    const res = await axios.post("http://127.0.0.1:8000/new-chat");
    setConversationId(res.data.conversation_id);
    setMessages([]);
    await loadConversations();
  };

  const loadConversations = async () => {
    const res = await axios.get("http://127.0.0.1:8000/chat-history");
    setConversations(res.data);
  };

  const openConversation = async (chat) => {
    const res = await axios.get(
      `http://127.0.0.1:8000/conversation/${chat.conversation_id}`
    );

    setConversationId(chat.conversation_id);

    const formatted = res.data.messages.map((msg) => ({
      question: msg.question,
      answer: msg.answer,
    }));

    setMessages(formatted);
  };

  return (
    <div style={styles.app}>
      {/* SIDEBAR */}
      <div style={styles.sidebar}>
        <div style={styles.brand}>
          🌎 MediTour Global
        </div>

        <button style={styles.newChatBtn} onClick={newChat}>
          + New Consultation
        </button>

        <div style={styles.sectionTitle}>Your Consultations</div>

        {conversations.map((chat) => (
          <div
            key={chat.conversation_id}
            style={styles.chatItem}
            onClick={() => openConversation(chat)}
          >
            {chat.title}
          </div>
        ))}
      </div>

      {/* MAIN */}
      <div style={styles.main}>
        <div style={styles.header}>
          <h2>Your AI Heath Companion</h2>
          <p style={{ color: "#64748B" }}>
             Receive personalized medical guidance
          </p>
        </div>

        <div style={styles.chatCard}>
          {messages.length === 0 && (
  <div
    style={{
      textAlign: "center",
      marginTop: "120px",
      color: "#64748B",
    }}
  >
    <h1 style={{ color: "#0F172A" }}>
      How can I help you today?
    </h1>

    <p>
      Describe your symptoms or ask about treatments,
      doctors, hospitals, and laboratory tests.
    </p>
  </div>
)}
          {messages.map((chat, i) => (
            <div key={i} style={styles.messageBlock}>
              <div style={styles.userMsg}>
                {chat.question}
              </div>

              <div style={styles.aiMsg}>
                <ReactMarkdown>{chat.answer}</ReactMarkdown>
              </div>
            </div>
          ))}

          {loading && (
            <div style={styles.aiMsg}>Analyzing....</div>
          )}
        </div>

        {/* INPUT */}
        <div style={styles.inputBar}>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Describe your symptoms or ask a medical question..."
            style={styles.input}
            onKeyDown={(e) => {
               if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage();
                }
            }}
          />

          <button onClick={sendMessage} style={styles.sendBtn}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  app: {
    display: "flex",
    height: "100vh",
    background: "#F8FAFC",
    fontFamily: "Inter, sans-serif",
  },

  /* SIDEBAR */
  sidebar: {
    width: "280px",
    background: "#0F172A",
    color: "white",
    padding: "24px",
    display: "flex",
    flexDirection: "column",
  },

  brand: {
    fontSize: "24px",
    fontWeight: "700",
    color: "#00A6A6",
    marginBottom: "30px",
  },

  newChatBtn: {
    background: "#00A6A6",
    color: "white",
    border: "none",
    borderRadius: "14px",
    padding: "14px",
    cursor: "pointer",
    fontSize: "15px",
    marginBottom: "25px",
  },

  sectionTitle: {
    color: "#94A3B8",
    fontSize: "13px",
    marginBottom: "10px",
  },

  chatItem: {
    background: "#1E293B",
    padding: "14px",
    borderRadius: "12px",
    marginBottom: "10px",
    cursor: "pointer",
    transition: ".2s",
  },

  /* MAIN */
  main: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
  },

  header: {
    background: "white",
    borderBottom: "1px solid #E2E8F0",
    padding: "20px 40px",
  },

  chatCard: {
    flex: 1,
    overflowY: "auto",
    padding: "40px",
    display: "flex",
    flexDirection: "column",
    gap: "20px",
  },

  messageBlock: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },

  userMsg: {
    alignSelf: "flex-end",
    background: "#00A6A6",
    color: "white",
    padding: "15px 18px",
    borderRadius: "20px",
    maxWidth: "70%",
    lineHeight: "1.6",
  },

  aiMsg: {
    background: "white",
    border: "1px solid #E2E8F0",
    padding: "18px",
    borderRadius: "20px",
    maxWidth: "80%",
    lineHeight: "1.8",
    boxShadow: "0 2px 8px rgba(0,0,0,.05)",
  },

  /* INPUT */
  inputBar: {
    padding: "20px 40px",
    background: "white",
    borderTop: "1px solid #E2E8F0",
    display: "flex",
    gap: "15px",
  },

  input: {
    flex: 1,
    border: "1px solid #CBD5E1",
    borderRadius: "18px",
    padding: "16px",
    resize: "none",
    fontSize: "15px",
    outline: "none",
    minHeight: "60px",
  },

  sendBtn: {
    width: "120px",
    background: "#00A6A6",
    color: "white",
    border: "none",
    borderRadius: "18px",
    fontWeight: "600",
    cursor: "pointer",
  },
};