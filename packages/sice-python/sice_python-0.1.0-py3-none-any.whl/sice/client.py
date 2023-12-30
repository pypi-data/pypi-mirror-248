class BaseClient(object):
    def __init__(
        self,
        host,
    ):
        self.host = host

    def request_confirmation(self):
        """Deposit confirmation method."""
