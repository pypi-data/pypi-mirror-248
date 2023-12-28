
class CmdParser:
    def __init__(self, cmd_name: str, args: list[str]):
        self.cmd_name = cmd_name
        self.args = args
        self.current_arg = 1

    def next_str(self):
        if len(self.args) == 0:
            raise ValueError(
                f"argument {self.current_arg} for command \"{self.cmd_name}\" not provided"
            )

        head, tail = self.args[0], self.args[1:]
        self.args = tail
        self.current_arg += 1

        return head

    def next_str_or(self, default: str) -> str:
        try:
            return self.next_str()
        except Exception:
            return default

