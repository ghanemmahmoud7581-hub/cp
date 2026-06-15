"""
=============================================================
  تطبيق البنك الرقمي الجزائري — نموذج أولي (Prototype)
  المستشار الشخصي الآلي (CPA) — مشروع تخرج تسويق بنكي
=============================================================
  الإصدار: 3.0 (متوافق مع Flet >= 0.80 — async/await)
  التشغيل: pip install flet  ثم  python main.py
  للويب:   python main.py  (مع تفعيل WEB_BROWSER)
=============================================================
"""

import flet as ft
import random
import string

# ─────────────────────────────────────────────────────────────
#  بيانات وهمية (Mock Data)
# ─────────────────────────────────────────────────────────────

NEWS_DATA = [
    {
        "title": "بنك الجزائر يرفع سعر الفائدة إلى 4.5%",
        "date": "24 مايو 2025",
        "desc": (
            "أعلن بنك الجزائر المركزي عن رفع سعر الفائدة الرئيسي بمقدار 0.25 نقطة"
            " أساس في إطار سياسته النقدية لمكافحة التضخم وتعزيز الاستقرار المالي."
        ),
    },
    {
        "title": "تيسير إجراءات القروض للمؤسسات الصغيرة والمتوسطة",
        "date": "20 مايو 2025",
        "desc": (
            "أعلنت وزارة المالية عن حزمة تدابير جديدة تهدف إلى تسهيل حصول"
            " المؤسسات الصغيرة والمتوسطة على التمويل البنكي وتقليص آجال معالجة الملفات."
        ),
    },
    {
        "title": "إطلاق خدمة التحويل الفوري بين البنوك",
        "date": "15 مايو 2025",
        "desc": (
            "دخلت منظومة التحويل الفوري بين البنوك الجزائرية حيز التنفيذ رسمياً،"
            " مما يتيح للمواطنين إجراء تحويلاتهم على مدار الساعة وفي أقل من 30 ثانية."
        ),
    },
    {
        "title": "البنوك الجزائرية تطلق تطبيقات الدفع عبر الهاتف",
        "date": "10 مايو 2025",
        "desc": (
            "في خطوة نحو الرقمنة الشاملة، أطلقت كبرى البنوك الجزائرية تطبيقات دفع"
            " متطورة تدعم الدفع بالبصمة وخدمة QR Code والإشعارات الفورية."
        ),
    },
]

OFFERS_DATA = [
    {
        "title": "بطاقة ذهبية مجانية",
        "desc": (
            "احصل على بطاقة ذهبية برسوم صفرية لأول سنة كاملة."
            " تمتع بمزايا التأمين والسفر والشراء الدولي."
        ),
        "icon": ft.Icons.CREDIT_CARD,
        "color": "#221686",
        "text_color": "#FFFFFF",
    },
    {
        "title": "قرض بلا فوائد — 12 شهراً",
        "desc": (
            "قرض استهلاكي يصل إلى 500,000 دج بدون فوائد"
            " لمدة سنة كاملة. شروط ميسّرة وإجراءات سريعة."
        ),
        "icon": ft.Icons.ACCOUNT_BALANCE,
         "color": "#221686",
        "text_color": "#FFFFFF",
    },
    {
        "title": "برنامج الإحالة — اربح معنا",
        "desc": (
            "أحِل صديقاً واحصل أنت وصديقك على 2,000 دج مكافأة"
            " فورية عند فتح حسابه وأول إيداع."
        ),
        "icon": ft.Icons.PEOPLE,
         "color": "#221686",
        "text_color": "#FFFFFF",
    },
    {
        "title": "تخفيضات مع متاجر شريكة",
        "desc": (
            "خصومات حصرية تصل إلى 30% في أكثر من 200 متجر شريك"
            " على المستوى الوطني عند الدفع ببطاقتك."
        ),
        "icon": ft.Icons.LOCAL_OFFER,
        "color": "#221686",
        "text_color": "#FFFFFF",
    },
]

