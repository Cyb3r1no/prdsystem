SECTIONS = [
    {
        "id": "idea",
        "title": "1. فكرة المشروع",
        "description": "نبي نفهم المشروع بطريقتك أنت، بدون مصطلحات تقنية أو تفاصيل تنفيذ.",
        "questions": [
            {
                "id": "contact_name",
                "label": "اسم المسؤول عن المشروع",
                "type": "text",
                "required": True,
                "placeholder": "الاسم",
            },
            {
                "id": "project_vision",
                "label": "صف لنا المشروع كما تتخيله بكلامك",
                "type": "textarea",
                "required": True,
                "placeholder": "وش تبي الموقع أو النظام يسوي؟ وش التجربة اللي تتخيلها للعميل أو الموظف؟",
            },
            {
                "id": "core_problem",
                "label": "وش المشكلة الأساسية اللي تبي المشروع يحلها؟",
                "type": "textarea",
                "required": True,
                "placeholder": "اكتب أهم المشاكل أو الأشياء اللي تضايقك في الوضع الحالي.",
            },
        ],
    },
    {
        "id": "today",
        "title": "2. كيف تشتغلون اليوم؟",
        "description": "خلّنا نفهم الواقع الحالي أول، وبعدها إحنا نستخرج منه المتطلبات والحلول المناسبة.",
        "questions": [
            {
                "id": "current_process",
                "label": "اشرح لنا باختصار كيف تتم العملية اليوم من البداية للنهاية",
                "type": "textarea",
                "required": True,
                "placeholder": "مثال: العميل يرسل واتساب → الموظف يبحث → يرسل العرض → العميل يدفع → يتم تنفيذ الطلب...",
            },
            {
                "id": "users",
                "label": "مين الأشخاص اللي راح يستخدمون النظام؟",
                "type": "checkboxes",
                "required": False,
                "options": [
                    "العملاء",
                    "الموظفون",
                    "الإدارة",
                    "المحاسبة",
                    "شركات / عملاء B2B",
                    "أطراف أخرى",
                ],
            },
            {
                "id": "current_systems",
                "label": "هل تستخدمون حالياً أنظمة أو مواقع أو مزودين نحتاج نعرف عنها؟",
                "type": "textarea",
                "required": False,
                "placeholder": "اكتب أسماء الأنظمة أو الخدمات فقط. لا تضع كلمات مرور أو API Keys.",
            },
        ],
    },
    {
        "id": "direction",
        "title": "3. وش أهم شيء بالنسبة لك؟",
        "description": "حدد لنا الأولويات والأفكار، والباقي نناقشه معك في جلسة الـ Discovery.",
        "questions": [
            {
                "id": "must_haves",
                "label": "وش أهم الأشياء اللي لازم تكون موجودة في أول نسخة من المشروع؟",
                "type": "textarea",
                "required": True,
                "placeholder": "اكتبها بطريقتك حتى لو كانت أفكار عامة.",
            },
            {
                "id": "automation_goal",
                "label": "هل فيه أعمال يدوية أو متكررة ودك النظام يختصرها أو يأتمتها؟",
                "type": "textarea",
                "required": False,
                "placeholder": "مثال: الردود، إدخال البيانات، المتابعة، التقارير، إصدار مستندات...",
            },
            {
                "id": "reference_examples",
                "label": "هل فيه موقع أو تطبيق أو نظام يعجبك وتبي شيء قريب من فكرته؟",
                "type": "textarea",
                "required": False,
                "placeholder": "ضع الاسم أو الرابط ووش اللي أعجبك فيه.",
            },
            {
                "id": "target_timeline",
                "label": "هل عندك موعد مستهدف أو ظرف مهم لازم نأخذه بالحسبان؟",
                "type": "text",
                "required": False,
                "placeholder": "اختياري",
            },
            {
                "id": "extra_notes",
                "label": "أي فكرة أو ملاحظة إضافية ودك نعرفها قبل الاجتماع؟",
                "type": "textarea",
                "required": False,
                "placeholder": "اكتب أي شيء في بالك حتى لو مو متأكد هل يدخل ضمن المشروع أو لا.",
            },
        ],
    },
]


def all_questions():
    return [q for section in SECTIONS for q in section["questions"]]


def question_map():
    return {q["id"]: q for q in all_questions()}
