from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    """
    Shows help info about payment and how to contact the admin directly for support.
    """

    help_text = (
        "💡 *Help & Support*\n\n"
        "🪙 To see payment options, use /payment.\n"
        "📸 After making payment, send your screenshot or transaction ID here.\n"
        "⏳ Your payment will be checked and approved by an admin soon.\n\n"
        "💬 For any problem or delay, contact the admin directly using the button below 👇"
    )

    # Contact button
    contact_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 Contact Admin", url="https://t.me/aruna175")]
    ])

    if update.message:  # If user sends /help command
        await update.message.reply_text(
            help_text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=contact_button
        )

    elif update.callback_query:  # If user clicks Help button
        await update.callback_query.message.reply_text(
            help_text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=contact_button
        )
        await update.callback_query.answer()
