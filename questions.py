SECTIONS = [
    {
        "id": "vision",
        "title": "1. الرؤية والهدف",
        "description": "نبدأ بفهم المشروع والنتيجة التي تريد الوصول لها، بدون الدخول في تفاصيل تقنية.",
        "questions": [
            {"id": "contact_name", "label": "اسم المسؤول عن المشروع", "type": "text", "required": True, "placeholder": "الاسم"},
            {"id": "contact_email", "label": "البريد الإلكتروني", "type": "email", "required": False, "placeholder": "name@example.com"},
            {"id": "contact_phone", "label": "رقم الجوال", "type": "text", "required": False, "placeholder": "05xxxxxxxx"},
            {"id": "project_vision", "label": "صف لنا المشروع كما تتخيله بكلامك", "type": "textarea", "required": True, "placeholder": "وش تبي الموقع والنظام يسوي لك؟ وكيف تتخيل تجربة العميل والموظف؟"},
            {"id": "top_problems", "label": "ما أهم 3 مشاكل تريد أن يحلها المشروع؟", "type": "textarea", "required": True, "placeholder": "مثال: كثرة العمل اليدوي، بطء متابعة الحجوزات، صعوبة معرفة الربح الحقيقي..."},
            {"id": "success_definition", "label": "بعد 6 أشهر من إطلاق النظام، وش النتيجة اللي تخليك تقول إن المشروع نجح؟", "type": "textarea", "required": True},
        ],
    },
    {
        "id": "current_workflow",
        "title": "2. طريقة العمل الحالية",
        "description": "هدفنا نفهم الواقع اليوم قبل ما نقترح أي أتمتة أو AI.",
        "questions": [
            {"id": "lead_channels", "label": "من وين تجيكم طلبات العملاء حالياً؟", "type": "checkboxes", "required": True, "options": ["واتساب", "اتصال", "زيارة المكتب", "إنستغرام / سوشال ميديا", "موقع إلكتروني", "عملاء شركات", "مصادر أخرى"]},
            {"id": "booking_flow", "label": "اشرح لنا رحلة الحجز الحالية من أول طلب العميل إلى إصدار التذكرة / تأكيد الفندق", "type": "textarea", "required": True, "placeholder": "مثال: العميل يرسل واتساب → الموظف يبحث → يرسل عرض → العميل يحول → الموظف يصدر..."},
            {"id": "employees_count", "label": "كم عدد الموظفين المرتبطين بالحجوزات وخدمة العملاء والمحاسبة؟", "type": "text", "required": True},
            {"id": "employee_tasks", "label": "وش أهم مهام الموظفين اليومية؟", "type": "textarea", "required": True, "placeholder": "اكتب الوظائف والمهام قدر الإمكان، حتى لو كانت متكررة وبسيطة."},
            {"id": "manual_time_wasters", "label": "وش أكثر الأعمال اليدوية اللي تاخذ وقت من الموظفين؟", "type": "textarea", "required": True},
            {"id": "booking_volume", "label": "تقريباً كم عدد الحجوزات في اليوم أو الشهر؟", "type": "text", "required": False, "placeholder": "إذا ما عندك رقم دقيق اكتب تقدير"},
            {"id": "customer_mix", "label": "نوع العملاء", "type": "checkboxes", "required": True, "options": ["أفراد B2C", "شركات B2B", "جهات / مجموعات", "وكلاء فرعيون", "أخرى"]},
        ],
    },
    {
        "id": "services",
        "title": "3. الخدمات وتجربة العميل",
        "description": "حدد الخدمات التي تريد أن يتمكن العميل من طلبها أو حجزها عبر المنصة.",
        "questions": [
            {"id": "launch_services", "label": "وش الخدمات المطلوبة في الإصدار الأول؟", "type": "checkboxes", "required": True, "options": ["حجز طيران", "حجز فنادق", "بكجات سياحية", "تأمين سفر", "تأشيرات", "نقل / سيارات", "جولات وأنشطة", "طلبات خاصة عبر الموظف"]},
            {"id": "customer_account", "label": "هل تريد حساب للعميل يتابع منه حجوزاته وفواتيره وطلباته؟", "type": "radio", "required": True, "options": ["نعم", "لا", "نحتاج نناقشها"]},
            {"id": "customer_self_service", "label": "وش الأشياء اللي تبي العميل يسويها بنفسه بدون موظف؟", "type": "textarea", "required": False, "placeholder": "مثال: حجز، دفع، تحميل التذكرة، طلب إلغاء، متابعة استرجاع..."},
            {"id": "languages", "label": "لغات المنصة المطلوبة", "type": "checkboxes", "required": True, "options": ["العربية", "الإنجليزية", "لغات إضافية لاحقاً"]},
            {"id": "reference_sites", "label": "هل فيه مواقع أو تطبيقات تعجبك كتجربة أو تصميم؟", "type": "textarea", "required": False, "placeholder": "ضع الروابط أو الأسماء ووش اللي أعجبك فيها"},
        ],
    },
    {
        "id": "suppliers",
        "title": "4. الطيران والفنادق والموردين",
        "description": "نحتاج نعرف المزودين الحاليين والربط المتاح. لا تضع أي كلمات مرور أو API Keys هنا.",
        "questions": [
            {"id": "flight_supplier", "label": "من هو مزود الطيران / النظام المستخدم حالياً؟", "type": "text", "required": False, "placeholder": "اسم الشركة أو GDS أو النظام"},
            {"id": "flight_api", "label": "هل يوجد GDS أو Flight API متاح لكم؟", "type": "radio", "required": True, "options": ["نعم", "لا", "غير متأكد"]},
            {"id": "flight_operations", "label": "من يقوم اليوم بإصدار التذاكر والتعديل والإلغاء وإعادة الإصدار؟", "type": "textarea", "required": False},
            {"id": "hotel_supplier", "label": "من هو مزود الفنادق / النظام المستخدم حالياً؟", "type": "text", "required": False},
            {"id": "hotel_api", "label": "هل يوجد Hotel API متاح لكم؟", "type": "radio", "required": True, "options": ["نعم", "لا", "غير متأكد"]},
            {"id": "multiple_suppliers", "label": "هل تستخدمون أكثر من مورد للطيران أو الفنادق؟ وكيف تختارون السعر الأفضل؟", "type": "textarea", "required": False},
            {"id": "pricing_model", "label": "كيف تحددون سعر البيع والربح حالياً؟", "type": "textarea", "required": True, "placeholder": "عمولة ثابتة؟ نسبة؟ تختلف حسب المورد أو العميل أو الخدمة؟"},
        ],
    },
    {
        "id": "payments",
        "title": "5. الدفع والإلغاء والاسترجاع",
        "description": "نحدد دورة المال والحالات اللي تحتاج تدخل بشري.",
        "questions": [
            {"id": "current_payments", "label": "كيف يدفع العملاء حالياً؟", "type": "checkboxes", "required": True, "options": ["تحويل بنكي", "شبكة داخل المكتب", "رابط دفع", "بطاقات", "Apple Pay", "نقدي", "آجل / حساب شركات", "طرق أخرى"]},
            {"id": "desired_payments", "label": "وش وسائل الدفع المطلوبة داخل المنصة؟", "type": "checkboxes", "required": True, "options": ["مدى", "Visa / Mastercard", "Apple Pay", "STC Pay", "تحويل بنكي", "دفع آجل للشركات", "نحددها لاحقاً"]},
            {"id": "payment_gateway", "label": "هل عندكم بوابة دفع حالية أو مزود مفضل؟", "type": "text", "required": False},
            {"id": "refund_flow", "label": "اشرح كيف تتم الإلغاءات والاسترجاعات حالياً", "type": "textarea", "required": True},
            {"id": "refund_pain", "label": "وش أكثر المشاكل في الإلغاء أو Refund اليوم؟", "type": "textarea", "required": False},
            {"id": "invoice_requirements", "label": "وش متطلبات الفواتير والضريبة عندكم؟", "type": "textarea", "required": False, "placeholder": "مثال: فاتورة ضريبية، فاتورة شركات، رقم ضريبي، تسوية شهرية..."},
        ],
    },
    {
        "id": "backoffice",
        "title": "6. لوحة الإدارة والمالية",
        "description": "نحدد السلوشن الداخلي اللي يدير المكتب، وليس الموقع فقط.",
        "questions": [
            {"id": "admin_dashboard", "label": "وش أهم المعلومات اللي تبي تشوفها أول ما تدخل لوحة الإدارة؟", "type": "textarea", "required": True, "placeholder": "مبيعات اليوم، الربح، الحجوزات المعلقة، Refunds، أداء الموظفين..."},
            {"id": "admin_modules", "label": "وش الأقسام المطلوبة داخل لوحة الإدارة؟", "type": "checkboxes", "required": True, "options": ["إدارة الحجوزات", "العملاء CRM", "الموظفين والصلاحيات", "الموردين", "المدفوعات", "الإلغاءات والاسترجاع", "المصروفات", "الأرباح والعمولات", "التقارير", "التسويات والمطابقة", "التذاكر وخدمة العملاء"]},
            {"id": "roles", "label": "وش الأدوار أو الصلاحيات الموجودة عندكم؟", "type": "textarea", "required": False, "placeholder": "مالك، مدير، موظف حجوزات، خدمة عملاء، محاسب..."},
            {"id": "accounting_system", "label": "هل تستخدمون نظام محاسبي حالياً؟", "type": "text", "required": False, "placeholder": "اسم النظام أو اكتب: لا يوجد"},
            {"id": "finance_scope", "label": "وش تحتاجون مالياً داخل النظام؟", "type": "checkboxes", "required": True, "options": ["الإيرادات", "تكلفة الحجز", "الربح لكل حجز", "المصروفات", "رصيد الموردين", "رصيد العملاء", "عمولات الموظفين", "رسوم بوابة الدفع", "Refunds", "التسويات", "محاسبة كاملة", "ربط مع برنامج محاسبي"]},
            {"id": "reconciliation", "label": "كيف تتم المطابقة والتسوية مع الموردين والبنوك حالياً؟", "type": "textarea", "required": False},
            {"id": "reports", "label": "وش أهم التقارير اللي تحتاجها الإدارة؟", "type": "textarea", "required": True},
        ],
    },
    {
        "id": "automation_ai",
        "title": "7. الأتمتة والذكاء الاصطناعي",
        "description": "نبحث عن المهام المتكررة التي يمكن تقليلها، مع تحديد ما يحتاج موافقة بشرية.",
        "questions": [
            {"id": "automation_targets", "label": "لو النظام يقدر يلغي عن الموظفين 5 مهام يومية، وش تختار؟", "type": "textarea", "required": True},
            {"id": "automation_events", "label": "وش العمليات اللي تتوقع تكون تلقائية؟", "type": "checkboxes", "required": True, "options": ["إرسال التذكرة / الفاوتشر", "إرسال الفاتورة", "تنبيهات الرحلة", "متابعة الحجز المعلق", "متابعة الدفع", "متابعة Refund", "متابعة العميل بعد عرض السعر", "تنبيه فشل الحجز", "مطابقة بعض العمليات المالية", "تقارير دورية"]},
            {"id": "ai_use_cases", "label": "وش تبي AI Agent يساعد فيه؟", "type": "checkboxes", "required": True, "options": ["خدمة العملاء", "اقتراح رحلات وفنادق", "تجهيز عروض أسعار", "قراءة حالة الحجز والرد عليها", "إرسال التذاكر والفواتير", "مراقبة مشاكل الحجوزات", "تقارير الإدارة", "تلخيص المحادثات", "مساعدة الموظف داخلياً", "أفكار أخرى"]},
            {"id": "human_approval", "label": "وش العمليات اللي لازم ما تنفذ إلا بعد موافقة موظف؟", "type": "textarea", "required": True, "placeholder": "مثال: إلغاء حجز، Refund، تغيير سعر، إصدار تذكرة بمبلغ معين..."},
            {"id": "whatsapp", "label": "هل واتساب جزء أساسي من المشروع؟", "type": "radio", "required": True, "options": ["نعم — مبيعات وخدمة عملاء", "نعم — إشعارات فقط", "لا", "نحتاج نناقش"]},
            {"id": "ai_expectation", "label": "صف لنا كيف تتخيل الـ AI Agent يخدم المكتب فعلياً", "type": "textarea", "required": False},
        ],
    },
    {
        "id": "integrations",
        "title": "8. الأنظمة والتكاملات",
        "description": "نحصر الأنظمة التي لازم نستبدلها أو نربط معها.",
        "questions": [
            {"id": "current_systems", "label": "اذكر الأنظمة والبرامج المستخدمة حالياً في المكتب", "type": "textarea", "required": False, "placeholder": "حجوزات، محاسبة، CRM، واتساب، Excel، Google Sheets..."},
            {"id": "required_integrations", "label": "وش الأنظمة أو الشركات اللي لازم المنصة تتكامل معها؟", "type": "textarea", "required": False},
            {"id": "notification_channels", "label": "قنوات التنبيه المطلوبة", "type": "checkboxes", "required": True, "options": ["داخل لوحة الإدارة", "واتساب", "SMS", "Email", "Push Notifications لاحقاً"]},
            {"id": "documents_links", "label": "إذا عندك مستندات أو API Docs أو عروض موردين، ضع الروابط هنا", "type": "textarea", "required": False, "placeholder": "لا تضع كلمات مرور أو مفاتيح API"},
            {"id": "constraints", "label": "هل فيه متطلبات أو قيود لازم نعرفها قبل التصميم؟", "type": "textarea", "required": False, "placeholder": "أنظمة داخلية، اشتراطات، بيانات حساسة، مزود محدد، طريقة تشغيل خاصة..."},
        ],
    },
    {
        "id": "scope",
        "title": "9. الأولويات والمرحلة الأولى",
        "description": "آخر خطوة: نفرق بين الضروري للإطلاق والأفكار اللي ممكن تتأجل.",
        "questions": [
            {"id": "mvp_must_have", "label": "لو اضطرينا نطلق أول نسخة بأهم الأشياء فقط، وش الأشياء اللي مستحيل تستغني عنها؟", "type": "textarea", "required": True},
            {"id": "later_features", "label": "وش الأشياء اللي ممكن تكون مرحلة ثانية أو مستقبلية؟", "type": "textarea", "required": False},
            {"id": "target_launch", "label": "هل عندكم موعد مستهدف للإطلاق؟", "type": "text", "required": False},
            {"id": "budget_range", "label": "هل فيه ميزانية تقريبية محددة للمشروع؟", "type": "select", "required": False, "options": ["غير محددة حالياً", "أقل من 25,000 ريال", "25,000 – 50,000 ريال", "50,000 – 100,000 ريال", "100,000 – 250,000 ريال", "أكثر من 250,000 ريال"]},
            {"id": "free_ideas", "label": "اكتب أي أفكار أو تفاصيل إضافية للمشروع حتى لو ما تعرف كيف تُنفذ", "type": "textarea", "required": False, "placeholder": "هذه المساحة لك — أي فكرة تعتبر مهمة."},
            {"id": "discovery_consent", "label": "أفهم أن هذه الإجابات تستخدم لدراسة المتطلبات وبناء PRD مبدئي، وليست اتفاق تنفيذ أو عرض سعر نهائي.", "type": "checkbox", "required": True},
        ],
    },
]


def all_questions():
    return [q for section in SECTIONS for q in section["questions"]]


def question_map():
    return {q["id"]: q for q in all_questions()}
