# Telegram Bot con Python

Un semplice bot Telegram con supporto multi-utente, pronto per essere ospitato su Render.com

## ✅ Funzionalità
- Risponde ai messaggi di ogni utente
- Multiutente supportato
- Può essere facilmente esteso

## 🚀 Avvio locale

1. Clona la repo
2. Crea un file `.env` e copia il contenuto da `.env.example`
3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
4. Avvia il bot:
   ```bash
   python bot.py
   ```

## ☁️ Deploy su Render

1. Crea un nuovo Web Service su [https://render.com](https://render.com)
2. Collega la tua repo GitHub
3. Imposta:
   - **Start command**: `python bot.py`
   - **Environment**: aggiungi `BOT_TOKEN`

Fatto! 🎉
