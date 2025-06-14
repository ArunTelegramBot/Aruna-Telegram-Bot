from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, CallbackQueryHandler, filters

# Admin Group ID
ADMIN_GROUP_ID = -1002594045216  # Replace with the real admin group ID
GROUP_LINK = "https://t.me/+kbMWRA7RG0FiZTM1"  # Replace with the real group link ID

# Store pending transactions
pending_transactions = {}

async def verify_payment(update: Update, context: CallbackContext):
    """Handles payment verification via screenshot upload."""
    user = update.message.from_user
    user_id = user.id

    if update.message.photo:
        # User sent a screenshot
        await update.message.reply_text(
            "📸 *Payment screenshot received!*\n"
            "Sending to admin for review...",
            parse_mode="Markdown"
        )

        # Get the highest quality image
        photo = update.message.photo[-1]
        file = await photo.get_file()

        # Store transaction for reference
        pending_transactions[user_id] = file.file_id

        # Send the image to the admin group
        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(
            chat_id=ADMIN_GROUP_ID,
            photo=file.file_id,
            caption=(
                f"📢 *New payment pending approval!*\n"
                f"👤 *User:* @{user.username} ({user_id})\n"
                "Admin, please review the payment manually."
            ),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

async def handle_approval(update: Update, context: CallbackContext):
    """Handles admin approval or rejection of payment."""
    query = update.callback_query
    action, user_id = query.data.split("_")
    user_id = int(user_id)

    if action == "approve":
        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ *Your payment has been approved!*\n"
                 f"Here is your access link: {GROUP_LINK}",
            parse_mode="Markdown"
        )
        try:
            await query.edit_message_text("✅ Payment approved.")
        except Exception as e:
            print(f"Warning: Tried to edit a deleted message. {e}") 
    
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ *Your payment was not approved.*\n"
                 "Please contact support for more details.",
            parse_mode="Markdown"
        )
        try:
            await query.edit_message_text("❌ Payment rejected.")
        except Exception as e:
            print(f"Warning: Tried to edit a deleted message. {e}")  # Apenas loga o erro

    # Remove from pending transactions
    pending_transactions.pop(user_id, None)

    await query.answer()



# Handlers
verification_handler = MessageHandler(filters.PHOTO, verify_payment)
approval_handler = CallbackQueryHandler(handle_approval, pattern="^(approve|reject)_")

def get_callback_handlers():
    return [verification_handler, approval_handler]
