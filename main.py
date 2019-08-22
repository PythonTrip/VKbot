import Bot
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import Abstract
import time
import threading


class CommandExecution(Abstract.ACommandExecution):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.COMMAND_PARAMS.append('/')
        self.COMMAND_LIST.update(help=self.help, threads=self.threads)

    def threads(self):
        bot.send_message(len(threading.enumerate()), user_id=self.event.user_id)

    def help(self):
        bot.send_message("HELP ONE", user_id=self.event.user_id)


# class Add:
#     def __init__(self):
#         self.SUB_LIST = {'new': self.new, 'dot': self.dot}
#
#     def start(self, params):
#         if len(params) == 1:
#             self.SUB_LIST[params]()
#         else:
#             self.SUB_LIST[params[0]](params[1:])
#
#     def new(self, param):
#         def command():
#             return "True", True
#
#         print("Added")
#         SUB_LIST = {'command': command}
#         if param in SUB_LIST:
#             SUB_LIST[param]()
#
#     def dot(self):
#         print("Dotted")


group = Abstract.TokenAuth(
    token="490742abb5da2183fd05392860650b4021805841db58b405fbe43c2a21ee5e1c50797633cd75daa0f8378")
mode = Abstract.ThreadMode()
bot = Bot.Bot(group, mode)

commands = CommandExecution(bot)
bot.set_commands(commands)


@bot.listen
def handler(event):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        tokens = event.text.split()
        bot.commands.set_event(event)
        id = (None, None)
        if event.from_user:
            id = (event.user_id, None)
        elif event.from_chat:
            id = (None, event.chat_id)

        for token in tokens:
            if bot.commands is not None:
                if token[0] in bot.commands.COMMAND_PARAMS:
                    if token in bot.commands.COMMAND_LIST:
                        bot.command_execution(token.lower())
                    else:
                        bot.send_message("Неизвестная команда", id[0], id[1])
                else:
                    bot.send_message(token, id[0], id[1])
