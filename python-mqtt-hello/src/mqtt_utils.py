import time
import traceback
import json
import threading
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    PublishToIoTCoreRequest,
    SubscribeToIoTCoreRequest,
)

TIMEOUT = 10


class GreengrassTopicPublisher:
    def __init__(self, topic=None, qos=QOS.AT_LEAST_ONCE):
        self.topic = topic
        self.qos = qos
        self.ipc_client = awsiot.greengrasscoreipc.connect()

    def set_default_topic(self, topic):
        self.topic = topic

    def publish(self, message, topic=None):
        try:
            if not topic:
                topic = self.topic
            if not topic:
                raise ValueError("[ERROR] Publish topic not provided")

            msgstring = json.dumps(message)
            pubrequest = PublishToIoTCoreRequest()
            pubrequest.topic_name = topic
            pubrequest.payload = bytes(msgstring, "utf-8")
            pubrequest.qos = self.qos
            operation = self.ipc_client.new_publish_to_iot_core()
            operation.activate(pubrequest)
            future = operation.get_response()
            future.result(TIMEOUT)
            print(f"[INFO] Published to {topic}: {message}")
        except Exception as e:
            print(f"[ERROR] Failed to publish to {topic}: {e}")


class GreengrassTopicSubscriber:
    def __init__(self, topic=None, qos=QOS.AT_MOST_ONCE):
        self.topic = topic
        self.qos = qos
        self.ipc_client = awsiot.greengrasscoreipc.connect()

    def set_default_topic(self, topic):
        self.topic = topic

    def subscribe(self, callback, topic=None):
        if not topic:
            topic = self.topic
        if not topic:
            raise ValueError("[ERROR] Subscribe topic not provided")

        def _subscribe():
            try:
                handler = SubHandler(callback)
                subrequest = SubscribeToIoTCoreRequest()
                subrequest.topic_name = topic
                subrequest.qos = self.qos
                operation = self.ipc_client.new_subscribe_to_iot_core(handler)
                future = operation.activate(subrequest)
                future.result(TIMEOUT)
                print(f"[INFO] Subscribed to {topic}")
            except Exception as e:
                print(f"[Error] Failed to subscribe to {topic}: {e}")

        # Start the subscription in a new thread
        threading.Thread(target=_subscribe).start()


class SubHandler(client.SubscribeToIoTCoreStreamHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            message = str(event.message.payload, "utf-8")
            self.callback(event.message.topic_name, json.loads(message))
        except:
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        return True  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        pass
