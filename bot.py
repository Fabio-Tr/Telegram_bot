import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Scrivi pure, ti risponderò qui 😊")

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    msg = f"Messaggio da @{user.username or user.first_name} (ID: {user.id}):\n{text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    await update.message.reply_text("Messaggio ricevuto! Ti risponderò appena possibile.")

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        original_text = update.message.reply_to_message.text
        lines = original_text.splitlines()
        user_line = next((line for line in lines if "ID:" in line), None)

        if user_line:
            try:
                user_id = int(user_line.split("ID:")[1].strip().replace(")", ""))
                await context.bot.send_message(chat_id=user_id, text=f"Risposta:\n{update.message.text}")
                await update.message.reply_text("Risposta inviata all'utente.")
            except Exception as e:
                await update.message.reply_text("Errore nel parsing dell'ID utente.")
        else:
            await update.message.reply_text("Impossibile trovare l'ID utente.")
    else:
        await update.message.reply_text("Usa 'rispondi' a un messaggio inoltrato per rispondere all'utente.")

async def rispondi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Uso: /rispondi <user_id> <messaggio>")
        return

    try:
        user_id = int(args[0])
        message_text = " ".join(args[1:])
        await context.bot.send_message(chat_id=user_id, text=message_text)
        await update.message.reply_text("Risposta inviata.")
    except Exception as e:
        await update.message.reply_text(f"Errore: {str(e)}")

async def background_task(app):
    while True:
        print("Esecuzione task di background...")
        await asyncio.sleep(30)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(background_task).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rispondi", rispondi))
    app.add_handler(MessageHandler(filters.TEXT & filters.User(user_id=ADMIN_ID), handle_admin_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.User(user_id=ADMIN_ID), handle_user_message))
    app.run_polling()

if __name__ == "__main__":
    main()
