import time
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
from flask import Flask
from multiprocessing import Process

# Bot Token
TOKEN = "8169420460:AAEs6bEoqdSSqchcpRa-y0h0ercCk3exZ3w"

# Mandatory channel for verification
MANDATORY_CHANNEL = "@GODPREDICTION69"

# Displayed channels (without removed channel)
CHANNELS = {
    "🎊𝙈𝙊𝘿 𝘾𝙃𝘼𝙉𝙉𝙀𝙇🎊": "https://t.me/+xVHt9WSvAsw4YzY1",
    "⏳𝙋𝙍𝙀𝘿𝙄𝘾𝙏𝙄𝙊𝙉 𝘾𝙃𝘼𝙉𝙉𝙀𝙇⏳": f"https://t.me/{MANDATORY_CHANNEL[1:]}",
    "👽2𝙉𝘿 𝙈𝙊𝘿 𝘾𝙃𝘼𝙉𝙉𝙀𝙇👽": "https://t.me/+RBaWtMQsKXU3MTJl",
}

# Image URLs for results
RESULT_IMAGES = {
    "BIG": "https://t.me/PREDICTIONZRX/10",
    "SMALL": "https://t.me/PREDICTIONZRX/11",
    "RED": "https://t.me/PREDICTIONZRX/13",
    "GREEN": "https://t.me/PREDICTIONZRX/12",
}

# Store last period results
last_period_results = {}

# Get current period number
def get_period():
    now = datetime.utcnow()
    total_minutes = now.hour * 60 + now.minute
    return now.strftime("%Y%m%d") + "1000" + str(10001 + total_minutes)

# Get remaining time in seconds
def get_remaining_time():
    now = datetime.utcnow()
    remaining_seconds = 60 - now.second
    return remaining_seconds

# Check if user is a member of @GODPREDICTION69
async def is_user_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(MANDATORY_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# Send "Join Channels" message
async def send_join_message(update):
    keyboard = [[InlineKeyboardButton(name, url=link)] for name, link in CHANNELS.items()]
    keyboard.append([InlineKeyboardButton("✔️ 𝗝𝗢𝗜𝗡𝗘𝗗", callback_data="joined")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        "🚀 <b>𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐭𝐡𝐞 𝐖𝐢𝐧𝐠𝐨 1-𝐌𝐢𝐧𝐮𝐭𝐞 𝐁𝐨𝐭!</b>\n\n"
        "🔴 <b>𝗙𝗼𝗹𝗹𝗼𝘄 𝘁𝗵𝗲𝘀𝗲 𝘀𝘁𝗲𝗽𝘀 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲:</b>\n"
        "1️⃣ 𝙅𝙤𝙞𝙣 𝙩𝙝𝙚 <b>𝐌𝐔𝐒𝐓 𝐉𝐎𝐈𝐍</b> 𝙘𝙝𝙖𝙣𝙣𝙚𝙡 📢\n"
        "2️⃣ 𝘾𝙡𝙞𝙘𝙠 𝙩𝙝𝙚 '✅ 𝙅𝙊𝙄𝙉𝙀𝘿' 𝙗𝙪𝙩𝙩𝙤𝙣\n\n"
        "🔒 <b>𝘼𝙘𝙘𝙚𝙨𝙨 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙜𝙧𝙖𝙣𝙩𝙚𝙙 𝙤𝙣𝙡𝙮 𝙖𝙛𝙩𝙚𝙧 𝙫𝙚𝙧𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣!</b>"
    )

    await update.message.reply_text(message, parse_mode="HTML", reply_markup=reply_markup)

# /start command
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if await is_user_member(user_id, context):
        await update.message.reply_text(
            "✅ 𝙔𝙤𝙪 𝙖𝙧𝙚 𝙫𝙚𝙧𝙞𝙛𝙞𝙚𝙙! 𝙏𝙖𝙥 '🎯 𝙂𝙀𝙏 𝙍𝙀𝙎𝙐𝙇𝙏' 𝙩𝙤 𝙧𝙚𝙘𝙚𝙞𝙫𝙚 𝙒𝙞𝙣𝙜𝙤 𝙧𝙚𝙨𝙪𝙡𝙩𝙨.", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 𝙂𝙀𝙏 𝙍𝙀𝙎𝙐𝙇𝙏", callback_data="predict")]])
        )
    else:
        await send_join_message(update)

# Handle "JOINED ✅" button
async def joined_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if await is_user_member(user_id, context):
        await query.message.edit_text(
            "🎉 <b>𝙑𝙚𝙧𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡!</b>\n\n"
            "✅ 𝗬𝗼𝘂 𝗰𝗮𝗻 𝗻𝗼𝘄 𝗴𝗲𝘁 𝗪𝗶𝗻𝗴𝗼 𝗿𝗲𝘀𝘂𝗹𝘁𝘀.\n"
            "🔮 𝘾𝙡𝙞𝙘𝙠 𝙩𝙝𝙚 𝙗𝙪𝙩𝙩𝙤𝙣 𝙗𝙚𝙡𝙤𝙬 𝙩𝙤 𝙧𝙚𝙘𝙚𝙞𝙫𝙚 𝙮𝙤𝙪𝙧 𝙛𝙞𝙧𝙨𝙩 𝙧𝙚𝙨𝙪𝙡𝙩!\n\n"
            "📢 <i>𝗦𝘁𝗮𝘆 𝘁𝘂𝗻𝗲𝗱 𝗳𝗼𝗿 𝗮𝗰𝗰𝘂𝗿𝗮𝘁𝗲 𝘀𝗶𝗴𝗻𝗮𝗹𝘀!</i>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 𝙂𝙀𝙏 𝙍𝙀𝙎𝙐𝙇𝙏", callback_data="predict")]])
        )
    else:
        await query.answer("❌ 𝙔𝙤𝙪 𝙝𝙖𝙫𝙚𝙣'𝙩 𝙟𝙤𝙞𝙣𝙚𝙙 𝙩𝙝𝙚 𝙧𝙚𝙦𝙪𝙞𝙧𝙚𝙙 𝙘𝙝𝙖𝙣𝙣𝙚𝙡!", show_alert=True)

