from subgraph_bot.db import get_session
from subgraph_bot.models.user import User
from sqlalchemy import and_
from subgraph_bot.graph_requests import query_current, query_pending, query_latest_block_num
from subgraph_bot.helpers import handle_query_exception


def check_subgraphs(context):
    session = get_session()

    users = session.query(User).filter(and_(User.current_subgraph.isnot(None), User.working.is_(True))).all()

    try:
        latest = query_latest_block_num()
    except Exception as e:
        handle_query_exception(e, context.bot)
        return

    for user in users:
        try:
            block = query_pending(user.current_subgraph)
            if not block:
                block = query_current(user.current_subgraph)
        except Exception as e:
            handle_query_exception(e, context.bot, user.id)
            continue

        if abs(latest - block) < 5:  # may be some delays in synchronization, consider synchronized
            context.bot.send_message(user.id, f"Sugraph {user.current_subgraph} has been synchronized!\nLink: https://thegraph.com/explorer/subgraph/{user.current_subgraph}")
            user.working = False
            user.current_subgraph = None

    session.commit()


