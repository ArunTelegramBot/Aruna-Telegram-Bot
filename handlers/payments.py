from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

SUBSCRIPTION_OPTIONS = [
    [InlineKeyboardButton("✅ 1 Week – ₹199", callback_data="sub_1w"),
     InlineKeyboardButton("✅ 1 Month – ₹299", callback_data="sub_1m")]
]

PAYMENT_METHODS = [
    [InlineKeyboardButton("📸 Pay via QR Code", callback_data="pay_qr"),
     InlineKeyboardButton("🏦 Pay via UPI ID", callback_data="pay_upi")]
]

async def payment_info(update: Update, context: CallbackContext):
    """Show the available subscription plans."""
    # Handle both command and callback query scenarios
    query = update.callback_query
    message = update.effective_message or (query.message if query else None)
    
    text = (
        "📜 *Dive into Aruna’s Naughty Pleasure Plans!* 😈❤️\n\n"
        "\n"
        "✅ *1 Week – ₹199 (~₹28/day):*\n"
        "   A sizzling tease to ignite your desires! 🔥\n\n"
        "\n"
        "✅ *1 Month – ₹299 (~₹10/day):*\n"
        "   Endless heat & savings to drive you wild! 💋\n\n"
        "\n"
        "👇 *Tap below to unleash the lusty fun NOW:*"
    )
    
    if query:
        await query.answer()
        # Edit the existing message if this is a callback
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(SUBSCRIPTION_OPTIONS)
        )
    elif message:
        # If called as a command (e.g., /payment), reply to the message
        await message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(SUBSCRIPTION_OPTIONS)
        )
    else:
        # Fallback: Send a new message
        await update.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(SUBSCRIPTION_OPTIONS)
        )

async def handle_payment_selection(update: Update, context: CallbackContext):
    """Show payment methods after the user selects a plan."""
    query = update.callback_query
    if not query:
        return  # Ignore if not a callback query

    await query.answer()

    # Determine the selected plan with updated prices and descriptions
    if query.data == "sub_1w":
        plan_text = (
            "✅ *Selected Plan:* 1 Week – ₹199 (~₹28/day)\n\n"
            "🔥 A sizzling tease to ignite your desires!\n\n"
        )
    elif query.data == "sub_1m":
        plan_text = (
            "✅ *Selected Plan:* 1 Month – ₹299 (~₹10/day)\n\n"
            "💋 Endless heat & savings to drive you wild!\n\n"
        )
    else:
        await query.edit_message_text("❌ Invalid plan selection. Please try again.")
        return

    # Edit the message to show payment methods
    await query.edit_message_text(
        f"{plan_text}\nChoose your preferred payment method:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(PAYMENT_METHODS)
    )

async def handle_payment_method(update: Update, context: CallbackContext):
    """Handle the payment action based on user choice."""
    query = update.callback_query
    if not query:
        return  # Ignore if not a callback query

    await query.answer()

    if query.data == "pay_qr":
        # Send the QR code photo as a new message
        try:
            await query.message.reply_photo(
                photo=open("assets/QR_Code.jpg", "rb"),  # Ensure this file exists in your project
                caption="📸 *Scan this QR Code to make the payment.*\n\n"
                        "After payment, send a screenshot for verification. An admin will review it soon! 😘",
                parse_mode="Markdown"
            )
        except FileNotFoundError:
            await query.message.reply_text(
                "❌ QR Code image not found. Please contact support for payment details.",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error sending QR code: {e}")
            await query.message.reply_text(
                "❌ An error occurred while loading the QR code. Try UPI or contact support.",
                parse_mode="Markdown"
            )
    elif query.data == "pay_upi":
        # Send UPI details as a new message
        await query.message.reply_text(
            "🏦 *Manual Payment via UPI*\n\n"
            "Send your payment to the following UPI ID:\n"
            "`> A:BHARATPE09895529437@yesbankltd`\n\n"
            "After payment, send a screenshot for verification. An admin will review it soon! 😘",
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text("❌ Invalid payment method. Please try again.")
        return

    # Edit the original query message to confirm selection (optional, for better UX)
    try:
        await query.edit_message_text(
            "✅ *Payment method selected successfully!*\n\n"
            "Follow the instructions above and send proof of payment to get VIP access. 🔥"
        )
    except Exception as e:
        print(f"Error editing confirmation message: {e}")
        # Fallback: Send a new confirmation message
        await query.message.reply_text(
            "✅ Payment method selected! Check the details above. 💸",
            parse_mode="Markdown"
        )
