from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def start_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💰 Join VIP Group", callback_data="payment_info")],
        [InlineKeyboardButton("❓ Need Help?", callback_data="help_info")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎉 *Welcome to Our Exclusive Service!* 🎉\n\n"
        "💰 *How It Works:*\n"
        "1️⃣ Choose a subscription plan.\n"
        "2️⃣ Complete your payment.\n"
        "3️⃣ Send proof of payment.\n"
        "4️⃣ Get access to the VIP group!\n\n"
        "✅ Use /payment to check payment details.\n"
        "🔹 Your payment will be reviewed by an admin before approval.\n\n"
        "👇 *Select an option below:*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
