import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import subprocess

# Masukkan Token Bot Anda
TOKEN = "7942974060:AAFdgWuOPMn7epSv5s3yRovClRGkgZsSG54"
bot = telebot.TeleBot(TOKEN)

# Link download Windows Server
WINDOWS_VERSIONS = {
    "2016": "https://go.microsoft.com/fwlink/p/?linkid=2195684&clcid=0x409&culture=en-us&country=us",
    "2019": "https://go.microsoft.com/fwlink/p/?linkid=2195685&clcid=0x409&culture=en-us&country=us",
    "2022": "https://go.microsoft.com/fwlink/p/?linkid=2195333",
    "2025": "https://go.microsoft.com/fwlink/?linkid=2273506"
}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = InlineKeyboardMarkup()

    for version in WINDOWS_VERSIONS.keys():
        markup.add(InlineKeyboardButton(f"Windows Server {version}", callback_data=f"install_{version}"))

    bot.send_message(chat_id, "Pilih versi Windows Server yang ingin diinstal:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("install_"))
def confirm_install(call):
    chat_id = call.message.chat.id
    version = call.data.split("_")[1]

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ YA, Instal Sekarang", callback_data=f"confirm_{version}"))
    markup.add(InlineKeyboardButton("❌ Batal", callback_data="cancel"))

    bot.send_message(chat_id, f"⚠️ Anda akan menginstal Windows Server {version}. Lanjutkan?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def install_windows(call):
    chat_id = call.message.chat.id
    version = call.data.split("_")[1]
    download_link = WINDOWS_VERSIONS[version]

    bot.send_message(chat_id, f"⚙️ Mengunduh Windows Server {version}...\nSilakan tunggu beberapa menit.")

    command = f"""
    wget {download_link} -O windows.img
    dd if=windows.img of=/dev/vda
    reboot
    """

    subprocess.Popen(command, shell=True)
    bot.send_message(chat_id, "✅ Instalasi dimulai. VPS akan reboot ke Windows Server.")

@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel_install(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "❌ Instalasi dibatalkan.")

bot.polling()

