from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# HERVOICE VERIFIED KNOWLEDGE BASE
# =========================================================

KNOWLEDGE_BASE: list[dict[str, Any]] = [

    # -----------------------------------------------------
    # 1. MINISTRY OF HUMAN RIGHTS — 1099
    # -----------------------------------------------------

    {
        "id": "pakistan_mohr_1099",

        "title": (
            "Pakistan Ministry of Human Rights — "
            "Toll-Free Helpline 1099"
        ),

        "country": "Pakistan",

        "topics": [
            "human rights",
            "legal assistance",
            "legal information",
            "women's rights",
            "support",
        ],

        "keywords": [
            "1099",
            "human rights",
            "legal help",
            "legal assistance",
            "legal advice",
            "rights",
            "women rights",
            "ministry of human rights",
            "pakistan",
            "پاکستان",
            "قانونی مدد",
            "قانونی معلومات",
            "انسانی حقوق",
        ],

        "content": (
            "Pakistan's Ministry of Human Rights provides "
            "the toll-free 1099 helpline for human-rights "
            "and legal assistance. The Ministry's official "
            "website currently states that the helpline "
            "operates from 8:30 AM to 9:00 PM on weekdays. "
            "Users should check the official Ministry website "
            "for the latest operating information and service details."
        ),

        "source": "Pakistan Ministry of Human Rights",

        "url": "https://www.mohr.gov.pk/",

        "verified": True,

        "verification_date": "2026-09-04",
    },


    # -----------------------------------------------------
    # 2. KP BOLO HELPLINE
    # -----------------------------------------------------

    {
        "id": "kp_bolo_helpline",

        "title": (
            "Khyber Pakhtunkhwa BOLO Helpline — "
            "0800-22227"
        ),

        "country": "Pakistan",

        "region": "Khyber Pakhtunkhwa",

        "topics": [
            "gender-based violence",
            "domestic violence",
            "women's support",
            "legal aid",
            "psychological counselling",
            "shelter",
            "police protection",
            "medical aid",
        ],

        "keywords": [
            "bolo",
            "0800-22227",
            "gender based violence",
            "gender-based violence",
            "gbv",
            "domestic violence",
            "abuse",
            "violence",
            "women",
            "woman",
            "legal aid",
            "counselling",
            "counseling",
            "shelter",
            "police protection",
            "medical aid",
            "khyber pakhtunkhwa",
            "kp",
            "kpk",
            "peshawar",
            "abbottabad",
            "خیبر پختونخوا",
            "گھریلو تشدد",
            "خواتین",
        ],

        "content": (
            "The Khyber Pakhtunkhwa government's BOLO Helpline "
            "is a support service for survivors of gender-based "
            "violence. The service provides accessible response "
            "support including psychological counselling, legal "
            "aid and advice, shelter, police protection, and "
            "medical-aid referrals. The service also connects "
            "with relevant government and protection services."
        ),

        "source": (
            "Khyber Pakhtunkhwa Social Welfare Department — "
            "BOLO Helpline"
        ),

        "url": "https://www.swkpk.gov.pk/bolohelpline.php",

        "phone": "0800-22227",

        "verified": True,

        "verification_date": "2026-09-04",
    },


    # -----------------------------------------------------
    # 3. NATIONAL COMMISSION ON STATUS OF WOMEN
    # -----------------------------------------------------

    {
        "id": "ncsw_pakistan",

        "title": (
            "National Commission on the Status of Women "
            "(NCSW)"
        ),

        "country": "Pakistan",

        "topics": [
            "women's rights",
            "women empowerment",
            "complaints",
            "laws",
            "policies",
            "gender equality",
        ],

        "keywords": [
            "ncsw",
            "national commission",
            "status of women",
            "women rights",
            "women's rights",
            "women empowerment",
            "gender equality",
            "complaint",
            "complaints",
            "pakistan",
            "خواتین کے حقوق",
            "خواتین",
        ],

        "content": (
            "The National Commission on the Status of Women "
            "is a statutory body that examines and reviews "
            "laws, policies and programmes relating to women "
            "and monitors implementation of laws concerning "
            "the protection and empowerment of women. Its "
            "official website provides information about "
            "complaints and available government channels."
        ),

        "source": (
            "National Commission on the Status of Women"
        ),

        "url": "https://www.ncsw.gov.pk/",

        "verified": True,

        "verification_date": "2026-09-04",
    },


    # -----------------------------------------------------
    # 4. WORKPLACE HARASSMENT LAW
    # -----------------------------------------------------

    {
        "id": "pakistan_workplace_harassment",

        "title": (
            "Pakistan Protection Against Harassment "
            "of Women at the Workplace"
        ),

        "country": "Pakistan",

        "topics": [
            "workplace harassment",
            "employment",
            "women",
            "workplace rights",
            "harassment law",
        ],

        "keywords": [
            "workplace harassment",
            "office harassment",
            "work harassment",
            "harassment at work",
            "women workplace",
            "workplace rights",
            "employment rights",
            "harassment law",
            "protection against harassment",
            "workplace",
            "job",
            "office",
            "کام کی جگہ",
            "ہراسانی",
        ],

        "content": (
            "Pakistan has legislation concerning protection "
            "against harassment of women at the workplace. "
            "The Ministry of Human Rights provides information "
            "about the Protection Against Harassment of Women "
            "at the Workplace (Amendment) Act, 2022. For a "
            "specific legal situation, users should seek "
            "qualified legal advice rather than treating "
            "general information as a legal conclusion."
        ),

        "source": "Pakistan Ministry of Human Rights",

        "url": (
            "https://www.mohr.gov.pk/"
        ),

        "verified": True,

        "verification_date": "2026-09-04",
    },

]


