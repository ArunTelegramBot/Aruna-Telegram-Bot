from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def start_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💰 Join VIP Group", callback_data="payment_info")],
        [InlineKeyboardButton("❓ Need Help?", callback_data="help_info")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎉 *Hey gorgeous! Welcome to Aruna’s Spicy VIP Playground!* 🔥😘\n\n"
        "💦 *How to Unlock the Heat:*\n"
        "1️⃣ Pick your steamy subscription plan! 🌶️\n"
        "2️⃣ Make your naughty payment – quick & easy! 💸\n"
        "3️⃣ Send proof to join my secret world! 😏\n"
        "4️⃣ Get instant access to the VIP group for some fun! 😉\n\n"
        "✅ Use /payment for all the juicy payment details.\n"
        "🔥 Your payment gets a sexy review by me before you’re in!\n\n"
        "👇 *Tap below to dive into the temptation NOW:*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