NOTIFICATIONS = [
    "🔔 تحديث: أسعار الفائدة على الادخار ارتفعت إلى 3.75%",
    "🎁 عرض محدود: قرض السيارة بدون ضمانات — تقدّم الآن",
    "📊 كشف حسابك لشهر أبريل جاهز للتحميل",
    "✅ تحويلك الأخير تم بنجاح",
]


# ─────────────────────────────────────────────────────────────
#  حالة التطبيق (App State / Session)
# ─────────────────────────────────────────────────────────────

class AppState:
    """Holds all session data across page navigations."""
    def __init__(self):
        self.full_name: str = ""
        self.account_type: str = "جاري"
        self.balance: float = 0.0
        self.account_number: str = ""

    def reset(self):
        self.__init__()


state = AppState()


# ─────────────────────────────────────────────────────────────
#  دوال مساعدة (Helpers)
# ─────────────────────────────────────────────────────────────

def fmt_dz(amount: float) -> str:
    return f"{amount:,.0f} دج"


def section_title(text: str) -> ft.Text:
    return ft.Text(
        text, size=16, weight=ft.FontWeight.BOLD,
        color="#1E3A5F", text_align=ft.TextAlign.RIGHT,
    )


def hdivider() -> ft.Divider:
    return ft.Divider(height=1, color="#E5E7EB")


# ══════════════════════════════════════════════════════════════
#  ASYNC MAIN — required for await page.push_route()
# ══════════════════════════════════════════════════════════════

