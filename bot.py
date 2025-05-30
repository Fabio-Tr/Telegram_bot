from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Inserisci qui il token del tuo bot e il tuo Telegram user ID
BOT_TOKEN = '7697456185:AAHwcqUbva8jcFNkwK_58uUvHvBzxrSkSwM'
ADMIN_ID = 150361594  # Il tuo ID Telegram (ti spiego sotto come trovarlo)

# Dizionario per salvare i messaggi degli utenti
user_messages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Scrivi pure, il mio creatore ti risponderà qui.")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    user_messages[ADMIN_ID] = user_messages.get(ADMIN_ID, {})
    user_messages[ADMIN_ID][update.message.message_id] = user_id
    
    # Inoltra all'admin
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"Nuovo messaggio da @{update.message.from_user.username}:\n\n{text}")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        text = update.message.text
        target_user_id = None

        # Cerca l'ID dell'utente originale
        for mid, uid in user_messages.get(ADMIN_ID, {}).items():
            if update.message.reply_to_message.text.startswith("Nuovo messaggio") and str(mid) in update.message.reply_to_message.text:
                target_user_id = uid
                break
        
        if target_user_id:
            await context.bot.send_message(chat_id=target_user_id, text=f"Risposta dell'amministratore:\n\n{text}")
        else:
            await update.message.reply_text("Impossibile trovare l'utente originale.")
    else:
        await update.message.reply_text("Rispondi a un messaggio per rispondere all'utente.")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_message if lambda u: u.effective_user.id != ADMIN_ID else reply))

app.run_polling()
