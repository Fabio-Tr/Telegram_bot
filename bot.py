import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # Inserisci il tuo ID Telegram come variabile d'ambiente

# Memorizza gli ID degli utenti per le risposte
user_message_map = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Scrivi pure, ti risponderò qui 😊")

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    msg = f"Messaggio da @{user.username or user.first_name} (ID: {user.id}):{text}"

    # Salva il riferimento al messaggio
    user_message_map[update.message.message_id] = user.id

    # Inoltra all'admin
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

    await update.message.reply_text("Messaggio ricevuto! Ti risponderò appena possibile.")

async def handle_admin_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        original_text = update.message.reply_to_message.text
        lines = original_text.splitlines()
        user_line = next((line for line in lines if "ID:" in line), None)

        if user_line:
            user_id = int(user_line.split("ID:")[1].strip().replace(")", ""))
            await context.bot.send_message(chat_id=user_id, text=f"Risposta:
{update.message.text}")
            await update.message.reply_text("Risposta inviata all'utente.")
        else:
            await update.message.reply_text("Impossibile trovare l'ID utente.")
    else:
        await update.message.reply_text("Per rispondere a un utente, usa la funzione 'rispondi' a un suo messaggio.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.User(user_id=ADMIN_ID),
        handle_admin_response
    ))

    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & ~filters.User(user_id=ADMIN_ID),
        handle_user_message
    ))

    app.run_polling()

if __name__ == "__main__":
    main()
