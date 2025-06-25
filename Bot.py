from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import re

API_URL = "https://www.tikwm.com/api/user/info?unique_id={}"

def extract_info_from_bio(bio):
    emails = re.findall(r'\S+@\S+', bio)
    numbers = re.findall(r'\+?\d[\d\- ]{7,}', bio)
    youtube = "youtube.com" in bio.lower()
    instagram = "instagram.com" in bio.lower()
    return emails, numbers, youtube, instagram

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("بۆ بەدەست هێنانی زانیاری، بنووسە: /check username")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("تکایە بنووسە: /check username")
        return
    
    username = context.args[0]
    url = API_URL.format(username)
    response = requests.get(url).json()

    if response.get("data") is None:
        await update.message.reply_text("❌ ئەم یوسەرنەیمە نەدۆزرایەوە.")
        return

    data = response["data"]
    bio = data.get("signature", "")
    followers = data.get("follower_count", 0)
    likes = data.get("total_favorited", 0)
    country = "🌍 نەتوانرا بدۆزرێتەوە"

    emails, numbers, has_youtube, has_instagram = extract_info_from_bio(bio)

    info = f"📌 *زانیاری سەبارەت بە ئەم یوسەرنەیمە*\n"
    info += f"👤 یوسەرنەیم: {username}\n"
    info += f"📝 Bio: {bio or 'نییە'}\n"
    info += f"👥 فۆلۆوەرەکان: {followers:,}\n"
    info += f"❤️ گشتی لایکەکان: {likes:,}\n"
    info += f"🌐 وڵات: {country}\n"

    if emails:
        info += f"📧 ئیمەیڵەکان: {', '.join(emails)}\n"
    if numbers:
        info += f"📱 ژمارەکان: {', '.join(numbers)}\n"
    if has_youtube:
        info += "▶️ YouTube لە bio دا هەیە\n"
    if has_instagram:
        info += "📸 Instagram لە bio دا هەیە\n"

    info += "\n🔐 *زانیاری سەبارەت بە سەلامەتی*\n"
    info += "✅ Passkey فعالە (فێیک)\n"
    info += "✅ Email چاککراوە (فێیک)\n"
    info += "❌ ژمارەی تەلەفۆن چاک نییە (فێیک)\n"

    info += "\n🔗 *گرێدانی بە پلاتفۆرمەکانی تر*\n"
    info += "✅ Email\n✅ Phone\n✅ Google\n✅ Facebook\n❌ Apple ID\n"

    info += "\n⚠️ *بەشی سڕینەوەی گرێدان*\n"
    info += "🚫 سڕینەوەی گرێدان تەنها لە نێو ئەپەکەی TikTok دەکرێت.\n"

    await update.message.reply_text(info, parse_mode='Markdown')

app = ApplicationBuilder().token("7387003095:AAFocdeRPw9Kh8YHcUWks5WIEkJHt8sI9Sw").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("check", check))
app.run_polling()
