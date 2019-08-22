import Bot
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import Abstract


class CommandExecution(Abstract.ACommandExecution):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.COMMAND_PARAMS.append('/')
        self.COMMAND_LIST.update(help=self.help, true='True')

    def help(self):
        bot.send_message("HELP ONE", user_id=self.event.user_id)


group = Abstract.TokenAuth(
    token="490742abb5da2183fd05392860650b4021805841db58b405fbe43c2a21ee5e1c50797633cd75daa0f8378")
mode = Abstract.SimpleMode()
bot = Bot.Bot(group, mode)

commands = CommandExecution(bot)
bot.set_commands(commands)


@bot.listen
def handler(event):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        bot.commands.set_event(event)
        if event.text:  # Если написали заданную фразу
            if event.from_user:
                if bot.commands is not None and event.text[0] in bot.commands.COMMAND_PARAMS:
                    bot.command_execution(event.text[1:].lower())
                    # bot.send_message(bot.commands.COMMAND_LIST[event.text[1:]], event.user_id)
                else:
                    bot.send_message(event.text, event.user_id)
