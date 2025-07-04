import logging
from telegram import Update, Message
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_CHAT_ID
from matchmaker import Matchmaker

# Log sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Bot va matchmaking obyektlari
app = ApplicationBuilder().token(BOT_TOKEN).build()
matchmaker = Matchmaker()

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! /search buyrug‘i orqali suhbatdosh qidiring.")
    await forward_to_admin(update.message)

# /search komandasi
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await matchmaker.add_user(user_id, update)
    await forward_to_admin(update.message)

# /stop komandasi
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await matchmaker.remove_user(user_id)
    await update.message.reply_text("❌ Suhbat yakunlandi.")
    await forward_to_admin(update.message)

# Har qanday xabarlar (matn, rasm, ovoz, video)ni uzatish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    partner_id = matchmaker.get_partner(user_id)
    if partner_id:
        try:
            await context.bot.copy_message(
                chat_id=partner_id,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )
        except Exception:
            await update.message.reply_text("Xabar yuborib bo‘lmadi.")
    await forward_to_admin(update.message)

# Xabarni adminga uzatish
async def forward_to_admin(message: Message):
    try:
        await message.copy(chat_id=ADMIN_CHAT_ID)
    except Exception:
        pass

# Komandalar va handlerlar
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(MessageHandler(filters.TEXT | filters.VOICE | filters.PHOTO | filters.VIDEO, handle_message))

# Botni ishga tushirish
if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    app.run_polling()
