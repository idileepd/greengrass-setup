from awsiot.greengrasscoreipc import GreengrassCoreIPCClient
from awsiot.greengrasscoreipc.model import (
    PublishToIoTCoreRequest,
    QOS,
    SubscribeToIoTCoreRequest,
    SubscribeToIoTCoreStreamHandler,
)


# Custom stream handler to process incoming messages on the subscribed topic
class MySubscribeHandler(SubscribeToIoTCoreStreamHandler):
    def on_stream_event(self, event):
        # Print the received message payload
        print(
            f"Received message on topic {event.message.topic_name}: {event.message.payload.decode()}"
        )

    def on_stream_error(self, error):
        # Handle any errors that occur while receiving messages
        print(f"Stream error: {error}")

    def on_stream_closed(self):
        # Clean up or perform any final actions when the stream is closed
        print("Stream closed")


def main():
    # Initialize the IPC client
    client = GreengrassCoreIPCClient()

    try:
        # Publish a message to a topic
        publish_request = PublishToIoTCoreRequest(
            topic_name="topic/to/publish",
            qos=QOS.AT_LEAST_ONCE,
            payload=b"Hello from Greengrass!",
        )
        client.publish_to_iot_core(publish_request)
        print("Message published successfully to 'topic/to/publish'.")

        # Subscribe to a different topic and handle incoming messages
        subscribe_request = SubscribeToIoTCoreRequest(
            topic_name="topic/to/subscribe", qos=QOS.AT_LEAST_ONCE
        )
        handler = MySubscribeHandler()
        client.subscribe_to_iot_core(subscribe_request, handler)
        print("Subscribed to 'topic/to/subscribe'. Waiting for messages...")

        # Keep the script running to listen for incoming messages
        input("Press Enter to exit...\n")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Clean up resources
        client.close()
        print("Client closed.")


if __name__ == "__main__":
    main()
