import {
  useEffect,
  useRef,
  useState,
  type KeyboardEvent,
} from "react";
import {
  ArrowUp,
  BriefcaseBusiness,
  ChevronLeft,
  CircleHelp,
  Compass,
  Heart,
  Menu,
  MessageCircle,
  Plus,
  Search,
  ShieldCheck,
  Sparkles,
  X,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import "./index.css";

type Mode =
  | "listen"
  | "understand"
  | "options"
  | "information"
  | "plan";

type Message = {
  id: number;
  sender: "user" | "assistant";
  text: string;
  resourcesUsed?: string[];
};

type Conversation = {
  id: string;
  title: string;
  date: "Today" | "Yesterday";
};

type ModeConfig = {
  id: Mode;
  title: string;
  description: string;
  icon: typeof Heart;
};

const modes: ModeConfig[] = [
  {
    id: "listen",
    title: "Just Listen",
    description: "A space to be heard.",
    icon: Heart,
  },
  {
    id: "understand",
    title: "Help Me Understand",
    description: "Make sense of what’s happening.",
    icon: CircleHelp,
  },
  {
    id: "options",
    title: "Explore My Options",
    description: "See the choices available.",
    icon: Compass,
  },
  {
    id: "information",
    title: "Find Information",
    description: "Get reliable information.",
    icon: Search,
  },
  {
    id: "plan",
    title: "Help Me Make a Plan",
    description: "Think through your next steps.",
    icon: BriefcaseBusiness,
  },
];

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const SESSION_STORAGE_KEY = "hervoice_anonymous_session";


/* =========================================================
   ANONYMOUS SESSION
   ========================================================= */

function getAnonymousSessionId(): string {
  const existing = localStorage.getItem(
    SESSION_STORAGE_KEY,
  );

  if (existing) {
    return existing;
  }

  const newId =
    typeof crypto !== "undefined" &&
    "randomUUID" in crypto
      ? crypto.randomUUID()
      : `${Date.now()}-${Math.random()
          .toString(36)
          .slice(2)}`;

  localStorage.setItem(
    SESSION_STORAGE_KEY,
    newId,
  );

  return newId;
}


/* =========================================================
   APP
   ========================================================= */

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const [language, setLanguage] =
    useState<"EN" | "UR">("EN");

  const [selectedMode, setSelectedMode] =
    useState<Mode>("listen");

  const [message, setMessage] =
    useState("");

  const [started, setStarted] =
    useState(false);

  const [loading, setLoading] =
    useState(false);

  const [messages, setMessages] =
    useState<Message[]>([]);

  const [conversations, setConversations] =
    useState<Conversation[]>([]);

  const [activeConversation, setActiveConversation] =
    useState<string | null>(null);

  const [sessionId, setSessionId] =
    useState<string | null>(null);

  const messagesContainerRef =
    useRef<HTMLDivElement | null>(null);

  const shouldAutoScrollRef =
    useRef(true);

  const selectedModeData = modes.find(
    (mode) => mode.id === selectedMode,
  );


  /* =======================================================
     RESTORE ANONYMOUS SESSION
     ======================================================= */

  useEffect(() => {
    const id = getAnonymousSessionId();

    setSessionId(id);
    setActiveConversation(id);

    const restoreConversation = async () => {
      try {
        const response = await fetch(
          `${API_URL}/api/sessions/${id}`,
        );

        if (!response.ok) {
          return;
        }

        const data = await response.json();

        if (
          Array.isArray(data.messages) &&
          data.messages.length > 0
        ) {
          const restoredMessages: Message[] =
            data.messages.map(
              (
                item: {
                  role: "user" | "assistant";
                  content: string;
                },
                index: number,
              ) => ({
                id: index + 1,
                sender:
                  item.role === "user"
                    ? "user"
                    : "assistant",
                text: item.content,
              }),
            );

          setMessages(restoredMessages);
          setStarted(true);

          const firstUserMessage =
            restoredMessages.find(
              (item) =>
                item.sender === "user",
            );

          if (firstUserMessage) {
            setConversations([
              {
                id,
                title:
                  firstUserMessage.text.length > 32
                    ? `${firstUserMessage.text.substring(
                        0,
                        32,
                      )}...`
                    : firstUserMessage.text,
                date: "Today",
              },
            ]);
          }
        }
      } catch (error) {
        console.warn(
          "Could not restore previous conversation.",
          error,
        );
      }
    };

    restoreConversation();
  }, []);


  /* =======================================================
     AUTO SCROLL
     ======================================================= */

  const scrollToLatest = (
    behavior: ScrollBehavior = "smooth",
    force = false,
  ) => {
    const container =
      messagesContainerRef.current;

    if (!container) {
      return;
    }

    if (
      !force &&
      !shouldAutoScrollRef.current
    ) {
      return;
    }

    container.scrollTo({
      top: container.scrollHeight,
      behavior,
    });
  };


  const handleMessagesScroll = () => {
    const container =
      messagesContainerRef.current;

    if (!container) {
      return;
    }

    const distanceFromBottom =
      container.scrollHeight -
      container.scrollTop -
      container.clientHeight;

    shouldAutoScrollRef.current =
      distanceFromBottom < 120;
  };


  useEffect(() => {
    if (!started) {
      return;
    }

    const frame =
      requestAnimationFrame(() => {
        scrollToLatest("smooth");
      });

    return () =>
      cancelAnimationFrame(frame);
  }, [messages, started]);


  useEffect(() => {
    if (!loading) {
      return;
    }

    const frame =
      requestAnimationFrame(() => {
        scrollToLatest("smooth");
      });

    return () =>
      cancelAnimationFrame(frame);
  }, [loading]);


  /* =======================================================
     NEW CHAT
     ======================================================= */

  const handleNewChat = () => {
    if (loading) {
      return;
    }

    setStarted(false);
    setMessages([]);
    setSelectedMode("listen");
    setMessage("");

    /*
     * Generate a fresh anonymous conversation ID.
     * The previous conversation remains in SQLite.
     */
    const newConversationId =
      crypto.randomUUID();

    setActiveConversation(
      newConversationId,
    );

    setSessionId(
      newConversationId,
    );

    localStorage.setItem(
      SESSION_STORAGE_KEY,
      newConversationId,
    );

    shouldAutoScrollRef.current = true;
  };


  /* =======================================================
     SEND MESSAGE
     ======================================================= */

  const handleSend = async () => {
    const trimmed =
      message.trim();

    if (!trimmed || loading) {
      return;
    }

    shouldAutoScrollRef.current =
      true;

    setStarted(true);
    setLoading(true);

    const conversationId =
      sessionId ||
      getAnonymousSessionId();

    if (!sessionId) {
      setSessionId(
        conversationId,
      );
    }

    setActiveConversation(
      conversationId,
    );

    const userMessage: Message = {
      id: Date.now(),
      sender: "user",
      text: trimmed,
    };

    setMessages((current) => [
      ...current,
      userMessage,
    ]);

    setMessage("");


    /* =====================================================
       ADD REAL CONVERSATION TO SIDEBAR
       ===================================================== */

    setConversations((current) => {
      const exists = current.some(
        (conversation) =>
          conversation.id ===
          conversationId,
      );

      if (exists) {
        return current;
      }

      return [
        {
          id: conversationId,
          title:
            trimmed.length > 32
              ? `${trimmed.substring(
                  0,
                  32,
                )}...`
              : trimmed,
          date: "Today",
        },
        ...current,
      ];
    });


    /* =====================================================
       API REQUEST
       ===================================================== */

    try {
      const response =
        await fetch(
          `${API_URL}/api/chat`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              session_id:
                conversationId,

              message:
                trimmed,

              mode:
                selectedMode,

              language:
                language === "UR"
                  ? "ur"
                  : "en",
            }),
          },
        );

      if (!response.ok) {
        throw new Error(
          `API request failed: ${response.status}`,
        );
      }

      const data =
        await response.json();

      const assistantMessage: Message = {
        id: Date.now() + 1,

        sender: "assistant",

        text:
          data.reply ||
          "I'm sorry, I wasn't able to generate a response right now.",

        resourcesUsed:
          Array.isArray(
            data.resources_used,
          )
            ? data.resources_used
            : [],
      };

      setMessages((current) => [
        ...current,
        assistantMessage,
      ]);

      shouldAutoScrollRef.current =
        true;

      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          scrollToLatest(
            "smooth",
            true,
          );
        });
      });
    } catch (error) {
      console.error(
        "HerVoice API error:",
        error,
      );

      const assistantMessage: Message = {
        id: Date.now() + 1,

        sender: "assistant",

        text:
          language === "UR"
            ? "اس وقت کنکشن میں مسئلہ آ رہا ہے۔ براہِ کرم تھوڑی دیر بعد دوبارہ کوشش کریں۔"
            : "I'm having trouble connecting right now. Please try again in a moment.",
      };

      setMessages((current) => [
        ...current,
        assistantMessage,
      ]);

      shouldAutoScrollRef.current =
        true;
    } finally {
      setLoading(false);
    }
  };


  /* =======================================================
     KEYBOARD
     ======================================================= */

  const handleKeyDown = (
    event: KeyboardEvent<HTMLTextAreaElement>,
  ) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      handleSend();
    }
  };


  /* =======================================================
     QUICK EXIT
     ======================================================= */

  const quickExit = () => {
    window.location.replace(
      "https://www.google.com",
    );
  };


  /* =======================================================
     UI
     ======================================================= */

  return (
    <div
      className={`app ${
        language === "UR"
          ? "rtl"
          : ""
      }`}
      lang={
        language === "UR"
          ? "ur"
          : "en"
      }
    >

      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />


      {/* ===================================================
          SIDEBAR
          =================================================== */}

      <AnimatePresence>
        {sidebarOpen && (
          <motion.aside
            initial={{
              x: -320,
              opacity: 0,
            }}
            animate={{
              x: 0,
              opacity: 1,
            }}
            exit={{
              x: -320,
              opacity: 0,
            }}
            transition={{
              duration: 0.28,
            }}
            className="sidebar"
            aria-label="Conversation sidebar"
          >

            <div className="sidebar-top">

              <div className="mini-brand">

                <div
                  className="mini-flower"
                  aria-hidden="true"
                >
                  ✿
                </div>

                <div>
                  <div className="mini-brand-name">
                    HerVoice
                  </div>

                  <div className="mini-brand-subtitle">
                    Your space to be heard.
                  </div>
                </div>

              </div>

              <button
                className="icon-button mobile-close"
                onClick={() =>
                  setSidebarOpen(false)
                }
                aria-label="Close sidebar"
                type="button"
              >
                <X size={18} />
              </button>

            </div>


            <button
              className="new-chat-button"
              onClick={
                handleNewChat
              }
              disabled={loading}
              type="button"
            >
              <Plus size={17} />
              <span>
                New chat
              </span>
            </button>


            <div className="conversation-area">

              <div className="conversation-heading">
                Conversations
              </div>

              <div className="conversation-list">

                {conversations.length === 0 ? (
                  <div className="empty-conversations">
                    Your conversations will
                    appear here.
                  </div>
                ) : (
                  conversations.map(
                    (
                      conversation,
                    ) => (
                      <button
                        key={
                          conversation.id
                        }
                        className={`conversation-item ${
                          activeConversation ===
                          conversation.id
                            ? "conversation-active"
                            : ""
                        }`}
                        onClick={() => {
                          if (loading) {
                            return;
                          }

                          setActiveConversation(
                            conversation.id,
                          );

                          if (
                            conversation.id ===
                            sessionId
                          ) {
                            setStarted(
                              messages.length >
                                0,
                            );
                          }
                        }}
                        type="button"
                        aria-current={
                          activeConversation ===
                          conversation.id
                            ? "page"
                            : undefined
                        }
                      >
                        <MessageCircle
                          size={15}
                          aria-hidden="true"
                        />

                        <span>
                          {
                            conversation.title
                          }
                        </span>
                      </button>
                    ),
                  )
                )}

              </div>
            </div>


            <div className="sidebar-bottom">

              <div className="privacy-mini">

                <div className="privacy-icon">
                  <ShieldCheck
                    size={16}
                    aria-hidden="true"
                  />
                </div>

                <div>
                  <strong>
                    Privacy first
                  </strong>

                  <span>
                    No name or personal
                    information is required
                    to start a chat.
                  </span>
                </div>

              </div>

            </div>

          </motion.aside>
        )}
      </AnimatePresence>


      {/* ===================================================
          MAIN
          =================================================== */}

      <main className="main">

        <header className="topbar">

          <div className="topbar-left">

            {!sidebarOpen && (
              <button
                className="icon-button"
                onClick={() =>
                  setSidebarOpen(true)
                }
                aria-label="Open sidebar"
                type="button"
              >
                <Menu size={19} />
              </button>
            )}

            <div className="mobile-brand">
              <span aria-hidden="true">
                ✿
              </span>
              HerVoice
            </div>

          </div>


          <div className="topbar-actions">

            <div
              className="language-switch"
              aria-label="Language selection"
            >

              <button
                className={
                  language === "EN"
                    ? "language-active"
                    : ""
                }
                onClick={() =>
                  setLanguage("EN")
                }
                type="button"
                aria-pressed={
                  language === "EN"
                }
              >
                EN
              </button>

              <span aria-hidden="true">
                /
              </span>

              <button
                className={
                  language === "UR"
                    ? "language-active"
                    : ""
                }
                onClick={() =>
                  setLanguage("UR")
                }
                type="button"
                aria-pressed={
                  language === "UR"
                }
              >
                اردو
              </button>

            </div>


            <button
              className="quick-exit"
              onClick={quickExit}
              title="Leave HerVoice quickly"
              aria-label="Quick exit HerVoice"
              type="button"
            >
              <span
                className="exit-dot"
                aria-hidden="true"
              />
              Quick exit
            </button>

          </div>

        </header>


        {/* =================================================
            CHAT SHELL
            ================================================= */}

        <section
          className={`chat-shell ${
            started
              ? "chat-started"
              : ""
          }`}
        >

          {!started ? (

            /* =================================================
               WELCOME
               ================================================= */

            <motion.div
              initial={{
                opacity: 0,
                y: 12,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              transition={{
                duration: 0.45,
              }}
              className="welcome"
            >

              <div
                className="hero-symbol"
                aria-hidden="true"
              >

                <div className="hero-ring ring-one" />
                <div className="hero-ring ring-two" />

                <motion.div
                  animate={{
                    y: [0, -5, 0],
                    rotate: [
                      0,
                      1.5,
                      -1.5,
                      0,
                    ],
                  }}
                  transition={{
                    duration: 5,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  className="hero-flower"
                >
                  ✿
                </motion.div>

              </div>


              <div className="eyebrow">
                <Sparkles size={13} />
                A private space for you
              </div>


              <h1>
                You don't have to
                <br />
                <span>
                  carry everything alone.
                </span>
              </h1>


              <p className="welcome-text">
                Whatever is on your mind,
                start wherever feels easiest.
                You don't need the perfect
                words.
              </p>


              <div className="mode-label">
                How would you like to begin?
              </div>


              <div
                className="mode-grid"
                role="group"
                aria-label="Conversation modes"
              >

                {modes.map(
                  (mode, index) => {
                    const Icon =
                      mode.icon;

                    return (
                      <motion.button
                        key={mode.id}
                        initial={{
                          opacity: 0,
                          y: 8,
                        }}
                        animate={{
                          opacity: 1,
                          y: 0,
                        }}
                        transition={{
                          duration: 0.3,
                          delay:
                            0.05 * index,
                        }}
                        whileHover={{
                          y: -2,
                        }}
                        whileTap={{
                          scale: 0.985,
                        }}
                        className={`mode-card ${
                          selectedMode ===
                          mode.id
                            ? "mode-selected"
                            : ""
                        }`}
                        onClick={() =>
                          setSelectedMode(
                            mode.id,
                          )
                        }
                        type="button"
                        aria-pressed={
                          selectedMode ===
                          mode.id
                        }
                      >

                        <div className="mode-card-top">

                          <div className="mode-icon">
                            <Icon
                              size={16}
                              strokeWidth={1.8}
                              aria-hidden="true"
                            />
                          </div>

                          {selectedMode ===
                            mode.id && (
                            <span className="selected-mark">
                              Selected
                            </span>
                          )}

                        </div>


                        <div className="mode-content">

                          <strong>
                            {mode.title}
                          </strong>

                          <span>
                            {
                              mode.description
                            }
                          </span>

                        </div>

                      </motion.button>
                    );
                  },
                )}

              </div>


              {/* =================================================
                 LANDING COMPOSER
                 ================================================= */}

              <div className="composer-wrap">

                <div className="composer-label">
                  <span>
                    {selectedModeData?.title ||
                      "Just Listen"}
                  </span>
                </div>


                <div className="composer">

                  <textarea
                    value={message}
                    onChange={(event) =>
                      setMessage(
                        event.target.value,
                      )
                    }
                    onKeyDown={
                      handleKeyDown
                    }
                    placeholder={
                      language ===
                      "UR"
                        ? "جو دل میں ہے، یہاں لکھیں..."
                        : "Write what's on your mind..."
                    }
                    rows={1}
                    disabled={loading}
                    aria-label="Message HerVoice"
                  />


                  <motion.button
                    whileHover={{
                      scale: 1.04,
                    }}
                    whileTap={{
                      scale: 0.96,
                    }}
                    className="send-button"
                    onClick={
                      handleSend
                    }
                    disabled={
                      !message.trim() ||
                      loading
                    }
                    aria-label="Send message"
                    type="button"
                  >
                    <ArrowUp
                      size={19}
                      strokeWidth={2}
                    />
                  </motion.button>

                </div>


                <div className="composer-meta">

                  <span>
                    Private by design ·
                    No name or email required
                  </span>

                  <span className="composer-keyboard">
                    Enter to send · Shift +
                    Enter for a new line
                  </span>

                </div>

              </div>

            </motion.div>

          ) : (

            /* =================================================
               ACTIVE CONVERSATION
               ================================================= */

            <div className="conversation-screen">

              <div className="conversation-header">

                <button
                  className="back-button"
                  onClick={
                    handleNewChat
                  }
                  disabled={loading}
                  type="button"
                >
                  <ChevronLeft
                    size={17}
                  />
                  New conversation
                </button>


                <div className="active-mode">

                  <span className="active-mode-dot" />

                  {
                    selectedModeData?.title
                  }

                </div>

              </div>


              {/* =================================================
                 MESSAGES
                 ================================================= */}

              <div
                ref={
                  messagesContainerRef
                }
                className="messages"
                onScroll={
                  handleMessagesScroll
                }
                aria-live="polite"
              >

                <div className="messages-inner">

                  {messages.map(
                    (item) => (
                      <motion.div
                        key={item.id}
                        initial={{
                          opacity: 0,
                          y: 8,
                        }}
                        animate={{
                          opacity: 1,
                          y: 0,
                        }}
                        transition={{
                          duration: 0.25,
                        }}
                        className={`message-row ${
                          item.sender ===
                          "user"
                            ? "message-user"
                            : "message-assistant"
                        }`}
                      >

                        {item.sender ===
                          "assistant" && (
                          <div
                            className="assistant-avatar"
                            aria-hidden="true"
                          >
                            ✿
                          </div>
                        )}


                        <div className="message-content">

                          <div className="message-bubble">
                            {item.text}
                          </div>


                          {item.sender ===
                            "assistant" &&
                            item.resourcesUsed &&
                            item.resourcesUsed
                              .length > 0 && (
                              <div className="source-indicator">

                                <ShieldCheck
                                  size={12}
                                  aria-hidden="true"
                                />

                                <span>
                                  Verified source used
                                </span>

                              </div>
                            )}

                        </div>

                      </motion.div>
                    ),
                  )}


                  {/* =================================================
                     TYPING INDICATOR
                     ================================================= */}

                  {loading && (
                    <motion.div
                      initial={{
                        opacity: 0,
                        y: 8,
                      }}
                      animate={{
                        opacity: 1,
                        y: 0,
                      }}
                      className="message-row message-assistant"
                    >

                      <div
                        className="assistant-avatar"
                        aria-hidden="true"
                      >
                        ✿
                      </div>


                      <div className="message-bubble typing-bubble">

                        <span
                          className="typing-dots"
                          aria-label="HerVoice is responding"
                        >
                          <span />
                          <span />
                          <span />
                        </span>

                      </div>

                    </motion.div>
                  )}

                </div>

              </div>


              {/* =================================================
                 ACTIVE COMPOSER
                 ================================================= */}

              <div className="chat-composer-area">

                <div className="composer">

                  <textarea
                    value={message}
                    onChange={(event) =>
                      setMessage(
                        event.target.value,
                      )
                    }
                    onKeyDown={
                      handleKeyDown
                    }
                    placeholder={
                      language ===
                      "UR"
                        ? "جو دل میں ہے، یہاں لکھیں..."
                        : "Continue the conversation..."
                    }
                    rows={1}
                    disabled={loading}
                    aria-label="Continue conversation"
                  />


                  <button
                    className="send-button"
                    onClick={
                      handleSend
                    }
                    disabled={
                      !message.trim() ||
                      loading
                    }
                    aria-label="Send message"
                    type="button"
                  >
                    <ArrowUp
                      size={19}
                    />
                  </button>

                </div>


                <div className="composer-meta chat-composer-meta">

                  <span>
                    Private by design ·
                    No name or email required
                  </span>

                  <span className="composer-keyboard">
                    HerVoice provides
                    supportive information,
                    not professional medical,
                    legal, or emergency
                    services.
                  </span>

                </div>

              </div>

            </div>
          )}

        </section>


        {/* ===================================================
            FOOTER
            =================================================== */}

        <footer className="footer">

          <span>
            HerVoice AI
          </span>

          <span>
            •
          </span>

          <span>
            You are heard. You are valued.
            You are in control.
          </span>

        </footer>

      </main>
    </div>
  );
}

export default App;