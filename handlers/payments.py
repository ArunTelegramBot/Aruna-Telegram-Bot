from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext
from verification import get_callback_handlers
import logging

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# UPI ID
UPI_ID = "BHARATPE09895529437@yesbankltd"

# Subscription buttons
SUBSCRIPTION_OPTIONS = [
    [
        InlineKeyboardButton("✅ 1 Week – ₹199", callback_data="sub_1w"),
        InlineKeyboardButton("✅ 1 Month – ₹299", callback_data="sub_1m")
    ]
]

# Command: /payment
async def payment_info(update: Update, context: CallbackContext):
    query = update.callback_query
    message = update.effective_message or (query.message if query else None)

    text = (
        "📜 *Dive into Aruna’s Naughty Pleasure Plans!* 😈❤️\n\n"
        "✅ *1 Week – ₹199 (~₹28/day):* A sizzling tease to ignite your desires! 🔥\n\n"
        "✅ *1 Month – ₹299 (~₹10/day):* Endless heat & savings to drive you wild! 💋\n\n"
        "👇 *Tap below to start your pleasure journey:*"
    )

    markup = InlineKeyboardMarkup(SUBSCRIPTION_OPTIONS)

    if query:
        await query.answer()
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=markup)
    elif message:
        await message.reply_text(text, parse_mode="Markdown", reply_markup=markup)
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=markup)


# Handle plan selection
async def handle_payment_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    if not query:
        return

    await query.answer()

    if query.data == "sub_1w":
        plan_name = "1 Week"
        amount = 199
        description = "🔥 A sizzling tease to ignite your desires!"
        direct_pay_link = "https://www.upi.me/pay?pa=BHARATPE09895529437@yesbankltd&am=199&tn=VIP%20subscription"
    elif query.data == "sub_1m":
        plan_name = "1 Month"
        amount = 299
        description = "💋 Endless heat & savings to drive you wild!"
        direct_pay_link = "https://www.upi.me/pay?pa=BHARATPE09895529437@yesbankltd&am=299&tn=VIP%20subscription"
    else:
        await query.edit_message_text("❌ Invalid plan selection. Please try again.")
        return

    # Payment buttons
    payment_methods = [
        [
            InlineKeyboardButton("📸 Pay via QR Code", callback_data=f"pay_qr_{amount}"),
            InlineKeyboardButton("🏦 Pay via UPI ID", callback_data=f"pay_upi_{amount}")
        ],
        [
            InlineKeyboardButton("💰 Pay Directly (via UPI App)", url=direct_pay_link)
        ]
    ]

    await query.edit_message_text(
        f"✅ *Selected Plan:* {plan_name} – ₹{amount}\n\n"
        f"{description}\n\n"
        "Choose your preferred payment method below 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(payment_methods)
    )


# Handle payment buttons
async def handle_payment_method(update: Update, context: CallbackContext):
    query = update.callback_query
    if not query:
        return

    await query.answer()
    data = query.data

    if data.startswith("pay_qr"):
        try:
            await query.message.reply_photo(
                photo=open("assets/QR_Code.jpg", "rb"),
                caption="📸 *Scan this QR Code to make the payment.*\n\n"
                        "After payment, send a screenshot for verification. 😘",
                parse_mode="Markdown"
            )
        except FileNotFoundError:
            await query.message.reply_text(
                "❌ QR Code image not found. Please contact support.",
                parse_mode="Markdown"
            )
    elif data.startswith("pay_upi"):
        amount = data.split("_")[-1]
        await query.message.reply_text(
            f"🏦 *Manual Payment via UPI*\n\n"
            f"Send ₹{amount} to the following UPI ID:\n"
            f"`{UPI_ID}`\n\n"
            "After payment, send a screenshot for verification. 😘",
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text("❌ Invalid payment method. Please try again.")
        return

    try:
        await query.edit_message_text(
            "✅ *Payment method selected successfully!*\n\n"
            "Follow the instructions above and send proof of payment to get VIP access. 🔥",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error editing confirmation message: {e}")


# Main function
def main():
    TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot token
    app = ApplicationBuilder().token(TOKEN).build()

    # Payment handlers
    app.add_handler(CommandHandler("payment", payment_info))
    app.add_handler(CallbackQueryHandler(handle_payment_selection, pattern="^sub_"))
    app.add_handler(CallbackQueryHandler(handle_payment_method, pattern="^pay_"))

    # Verification handlers (from verification.py)
    for handler in get_callback_handlers():
        app.add_handler(handler)

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
