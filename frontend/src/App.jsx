import React, { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

export default function App() {

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {

    if (!message.trim()) return;

    setLoading(true);

    try {

      const res = await axios.post(
        "https://saul-monic-damon.ngrok-free.dev/chat",
        {
          message
        }
      );

      setResponse(res.data.response);

    } catch (error) {

      setResponse("Error connecting to AI backend.");

    }

    setLoading(false);
  };

  return (

    <div style={styles.page}>

      <div style={styles.card}>

        <h1 style={styles.title}>
          🩺 Medical AI Assistant
        </h1>

        <p style={styles.subtitle}>
          How can I help you today?
        </p>

        <textarea
          rows="6"
          placeholder="Example: I have skin allergy and itching..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={styles.textarea}
        />

        <button
          onClick={sendMessage}
          style={styles.button}
        >
          {loading ? "Analyzing..." : "Ask AI"}
        </button>
         
        {response && (

          <div style={styles.responseBox}>

            <h2 style={styles.responseTitle}>
              AI Response
            </h2>

            <div style={styles.responseText}>
              <ReactMarkdown>
              {response}
              </ReactMarkdown>
            </div>

          </div>
        )}

      </div>

    </div>
  );
}

const styles = {

  page: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background:
      "linear-gradient(135deg, #0f172a, #1e3a8a, #14b8a6)",
    fontFamily: "Arial",
    padding: "20px"
  },

  card: {
    width: "100%",
    maxWidth: "700px",
    background: "rgba(255,255,255,0.1)",
    backdropFilter: "blur(12px)",
    borderRadius: "20px",
    padding: "40px",
    boxShadow: "0 8px 32px rgba(0,0,0,0.3)",
    border: "1px solid rgba(255,255,255,0.2)"
  },

  title: {
    color: "white",
    textAlign: "center",
    fontSize: "38px",
    marginBottom: "10px"
  },

  subtitle: {
    color: "#dbeafe",
    textAlign: "center",
    marginBottom: "30px",
    fontSize: "18px"
  },

  textarea: {
    width: "100%",
    padding: "18px",
    borderRadius: "14px",
    border: "none",
    outline: "none",
    fontSize: "16px",
    resize: "none",
    background: "rgba(255,255,255,0.15)",
    color: "white",
    marginBottom: "20px"
  },

  button: {
    width: "100%",
    padding: "16px",
    borderRadius: "14px",
    border: "none",
    background:
      "linear-gradient(90deg, #14b8a6, #3b82f6)",
    color: "white",
    fontSize: "18px",
    fontWeight: "bold",
    cursor: "pointer",
    transition: "0.3s"
  },

  responseBox: {
    marginTop: "30px",
    background: "rgba(255,255,255,0.12)",
    borderRadius: "16px",
    padding: "25px",
    color: "white",
    border: "1px solid rgba(255,255,255,0.15)"
  },

  responseTitle: {
    marginBottom: "15px",
    color: "#a7f3d0"
  },

  responseText: {
    lineHeight: "1.8",
    color: "#f1f5f9"
  }
};
