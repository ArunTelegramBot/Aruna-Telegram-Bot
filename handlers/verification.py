from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, CallbackQueryHandler, filters
from .payments import pending_transactions  # Import the dict to know plan/amount

ADMIN_GROUP_ID = -1002594045216  # Replace with your admin group ID
GROUP_LINK = "https://t.me/+kbMWRA7RG0FiZTM1"  # Replace with your VIP group link

async def verify_payment(update: Update, context: CallbackContext):
    """Handles payment verification via screenshot upload."""
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if update.message.photo:
        # Get highest quality photo
        photo = update.message.photo[-1]
        file = await photo.get_file()

        # Get user's plan
        plan_info = pending_transactions.get(user_id, {"plan": "Unknown", "amount": "Unknown"})
        plan_name = plan_info["plan"]
        amount = plan_info["amount"]

        # Inline buttons for admin
        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send screenshot to admin
        await context.bot.send_photo(
            chat_id=ADMIN_GROUP_ID,
            photo=file.file_id,
            caption=(
                f"📢 *New payment pending approval!*\n"
                f"👤 User: @{username} ({user_id})\n"
                f"💰 Plan: {plan_name} – ₹{amount}"
            ),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def handle_approval(update: Update, context: CallbackContext):
    """Handle admin approve/reject."""
    query = update.callback_query
    action, user_id = query.data.split("_")
    user_id = int(user_id)

    if action == "approve":
        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ Your payment has been approved!\nAccess link: {GROUP_LINK}"
        )
        await query.edit_message_text("✅ Payment approved.")
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Your payment was rejected. Contact support for details."
        )
        await query.edit_message_text("❌ Payment rejected.")

    # Remove from pending transactions
    pending_transactions.pop(user_id, None)
    await query.answer()

# Handlers
verification_handler = MessageHandler(filters.PHOTO, verify_payment)
approval_handler = CallbackQueryHandler(handle_approval, pattern="^(approve|reject)_")

def get_callback_handlers():
    return [verification_handler, approval_handler]
