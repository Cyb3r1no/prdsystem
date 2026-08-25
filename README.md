# PRD System — Client Discovery Portal

بوابة عربية لاكتشاف متطلبات العميل قبل بناء الـ PRD. الفكرة التشغيلية بسيطة ومقصودة:

- **رابط واحد** يرسل لأي عميل.
- العميل يشرح الفكرة، المشكلة، طريقة العمل الحالية والنتيجة المطلوبة.
- الرد يظهر في **لوحة Admin واحدة** للفريق.
- النظام يحسب **Discovery Readiness** ويعرض أهم الفجوات والأسئلة التي يجب إقفالها.
- الفريق يناقش العميل في النقاط الناقصة، ثم يبني الـ PRD ويقترح الحل.

> النظام لا يولد حلولاً تلقائياً ولا يعتبر كلام العميل Requirements معتمدة. دوره هو تحسين جودة الـ Discovery وتقليل الافتراضات قبل كتابة الـ PRD.

## Workflow

```text
Single Client Link
        ↓
Client Discovery Brief
        ↓
Admin Discovery Inbox
        ↓
Readiness + Gaps + Executive Snapshot
        ↓
Focused Client Discussion
        ↓
Team Solution / MVP Decisions
        ↓
PRD v0.1
        ↓
Client Review
        ↓
PRD v1.0 / Scope / Cost / Timeline
```

## تجربة العميل

النموذج مقسم إلى 4 مراحل قصيرة:

1. الفكرة والمشكلة.
2. طريقة العمل الحالية ونقاط الألم.
3. النتيجة المطلوبة وMust-have للنسخة الأولى.
4. التكاملات والقيود والموعد وأصحاب القرار.

الأسئلة المطلوبة محدودة حتى لا يتحول الـ Discovery إلى استبيان طويل، بينما الأسئلة الاختيارية تساعد العميل يعطي سياقاً أعمق إذا كان متاحاً.

## لوحة الفريق

كل Submission يعرض:

- Discovery Readiness من 0–100%.
- حالة وضوح المشكلة، الوضع الحالي، النتيجة ونطاق V1.
- Executive Snapshot لأهم أربع نقاط.
- أهم أسئلة يجب إقفالها قبل كتابة PRD.
- جميع إجابات العميل الأصلية كـ Source of Truth.
- تصدير JSON خام.
- تصدير Markdown منظم كـ **Discovery Brief** جاهز لاستخدامه في جلسة الفريق أو كمدخل لصياغة PRD.

## الخصوصية والأمان

- الردود تحفظ في SQLite داخل السيرفر فقط.
- مجلد `data/` غير مرفوع إلى GitHub.
- Admin محمي بـ `ADMIN_TOKEN` وجلسة HttpOnly.
- Security headers مفعلة، وصفحات Admin تستخدم `Cache-Control: no-store`.
- المدخلات تتحقق Server-side ويتم تجاهل الحقول غير المعروفة قبل التخزين.
- Honeypot لتقليل السبام.
- حد أقصى لحجم الطلب 1 MB.

**لا تطلب من العميل إدخال:** كلمات مرور، API keys، بيانات بطاقات، 2FA، أسرار أو بيانات حساسة غير لازمة للـ Discovery.

## التشغيل

```bash
git clone https://github.com/Cyb3r1no/prdsystem.git
cd prdsystem
cp .env.example .env
# عدل SECRET_KEY و ADMIN_TOKEN
docker compose up -d --build
```

ثم:

- رابط العميل: `http://SERVER_IP:8080/`
- Admin: `http://SERVER_IP:8080/admin/login`
- Health: `http://SERVER_IP:8080/health`

## إعداد `.env`

```env
SECRET_KEY=replace-with-a-long-random-secret
ADMIN_TOKEN=replace-with-a-long-random-admin-token
PORT=8080
COOKIE_SECURE=0

PROJECT_SLUG=discovery
PROJECT_NAME=VOYAGE
PROJECT_NAME_AR=ڤوياج للسفر والسياحة
PROJECT_SUBTITLE=مرحلة اكتشاف المتطلبات قبل بناء الـ PRD
```

إذا كان التطبيق خلف HTTPS اضبط:

```env
COOKIE_SECURE=1
```

## Cloudflare Tunnel

اربط Hostname بالخدمة:

```text
discovery.example.com -> http://localhost:8080
```

ويظل عندك رابط عام واحد لكل العملاء.

## التحديث

```bash
git pull
docker compose up -d --build
```

## قاعدة الفريق

**Client request ≠ Requirement.**

قبل إدخال أي Feature في PRD تأكد من:

- المشكلة التي يحلها.
- المستخدم المستفيد.
- النتيجة المطلوبة.
- حدود MVP وOut of Scope.
- التكاملات والقيود.
- Acceptance Criteria قابلة للاختبار.
