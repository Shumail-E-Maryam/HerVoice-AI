import re


EMOTION_KEYWORDS = {
    "anxious": [
        "anxious",
        "anxiety",
        "panic",
        "panicking",
        "worried",
        "worry",
        "nervous",
        "stressed",
        "stress",
        "ghabrahat",
        "ghabra raha",
        "ghabra rahi",
        "pareshan",
        "پریشان",
        "گھبراہٹ",
    ],
    "sad": [
        "sad",
        "unhappy",
        "crying",
        "cry",
        "depressed",
        "depress",
        "hurt",
        "upset",
        "dukhi",
        "udaas",
        "اداس",
        "دکھی",
    ],
    "angry": [
        "angry",
        "anger",
        "mad",
        "furious",
        "annoyed",
        "irritated",
        "ghussa",
        "gussa",
        "غصہ",
    ],
    "overwhelmed": [
        "overwhelmed",
        "pressure",
        "pressurized",
        "too much",
        "can't handle",
        "cannot handle",
        "on my shoulders",
        "bohat pressure",
        "pressure hai",
        "بہت پریشر",
    ],
    "confused": [
        "confused",
        "confusing",
        "don't understand",
        "dont understand",
        "idk",
        "not sure",
        "samajh nahi",
        "سمجھ نہیں",
    ],
    "happy": [
        "happy",
        "excited",
        "great",
        "amazing",
        "good",
        "khush",
        "خوش",
    ],
}


INTENT_KEYWORDS = {
    "venting": [
        "need to vent",
        "want to vent",
        "just listen",
        "let me vent",
        "i need to talk",
        "need someone to listen",
        "bas baat karni",
        "dil halka",
    ],
    "advice": [
        "what should i do",
        "what do i do",
        "should i",
        "give me advice",
        "advice",
        "kya karun",
        "kya karoon",
        "mujhe kya karna chahiye",
    ],
    "information": [
        "what is",
        "what are",
        "how does",
        "why does",
        "tell me about",
        "explain",
        "information",
        "opportunity",
        "opportunities",
        "how can i",
    ],
    "planning": [
        "make a plan",
        "plan",
        "next steps",
        "steps",
        "roadmap",
        "how should i start",
        "kaise start",
        "agla step",
    ],
    "conversation": [
        "hello",
        "hi",
        "hey",
        "acha",
        "okay",
        "ok",
    ],
}


def _normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def classify_emotion(text: str) -> str:
    normalized = _normalize(text)

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized:
                return emotion

    return "neutral"


def classify_intent(text: str) -> str:
    normalized = _normalize(text)

    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized:
                return intent

    return "conversation"