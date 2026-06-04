import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# تفعيل سجلات المتابعة للتحكم الإداري
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# الترحيب الذكي بـ "اللهجة البيضاء"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="أهلاً بك في وكالة بيانانا. معك مساعد بيانانا الذكي. كيف يمكنني مساعدتك في تطوير أعمالك اليوم؟"
    )

# المنطق الأساسي للرد على العملاء
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # هنا سيتم لاحقاً ربط المنطق الذكي لتحليل الطلب
    response = f"وصلني طلبك بخصوص: '{user_text}'. سأقوم برفعه للإدارة فوراً."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

if __name__ == '__main__':
    # ضع هنا الـ Token الخاص بك
    TOKEN = '8651679774:AAGi946G4Xdz3IJn_InbhkCSmX6oiWTe4VU'
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    application.run_polling()
    
