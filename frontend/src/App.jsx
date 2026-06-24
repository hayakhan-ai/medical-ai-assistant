import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

export default function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [recording, setRecording] = useState(false);

  const messagesEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
    
    useEffect(() => {
       loadConversations();
     }, [])

    useEffect(() => {
       messagesEndRef.current?.scrollIntoView({
       behavior: "smooth"
      });
    }, [messages]);

  const sendMessage = async () => {
  if (!message.trim() || loading) return;

  const userQuestion = message;

  setMessage("");
  setLoading(true);

  // show user message immediately
  setMessages((prev) => [
    ...prev,
    {
      question: userQuestion,
      answer: ""
    }
  ]);

  try {

    const { data } = await axios.post(
      "http://127.0.0.1:8000/chat",
      {
        message: userQuestion,
        conversation_id: conversationId
      }
    );

    if (!conversationId && data.conversation_id) {
      setConversationId(data.conversation_id);
    }

    // insert response into last message
    setMessages((prev) => {
      const updated = [...prev];

      updated[updated.length - 1] = {
        ...updated[updated.length - 1],
        answer: data.response
      };

      return updated;
    });

    await loadConversations();

  } catch (error) {

    console.error(error);

    setMessages((prev) => {
      const updated = [...prev];

      updated[updated.length - 1] = {
        ...updated[updated.length - 1],
        answer: "Something went wrong. Please try again."
      };

      return updated;
    });

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

  const toggleRecording = async () => {

  if (loading) return;  

  if (!recording) {

    const stream = await navigator.mediaDevices.getUserMedia({
      audio: true
    });

    const recorder = new MediaRecorder(stream);

    chunksRef.current = [];

    recorder.ondataavailable = (e) => {
      chunksRef.current.push(e.data);
    };

    recorder.onstop = async () => {

      const blob = new Blob(chunksRef.current, {
        type: "audio/webm"
      });

      const formData = new FormData();

      formData.append(
        "file",
        blob,
        "voice.webm"
      );

      formData.append(
        "conversation_id",
        conversationId || ""
      );

      setLoading(true);

      try {

        const { data } = await axios.post(
          "http://127.0.0.1:8000/voice-chat",
          formData
        );

        if (!conversationId) {
          setConversationId(data.conversation_id);
        }

        setMessages(prev => [
          ...prev,
          {
            question: data.query,
            answer: data.response
          }
        ]);

        const audio = new Audio(
          `http://127.0.0.1:8000/${data.audio}`
        );

        audio.play().catch(err => {console.log("Autoplay blocked", err);});

        await loadConversations();

      }
      catch (err) {

        console.error(err);

        setMessages(prev => [
           ...prev,
          {
              question: "Voice message",
              answer: "Voice service unavailable."
          }
        ]);

      }
      finally {

        setLoading(false);

      }

    };   // ← onstop ends here

    recorder.start();

    mediaRecorderRef.current = recorder;

    setRecording(true);

  }

  else {

    mediaRecorderRef.current.stop();

    mediaRecorderRef.current.stream
    .getTracks()
    .forEach(track => track.stop());


    setRecording(false);

  }

};

  return (
    <div style={styles.app}>
      {/* SIDEBAR */}
      <div style={styles.sidebar}>
        <div style={styles.brand}>
          <img
              src="/image.png"
              alt="MediTour Global"
              style={styles.logo}
            />

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
                 onMouseEnter={(e) => {
                 e.currentTarget.style.background = "rgba(255,255,255,.25)";
                 e.currentTarget.style.transform = "translateX(4px)";
               }}
                 onMouseLeave={(e) => {
                 e.currentTarget.style.background = "rgba(255,255,255,.15)";
                 e.currentTarget.style.transform = "translateX(0px)";
               }}>
                  {chat.title}
             </div>
           ))}
      </div>

      {/* MAIN */}
      <div style={styles.main}>
        <div style={styles.header}>
          <h2>MediTour AI Assistant</h2>
          <p style={{ color: "#64748B" }}>
             Personalized medical guidance and treatment information
          </p>
        </div>

        <div style={styles.chatCard}>
          {messages.length === 0 && (
  <div
    style={{
      textAlign: "center",
      marginTop: "80px",
      maxWidth: "800px",
      marginLeft: "auto",
      marginRight: "auto",
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
            <div style={styles.aiMsg}>Processing....</div>
          )}
          <div ref={messagesEndRef}></div>
        </div>

        {/* INPUT */}
        <div style={styles.inputBar}>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Your query...."
            style={styles.input}
            onKeyDown={(e) => {
               if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage();
                }
            }}
          />

          <button onClick={sendMessage} style={styles.sendBtn} disabled={loading}>
            Send
          </button>
          <button onClick={toggleRecording} style={styles.voiceBtn} disabled={loading}>
            {recording ? "🔴" : "🎤"}
          </button>
        </div>
           <div
              style={{
                  textAlign: "center",
                  padding: "8px",
                  color: "#64748B",
                  fontSize: "12px",
                 }}
              >
              Powered by MediTour Global
           </div>
        </div>
    </div>
  );
}

