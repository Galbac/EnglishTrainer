import asyncio
import logging
import os
from datetime import datetime, UTC

from celery import Celery

from app.database import get_db
from app.model import User, UserWord, Word
from app.utils.email_sender import send_daily_reminder_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL")
celery_app = Celery(
    "english_trainer",
    backend=REDIS_URL,
    broker=REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'send-daily-reminders': {
            'task': 'app.celery.celery_app.send_daily_reminders',
            'schedule': 30,
            # 'schedule': crontab(hour=8, minute=0),
        },
    },
)


@celery_app.task
def send_daily_reminders():
    logger.info("Запущена задача отправки ежедневных напоминаний...")

    db_gen = get_db()
    db = next(db_gen)

    try:
        users = db.query(User).filter(
            User.receive_reminders.is_(True),
            User.email.is_not(None)
        ).all()

        for user in users:
            pending_words = ((db.query(UserWord)
                              .join(Word))
                             .filter(
                UserWord.user_id == user.id,
                UserWord.next_review <= datetime.now(UTC),
                UserWord.progress < 80
            ).limit(10).all())

            if not pending_words:
                continue

            word_list = [uw.word.english for uw in pending_words]
            word_str = ", ".join(f'"{w}"' for w in word_list)

            try:
                DOMAIN = os.getenv("DOMAIN")
                asyncio.run(send_daily_reminder_email(
                    to_email=user.email,
                    username=user.user,
                    words=word_str,
                    base_url=DOMAIN
                ))
                logger.info(f"Напоминание отправлено {user.email}")
            except Exception as e:
                logger.error(f"Ошибка отправки письма {user.email}: {e}")

    except Exception as e:
        logger.error(f"Ошибка в задаче send_daily_reminders: {e}")
    finally:
        db.close()
