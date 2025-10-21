import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

# UPI ID
UPI_ID = "BHARATPE09895529437@yesbankltd"

# Subscription buttons
SUBSCRIPTION_OPTIONS = [
    [
        InlineKeyboardButton("✅ 1 Week – ₹199", callback_data="sub_1w"),
        InlineKeyboardButton("✅ 1 Month – ₹299", callback_data="sub_1m")
    ]
]

async def payment_info(update: Update, context: CallbackContext):
    """Send subscription options."""
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
    """Send payment options based on selected plan."""
    query = update.callback_query
    await query.answer()

    if query.data == "sub_1w":
        plan_name = "1 Week"
        amount = 199
        desc = "🔥 Sizzling tease!"
        direct_link = "https://www.upi.me/pay?pa=BHARATPE09895529437@yesbankltd&am=199&tn=VIP%20subscription"
    elif query.data == "sub_1m":
        plan_name = "1 Month"
        amount = 299
        desc = "💋 Endless heat!"
        direct_link = "https://www.upi.me/pay?pa=BHARATPE09895529437@yesbankltd&am=299&tn=VIP%20subscription"
    else:
        await query.edit_message_text("❌ Invalid plan selection.")
        return

    buttons = [
        [
            InlineKeyboardButton("📸 Pay via QR Code", callback_data=f"pay_qr_{amount}"),
            InlineKeyboardButton("🏦 Pay via UPI ID", callback_data=f"pay_upi_{amount}")
        ],
        [
            InlineKeyboardButton("💰 Pay Directly", url=direct_link)
        ]
    ]

    await query.edit_message_text(
        f"✅ *Selected Plan:* {plan_name} – ₹{amount}\n{desc}\nChoose payment method 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def handle_payment_method(update: Update, context: CallbackContext):
    """Handle QR code or UPI payments."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("pay_qr"):
        amount = data.split("_")[-1]
        # Correct path to QR code file
        qr_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "QR_Code.jpg")
        try:
            await query.message.reply_photo(
                photo=open(qr_path, "rb"),
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
            f"🏦 Send ₹{amount} to UPI ID `{UPI_ID}` and then send a screenshot for verification.",
            parse_mode="Markdown"
        )

    # Edit original message for confirmation
    await query.edit_message_text(
        "✅ Payment method selected. Send screenshot for verification.",
        parse_mode="Markdown"
    )
