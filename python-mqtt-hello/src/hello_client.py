from awsiot import greengrasscoreipc
from awsiot.greengrasscoreipc import model
import json
from time import gmtime, strftime


class HelloClient:
    def __init__(self, message: str):
        self._client = greengrasscoreipc.connect()
        self._message = json.dumps(
            {"message": message, "time": strftime("%Y-%m-%d %H:%M:%S", gmtime())}
        )
        self._subscription = None

    def subscribe(self):
        # Create a stream handler function
        def stream_handler(event: model.SubscribeToIoTCoreResponse):
            print(":::::Received message from 'hello' topic:", event.payload.decode())

        # Create a subscription to the 'hello' topic
        self._subscription = self._client.new_subscribe_to_iot_core()
        self._subscription.activate(
            model.SubscribeToIoTCoreRequest(
                topic_name="hello", qos=model.QOS.AT_LEAST_ONCE
            ),
            stream_handler=stream_handler,
        )

        # Handle the subscription response
        try:
            response = self._subscription.get_response().result(timeout=5.0)
            print(":::::Successfully subscribed to 'hello' topic.", response)
        except Exception as e:
            print("Failed to subscribe to 'hello' topic:", e)

    def tick(self):
        op = self._client.new_publish_to_iot_core()
        op.activate(
            model.PublishToIoTCoreRequest(
                topic_name="hello",
                qos=model.QOS.AT_LEAST_ONCE,
                payload=self._message.encode(),
            )
        )
        try:
            result = op.get_response().result(timeout=5.0)
            print("::::Successfully published message:", result)
        except Exception as e:
            print(":::::Failed to publish message:", e)
