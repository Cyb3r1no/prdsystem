SECTIONS = [
    {
        "id": "idea",
        "title": "1. الفكرة والمشكلة",
        "description": "ابدأ من المشكلة والنتيجة اللي تبيها. ما نحتاج منك أي تفاصيل تقنية.",
        "questions": [
            {
                "id": "contact_name",
                "label": "اسم المسؤول عن المشروع",
                "type": "text",
                "required": True,
                "placeholder": "الاسم",
                "gap_prompt": "من الشخص المسؤول عن متابعة المشروع من جهتكم؟",
            },
            {
                "id": "company_name",
                "label": "اسم الجهة أو النشاط",
                "type": "text",
                "required": False,
                "placeholder": "اختياري",
            },
            {
                "id": "contact_email",
                "label": "البريد الإلكتروني للتواصل",
                "type": "email",
                "required": False,
                "placeholder": "name@example.com",
            },
            {
                "id": "project_vision",
                "label": "صف لنا المشروع كما تتخيله بكلامك",
                "type": "textarea",
                "required": True,
                "placeholder": "وش الخدمة أو النظام اللي تبيه؟ ومن المفترض يستفيد منه؟",
                "gap_prompt": "وش الصورة النهائية اللي تتخيلها للمشروع لو نجح بالشكل المطلوب؟",
            },
            {
                "id": "core_problem",
                "label": "وش المشكلة الأساسية اللي تبي المشروع يحلها؟",
                "type": "textarea",
                "required": True,
                "placeholder": "ركز على المشكلة الحالية وتأثيرها، مو على الحل التقني.",
                "gap_prompt": "وش المشكلة الأساسية اليوم؟ وش أثرها عليكم أو على العميل؟",
            },
        ],
    },
    {
        "id": "today",
        "title": "2. كيف تشتغلون اليوم؟",
        "description": "فهم الواقع الحالي يساعدنا نقترح حل مناسب بدل ما نبني شيء ما يخدمكم.",
        "questions": [
            {
                "id": "current_process",
                "label": "اشرح لنا كيف تتم العملية اليوم من البداية للنهاية",
                "type": "textarea",
                "required": True,
                "placeholder": "مثال: العميل يرسل واتساب → الموظف يجمع البيانات → يدخلها بالنظام → يتم التنفيذ...",
                "gap_prompt": "اشرحوا لنا الرحلة الحالية خطوة بخطوة من بداية الطلب إلى نهايته.",
            },
            {
                "id": "pain_points",
                "label": "وين أكثر شيء يضيع وقت أو يسبب أخطاء أو إزعاج؟",
                "type": "textarea",
                "required": True,
                "placeholder": "اذكر أكثر 2–3 نقاط مزعجة أو مكلفة في الطريقة الحالية.",
                "gap_prompt": "وش أكثر النقاط اللي تسبب تأخير، أخطاء، تكلفة أو شكاوى؟",
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
                "gap_prompt": "مين المستخدمون الأساسيون؟ وهل تختلف صلاحياتهم أو احتياجاتهم؟",
            },
            {
                "id": "current_systems",
                "label": "وش الأنظمة أو الأدوات اللي تستخدمونها حالياً؟",
                "type": "textarea",
                "required": False,
                "placeholder": "مثال: Odoo، Excel، WhatsApp، نظام داخلي. إذا ما فيه اكتب: لا يوجد.",
                "gap_prompt": "وش الأنظمة الحالية اللي لازم نراعيها أو نتكامل معها؟",
            },
        ],
    },
    {
        "id": "outcome",
        "title": "3. النتيجة المطلوبة",
        "description": "نبي نعرف وش يعتبر نجاح بالنسبة لكم، ووش لازم يدخل في النسخة الأولى.",
        "questions": [
            {
                "id": "desired_outcome",
                "label": "بعد تنفيذ المشروع، وش الشي اللي ودك يصير أفضل بشكل واضح؟",
                "type": "textarea",
                "required": True,
                "placeholder": "مثال: تقليل وقت المعالجة، تنظيم الطلبات، تحسين تجربة العميل، تقليل العمل اليدوي...",
                "gap_prompt": "وش التغيير الواضح اللي تتوقعونه بعد إطلاق المشروع؟",
            },
            {
                "id": "must_haves",
                "label": "وش الأشياء اللي لازم تكون موجودة في أول نسخة؟",
                "type": "textarea",
                "required": True,
                "placeholder": "اكتب أهم الوظائف أو القدرات اللي ما تقدر تبدأ بدونها.",
                "gap_prompt": "وش الحد الأدنى اللي تعتبرون المشروع بدونه غير قابل للاستخدام؟",
            },
            {
                "id": "success_metrics",
                "label": "كيف نعرف أن المشروع نجح؟",
                "type": "textarea",
                "required": False,
                "placeholder": "مثال: تقليل وقت الإجراء من 20 إلى 5 دقائق، خفض الأخطاء، زيادة الطلبات المكتملة...",
                "gap_prompt": "وش المقياس أو النتيجة اللي نقدر نقيس بها نجاح المشروع بعد الإطلاق؟",
            },
            {
                "id": "automation_goal",
                "label": "هل فيه أعمال يدوية أو متكررة ودك النظام يختصرها أو يأتمتها؟",
                "type": "textarea",
                "required": False,
                "placeholder": "مثال: إدخال البيانات، الردود، المتابعة، التقارير، إصدار المستندات...",
            },
            {
                "id": "reference_examples",
                "label": "هل فيه موقع أو تطبيق أو تجربة تعجبك؟",
                "type": "textarea",
                "required": False,
                "placeholder": "اكتب الاسم أو الرابط، ووضح وش اللي أعجبك فيه تحديداً.",
            },
        ],
    },
    {
        "id": "constraints",
        "title": "4. القيود والنقاط المهمة",
        "description": "آخر خطوة: أي شيء ممكن يأثر على الحل أو الموعد أو طريقة التنفيذ.",
        "questions": [
            {
                "id": "integrations",
                "label": "هل فيه خدمات أو أنظمة لازم المشروع يرتبط معها؟",
                "type": "textarea",
                "required": False,
                "placeholder": "مثال: بوابة دفع، WhatsApp، ERP، خرائط، SMS. إذا ما فيه اكتب: لا يوجد.",
                "gap_prompt": "هل توجد تكاملات إلزامية مع أنظمة أو مزودين خارجيين؟",
            },
            {
                "id": "constraints",
                "label": "هل عندكم أي شروط أو قيود لازم نعرفها؟",
                "type": "textarea",
                "required": False,
                "placeholder": "مثال: استضافة معينة، صلاحيات، بيانات حساسة، نظام قديم، متطلبات داخلية...",
                "gap_prompt": "هل فيه قيود تقنية، تشغيلية، أمنية أو تنظيمية لازم تدخل بالحسبان؟",
            },
            {
                "id": "decision_context",
                "label": "مين عادة يراجع أو يعتمد القرار النهائي للمشروع؟",
                "type": "text",
                "required": False,
                "placeholder": "مثال: المدير العام، صاحب النشاط، إدارة تقنية المعلومات...",
                "gap_prompt": "مين أصحاب القرار أو الجهات اللي لازم تعتمد النطاق قبل التنفيذ؟",
            },
            {
                "id": "target_timeline",
                "label": "هل عندك موعد مستهدف أو ظرف مهم لازم نأخذه بالحسبان؟",
                "type": "text",
                "required": False,
                "placeholder": "اختياري — وإذا فيه موعد وضح سببه",
                "gap_prompt": "هل فيه موعد إطلاق مستهدف أو التزام زمني مؤثر على النطاق؟",
            },
            {
                "id": "extra_notes",
                "label": "أي شيء إضافي ودك نعرفه قبل ما نحلل المشروع؟",
                "type": "textarea",
                "required": False,
                "placeholder": "أي ملاحظة، تخوف، فكرة أو نقطة ما غطيناها فوق.",
            },
        ],
    },
]


READINESS_WEIGHTS = {
    "project_vision": 12,
    "core_problem": 15,
    "current_process": 12,
    "pain_points": 12,
    "users": 8,
    "current_systems": 5,
    "desired_outcome": 12,
    "must_haves": 10,
    "success_metrics": 6,
    "integrations": 3,
    "constraints": 2,
    "decision_context": 2,
    "target_timeline": 1,
}


def all_questions():
    return [q for section in SECTIONS for q in section["questions"]]


def question_map():
    return {q["id"]: q for q in all_questions()}
