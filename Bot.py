import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import Abstract


class Bot:
    def __init__(self, realization: Abstract.AAuth, mode: Abstract.AMode = Abstract.SimpleMode):
        obj = realization
        self.session = obj.auth()
        self.longpoll = VkLongPoll(self.session)
        self.vk = self.session.get_api()
        self.mode = mode
        self.commands = None

    def set_commands(self, commands: Abstract.ACommandExecution):
        self.commands = commands

    def command_execution(self, token):
        self.commands.execution(token)

    def listen(self, func):
        self.mode.listen(func, self.longpoll)

    def send_message(self, message="1", user_id=None, chat_id=None):
        if user_id is not None:
            self.vk.messages.send(
                user_id=user_id,
                random_id=get_random_id(),
                message=message)

        elif chat_id is not None:
            self.vk.messages.send(
                chat_id=chat_id,
                random_id=get_random_id(),
                message=message)


class Tools:
    pass
