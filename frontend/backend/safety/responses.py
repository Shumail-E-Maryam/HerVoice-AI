def get_safety_response(language: str, risk_type: str) -> str:

    # ---------------------------------------------------------
    # URDU
    # ---------------------------------------------------------

    if language == "UR":

        if risk_type == "immediate_danger":
            return (
                "مجھے افسوس ہے کہ آپ اس وقت ایسی صورتحال میں ہیں۔ "
                "اگر آپ کو فوری خطرہ ہے تو کسی محفوظ جگہ جانے کی کوشش کریں "
                "اور کسی قابلِ اعتماد شخص یا مقامی ایمرجنسی سروس سے فوراً رابطہ کریں۔ "
                "پاکستان میں انسانی حقوق کی خلاف ورزیوں اور قانونی رہنمائی کے لیے "
                "وزارتِ انسانی حقوق کی ٹول فری ہیلپ لائن 1099 دستیاب ہے۔ "
                "اگر آپ کے لیے محفوظ ہو تو کسی قابلِ اعتماد شخص کو بھی ابھی بتائیں۔"
            )

        return (
            "مجھے خوشی ہے کہ آپ نے یہ بات بتائی۔ "
            "آپ کو یہ سب کچھ اکیلے سنبھالنے کی ضرورت نہیں ہے۔ "
            "اگر آپ کو لگتا ہے کہ آپ محفوظ نہیں ہیں یا صورتحال فوری نوعیت کی ہے، "
            "تو کسی قابلِ اعتماد شخص یا مقامی ایمرجنسی سروس سے فوراً رابطہ کریں۔ "
            "پاکستان میں انسانی حقوق کی خلاف ورزیوں اور قانونی مدد کے لیے "
            "وزارتِ انسانی حقوق کی ٹول فری ہیلپ لائن 1099 دستیاب ہے۔ "
            "اگر ممکن ہو تو ابھی کسی قابلِ اعتماد شخص کے قریب رہیں۔"
        )

    # ---------------------------------------------------------
    # ENGLISH
    # ---------------------------------------------------------

    if risk_type == "immediate_danger":
        return (
            "I'm sorry you're dealing with something this serious. "
            "If you are in immediate danger, try to move toward a safer "
            "place and contact a trusted person or local emergency service "
            "right away. In Pakistan, the Ministry of Human Rights provides "
            "the toll-free 1099 helpline for human-rights and legal assistance. "
            "If it is safe to do so, please let someone you trust know what is happening."
        )

    return (
        "I'm glad you reached out. You don't have to handle something this "
        "serious completely on your own. If you feel unsafe or the situation "
        "is becoming urgent, contact a trusted person or local emergency "
        "service. In Pakistan, the Ministry of Human Rights provides the "
        "toll-free 1099 helpline for human-rights and legal assistance. "
        "If possible, stay connected with someone you trust."
    )