# =========================================================
# NORMALIZATION
# =========================================================

def _normalize(text: str) -> str:

    return " ".join(
        text.lower().strip().split()
    )


# =========================================================
# SEARCH TEXT
# =========================================================

def _build_search_text(
    item: dict[str, Any],
) -> str:

    return " ".join(
        [
            item.get("title", ""),
            item.get("country", ""),
            item.get("region", ""),
            " ".join(item.get("topics", [])),
            " ".join(item.get("keywords", [])),
            item.get("content", ""),
        ]
    )


# =========================================================
# VERIFIED DOCUMENTS ONLY
# =========================================================

VERIFIED_DOCUMENTS = [
    item
    for item in KNOWLEDGE_BASE
    if item.get("verified", False)
]


SEARCH_DOCUMENTS = [
    _build_search_text(item)
    for item in VERIFIED_DOCUMENTS
]


# =========================================================
# TF-IDF INDEX
# =========================================================

if SEARCH_DOCUMENTS:

    VECTORIZER = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        max_features=10000,
    )

    DOCUMENT_MATRIX = VECTORIZER.fit_transform(
        SEARCH_DOCUMENTS
    )

else:

    VECTORIZER = None
    DOCUMENT_MATRIX = None


# =========================================================
# RETRIEVAL
# =========================================================

def retrieve_knowledge(
    query: str,
    limit: int = 3,
    min_score: float = 0.05,
) -> list[dict[str, Any]]:

    normalized_query = _normalize(query)

    if not normalized_query:
        return []

    if (
        VECTORIZER is None
        or DOCUMENT_MATRIX is None
        or not VERIFIED_DOCUMENTS
    ):
        return []

    query_vector = VECTORIZER.transform(
        [normalized_query]
    )

    similarities = cosine_similarity(
        query_vector,
        DOCUMENT_MATRIX,
    )[0]

    scored_results = []

    for index, score in enumerate(similarities):

        if score >= min_score:

            scored_results.append(
                (
                    float(score),
                    VERIFIED_DOCUMENTS[index],
                )
            )

    scored_results.sort(
        key=lambda result: result[0],
        reverse=True,
    )

    return [
        item
        for _, item in scored_results[:limit]
    ]


# =========================================================
# FORMAT KNOWLEDGE FOR AI
# =========================================================

def format_knowledge_context(
    results: list[dict[str, Any]],
) -> str:

    if not results:
        return ""

    sections: list[str] = []

    for item in results:

        section = f"""
SOURCE:
{item["source"]}

TITLE:
{item["title"]}

VERIFIED:
{item["verified"]}

VERIFICATION DATE:
{item["verification_date"]}

INFORMATION:
{item["content"]}

OFFICIAL SOURCE:
{item["url"]}
"""

        if item.get("phone"):
            section += f"""
OFFICIAL CONTACT:
{item["phone"]}
"""

        sections.append(
            section.strip()
        )

    return "\n\n---\n\n".join(
        sections
    )