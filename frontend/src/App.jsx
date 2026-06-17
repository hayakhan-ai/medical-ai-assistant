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
    console.log("Conversation ID:", conversationId);

    const { data } = await axios.post(
      "http://127.0.0.1:8000/chat",
      {
        message: userQuestion,
        conversation_id: conversationId,
      }
    );

    console.log(data);

    // Save conversation ID if backend created a new chat
    if (!conversationId && data.conversation_id) {
      setConversationId(data.conversation_id);
    }

    // Add new message pair
    setMessages((prev) => [
      ...prev,
      {
        question: userQuestion,
        answer: data.response,
      },
    ]);

    // Refresh sidebar
    await loadConversations();

  } catch (error) {
    console.error("Send message failed:", error);
  } finally {
    setLoading(false);
  }
};
  const newChat = async () => {
     try {
           const res = await axios.post(
           "http://127.0.0.1:8000/new-chat",
        );

          setConversationId(res.data.conversation_id);
          setMessages([]);

          await loadConversations();

        } catch (err) {
           console.error(err);
          }
  };
  const loadConversations = async () => {
         try {
               const res = await axios.get(
               "http://127.0.0.1:8000/chat-history"
               );

               setConversations(res.data);

            } catch (err) {
             console.error(err);
            }
   };
  const openConversation = async (chat) => {

     try {

          const res = await axios.get(
      `   http://127.0.0.1:8000/conversation/${chat.conversation_id}`
          );

          setConversationId(chat.conversation_id);

          const formatted = res.data.messages.map(msg => ({
          question: msg.question,
          answer: msg.answer,
          feedback: null
      }));

          setMessages(formatted);

      }
       catch(err){
       console.error(err);
      }
  };

  return (
    <div style={styles.page}>
      <div style={styles.sidebar}>
        <button
          style={styles.newChat}
          onClick={newChat}
        >
          + New Chat
        </button>

        {conversations.map((chat) => (
          <div
              key={chat.conversation_id}
              style={styles.history}
              onClick={() => openConversation(chat)}
            >
             {chat.title}
          </div>
))}
      </div>

      <div style={styles.chatArea}>
        <h1 style={styles.title}>
           ✦ MediTour AI ✦
        </h1>

        <div style={styles.chatBox}>
          {messages.map((chat, index) => (
            <div key={index}>
              <div style={styles.userBubble}>
                {chat.question}
              </div>

              <div style={styles.aiBubble}>
                <ReactMarkdown>
                  {chat.answer}
                </ReactMarkdown>
              </div>
            </div>
          ))}

          {loading && (
            <div style={styles.aiBubble}>
              Thinking...
            </div>
          )}
        </div>

        <div style={styles.inputArea}>
          <textarea
            rows="3"
            value={message}
            placeholder="Ask a medical question..."
            onChange={(e) =>
              setMessage(e.target.value)
            }
            style={styles.input}
          />

          <button
            style={styles.send}
            onClick={sendMessage}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    display: "flex",
    height: "100vh",
    background: "#0f172a",
    color: "white"
  },

  sidebar: {
    width: "260px",
    background: "#111827",
    padding: "20px",
    overflowY: "auto"
  },

  newChat: {
    width: "100%",
    padding: "15px",
    borderRadius: "10px",
    border: "none",
    background: "#14b8a6",
    color: "white",
    cursor: "pointer"
  },

  history: {
    marginTop: "15px",
    padding: "12px",
    background: "#1e293b",
    borderRadius: "10px"
  },

  chatArea: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    padding: "20px"
  },

  title: {
    color: "#fff",
    fontSize: "3.5rem",
    fontWeight: "800",
    letterSpacing: "2px",
    textAlign: "center",
    marginBottom: "10px",
    textShadow: "0 0 15px rgba(255,255,255,0.5)",
    fontFamily: "'Poppins', sans-serif"
  },

  chatBox: {
    flex: 1,
    overflowY: "auto"
  },

  userBubble: {
    background: "#2563eb",
    padding: "15px",
    borderRadius: "15px",
    margin: "15px 0",
    alignSelf: "flex-end"
  },

  aiBubble: {
    background: "#1e293b",
    padding: "20px",
    borderRadius: "15px",
    marginBottom: "20px"
  },

  feedbackRow: {
    display: "flex",
    gap: "10px",
    marginTop: "15px"
  },

  feedbackButton: {
    padding: "10px",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer"
  },

  success: {
    marginTop: "10px",
    color: "#4ade80"
  },

  inputArea: {
    display: "flex",
    gap: "10px"
  },

  input: {
    flex: 1,
    padding: "15px",
    borderRadius: "12px"
  },

  send: {
    width: "120px",
    border: "none",
    borderRadius: "12px",
    background: "#14b8a6",
    color: "white",
    cursor: "pointer"
  }
};