import websocket
import platform

from disco.util.emitter import Emitter
from disco.util.logging import LoggingClass


class Websocket(LoggingClass, websocket.WebSocketApp):
    """
    A utility class which wraps the functionality of :class:`websocket.WebSocketApp`
    changing its behavior to better conform with standard style across disco.

    The major difference comes with the move from callback functions, to all
    events being piped into a single emitter.
    """
    def __init__(self, *args, **kwargs):
        LoggingClass.__init__(self)

        if platform.system() not in ["Windows", "Darwin"]:
            websocket.setdefaulttimeout(5)
        else:
            self.log.warning("Running on Windows/OSX may result in websocket timeouts using the defaulttimeout of 5, so the value is boosted.")
            websocket.setdefaulttimeout(45)
        
        websocket.WebSocketApp.__init__(self, *args, **kwargs)

        self.is_closed = False
        self.emitter = Emitter()

        # Hack to get events to emit
        for var in self.__dict__.keys():
            if not var.startswith('on_'):
                continue

            setattr(self, var, var)

    def _callback(self, callback, *args):
        if not callback:
            return

        self.emitter.emit(callback, *args)
