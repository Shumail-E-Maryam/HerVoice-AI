import re


# These are intentionally broad safety signals.
# They are NOT intended to diagnose anything.
HIGH_RISK_PATTERNS = [
    # English
    r"\bkill myself\b",
    r"\bend my life\b",
    r"\btake my own life\b",
    r"\bsuicid(?:e|al)\b",
    r"\bhurt myself\b",

    # Common Roman Urdu expressions
    r"\bkhudkushi\b",
    r"\bkhud kushi\b",
    r"\bapni jaan\b",
    r"\bjaan de doon\b",
    r"\bkhud ko nuqsan\b",

    # Urdu script
    r"خودکشی",
    r"خود کشی",
    r"اپنی جان",
    r"خود کو نقصان",
]

IMMEDIATE_DANGER_PATTERNS = [
    r"\bhe is hurting me\b",
    r"\bhe is attacking me\b",
    r"\bi am being attacked\b",
    r"\bin immediate danger\b",
    r"\bhelp me now\b",

    r"\bmujhe abhi khatra hai\b",
    r"\babhi khatra hai\b",
    r"\bwoh mujhe maar raha\b",
    r"\bwoh mujhe maarne\b",

    r"مجھے ابھی خطرہ ہے",
    r"مجھے فوری مدد چاہیے",
    r"وہ مجھے مار رہا",
]


def _matches(text: str, patterns: list[str]) -> bool:
    normalized = text.lower().strip()

    for pattern in patterns:
        if re.search(pattern, normalized):
            return True

    return False


def detect_safety_risk(text: str) -> tuple[bool, str]:
    if _matches(text, HIGH_RISK_PATTERNS):
        return True, "high_risk"

    if _matches(text, IMMEDIATE_DANGER_PATTERNS):
        return True, "immediate_danger"

    return False, "none"