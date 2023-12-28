class EditError(Exception):
    pass

class EditExit(Exception):
    pass

class EditContinue(Exception):
    pass

class EditUndo(Exception):
    def __init__(self, num: str | int):
        self.num = num
        super().__init__()

