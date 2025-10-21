async def handle_payment_method(update: Update, context: CallbackContext):
    """Handle QR code or UPI payments."""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("pay_qr"):
        amount = data.split("_")[-1]
        # Use the relative path you provided (assuming it's relative to the script's directory)
        qr_path = os.path.join(os.path.dirname(__file__), "assets", "QR_Code.jpg")
        try:
            await query.message.reply_photo(
                photo=open(qr_path, "rb"),
                caption="📸 *Scan this QR Code to make the payment.*\n\n"
                        "After payment, send a screenshot for verification. 😘",
                parse_mode="Markdown"
            )
        except FileNotFoundError:
            await query.message.reply_text(
                "❌ QR Code image not found. Please contact support or ensure the file exists at 'assets/QR_Code.jpg'.",
                parse_mode="Markdown"
            )
        except Exception as e:
            await query.message.reply_text(
                f"❌ Error loading QR Code: {str(e)}. Please contact support.",
                parse_mode="Markdown"
            )
    elif data.startswith("pay_upi"):
        amount = data.split("_")[-1]
        # Generate UPI payment link
        link = f"https://www.upi.me/pay?pa={UPI_ID}&am={amount}&tn=VIP%20subscription"
        # Send a message with a clickable UPI link button
        buttons = [[InlineKeyboardButton("💳 Pay via UPI App", url=link)]]
        await query.message.reply_text(
            f"🏦 Click below to pay ₹{amount} via UPI.\nAfter payment, send a screenshot for verification.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # Edit original message for confirmation
    await query.edit_message_text(
        "✅ Payment method selected. Send screenshot for verification.",
        parse_mode="Markdown"
    )
