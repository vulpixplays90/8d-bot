import telebot
import time 
import os
import uuid
import subprocess
from db import get_user_settings, update_user_setting, reset_user_settings
from threading import Thread 
from flask import Flask 


BOT_TOKEN = '7174547352:AAEvSSJpA_51UFLuvh9jJv2f2F-6qmoDbq8'
bot = telebot.TeleBot(BOT_TOKEN)

CHANNEL_ID = -1002433942287

app = Flask('')

@app.route('/')
def home():
    return "I am alive"

def run_http_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_http_server)
    t.start()




from db import get_user_settings, update_user_setting

@bot.message_handler(commands=['settings'])
def show_settings(message):
    settings = get_user_settings(message.chat.id)

    # Friendly names + hints for normal users
    friendly_settings = {
        "panBoundary": ("Panning Range", "How far sound moves left/right"),
        "jumpPercentage": ("Pan Step Size", "Smoothness of movement"),
        "timeLtoR": ("Pan Cycle Time", "Time to move Left to Right (ms)"),
        "volumeMultiplier": ("Edge Volume Boost", "Volume increase at sides (dB)"),
        "speedMultiplier": ("Playback Speed", "1 = normal, 0.9 = slower"),
        "reverb.room_size": ("Reverb Room Size", "How big the echo space feels"),
        "reverb.damping": ("Reverb Damping", "Softens high frequencies"),
        "reverb.width": ("Reverb Width", "Stereo wideness"),
        "reverb.wet_level": ("Effect Volume", "How loud the echo is"),
        "reverb.dry_level": ("Original Volume", "How loud the original audio is"),
    }

    main_settings = ""
    reverb_settings = ""

    for key, value in settings.items():
        if key == "reverb":
            for subkey, subval in value.items():
                full_key = f"reverb.{subkey}"
                label, hint = friendly_settings.get(full_key, (subkey, ""))
                reverb_settings += (
                    f"*{label}*\n"
                    f"`{full_key}` = `{subval}`\n"
                    f"_{hint}_\n\n"
                )
        else:
            label, hint = friendly_settings.get(key, (key, ""))
            main_settings += (
                f"*{label}*\n"
                f"`{key}` = `{value}`\n"
                f"_{hint}_\n\n"
            )

    message_text = (
        "*Your Current Audio Settings:*\n\n"
        "*Main Effects:*\n\n"
        f"{main_settings}"
        "*Reverb Settings:*\n\n"
        f"{reverb_settings}"
    )

    bot.reply_to(message, message_text, parse_mode="Markdown")


@bot.message_handler(commands=['set'])
def set_parameter(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            raise ValueError
        param, value = parts[1], parts[2]
        if param in ['speedMultiplier', 'jumpPercentage', 'panBoundary', 'timeLtoR', 'volumeMultiplier']:
            value = float(value) if '.' in value else int(value)
        update_user_setting(message.chat.id, param, value)
        bot.reply_to(message, f"Updated setting '{param}' to {value}")
    except Exception:
        bot.reply_to(message, "Usage: /set [parameter] [value]\nExample: /set speedMultiplier 0.85")

@bot.message_handler(commands=['resetsettings'])
def reset_settings(message):
    reset_user_settings(message.chat.id)
    bot.reply_to(message, "✅ Your settings have been reset to default values.")


from db import get_all_users  # Add this import

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ You're not allowed to use this.")

    users = list(user_collection.find())
    bot.reply_to(message, f"Total registered users: {len(users)}")


ADMIN_ID = 6897739611  # Replace with your actual Telegram ID

from db import user_collection  # Add this if not already imported

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ You're not allowed to use this.")

    if not message.reply_to_message:
        return bot.reply_to(message, "📌 Reply to a message you want to broadcast.")

    success = 0
    for user in user_collection.find():
        try:
            bot.copy_message(
                chat_id=user['_id'],
                from_chat_id=message.chat.id,
                message_id=message.reply_to_message.message_id
            )
            success += 1
        except:
            continue

    bot.send_message(message.chat.id, f"✅ Broadcast sent to {success} users.")

@bot.message_handler(commands=['feedback'])
def handle_feedback(message):
    # Extract feedback text
    if len(message.text.split(' ', 1)) < 2:
        return bot.reply_to(message, "✏️ Please provide feedback text.\nExample: /feedback Love this bot!")

    feedback_text = message.text.split(' ', 1)[1]

    # Format feedback with user info
    feedback_msg = (
        "📬 *New Feedback Received!*\n\n"
        f"{feedback_text}\n\n"
        f"👤 Username: @{message.from_user.username or 'N/A'}\n"
        f"🆔 User ID: `{message.from_user.id}`"
    )

    # Send to your private channel
    bot.send_message(CHANNEL_ID, feedback_msg, parse_mode="Markdown")

    # Confirm to the user
    bot.reply_to(message, "✅ Thank you! Your feedback has been sent.")











from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import register_user

@bot.message_handler(commands=['start'])
def start_handler(message):
    register_user(message.chat.id)

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("👤 Developer", url="https://t.me/botplays90"),
        InlineKeyboardButton("📢 Channel", url="https://t.me/join_hyponet")
    )

    welcome_text = (
        "🎧 *Welcome to the 8D Slowed Reverb Bot!*\n\n"
        "✨ This bot will automatically apply the following effects to any audio or voice message:\n"
        "▪️ *Slowed*\n"
        "▪️ *Reverb*\n"
        "▪️ *8D Audio Effect*\n\n"
        "Just send me a file and I'll return the enhanced version!\n\n"
        "Need customization? Use /settings or /resetsettings To Use Default Audio Settings.⚙️\n"
        "For help, tap /help below."
    )

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


