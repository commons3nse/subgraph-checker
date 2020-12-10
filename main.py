import logging
import os

from dotenv import load_dotenv

load_dotenv()

from init_db import init_db
from telegram.ext import filters

from telegram.ext import (
    Filters,
    MessageHandler,
    Updater,
    CommandHandler,
)

from subgraph_bot.telegram.message_handlers import (
    start,
    private_message,
    subscribe,
    status
)

from subgraph_bot.telegram.jobs import check_subgraphs

init_db()

logging.basicConfig(level=getattr(logging, os.environ['LOGGING_LEVEL']),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize telegram updater and dispatcher
updater = Updater(
    token=os.environ['TELEGRAM_API_KEY'],
    workers=int(os.environ['TELEGRAM_WORKER_COUNT']),
    use_context=True,
    request_kwargs={'read_timeout': 20, 'connect_timeout': 20}
)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('subscribe', subscribe))
dispatcher.add_handler(CommandHandler('status', status))
dispatcher.add_handler(MessageHandler(Filters.private, private_message))

job_queue = updater.job_queue
minute = 60
job_queue.run_repeating(check_subgraphs, interval=int(os.environ['SUBGRAPH_CHECK_INTERVAL']),
                                first=0, name='Check subgraphs')

updater.start_polling()
updater.idle()


