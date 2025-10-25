import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

UPI_ID = "BHARATPE09895529437@yesbankltd"

SUBSCRIPTION_OPTIONS = [
    [
        InlineKeyboardButton("✅ 1 Week – ₹199", callback_data="sub_1w"),
        InlineKeyboardButton("✅ 1 Month – ₹299", callback_data="sub_1m")
    ]
]

pending_transactions = {}

async def payment_info(update: Update, context: CallbackContext):
    text = (
        "📜 *Dive into Aruna’s Naughty Pleasure Plans!* 😈❤️\n\n"
        "✅ *1 Week – ₹199 (~₹28/day)*: A sizzling tease!\n"
        "✅ *1 Month – ₹299 (~₹10/day)*: Endless heat & savings!\n\n"
        "👇 Tap below to start:"
    )
    markup = InlineKeyboardMarkup(SUBSCRIPTION_OPTIONS)
    message = update.effective_message or update.message
    await message.reply_text(text, parse_mode="Markdown", reply_markup=markup)

async def handle_payment_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "sub_1w":
        plan_name, amount, desc = "1 Week", 199, "🔥 Sizzling tease!"
    elif query.data == "sub_1m":
        plan_name, amount, desc = "1 Month", 299, "💋 Endless heat!"
    else:
        await query.edit_message_text("❌ Invalid plan selection.")
        return

    user_id = query.from_user.id
    pending_transactions[user_id] = {"plan": plan_name, "amount": amount}

    direct_link = f"https://www.upi.me/pay?pa={UPI_ID}&am={amount}&tn=VIP%20subscription"

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
    query = update.callback_query
    await query.answer()
    data = query.data
    amount = data.split("_")[-1]

    if data.startswith("pay_qr"):
        qr_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "QR_Code.jpg")
        try:
            await query.message.reply_photo(
                photo=open(qr_path, "rb"),
                caption="📸 Scan this QR Code to make the payment.\nAfter payment, send a screenshot for verification. 😘",
            )
        except Exception as e:
            await query.message.reply_text(f"❌ Error loading QR Code: {str(e)}")
    elif data.startswith("pay_upi"):
        link = f"https://www.upi.me/pay?pa={UPI_ID}&am={amount}&tn=VIP%20subscription"
        buttons = [[InlineKeyboardButton("💳 Pay via UPI App", url=link)]]
        await query.message.reply_text(
            f"🏦 Click below to pay ₹{amount} via UPI.\nAfter payment, send a screenshot for verification.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # Upload button for both methods
    await query.message.reply_text(
        "📤 Upload your payment screenshot here for verification:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📤 Upload Screenshot", callback_data="upload_screenshot")]])
    )

async def handle_upload_screenshot(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "📤 Please send your payment screenshot as a photo. It will be processed for verification."
    )
