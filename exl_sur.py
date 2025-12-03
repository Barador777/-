import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = 'Ваш токен'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Меню с полезной информацией", "Расположние техникума"],
        ["О нас", "Помощь"],
        ["Связь с нами"]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Добро пожаловать! Выберите действие:",
        reply_markup=reply_markup
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "Меню с полезной информацией":
        # Инлайн-клавиатура для выбора уровня
        keyboard = [
            [InlineKeyboardButton("Номер телефона секретаря", callback_data="level_easy")],
            [InlineKeyboardButton("Режим работы", callback_data="level_medium")],
            [InlineKeyboardButton("Докумкенты для поступления", callback_data="level_hard")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Выберите нужную информацию:", reply_markup=reply_markup)
    
    elif text == "Расположние техникума":
        await update.message.reply_text("г.Ижевск, улица Молодежная, 109")
    
    elif text == "Связь с нами":
        keyboard = [[InlineKeyboardButton("Написать разработчику", url="https://t.me/Bratik_SmaiL")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Свяжитесь с нами:", reply_markup=reply_markup)
    elif text == "О нас":
        await update.message.reply_text("У техникума богатейшая история, а начиналась она в далеком 1930 году в городе Сарапуле, на берегу красавицы-реки Камы. В то время набирала темпы культурная революция, страна задыхалась от безграмотности, нуждалась в квалифицированных кадрах не только для подъема промышленности, но и для села. Поэтому, в соответствии с постановлением Уральского областного союза потребкооперации 1 сентября 1930 года, в Сарапуле был открыт Сарапульский кооперативный техникум.")
    elif text == "Помощь":
        await update.message.reply_text("Помощи нет, справляйтесь сами")

async def handle_inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "level_easy":
        await query.edit_message_text("+7 (3412) 37-04-88")
    elif query.data == "level_medium":
        await query.edit_message_text("Режим работы Ижевского техникума экономики, управления и права Удмуртпотребсоюза (ИТЭУП) в 2025 году: ПН–ПТ — с 8:00 до 17:00, воскресенье и суббота — выходные.")
    elif query.data == "level_hard":
        await query.edit_message_text("Заявление, аттестат или диплом, копия паспорта, фото 3×4 (4 шт.), СНИЛС.")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    application.add_handler(CallbackQueryHandler(handle_inline_buttons))
    
    application.run_polling()

if __name__ == '__main__':
    main()