import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# إعدادات الإدارة
TOKEN = '8651679774:AAGi946G4Xdz3IJn_InbhkCSmX6oiWTe4VU'
ADMIN_ID = "6647526076"

# هيكلية الخدمات مع الملصقات
SERVICES_DATA = {
    "برمجة": ["💻 تطوير بوتات", "🌐 تطبيقات ويب", "⚙️ أتمتة أنظمة", "📜 سكربتات خاصة", "🔌 برمجة API", "🛠 صيانة تقنية"],
    "تصميم": ["🆔 هوية بصرية", "🎨 تصميم UI/UX", "🖼 بنرات إعلانية", "📱 سوشيال ميديا", "🎥 موشن جرافيك", "✂️ تحرير فيديو"],
    "تسويق": ["📢 حملات إعلانية", "✍️ كتابة محتوى", "🔍 سيو SEO", "📊 إدارة منصات", "💡 استشارات أعمال", "📈 تحليل منافسين"],
    "أمن": ["🛡️ فحص ثغرات", "🔒 تأمين خوادم", "🧠 استشارات أمنية", "🔑 تشفير بيانات", "🧱 حماية مواقع", "📋 تدقيق أمني"],
    "ذكاء_اصطناعي": ["🤖 تحليل بيانات", "🧠 تدريب نماذج", "📊 استخراج بيانات", "⚡ أتمتة مهام", "🧹 تنظيف بيانات", "🔗 ربط أنظمة"],
    "استشارات": ["👔 استشارات تقنية", "🎯 تقييم مشاريع", "🗺 خطط تطوير", "📄 تقارير تقنية", "👥 إدارة فرق", "🎓 تدريب تقني"]
}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # دعم التتبع عبر الرابط (Deep Linking)
    args = context.args
    source = args[0] if args else "الزوار الأعزاء"
    
    keyboard = [[InlineKeyboardButton(f"{cat} ✨", callback_data=f"cat_{cat}")] for cat in SERVICES_DATA.keys()]
    await update.message.reply_text(
        f"مرحباً بك يا {source} في وكالة بيانانا للابتكار! 🚀\n"
        "نحن هنا لتحويل أفكارك إلى واقع تقني ملموس. 💡\n\n"
        "اختر قسماً لنبدأ رحلة النجاح:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("cat_"):
        cat = query.data.split("_")[1]
        keyboard = [[InlineKeyboardButton(item, callback_data=f"svc_{item}")] for item in SERVICES_DATA[cat]]
        keyboard.append([InlineKeyboardButton("🔙 العودة للرئيسية 🏠", callback_data="back")])
        await query.edit_message_text(f"خدمات قسم {cat} المميزة: 🌟", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query.data == "back":
        keyboard = [[InlineKeyboardButton(f"{cat} ✨", callback_data=f"cat_{cat}")] for cat in SERVICES_DATA.keys()]
        await query.edit_message_text("اختر قسماً للبدء رحلة الابتكار: 🚀", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif query.data.startswith("svc_"):
        service = query.data.split("_")[1]
        context.user_data['selected_service'] = service
        await query.edit_message_text(
            f"✅ لقد اخترت: {service}\n\n"
            "يرجى كتابة (تفاصيل طلبك + رقم هاتفك أو معرف تليجرام) لنتواصل معك في أسرع وقت: 📞"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'selected_service' in context.user_data:
        service = context.user_data['selected_service']
        details = update.message.text
        user = update.effective_user
        
        msg = (
            f"🚨 **طلب خدمة جديد في بيانانا** 🚨\n"
            f"━━━━━━━━━━━━━━\n"
            f"🛠 **الخدمة**: {service}\n"
            f"👤 **العميل**: {user.full_name}\n"
            f"🆔 **المعرف**: @{user.username if user.username else 'لا يوجد'}\n"
            f"📝 **التفاصيل**: {details}\n"
            f"━━━━━━━━━━━━━━\n"
            f"بيانانا للابتكار - نحن نصنع المستقبل! 🚀"
        )
        
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
        await update.message.reply_text("✅ تم استلام طلبك بنجاح! سيقوم فريقنا الإداري بالتواصل معك قريباً. 🤝")
        del context.user_data['selected_service']
    else:
        await update.message.reply_text("للبدء، يرجى الضغط على /start 🚀")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
        
