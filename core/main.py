import logging
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(BASE_DIR.resolve().as_posix())

import discord
from discord import Message
from typing import List

from core.kill_counter.file_kill_counter import FileKillCounter
from core.utils import load_env

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s: %(message)s")
logger = logging.getLogger(__name__)

load_env()
LEGION_GROUPS = os.environ.get("LEGION_GROUPS", '').strip().split(";")
KENY_GROUPS = os.environ.get("KENY_GROUPS", '').strip().split(";")
BOT_TOKEN = os.environ.get("PETR_BOT_TOKEN")


kill_counter = FileKillCounter(Path("kill.json"))


async def they_killed_kenny(message: Message):
    user_id = str(message.author.id)
    kill_counter.increment_kill_count(user_id)
    emojies = kill_counter.get_emoji_kill_count(user_id)
    await message.reply(f"Они убили Кенни, сволочи! {''.join(emojies)}")


class PetyaClient(discord.Client):
    async def on_ready(self):
        logger.info(f"We have logged in as {self.user}")
        logger.info(f"Available servers {list(self.get_all_channels())}")

    @staticmethod
    def _member_in_group(member, groups: List[str]) -> bool:
        if list(filter(lambda role: role.name in groups, member.roles)):
            return True
        return False

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        logger.info(f"Message from {message.author.id}-{message.author.name}: {message.content}")
        if (
            self._member_in_group(message.author, LEGION_GROUPS)
            and "легион" in message.content.lower()
        ):
            for reaction in "🇱 🇪 🇬 🇮 🇴 🇳".split():
                await message.add_reaction(reaction.strip())
        # if message.
        if "я умер" in message.content.lower().strip() and self._member_in_group(
            message.author, KENY_GROUPS
        ):
            await they_killed_kenny(message)
        if message.content.startswith("$hello"):
            await message.reply(f"Hello!, {message.author.name}")


bot = PetyaClient()
bot.run(BOT_TOKEN)
