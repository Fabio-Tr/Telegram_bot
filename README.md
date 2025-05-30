# Telegram Bot con Risposte Admin

Un bot Telegram multiutente dove l'amministratore può ricevere e rispondere ai messaggi.

## ✅ Funzionalità
- Gli utenti scrivono → il messaggio viene inoltrato all’admin
- L’admin risponde → la risposta viene inviata all’utente
- Supporta più utenti contemporaneamente

## 🚀 Avvio locale

1. Clona la repo
2. Crea un file `.env` copiando `.env.example`
3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
4. Avvia il bot:
   ```bash
   python bot.py
   ```

## ☁️ Deploy su Render

1. Crea un Web Service su [https://render.com](https://render.com)
2. Collega la repo GitHub
3. Imposta:
   - **Start command**: `python bot.py`
   - **Environment**: aggiungi `BOT_TOKEN` e `ADMIN_ID`

## 🔐 Dove trovare il tuo ADMIN_ID

Scrivi a questo bot: [@userinfobot](https://t.me/userinfobot) e otterrai il tuo ID.