@bot.message_handler(commands=['help'])
def help_handler(message):
    help_text = (
        "ℹ️ *Bot Help Guide:*\n\n"
        "1. Send an audio or voice message — I’ll return the 8D slowed reverb version.\n"
        "2. Use /settings to view your current effect settings.\n"
        "3. Use /set [parameter] [value] to customize settings.\n"
        "   Example: `/set speedMultiplier 0.85`\n"
        "4. Use /resetsettings to restore default effects.\n\n"
        "Need support? Contact @botplays90"
    )

    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")



@bot.message_handler(content_types=['audio', 'voice'])
def handle_audio(message):
   

    file_info = bot.get_file(message.audio.file_id if message.audio else message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    original_name = message.audio.file_name if message.audio else "voice_message"
    base_name = os.path.splitext(original_name)[0]
    unique_id = str(uuid.uuid4())

    input_path = f"{unique_id}.mp3"
    output_path = f"{unique_id}_slowedReverb.mp3"

    # Save the downloaded file
    with open(input_path, 'wb') as f:
        f.write(downloaded_file)

    # Send original audio to channel with user info
    caption = (
        f"🆕 New audio received\n"
        f"👤 Username: @{message.from_user.username or 'N/A'}\n"
        f"🆔 User ID: `{message.from_user.id}`"
    )

    with open(input_path, 'rb') as audio_file:
        bot.send_audio(
            chat_id=CHANNEL_ID,
            audio=audio_file,
            caption=caption,
            parse_mode="Markdown"
        )

    # Progress bar to user
    progress_msg = bot.send_message(
        message.chat.id,
        "⏳ *Processing your audio...*\n`[▓░░░░░░░░░] 10%`",
        parse_mode="Markdown"
    )
    time.sleep(1)
    bot.edit_message_text("⏳ *Processing your audio...*\n`[▓▓▓░░░░░░░] 30%`", message.chat.id, progress_msg.message_id, parse_mode="Markdown")
    time.sleep(1)
    bot.edit_message_text("⏳ *Processing your audio...*\n`[▓▓▓▓▓░░░░░] 60%`", message.chat.id, progress_msg.message_id, parse_mode="Markdown")
    time.sleep(1)
    bot.edit_message_text("⏳ *Processing your audio...*\n`[▓▓▓▓▓▓▓▓░░] 90%`", message.chat.id, progress_msg.message_id, parse_mode="Markdown")

    # Process the audio
    try:
        subprocess.run(["python3", "main.py", input_path, output_path, str(message.chat.id)], check=True)

        with open(output_path, 'rb') as audio_file, open("image.jpg", 'rb') as thumb_file:
            bot.send_audio(
                chat_id=message.chat.id,
                audio=audio_file,
                caption="Here’s your slowed + reverb + 8D audio!\n\n By @username",
                title=f"{base_name} - Slowed Reverb",
                thumbnail=thumb_file
            )

        # Delete progress message after success
        bot.delete_message(message.chat.id, progress_msg.message_id)

    except subprocess.CalledProcessError as e:
        bot.edit_message_text(f"⚠️ Error processing audio:\n`{e}`", message.chat.id, progress_msg.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.edit_message_text(f"⚠️ Unexpected error:\n`{e}`", message.chat.id, progress_msg.message_id, parse_mode="Markdown")

    finally:
        # Clean up temporary files
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

keep_alive()

bot.infinity_polling()
