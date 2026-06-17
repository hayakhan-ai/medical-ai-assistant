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
          MediTour Global
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
          <h2>Medical AI Assistant</h2>
          <p>Get preliminary medical guidance and specialist suggestions</p>
        </div>

        <div style={styles.chatCard}>
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
            <div style={styles.aiMsg}>Analyzing symptoms...</div>
          )}
        </div>

        {/* INPUT */}
        <div style={styles.inputBar}>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Describe your symptoms or ask a medical question..."
            style={styles.input}
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
    background: "#f5f7fb",
    fontFamily: "Inter, sans-serif",
  },

  /* SIDEBAR */
  sidebar: {
    width: "280px",
    background: "#ffffff",
    borderRight: "1px solid #e5e7eb",
    padding: "20px",
  },

  brand: {
    fontSize: "20px",
    fontWeight: "700",
    color: "#2563eb",
    marginBottom: "20px",
  },

  newChatBtn: {
    width: "100%",
    padding: "12px",
    background: "#2563eb",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    marginBottom: "20px",
  },

  sectionTitle: {
    fontSize: "12px",
    color: "#6b7280",
    marginBottom: "10px",
  },

  chatItem: {
    padding: "10px",
    borderRadius: "8px",
    cursor: "pointer",
    background: "#f3f4f6",
    marginBottom: "8px",
  },

  /* MAIN */
  main: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    padding: "20px",
  },

  header: {
    marginBottom: "20px",
  },

  chatCard: {
    flex: 1,
    overflowY: "auto",
    background: "#ffffff",
    borderRadius: "12px",
    padding: "20px",
    border: "1px solid #e5e7eb",
  },

  messageBlock: {
    marginBottom: "20px",
  },

  userMsg: {
    background: "#2563eb",
    color: "white",
    padding: "12px",
    borderRadius: "10px",
    marginBottom: "10px",
    maxWidth: "70%",
    marginLeft: "auto",
  },

  aiMsg: {
    background: "#f3f4f6",
    padding: "15px",
    borderRadius: "10px",
    maxWidth: "85%",
  },

  inputBar: {
    display: "flex",
    gap: "10px",
    marginTop: "15px",
  },

  input: {
    flex: 1,
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #d1d5db",
  },

  sendBtn: {
    width: "120px",
    background: "#10b981",
    color: "white",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
  },
};