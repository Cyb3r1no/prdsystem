# PRD System — VOYAGE Discovery Portal

بوابة ويب عربية لجمع متطلبات العميل قبل بناء الـ PRD.

## الهدف

الرابط يُرسل للعميل قبل التنفيذ. العميل يشرح فكرته وطريقة عمله الحالية، يحدد الأولويات والتكاملات والأتمتة المطلوبة، ثم تحفظ الإجابات على السيرفر وتظهر في لوحة خاصة لصاحب المشروع. بعدها تُستخدم الإجابات لبناء PRD v0.1 ومناقشته مع العميل.

## المزايا

- واجهة عربية RTL ومتجاوبة مع الجوال.
- نموذج متعدد المراحل مع Progress Bar.
- حفظ التقدم تلقائياً في المتصفح حتى لو أغلق العميل الصفحة.
- صفحة مراجعة قبل الإرسال.
- تخزين الردود محلياً في SQLite على السيرفر — لا تُرفع إجابات العملاء إلى GitHub.
- لوحة إدارة محمية بـ `ADMIN_TOKEN`.
- تصدير الرد كـ JSON أو Markdown جاهز للتحليل وبناء PRD.
- Honeypot + حدود على حجم الطلب + تحقق Server-side للحد من السبام والمدخلات غير الصحيحة.
- Docker Compose للنشر السريع.

## تشغيل سريع

```bash
git clone https://github.com/Cyb3r1no/prdsystem.git
cd prdsystem
cp .env.example .env
# غيّر القيم داخل .env
docker compose up -d --build
```

ثم افتح:

- نموذج العميل: `http://SERVER_IP:8080/`
- لوحة الإدارة: `http://SERVER_IP:8080/admin/login`
- فحص الخدمة: `http://SERVER_IP:8080/health`

## الإعدادات

`.env`:

```env
SECRET_KEY=change-this-to-a-long-random-value
ADMIN_TOKEN=change-this-to-a-long-random-admin-token
PORT=8080
```

> مهم: لا تستخدم كلمة مرور قصيرة. وللنشر على الإنترنت ضع التطبيق خلف HTTPS عبر Caddy / Nginx / Cloudflare Tunnel.

## البيانات

الردود تحفظ في:

```text
data/prdsystem.db
```

`data/` مستثنى من Git حتى لا تدخل بيانات العملاء إلى المستودع.

## تحديث المشروع

```bash
git pull
docker compose up -d --build
```

## نشر عبر Cloudflare Tunnel

إذا كان عندك Cloudflare Tunnel، اربط Hostname بالخدمة:

```text
http://localhost:8080
```

مثال:

```text
discovery.example.com -> http://localhost:8080
```

## سير العمل المقترح

```text
Client Discovery Link
        ↓
Client submits needs + current workflow
        ↓
Review answers in Admin
        ↓
Export Markdown / JSON
        ↓
Analyze requirements
        ↓
Discovery Meeting
        ↓
PRD v0.1
        ↓
Client Review
        ↓
PRD v1.0 Approved
        ↓
Scope / Cost / Timeline
        ↓
Development
```

## ملاحظة أمنية

لا تطلب من العميل إدخال كلمات مرور، API keys، بيانات بطاقات، أو أسرار تشغيلية داخل النموذج. المطلوب أسماء الأنظمة والمزودين وطريقة العمل فقط.
