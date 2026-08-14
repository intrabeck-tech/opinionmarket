import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes


OPINIONMARKET_URL = "https://opinionmarket.ng"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome users and provide the OpinionMarket Mini App launch button."""
    if update.message is None:
        return

    keyboard = [
        [
            InlineKeyboardButton(
                text="🚀 Open OpinionMarket",
                web_app=WebAppInfo(url=OPINIONMARKET_URL),
            )
        ]
    ]

    await update.message.reply_text(
        "Welcome to OpinionMarket 👋\n"
        "Explore real-world markets across sports, politics, crypto, business, and more.\n"
        "Tap the button below to open OpinionMarket and start exploring.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def open_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provide a button that opens the OpinionMarket Mini App."""
    if update.message is None:
        return

    keyboard = [
        [
            InlineKeyboardButton(
                text="🚀 Open OpinionMarket",
                web_app=WebAppInfo(url=OPINIONMARKET_URL),
            )
        ]
    ]

    await update.message.reply_text(
        "Open OpinionMarket:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Explain the bot's available commands."""
    if update.message is None:
        return

    await update.message.reply_text(
        "Need help with OpinionMarket?\n\n"
        "🚀 Use /open to launch OpinionMarket. 🔄 Use /start to restart the bot. "
        "🌐 Visit the OpinionMarket Mini App to explore available markets."
    )


async def error_handler(
    update: object, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Log unexpected update errors without exposing the bot token."""
    logger.error("Exception while handling an update", exc_info=context.error)


def main() -> None:
    """Start the bot using Telegram long polling."""
    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError(
            "BOT_TOKEN is not set. Add the Telegram bot token as a secure secret."
        )

    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("open", open_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_error_handler(error_handler)

    logger.info("OpinionMarket Telegram bot is starting")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
