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

HELP_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🆘 Help", callback_data="help_info")]
])

COUNTRY_OPTIONS = [
    [InlineKeyboardButton("🇮🇳 India", callback_data="country_India")],
    [InlineKeyboardButton("🇺🇸 USA", callback_data="country_USA")],
    [InlineKeyboardButton("🇬🇧 UK", callback_data="country_UK")],
    [InlineKeyboardButton("🇨🇦 Canada", callback_data="country_Canada")]
]

# -------------------------------
# Show Subscription Plans
# -------------------------------
async def payment_info(update: Update, context: CallbackContext):
    text = (
        "📜 *Dive into Your Naughty Subscription Plans!* 😈❤️\n\n"
        "1 Week – ₹199\n"
        "1 Month – ₹299\n\n"
        "👇 Choose your plan:"
    )
    await update.effective_message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(SUBSCRIPTION_OPTIONS)
    )

# -------------------------------
# Handle Plan Selection
# -------------------------------
async def handle_payment_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "sub_1w":
        plan_name, amount = "1 Week", 199
    else:
        plan_name, amount = "1 Month", 299

    user_id = query.from_user.id
    pending_transactions[user_id] = {"plan": plan_name, "amount": amount}

    upi_link = f"https://www.upi.me/pay?pa={UPI_ID}&am={amount}"

    buttons = [
        [InlineKeyboardButton("📸 Pay via QR Code", callback_data=f"pay_qr_{amount}")],
        [InlineKeyboardButton("💳 Pay Directly", url=upi_link)],
        [InlineKeyboardButton("🌍 Pay via PayPal / Card 💳", callback_data="pay_card")],
        [InlineKeyboardButton("🆘 Help", callback_data="help_info")]
    ]

    await query.edit_message_text(
        f"✅ *Selected Plan:* {plan_name} – ₹{amount}\nChoose payment method 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# -------------------------------
# Handle Payment Method
# -------------------------------
async def handle_payment_method(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("pay_qr"):
        qr_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "QR_Code.jpg")

        await query.message.reply_photo(
            photo=open(qr_path, "rb"),
            caption="📸 Scan this QR Code to pay.\nAfter payment, send screenshot.",
            reply_markup=HELP_BUTTON
        )

        await query.message.reply_text(
            "📤 Upload your screenshot:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📤 Upload Screenshot", callback_data="upload_screenshot")]
            ])
        )

    elif query.data == "pay_card":
        await query.message.reply_text(
            "🌍 Select your country for PayPal/Card payment:",
            reply_markup=InlineKeyboardMarkup(COUNTRY_OPTIONS)
        )

# -------------------------------
# Handle Country Selection
# -------------------------------
async def handle_country_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    country = query.data.split("_")[1]
    user_id = query.from_user.id

    if user_id in pending_transactions:
        pending_transactions[user_id]["country"] = country

    await query.message.reply_text(
        "✉️ Please enter your email address for PayPal/Card payment:"
    )

# -------------------------------
# Handle Email Input
# -------------------------------
async def handle_email_input(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    email = update.message.text

    if user_id in pending_transactions:
        pending_transactions[user_id]["email"] = email
        plan = pending_transactions[user_id]["plan"]
        amount = pending_transactions[user_id]["amount"]
        country = pending_transactions[user_id].get("country", "Not Provided")

        await context.bot.send_message(
            chat_id=-1002594045216,
            text=(
                f"🌍 *New PayPal/Card Payment Request*\n\n"
                f"👤 User: @{user.username if user.username else 'No Username'} ({user_id})\n"
                f"💰 Plan: {plan} – ₹{amount}\n"
                f"🌎 Country: {country}\n"
                f"✉️ Email: {email}"
            ),
            parse_mode="Markdown"
        )

    await update.message.reply_text(
        "📨 Details submitted! Admin will contact you shortly 💞"
    )

# -------------------------------
# Handle Screenshot Upload Prompt
# -------------------------------
async def handle_upload_screenshot(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "📤 Please send your payment screenshot as a photo."
    )
