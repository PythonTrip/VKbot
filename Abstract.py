from abc import ABC, abstractmethod
import vk_api
from threading import Thread


class ACommandExecution(ABC):
    def __init__(self):
        self.COMMAND_PARAMS = []
        self.COMMAND_LIST = {}
        self.event = None
        self.waiting_flag = False

    def execution(self, command):
        self.COMMAND_LIST[command]()

    def set_event(self, event):
        self.event = event


class AAuth(ABC):
    @abstractmethod
    def auth(self): pass


class TokenAuth(AAuth):
    def __init__(self, token=''):
        self.TOKEN = token

    def auth(self):
        return vk_api.VkApi(token=self.TOKEN)


class AMode(ABC):
    @abstractmethod
    def listen(self, func, longpoll): pass


class ThreadMode(AMode):
    def listen(self, func, longpoll):
        for event in longpoll.listen():
            thread = Thread(target=func, args=(event,))
            thread.start()
            #thread.join()


class SimpleMode(AMode):
    def listen(self, func, longpoll):
        for event in longpoll.listen():
            func(event)
