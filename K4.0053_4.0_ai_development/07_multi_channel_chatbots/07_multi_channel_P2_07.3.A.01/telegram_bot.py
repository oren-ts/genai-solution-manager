from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from business_logic import get_weather, confirm_appointment
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /start command - welcome message.
    """
    welcome_message = (
        "👋 Welcome to Weather & Appointment Bot!\n\n"
        "Available commands:\n"
        "🌤 /weather [city] - Get weather information\n"
        "📅 /appointment [date] [time] - Book an appointment\n\n"
        "Examples:\n"
        "/weather Berlin\n"
        "/appointment 2024-03-15 14:00"
    )
    await update.message.reply_text(welcome_message)


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /weather command.
    Extract city from message and call business logic.
    """
    # Extract city from command
    # context.args contains everything after the command
    # e.g., "/weather New York" → context.args = ["New", "York"]
    
    if context.args:
        city = " ".join(context.args)  # Join for multi-word cities
    else:
        city = ""  # Empty if no city provided
    
    # Call business logic
    response = get_weather(city)
    
    # Send response back to user
    await update.message.reply_text(response)


async def appointment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /appointment command.
    Extract date and time from message and call business logic.
    """
    # Extract date and time from command
    # e.g., "/appointment 2024-03-15 14:00" → context.args = ["2024-03-15", "14:00"]
    
    if len(context.args) >= 2:
        date = context.args[0]
        time = context.args[1]
    elif len(context.args) == 1:
        date = context.args[0]
        time = ""  # Missing time
    else:
        date = ""  # Missing both
        time = ""
    
    # Call business logic
    response = confirm_appointment(date, time)
    
    # Send response back to user
    await update.message.reply_text(response)


def main():
    """
    Main function to start the Telegram bot.
    """
    print("🤖 Starting Telegram Bot...")
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("appointment", appointment))
    
    print("✅ Bot is running! Press Ctrl+C to stop.")
    print("💬 Open Telegram and send commands to your bot.")
    
    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()