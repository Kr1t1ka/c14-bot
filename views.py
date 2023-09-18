from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks

from database import get_db
from models.users import User
from serializers.messages import VKRequest
from settings import VK_CONFIRMATION_CODE
from vk_methods import (
    send_message,
    get_user,
    perform_background_task,
    create_keyboard,
)

router = APIRouter()

MESSAGE_DATA = {
    0: {
        "msg": (
            "Здравствуйте! "
            "Мы рады приветствовать вас в отеле «Балтиец». "
            "Спасибо, что вы выбрали именно нас, ведь с нами вы сможете "
            "сделать свой отдых незабываемым! А сейчас пришло время проверить "
            "наличие номеров. "
            "Вы определились с датами путешествия и готовы начать бронирование? "
        ),
        "keyboard": create_keyboard("Да, готов", one_time=False),
        "keyboard_required": False,
    },
    1: {
        "msg": (
            "Вам необходимо выбрать дату заселения в отель. Перед вами все "
            "свободные даты, пожалуйста, выберите подходящий для вас вариант. "
        ),
        "keyboard": create_keyboard("14 октября 2023 года", one_time=False),
        "keyboard_required": True,
    },
    2: {
        "msg": (
            "Мы уже ищем для вас номер. Подскажите, пожалуйста, на какое "
            "количество человек он вам необходим? "
        ),
        "keyboard": create_keyboard("1", one_time=True),
        "keyboard_required": True,
    },
    3: {
        "msg": (
            "Прекрасно, кажется, у нас есть подходящие номера. Однако, уточните, "
            "пожалуйста, есть ли у вас особые пожелания касательно удобств в номере?"
        ),
        "keyboard": create_keyboard(""),
        "keyboard_required": False,
    },
    4: {
        "msg": (
            "Нам потребуется некоторое время, чтобы подобрать для "
            "вас идеальный номер. "
            "На данный момент мы уже занимаемся его поисками. "
        ),
        "keyboard": create_keyboard(""),
        "keyboard_required": False,
    },
    5: {
        "msg": (
            "Мы сможем предоставить вам номер вашей мечты на выбранную дату. "
            "Однако, для завершения бронирования вам необходимо оставить "
            "ваши контактные данные: "
            "https://docs.google.com/forms/d/e/1FAIpQLScKB8MKLWi3PO4uo0Ccbi2DDzwWTGpUetDds9Lfu1PdQKRtvA/viewform "
            "После рассмотрения вашей заявки мы обязательно свяжемся с вами, "
            "и помните, что с нами вы сможете сделать свой отдых незабываемым!"
        ),
        "keyboard": create_keyboard(""),
        "keyboard_required": False,
    },
}


@router.post("/bot")
async def vk_bot(
    data: VKRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    if data.type == "confirmation":
        return Response(content=VK_CONFIRMATION_CODE)
    message = data.object.message
    vk_user = await get_user({"user_ids": message.from_id})
    user = await User.get_or_create(
        db, vk_user["id"], vk_user["first_name"], vk_user["last_name"]
    )
    if message.text == "ffr":
        user.state = 0
        await db.commit()
        return Response(content="ok")

    if MESSAGE_DATA[user.state]["keyboard_required"]:
        if not message.payload:
            data = {
                "peer_id": message.peer_id,
                "message": "Пожалуйста, воспользуйтесь клавиатурой",
            }
            await send_message(data)
            return Response(content="ok")

    if user.state < 5:
        data = {
            "peer_id": message.peer_id,
            "message": MESSAGE_DATA[user.state]["msg"],
            "keyboard": MESSAGE_DATA[user.state]["keyboard"],
        }
        await send_message(data)

    user.state += 1
    await db.commit()

    if user.state == 5:
        data = {
            "peer_id": message.peer_id,
            "message": MESSAGE_DATA[5]["msg"],
            "keyboard": MESSAGE_DATA[5]["keyboard"],
        }
        background_tasks.add_task(perform_background_task, data)

    return Response(content="ok")