# Generate Wingo result
def get_wingo_result():
    result = random.choice(["BIG", "SMALL", "RED", "GREEN"])
    return result, RESULT_IMAGES[result]

# Handle "🎯 𝙂𝙀𝙏 𝙍𝙀𝙎𝙐𝙇𝙏" button
async def prediction_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    current_period = get_period()

    if not await is_user_member(user_id, context):
        await send_join_message(query)
        return

    if current_period in last_period_results:
        # If the result for this period is already given, show timer
        remaining_time = get_remaining_time()
        await query.answer(f"⏳ Wait for {remaining_time} seconds to get the next result.", show_alert=True)
    else:
        # Generate new result for the current period
        result, image_url = get_wingo_result()
        last_period_results[current_period] = result

        keyboard = [[InlineKeyboardButton("𝗡𝗘𝗫𝗧 🔄", callback_data="predict")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            f"🎯 <b>𝙒𝙞𝙣𝙜𝙤 1-𝙈𝙞𝙣𝙪𝙩𝙚 𝙍𝙚𝙨𝙪𝙡𝙩</b>\n"
            f"📅 <b>𝐏𝐞𝐫𝐢𝐨𝐝:</b> <code>{current_period}</code>\n"
            f"🕒 <b>𝙍𝙚𝙢𝙖𝙞𝙣𝙞𝙣𝙜 𝙏𝙞𝙢𝙚:</b> {get_remaining_time()} seconds\n\n"
            f"🔥 <b>𝐑𝐞𝐬𝐮𝐥𝐭:</b> <tg-spoiler>{result}</tg-spoiler>\n\n"
            f"🎭 𝙈𝙖𝙙𝙚 𝙗𝙮 @TaNMaYpaul21"
        )

        # Send prediction result with image
        await query.message.reply_photo(
            photo=image_url,
            caption=message,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

        # Send a sticker after the result
        STICKER_ID = "CAACAgUAAxkBAAENsJxnnkzNiI3lAQwoOKLAfbJv6F1lsQACUgMAAtKqAVVNzYqUuDTsQjYE"  # Replace with your sticker ID
        await query.message.reply_sticker(sticker=STICKER_ID)

# Flask App Initialization
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "Flask server is running successfully!"

# Function to Start the Flask App
def start_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# Main function
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(joined_callback, pattern="joined"))
    app.add_handler(CallbackQueryHandler(prediction_callback, pattern="predict"))

    # Start Flask server in a separate process
    flask_process = Process(target=start_flask)
    flask_process.start()

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
