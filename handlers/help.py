from telegram import Update
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    """Provides information about payment and displays Arun's contact for support."""
    help_text = (
    "💡 *Help & Support*\n\n"
    "🔹 To check payment details, use /payment.\n"
    "🔹 To submit proof of payment, send an image or transaction ID.\n"
    "🔹 Your payment will be reviewed by an admin before approval.\n"
    "🔹 If you need assistance, contact an Admin directly:\n"
    "📩 [@aruna175](https://t.me/aruna175)"
)



    if update.message:  # Se for chamado via comando /help
        await update.message.reply_text(help_text, parse_mode="Markdown", disable_web_page_preview=True)
    elif update.callback_query:  # Se for chamado via botão
        await update.callback_query.message.reply_text(help_text, parse_mode="Markdown", disable_web_page_preview=True)
        await update.callback_query.answer()

