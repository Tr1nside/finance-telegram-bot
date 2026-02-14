#!/usr/bin/env python3.12
"""
Finance Telegram Bot Runner (Conda/Jupyter fix)
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Добавляем src в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src" / "telegram-bot-src"))

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Загружаем .env
load_dotenv()


def validate_env() -> None:
    """Проверяет наличие обязательных переменных."""
    required = ["TELEGRAM_TOKEN"]
    missing = [key for key in required if not os.getenv(key)]

    if missing:
        logger.error(f"❌ Отсутствуют переменные: {', '.join(missing)}")
        logger.error("Создайте .env файл с TELEGRAM_TOKEN!")
        sys.exit(1)

    logger.info("✅ Переменные окружения загружены")


def main() -> None:
    """Запуск БЕЗ asyncio.run()"""
    try:
        validate_env()

        from src.bot import create_application

        logger.info("🚀 Запускаем Finance Telegram Bot...")
        app = create_application()

        # ptb сам запускает event loop!
        app.run_polling(drop_pending_updates=True)

    except KeyboardInterrupt:
        logger.info("🛑 Остановка по Ctrl+C")
    except Exception as e:
        logger.error(f"💥 Ошибка: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()  # ← НЕ asyncio.run(main())
