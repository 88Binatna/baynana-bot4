import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# إعداد السجلات لمراقبة أداء البوت
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ضع هنا الـ Token الخاص بالبوت الآخر
TOKEN = "8651679774:AAGi946G4Xdz3IJn_InbhkCSmX6oiWTe4VU"

# لمسة بيانانا: قاموس الذكاء الاستراتيجي
STRATEGIC_KNOWLEDGE = {
    "سعر": "الاستثمار في بيانانا يضمن لك الجودة والاحترافية. هل نناقش تفاصيل ميزانيتك لنقدم لك عرضاً لا يُرفض؟",
    "تطوير": "نحن نصنع البرمجيات التي تخدم نمو أعمالك. ما هو النظام الذي تطمح لبنائه؟",
    "مبيعات": "أنا هنا لأكون مندوب مبيعاتك الذكي. دعنا نبدأ بزيادة أرباحك الآن عبر أتمتة عملياتك.",
    "شكرا": "العفو! نحن هنا لنرتقي بمشاريعك الرقمية إلى آفاق جديدة."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تحسين الواجهة بأزرار أكثر جاذبية
    keyboard = [
        [InlineKeyboardButton("🚀 خدماتنا الاستراتيجية", callback_data='services')],
        [InlineKeyboardButton("💎 طلب استشارة/شراء", callback_data='order')],
        [InlineKeyboardButton("📞 تواصل مع الإدارة", callback_data='contact')]
    ]
    await update.message.reply_text(
        "✨ **مرحباً بك في بيانانا (نسخة الإدارة المتطورة)**\n"
        "أنا لست مجرد مساعد، أنا ذكاء بيانانا الاصطناعي، هنا لأدير طلباتك باحترافية.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    responses = {
        'services': "📦 خدماتنا: تطوير تطبيقات، أنظمة ذكاء اصطناعي، وهندسة الأتمتة.",
        'order': "📝 أرسل تفاصيل مشروعك هنا، وسأقوم بتحليلها فوراً وإبلاغ الإدارة.",
        'contact': "📞 يمكنك مراسلتنا عبر الواتساب: https://wa.me/212771788862"
    }
    
    await query.edit_message_text(text=responses.get(query.data, "عذراً، لم أستطع فهم طلبك."))

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    # نظام الرد الذكي
    for key, val in STRATEGIC_KNOWLEDGE.items():
        if key in text:
            await update.message.reply_text(val)
            return
    await update.message.reply_text("أنا أحلل طلبك... كيف يمكنني مساعدتك في تطوير مشروعك اليوم؟")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()
    