const styles = {
  app: {
    display: "flex",
    height: "100vh",
    background: "#F4F8F8",
    fontFamily: "Nunito, sans-serif",
  },

  /* SIDEBAR */
  sidebar: {
    width: "250px",
    height: "100vh",
    overflowY: "auto",
    background: "#234C97",
    color: "white",
    padding: "24px",
    display: "flex",
    flexDirection: "column",
    boxShadow: "2px 0 10px rgba(0,0,0,.08)"
  },

  brand: {
    fontSize: "28px",
    fontWeight: "800",
    color: "#FFFFFF",
    marginBottom: "30px",
  },

  newChatBtn: {
    background: "#F47B2A",
    color: "white",
    border: "none",
    borderRadius: "18px",
    padding: "14px",
    cursor: "pointer",
    fontSize: "15px",
    fontWeight: "700",
    marginBottom: "25px",
  },

  sectionTitle: {
    color: "#D6E2FF",
    fontSize: "13px",
    marginBottom: "10px",
  },

  chatItem: {
    background: "rgba(255,255,255,.15)",
    padding: "14px",
    borderRadius: "14px",
    marginBottom: "10px",
    cursor: "pointer",
    wordBreak: "break-word",
    transition: "0.2s",
  },

  /* MAIN */
  main: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
  },

  header: {
    background: "white",
    borderBottom: "3px solid #F47B2A",
    padding: "20px 40px",
  },

  chatCard: {
    flex: 1,
    overflowY: "auto",
    padding: "40px",
    display: "flex",
    flexDirection: "column",
    gap: "20px",
    background: "#F8FAFC",
  },

  messageBlock: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },

  userMsg: {
    alignSelf: "flex-end",
    background: "linear-gradient(135deg,#2596D9,#234C97)",
    color: "white",
    padding: "16px 20px",
    borderRadius: "22px",
    maxWidth: "70%",
    lineHeight: "1.7",
    boxShadow: "0 4px 12px rgba(0,0,0,.1)"
  },

  aiMsg: {
    background: "white",
    borderLeft: "5px solid #F47B2A",
    padding: "18px",
    borderRadius: "20px",
    maxWidth: "80%",
    lineHeight: "1.8",
    boxShadow: "0 4px 15px rgba(0,0,0,.06)"
  },

  /* INPUT */
  inputBar: {
    padding: "20px 40px",
    background: "white",
    borderTop: "1px solid #E2E8F0",
    display: "flex",
    gap: "12px",
    boxShadow: "0 -2px 10px rgba(0,0,0,.04)",
  },

  input: {
    flex: 1,
    border: "1px solid #D6DCE5",
    borderRadius: "25px",
    padding: "16px",
    resize: "none",
    fontSize: "15px",
    outline: "none",
    minHeight: "60px",
  },

  sendBtn: {
    width: "120px",
    background: "#F47B2A",
    color: "white",
    border: "none",
    borderRadius: "20px",
    fontWeight: "700",
    cursor: "pointer",
  },

  voiceBtn: {
    width: "70px",
    background: "#234C97",
    color: "white",
    border: "none",
    borderRadius: "20px",
    cursor: "pointer",
    fontSize: "22px"
  },

  logo: {
    width: "85%",
    height: "auto",
    borderRadius: "16px",
    background: "white",
    padding: "10px",
    margin: "0 auto",
    display: "block",
    objectFit: "contain",
  },

  brand: {
    background: "white",
    borderRadius: "20px",
    padding: "12px",
    marginBottom: "30px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  }
};