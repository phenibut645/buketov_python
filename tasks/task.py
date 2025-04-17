from enum import Enum

class Status(Enum):
    TODO = 1
    DONE = 2


class Task:
    def __init__(self, title: str, status: Status = Status.TODO):
        self.title = title
        if isinstance(status, Status):
            self.__status = status
        else:
            self.__status = Status.TODO
    
    def get_status(self):
        return self.__status

    def set_status(self, status: Status):
        if isinstance(status, Status):
            self.__status = status