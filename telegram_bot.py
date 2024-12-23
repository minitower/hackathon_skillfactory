import logging
import random
import os
from io import BytesIO
import requests
from telegram import Update
import pathlib
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

data_path = pathlib.Path(__file__).parent.resolve()/'..'/'..'/'data'

# Пути к папкам
source_folder = data_path/"images"
destination_folder = data_path/"users_images"

# Функция для получения случайного изображения из папки
def get_random_image():
    images = os.listdir(source_folder)
    random_image = random.choice(images)
    return os.path.join(source_folder, random_image)

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение."""
    await update.message.reply_text("Привет! Напишите любое сообщение или отправьте изображение, и я отправлю вам случайное изображение из папки.")

# Обработка любых текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает любое сообщение и отправляет случайное изображение из папки.
    """
    
    # Получаем путь к случайному изображению
    image_path = get_random_image()
    
    with open(image_path, 'rb') as image_file:
        await update.message.reply_photo(photo=image_file)

# Обработка изображений
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сохраняет полученное изображение в папку."""
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = os.path.join(destination_folder, file.file_unique_id + ".jpg")
    await file.download_to_drive(file_path)
    await update.message.reply_text(f"Изображение сохранено в {file_path}")

def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(os.environ.get('TELEGRAM_BOT_API')).build() 

    # Обработка команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Запускаем бота до тех пор, пока пользователь не нажмет Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