async def main(page: ft.Page):

    # ── Page configuration ────────────────────────────────────
    page.title   = "بنك CPA"
    page.rtl     = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F1F5F9"
    page.padding = 0
    page.width   = 480

    page.fonts = {
        "Cairo": (
            "https://fonts.gstatic.com/s/cairo/v28/"
            "SLXgc1nY6HkvalIvTp0mxdt0UX8.woff2"
        ),
    }
    page.theme = ft.Theme(
        font_family="Cairo",
        color_scheme=ft.ColorScheme(
            primary="#1E3A5F",
            secondary="#3B82F6",
        ),
    )

    # ─────────────────────────────────────────────────────────
    #  Shared: AppBar builder
    # ─────────────────────────────────────────────────────────

    def build_appbar(title: str, show_back: bool = False,
                     back_route: str = "/dashboard") -> ft.AppBar:
        async def go_back(_e):
            await page.push_route(back_route)

        leading = (
            ft.IconButton(
                icon=ft.Icons.ARROW_FORWARD,   # RTL: forward = back visually
                icon_color="white",
                tooltip="رجوع",
                on_click=go_back,
            )
            if show_back else None
        )
        return ft.AppBar(
            title=ft.Text(title, color="#F2FF3E", size=20,
                          weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor="#0D2855",
            leading=leading,
            leading_width=50,
            actions=[
                ft.Container(
                    content=ft.Text("CPA", color="#F2FF3E", size=22,
                                    weight=ft.FontWeight.BOLD),
                    margin=ft.margin.only(left=14),
                )
            ],
        )

    # ─────────────────────────────────────────────────────────
    #  PAGE 1 — فتح حساب جديد  route: /open
    # ─────────────────────────────────────────────────────────

    def build_open_account_view() -> ft.View:

        name_field = ft.TextField(
            label="الاسم الكامل",
            hint_text="مثال: محمد بن علي",
            prefix_icon=ft.Icons.PERSON,
            border_radius=12,
            filled=True, bgcolor="white",
            text_align=ft.TextAlign.RIGHT,
        )
        type_dd = ft.Dropdown(
            label="نوع الحساب",
            
            options=[
                ft.dropdown.Option(key="جاري",  text="حساب جاري"),
                ft.dropdown.Option(key="ادخار", text="حساب ادخار"),
                
            ],
            value="جاري",
            border_radius=12,
            filled=True, bgcolor="white",
        )
        amount_field = ft.TextField(
            label="مبلغ الإيداع الأولي (دج)",
            hint_text="الحد الأدنى: 5,000 دج",
            prefix_icon=ft.Icons.PAYMENTS,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
            filled=True, bgcolor="white",
            text_align=ft.TextAlign.RIGHT,
        )
        error_text = ft.Text(
            "", color="#EF4444", size=13,
            text_align=ft.TextAlign.RIGHT, visible=False,
        )

        def show_err(msg: str):
            error_text.value = msg
            error_text.visible = True
            page.update()

        async def on_submit(_e):
            error_text.visible = False

            name = (name_field.value or "").strip()
            if len(name) < 3:
                show_err("⚠️ يرجى إدخال الاسم الكامل (3 أحرف على الأقل)")
                return

            raw = (amount_field.value or "").replace(",", "").replace(" ", "")
            try:
                amount = float(raw)
            except ValueError:
                show_err("⚠️ يرجى إدخال مبلغ صحيح")
                return

            if amount < 5000:
                show_err("⚠️ الحد الأدنى للإيداع هو 5,000 دج")
                return

            # Save session
            state.full_name     = name
            state.account_type  = type_dd.value or "جاري"
            state.balance       = amount
            state.account_number = "DZ" + "".join(random.choices(string.digits, k=14))

            await page.push_route("/dashboard")

        def feature_chip(icon, label):
            return ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
                controls=[
                    ft.Icon(icon, color="#3B82F6", size=22),
                    ft.Text(label, size=12, color="#475569"),
                ],
            )

        return ft.View(
            route="/open",
            appbar=build_appbar("فتح حساب جديد"),
            bgcolor="#F1F5F9",
            padding=0,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Column(
                    spacing=0,
                    controls=[
                        # Hero banner
                        ft.Container(
                            width=float("inf"),
                            bgcolor="#1E3A5F",
                            padding=ft.padding.symmetric(vertical=32, horizontal=20),
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.ACCOUNT_BALANCE,
                                            size=54, color="white"),
                                    ft.Text(
                                        "مرحباً بك في بنك CPA",
                                        size=22, weight=ft.FontWeight.BOLD,
                                        color="#FBFF26",
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Text(
                                      " خدمتك على مدار الساعة",
                                        size=13, color="#FBFF26",
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                ],
                            ),
                        ),
                        # Form card
                        ft.Container(
                            bgcolor="white",
                            border_radius=20,
                            padding=24,
                            margin=ft.margin.all(16),
                            shadow=ft.BoxShadow(blur_radius=12, color="#1E3A5F22"),
                            content=ft.Column(
                                spacing=16,
                                controls=[
                                    ft.Text(
                                        "بياناتك الشخصية",
                                        size=17, weight=ft.FontWeight.BOLD,
                                        color="#1E3A5F",
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                    name_field,
                                    type_dd,
                                    amount_field,
                                    error_text,
                                    ft.Container(height=4),
                                    ft.Container(
                                        alignment=ft.Alignment.CENTER,
                                        content=ft.ElevatedButton(
                                           "فتح الحساب",
                                            icon=ft.Icons.CHECK_CIRCLE,
                                            width=300, height=52,
                                            style=ft.ButtonStyle(
                                                bgcolor="#1E3A5F",
                                                color="white",
                                                shape=ft.RoundedRectangleBorder(radius=14),
                                                text_style=ft.TextStyle(
                                                    size=16,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                                elevation=4,
                                            ),
                                            on_click=on_submit,
                                        ),
                                    ),
                                    ft.Text(
                                        "بفتح الحساب، أنت توافق على الشروط والأحكام",
                                        size=11, color="#94A3B8",
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                ],
                            ),
                        ),
                        # Feature chips
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                controls=[
                                    feature_chip(ft.Icons.SECURITY,      "أمان 100%"),
                                    feature_chip(ft.Icons.FLASH_ON,      "فوري"),
                                    feature_chip(ft.Icons.SUPPORT_AGENT, "دعم 24/7"),
                                ],
                            ),
                        ),
                    ],
                )
            ],
        )

    # ─────────────────────────────────────────────────────────
    #  PAGE 2 — لوحة التحكم  route: /dashboard
    # ─────────────────────────────────────────────────────────

    def build_dashboard_view() -> ft.View:

        balance_ref = ft.Ref[ft.Text]()

        # ── Transfer dialog ──
        t_amount    = ft.TextField(
            label="مبلغ التحويل (دج)",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.Icons.PAYMENTS,
            border_radius=10, filled=True,
            text_align=ft.TextAlign.RIGHT,
        )
        t_recipient = ft.TextField(
            label="رقم حساب المستلم",
            prefix_icon=ft.Icons.PERSON_SEARCH,
            border_radius=10, filled=True,
            text_align=ft.TextAlign.RIGHT,
        )
        t_status = ft.Text(
            "", size=13, text_align=ft.TextAlign.CENTER, visible=False,
        )

        transfer_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "💸 تحويل مالي",
                text_align=ft.TextAlign.RIGHT,
                weight=ft.FontWeight.BOLD,
                color="#1E3A5F",
            ),
            content=ft.Column(
                tight=True, spacing=12,
                controls=[t_amount, t_recipient, t_status],
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def close_dialog(_e):
            transfer_dialog.open = False
            t_status.visible = False
            page.update()

        def confirm_transfer(_e):
            t_status.visible = False
            raw = (t_amount.value or "").replace(",", "").replace(" ", "")
            try:
                amount = float(raw)
            except ValueError:
                t_status.value  = "⚠️ يرجى إدخال مبلغ صحيح"
                t_status.color  = "#EF4444"
                t_status.visible = True
                page.update()
                return

            if amount <= 0:
                t_status.value  = "⚠️ المبلغ يجب أن يكون أكبر من صفر"
                t_status.color  = "#EF4444"
                t_status.visible = True
                page.update()
                return

            if not (t_recipient.value or "").strip():
                t_status.value  = "⚠️ يرجى إدخال رقم حساب المستلم"
                t_status.color  = "#EF4444"
                t_status.visible = True
                page.update()
                return

            if amount > state.balance:
                t_status.value = (
                    f"❌ رصيدك غير كافٍ. الرصيد الحالي: {fmt_dz(state.balance)}"
                )
                t_status.color  = "#EF4444"
                t_status.visible = True
                page.update()
                return

            # Deduct and refresh balance display
            state.balance -= amount
            if balance_ref.current:
                balance_ref.current.value = fmt_dz(state.balance)

            t_status.value   = f"✅ تم التحويل بنجاح! المبلغ: {fmt_dz(amount)}"
            t_status.color   = "#10B981"
            t_status.visible  = True
            t_amount.value    = ""
            t_recipient.value = ""
            page.update()

        # Wire dialog buttons AFTER defining callbacks
        transfer_dialog.actions = [
            ft.TextButton(
                "إلغاء",
                style=ft.ButtonStyle(color="#EF4444"),
                on_click=close_dialog,
            ),
            ft.ElevatedButton(
                "تأكيد التحويل",
                icon=ft.Icons.SEND,
                style=ft.ButtonStyle(
                    bgcolor="#1E3A5F", color="white",
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                on_click=confirm_transfer,
            ),
        ]

        def open_dialog(_e):
            transfer_dialog.open = True
            page.update()

        # ── Quick action button ──
        def quick_btn(icon, label, color, handler):
            return ft.GestureDetector(
                on_tap=handler,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                    controls=[
                        ft.Container(
                            content=ft.Icon(icon, color="white", size=26),
                            bgcolor=color,
                            border_radius=16,
                            width=60, height=60,
                            alignment=ft.Alignment.CENTER,
                            shadow=ft.BoxShadow(blur_radius=8, color=color + "66"),
                        ),
                        ft.Text(label, size=12, color="#374151",
                                text_align=ft.TextAlign.CENTER),
                    ],
                ),
            )

        async def go_news(_e):   await page.push_route("/news")
        async def go_offers(_e): await page.push_route("/offers")

        acc_emoji = {"جاري": "💳", "ادخار": "💰", "شباب": "🌟"}.get(
            state.account_type, "🏦"
        )

        notif_items = ft.Column(
            spacing=8,
            controls=[
                ft.Container(
                    content=ft.Text(n, size=12, text_align=ft.TextAlign.RIGHT),
                    bgcolor="#EFF6FF",
                    border_radius=10,
                    padding=ft.padding.symmetric(horizontal=14, vertical=10),
                    border=ft.border.all(1, "#BFDBFE"),
                )
                for n in NOTIFICATIONS
            ],
        )

        first_name = state.full_name.split()[0] if state.full_name else ""

        return ft.View(
            route="/dashboard",
            appbar=build_appbar(f"أهلاً، {first_name}"),
            bgcolor="#F1F5F9",
            padding=0,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Column(
                    spacing=0,
                    controls=[
                        # Balance card
                        ft.Container(
                            width=float("inf"),
                            padding=ft.padding.symmetric(vertical=28, horizontal=20),
                            gradient=ft.LinearGradient(
                                begin=ft.Alignment.TOP_RIGHT,
                                end=ft.Alignment.BOTTOM_LEFT,
                                colors=["#1E3A5F", "#0F172A"],
                            ),
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=6,
                                controls=[
                                    ft.Text(
                                        f"{acc_emoji} حساب {state.account_type}",
                                        size=14, color="#CBD5E1",
                                    ),
                                    ft.Text(
                                        fmt_dz(state.balance),
                                        ref=balance_ref,
                                        size=36,
                                        weight=ft.FontWeight.BOLD,
                                        color="white",
                                    ),
                                    ft.Text("رصيدك الحالي", size=12, color="#F4FF5F"),
                                    ft.Container(height=4),
                                    ft.Container(
                                        content=ft.Text(
                                            state.account_number,
                                            size=11, color="#67FF73", selectable=True,
                                        ),
                                        bgcolor="#0F172A",
                                        border_radius=8,
                                        padding=ft.padding.symmetric(
                                            horizontal=12, vertical=6),
                                    ),
                                ],
                            ),
                        ),

                        ft.Container(height=16),

                        # Quick actions card
                        ft.Container(
                            bgcolor="#FFFFFF",
                            border_radius=16,
                            padding=20,
                            margin=ft.margin.symmetric(horizontal=16),
                            shadow=ft.BoxShadow(blur_radius=8, color="#09144E"),
                            content=ft.Column(
                                spacing=16,
                                controls=[
                                    section_title("الإجراءات السريعة"),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                        controls=[
                                            quick_btn(ft.Icons.NEWSPAPER,
                                                      "آخر الأخبار",    "#3B82F6", go_news),
                                            quick_btn(ft.Icons.LOCAL_OFFER,
                                                      "العروض الحصرية", "#10B981", go_offers),
                                            quick_btn(ft.Icons.SEND,
                                                      "تحويل",          "#FF6E6E", open_dialog),
                                        ],
                                    ),
                                ],
                            ),
                        ),

                        ft.Container(height=16),

                        # Notifications card
                        ft.Container(
                            bgcolor="white",
                            border_radius=16,
                            padding=20,
                            margin=ft.margin.symmetric(horizontal=16),
                            shadow=ft.BoxShadow(blur_radius=8, color="#1E3A5F18"),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    section_title("🔔 الإشعارات"),
                                    notif_items,
                                ],
                            ),
                        ),

                        ft.Container(height=20),

                        # AlertDialog lives inside the view's control tree
                        transfer_dialog,
                    ],
                )
            ],
        )

    # ─────────────────────────────────────────────────────────
    #  PAGE 3 — الأخبار  route: /news
    # ─────────────────────────────────────────────────────────

    def build_news_view() -> ft.View:
        cards = ft.Column(
            spacing=14,
            controls=[
                ft.Container(
                    bgcolor="white",
                    border_radius=16,
                    padding=18,
                    shadow=ft.BoxShadow(blur_radius=6, color="#1E3A5F15"),
                    border=ft.border.only(right=ft.BorderSide(4, "#3B82F6")),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Container(
                                        content=ft.Text(item["date"], size=11,
                                                        color="#6B7280"),
                                        bgcolor="#F3F4F6",
                                        border_radius=6,
                                        padding=ft.padding.symmetric(
                                            horizontal=8, vertical=3),
                                    ),
                                    ft.Icon(ft.Icons.ARTICLE,
                                            color="#3B82F6", size=18),
                                ],
                            ),
                            ft.Text(
                                item["title"],
                                size=15, weight=ft.FontWeight.BOLD,
                                color="#1E3A5F",
                                text_align=ft.TextAlign.RIGHT,
                            ),
                            hdivider(),
                            ft.Text(
                                item["desc"],
                                size=13, color="#4B5563",
                                text_align=ft.TextAlign.RIGHT,
                            ),
                        ],
                    ),
                )
                for item in NEWS_DATA
            ],
        )

        return ft.View(
            route="/news",
            appbar=build_appbar("آخر الأخبار المالية", show_back=True),
            bgcolor="#F1F5F9",
            padding=16,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Container(
                            bgcolor="#EFF6FF",
                            border_radius=10,
                            padding=12,
                            margin=ft.margin.only(bottom=16),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.TRENDING_UP,
                                            color="#3B82F6", size=18),
                                    ft.Text(
                                        "  أحدث الأخبار الاقتصادية والمصرفية في الجزائر",
                                        size=13, color="#64748B",
                                    ),
                                ],
                            ),
                        ),
                        cards,
                        ft.Container(height=8),
                    ],
                )
            ],
        )

    # ─────────────────────────────────────────────────────────
    #  PAGE 4 — العروض التسويقية  route: /offers
    # ─────────────────────────────────────────────────────────

    def build_offers_view() -> ft.View:
        cards = ft.Column(
            spacing=14,
            controls=[
                ft.Container(
                    bgcolor=o["color"],
                    border_radius=20,
                    padding=20,
                    shadow=ft.BoxShadow(blur_radius=10, color=o["color"] + "55"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=14,
                        controls=[
                            ft.Column(
                                expand=True,
                                spacing=6,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                controls=[
                                    ft.Text(
                                        o["title"],
                                        size=15, weight=ft.FontWeight.BOLD,
                                        color=o["text_color"],
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                    ft.Text(
                                        o["desc"],
                                        size=12, color=o["text_color"],
                                        text_align=ft.TextAlign.RIGHT,
                                        opacity=0.88,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "احصل على العرض ←",
                                            size=12, color="#000000",
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        bgcolor="#FFFFFF33",
                                        border_radius=20,
                                        padding=ft.padding.symmetric(
                                            horizontal=14, vertical=6),
                                    ),
                                ],
                            ),
                            ft.Container(
                                content=ft.Icon(o["icon"],
                                                color="#686565", size=36),
                                bgcolor="#FFFFFF22",
                                border_radius=16,
                                width=64, height=64,
                                alignment=ft.Alignment.CENTER,
                            ),
                        ],
                    ),
                )
                for o in OFFERS_DATA
            ],
        )

        return ft.View(
            route="/offers",
            appbar=build_appbar("العروض الحصرية", show_back=True),
            bgcolor="#F1F5F9",
            padding=16,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Container(
                            bgcolor="#FFFBEB",
                            border_radius=10,
                            padding=12,
                            margin=ft.margin.only(bottom=16),
                            border=ft.border.all(1, "#FDE68A"),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.STAR, color="#F59E0B", size=18),
                                    ft.Text(
                                        "  عروض حصرية مصممة خصيصاً لعملائنا المميزين",
                                        size=13, color="#64748B",
                                    ),
                                ],
                            ),
                        ),
                        cards,
                        ft.Container(height=8),
                    ],
                )
            ],
        )

    # ─────────────────────────────────────────────────────────
    #  ROUTER — async on_route_change
    # ─────────────────────────────────────────────────────────

    async def route_change(_e: ft.RouteChangeEvent):
        route = page.route

        # Guard: redirect to /open if no active session
        if route in {"/dashboard", "/news", "/offers"} and not state.full_name:
            await page.push_route("/open")
            return

        builders = {
            "/":          build_open_account_view,
            "/open":      build_open_account_view,
            "/dashboard": build_dashboard_view,
            "/news":      build_news_view,
            "/offers":    build_offers_view,
        }

        builder = builders.get(route)
        if builder is None:
            await page.push_route("/open")
            return

        page.views.clear()
        page.views.append(builder())
        page.update()

    # ── Register handlers ──────────────────────────────────────
    page.on_route_change = route_change

    # Start the app
    await page.push_route("/open")


# ══════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    ft.run(main)
