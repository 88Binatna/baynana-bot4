import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = "8651679774:AAGi946G4Xdz3IJn_InbhkCSmX6oiWTe4VU"

# قائمة الطلبات الذكية التي يديرها البوت
ORDER_MENU = {
    "1": "تصميم بوت تليجرام احترافي",
    "2": "أتمتة عمليات الوكالة",
    "3": "تصميم هوية بصرية",
    "4": "استشارة تقنية شاملة"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # قائمة الطلبات تظهر للعميل فوراً كقائمة خيارات
    keyboard = [[InlineKeyboardButton(f"{k}. {v}", callback_data=f"order_{k}")] for k, v in ORDER_MENU.items()]
    await update.message.reply_text(
        "✨ **بيانانا في خدمتك!**\nأنا المسؤول عن إدارة مشاريعك. اختر نوع الطلب لنبدأ التنفيذ:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("order_"):
        order_id = query.data.split("_")[1]
        selected_service = ORDER_MENU.get(order_id)
        # البوت الآن "مسؤول" ويطلب تفاصيل لإغلاق الصفقة
        await query.edit_message_text(
            f"✅ لقد اخترت: {selected_service}.\n\n"
            "لأتمم المسؤولية، أرسل لي تفاصيل مشروعك أو ميزانيتك، وسأقوم بتحليلها فوراً وإبلاغ الإدارة."
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    
    # البوت يجادل ويجيب على الاستفسارات كمدير
    if any(word in user_text for word in ["سعر", "بكم"]):
        await update.message.reply_text("الجودة هي عنواننا. أخبرني بتفاصيل طلبك، وسأقدم لك عرضاً يضمن لك أعلى عائد استثماري.")
    else:
        await update.message.reply_text("أنا أدير هذه المحادثة... هل لديك استفسار محدد بخصوص خدماتنا؟")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("--- بيانانا: نظام الإدارة الذاتي يعمل بكامل طاقته ---")
    app.run_polling()
    
