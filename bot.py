import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Memoria in RAM degli utenti che hanno scritto
user_messages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Scrivi pure il tuo messaggio.")

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if user.id == ADMIN_ID and update.message.reply_to_message:
        # Risposta dell'admin a un messaggio utente
        replied_text = update.message.reply_to_message.text
        target_id = None
        for uid, msg in user_messages.items():
            if msg == replied_text:
                target_id = uid
                break
        if target_id:
            await context.bot.send_message(chat_id=target_id, text=text)
            await update.message.reply_text("Messaggio inviato all'utente.")
        else:
            await update.message.reply_text("Utente non trovato.")
        return

    # Salva l'ultimo messaggio ricevuto da ogni utente
    user_messages[user.id] = text

    msg = f"Messaggio da @{user.username or user.first_name} (ID: {user.id}):\n{text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_to_admin))

    print("Bot avviato...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
