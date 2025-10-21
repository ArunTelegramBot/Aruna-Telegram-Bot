from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext
from verification import get_callback_handlers  # <-- Make sure both files are same folder
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

UPI_ID = "BHARATPE09895529437@yesbankltd"

SUBSCRIPTION_OPTIONS = [
    [InlineKeyboardButton("✅ 1 Week – ₹199", callback_data="sub_1w"),
     InlineKeyboardButton("✅ 1 Month – ₹299", callback_data="sub_1m")]
]

async def payment_info(update: Update, context: CallbackContext):
    text = (
        "📜 *Dive into Aruna’s Naughty Pleasure Plans!* 😈❤️\n\n"
        "✅ *1 Week – ₹199 (~₹28/day):* A sizzling tease!\n"
        "✅ *1 Month – ₹299 (~₹10/day):* Endless heat & savings!\n\n"
        "👇 Tap below to start:"
    )
    markup = InlineKeyboardMarkup(SUBSCRIPTION_OPTIONS)
    message = update.effective_message or update.message
    await message.reply_text(text, parse_mode="Markdown", reply_markup=markup)

async def handle_payment_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == "sub_1w":
        plan_name = "1 Week"; amount = 199; desc = "🔥 Sizzling tease!"
        link = "https://www.upi.me/pay?pa=BHARATPE09895529437@yesbankltd&am=199&tn=VIP%20subscription"
    elif query.data == "sub_1m":
        plan_name = "1 Month"; amount = 299; desc = "💋 Endless heat!"
        link = "https://www.upi.me/pay?pa=BHARATPE09895529437@yesbankltd&am=299&tn=VIP%20subscription"
    else:
        await query.edit_message_text("❌ Invalid selection."); return

    buttons = [
        [InlineKeyboardButton("📸 Pay via QR Code", callback_data=f"pay_qr_{amount}"),
         InlineKeyboardButton("🏦 Pay via UPI ID", callback_data=f"pay_upi_{amount}")],
        [InlineKeyboardButton("💰 Pay Directly", url=link)]
    ]
    await query.edit_message_text(f"✅ *{plan_name} – ₹{amount}*\n{desc}\nChoose a payment method 👇",
                                  parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))

async def handle_payment_method(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("pay_qr"):
        await query.message.reply_text("Send your QR payment screenshot for verification.")
    elif data.startswith("pay_upi"):
        amount = data.split("_")[-1]
        await query.message.reply_text(f"Send ₹{amount} to UPI ID `{UPI_ID}` and then send screenshot for verification.")
    await query.edit_message_text("✅ Payment method selected. Send screenshot for verification.", parse_mode="Markdown")

def main():
    TOKEN = "YOUR_BOT_TOKEN_HERE"
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("payment", payment_info))
    app.add_handler(CallbackQueryHandler(handle_payment_selection, pattern="^sub_"))
    app.add_handler(CallbackQueryHandler(handle_payment_method, pattern="^pay_"))

    # Add verification.py handlers
    for handler in get_callback_handlers():
        app.add_handler(handler)

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
