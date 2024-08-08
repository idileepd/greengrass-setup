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
            print("Successfully published message:", result)
        except Exception as e:
            print("Failed to publish message:", e)
