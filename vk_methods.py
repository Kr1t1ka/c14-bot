import asyncio
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import httpx

from settings import VK_BOT_TOKEN

URL = "https://api.vk.com/method/"
DEFAULT_DATA = {"access_token": VK_BOT_TOKEN, "v": "5.131"}


def create_keyboard(name, one_time=True):
    if not name:
        return {}
    keyboard = VkKeyboard(one_time=one_time, inline=False)
    keyboard.add_button(
        name, color=VkKeyboardColor.SECONDARY, payload={"button": name}
    )
    return keyboard.get_keyboard()


async def send_message(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{URL}messages.send",
            data={
                **data,
                **DEFAULT_DATA,
                "random_id": random.randint(-2147483648, +2147483648),
            },
        )
        return response.json()


async def get_user(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{URL}users.get", data={**data, **DEFAULT_DATA}
        )
        res = response.json()
        if "response" in res:
            return res["response"][0] if res["response"] else None


async def perform_background_task(data):
    await asyncio.sleep(43200)
    await send_message(data)
