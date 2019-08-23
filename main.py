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
        self.SLASH_COMMAND_LIST = {'help': self.slash_help, 'thread': self.threads, 'add': self.create_new_command,
                                   'check': self.get_new_command}
        self.HASH_COMMAND_LIST = {'hash': self.hash, 'sqrt': self.sqrt}
        self.NEW_COMMAND = {}
        param_keys = {"/": self.SLASH_COMMAND_LIST, "#": self.HASH_COMMAND_LIST}
        self.COMMAND_PARAMS.update(param_keys)

    def create_new_command(self):
        tokens = self.event.text.split()
        content = ""
        if len(tokens) < 2:
            bot.send_message("/add content", user_id=self.event.user_id)
            return
        for token in tokens[1:]:
            content += token + " "
        self.NEW_COMMAND.update({tokens[0]: content})
        bot.send_message("Command add in queue", user_id=self.event.user_id)

    def get_new_command(self):
        command_list = ""
        for key, value in self.NEW_COMMAND.items():
            command_list += key + " " + value + "\n"
        bot.send_message(command_list, user_id=self.event.user_id)

    def set_command_param(self, key):
        if key in self.COMMAND_PARAMS.keys():
            self.COMMAND_LIST.update(self.COMMAND_PARAMS[key])
            return True
        else:
            return False

    def sqrt(self):
        tokens = self.event.text.split()
        if len(tokens) < 2:
            bot.send_message("#sqrt num", user_id=self.event.user_id)
        else:
            for num in tokens[1:]:
                try:
                    bot.send_message(str(int(num) ** 0.5), user_id=self.event.user_id)
                except:
                    bot.send_message("Error", user_id=self.event.user_id)

    def hash(self):
        tokens = self.event.text.split()
        if len(tokens) < 2:
            bot.send_message("#hash text", user_id=self.event.user_id)
        else:
            bot.send_message(tokens[1:], user_id=self.event.user_id)

    def threads(self):
        bot.send_message(len(threading.enumerate()), user_id=self.event.user_id)

    def slash_help(self):
        command_list = "Commands: \n"
        for key, value in self.COMMAND_LIST.items():
            command_list += "/" + key + "\n"
        bot.send_message(command_list, user_id=self.event.user_id)


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

        if bot.commands is not None:
            if bot.commands.set_command_param(tokens[0][0]):
                if tokens[0][1:] in bot.commands.COMMAND_LIST:
                    bot.command_execution(tokens[0][1:].lower())
                else:
                    bot.send_message("Неизвестная команда", id[0], id[1])
