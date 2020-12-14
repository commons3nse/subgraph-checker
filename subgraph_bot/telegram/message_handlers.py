from subgraph_bot.models.user import User
from subgraph_bot.db import get_session
from subgraph_bot.graph_requests import query_current, query_pending, query_latest_block_num
from subgraph_bot.helpers import handle_query_exception


def start(update, context):
    chat = update.message.chat
    chat.send_message(f'''Welcome!
This bot notifies you when your subgraph has been synchronized.
You can also check current synchronization status.

Commands:
/subscribe <author>/<subgraph_name> - subscribe to get notification when subgraph is synchronized
/status - get current synchronization status''')


def subscribe(update, context):
    session = get_session()
    chat = update.message.chat
    text = update.message.text

    if not (len(text.split(' ')) == 2 and len(text.split(' ')[1].lower().split('/')) == 2):
        chat.send_message("Please send message in format\n/subscribe <author>/<subgraph_name>")
        return

    subgraph = text.split(' ')[1].lower()
    user_id = update.message.chat.id
    user = session.query(User).get(update.message.chat.id)
    if not user:
        user = User(user_id)

    try:
        latest = query_latest_block_num()
        block = query_pending(subgraph)
        if not block:
            block = query_current(subgraph)
    except Exception as e:
        handle_query_exception(e, context.bot, user.id)
        return

    if not block:
        chat.send_message("Subgraph not found. Are you sure you deployed it?")
    else:
        if abs(block - latest) < 3:
            chat.send_message("Your subgraph is already synchronized!")
        else:
            chat.send_message(f"Subscribed. I will text you when {subgraph} is ready.")
            user.current_subgraph = subgraph
            user.working = True

    session.add(user)

    session.commit()


def status(update, context):
    session = get_session()
    chat = update.message.chat

    user = session.query(User).get(update.message.chat.id)
    if not user or not (user.current_subgraph and user.working):
        chat.send_message("You need to subscribe first. Send command:\n/subscribe <author>/<subgraph_name>")
        return

    try:
        latest = query_latest_block_num()
        block = query_pending(user.current_subgraph)
        if not block:
            block = query_current(user.current_subgraph)
    except Exception as e:
        handle_query_exception(e, context.bot, user.id)
        return

    percents = 100
    if abs(block - latest) > 5:
        percents = block / latest * 100
    chat.send_message(f"Synchronized: {percents:.1f}% ({block} blocks out of {latest}.")


def private_message(update, context):
    context.bot.send_message(update.effective_user.id, 'Unrecognized command. Try /start')
