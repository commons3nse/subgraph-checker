import logging


def handle_query_exception(e, bot, user_id=None):
    if hasattr(e, "message"):
        logging.log(logging.ERROR, e.message)
        if "Store error" in e.message and user_id is not None:
            bot.sent_message(user_id, "Store error:\nSomething went wrong; possibly error on server or with subgraph")
    else:
        logging.log(logging.ERROR, "unknown error")