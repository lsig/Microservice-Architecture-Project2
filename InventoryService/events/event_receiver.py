



from events.i_event_connection import IEventConnection


class EventReceiver:
    def __init__(self, event_connection: IEventConnection) -> None:
        self.__connection = event_connection