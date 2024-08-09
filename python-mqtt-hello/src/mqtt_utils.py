import time
import traceback
import json
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    PublishToIoTCoreRequest,
    SubscribeToIoTCoreRequest,
)

TIMEOUT = 10


class MQTTClient:
    def __init__(
        self,
        pub_topic=None,
        sub_topic=None,
        pub_qos=QOS.AT_LEAST_ONCE,
        sub_qos=QOS.AT_MOST_ONCE,
    ):
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic
        self.pub_qos = pub_qos
        self.sub_qos = sub_qos
        self.ipc_client = awsiot.greengrasscoreipc.connect()

    def set_default_pub_topic(self, topic):
        self.pub_topic = topic

    def set_default_sub_topic(self, topic):
        self.sub_topic = topic

    def publish(self, message, topic=None):
        try:
            if not topic:
                topic = self.pub_topic
            if not topic:
                raise ValueError("Publish topic not provided")

            msgstring = json.dumps(message)
            pubrequest = PublishToIoTCoreRequest()
            pubrequest.topic_name = topic
            pubrequest.payload = bytes(msgstring, "utf-8")
            pubrequest.qos = self.pub_qos
            operation = self.ipc_client.new_publish_to_iot_core()
            operation.activate(pubrequest)
            future = operation.get_response()
            future.result(TIMEOUT)
            print(f"Published to {topic}: {message}")
        except Exception as e:
            print(f"Failed to publish to {topic}: {e}")

    def subscribe(self, callback, topic=None):
        try:
            if not topic:
                topic = self.sub_topic
            if not topic:
                raise ValueError("Subscribe topic not provided")

            handler = SubHandler(callback)
            subrequest = SubscribeToIoTCoreRequest()
            subrequest.topic_name = topic
            subrequest.qos = self.sub_qos
            operation = self.ipc_client.new_subscribe_to_iot_core(handler)
            future = operation.activate(subrequest)
            future.result(TIMEOUT)
            print(f"Subscribed to {topic}")
        except Exception as e:
            print(f"Failed to subscribe to {topic}: {e}")


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
