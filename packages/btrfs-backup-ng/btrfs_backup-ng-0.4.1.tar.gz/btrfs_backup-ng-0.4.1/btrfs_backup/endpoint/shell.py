from .common import Endpoint


class ShellEndpoint(Endpoint):
    def __init__(self, cmd, **kwargs):
        super(ShellEndpoint, self).__init__(**kwargs)
        if self.source:
            raise ValueError("Shell can't be used as source.")
        self.cmd = cmd

    def __repr__(self):
        return f"(Shell) {self.cmd}"

    def get_id(self):
        return "shell://{self.cmd}"

    def _build_receive_cmd(self, destination):
        return ["sh", "-c", self.cmd]
