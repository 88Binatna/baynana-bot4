import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = "8651679774:AAGi946G4Xdz3IJn_InbhkCSmX6oiWTe4VU"
ADMIN_ID = "6647526076" # هذا هو رقمك الإداري الذي استخرجناه من 1000008740.jpg

# قائمة الطلبات الذكية
ORDER_MENU = {
    "1": "تصميم بوت تليجرام احترافي",
    "2": "أتمتة عمليات الوكالة",
    "3": "تصميم هوية بصرية",
    "4": "استشارة تقنية شاملة"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(f"{k}. {v}", callback_data=f"order_{k}")] for k, v in ORDER_MENU.items()]
    await update.message.reply_text("✨ مرحباً بك في بيانانا. اختر نوع الطلب لنبدأ التنفيذ:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("order_"):
        order_id = query.data.split("_")[1]
        service = ORDER_MENU.get(order_id)
        
        # رسالة للعميل
        await query.edit_message_text(f"✅ تم تسجيل طلبك ({service}). جاري المعالجة الرقمية...")
        
        # إرسال الإشعار للإدارة (لك أنت)
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 **طلب جديد من العميل!**\n\nالخدمة: {service}\nالاسم: {update.effective_user.full_name}"
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
    
