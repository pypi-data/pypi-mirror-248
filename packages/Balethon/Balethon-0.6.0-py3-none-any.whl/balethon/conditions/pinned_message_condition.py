from .condition import Condition


@Condition.create
async def pinned_message(condition, client, message) -> bool:
    return bool(message.pinned_message)
