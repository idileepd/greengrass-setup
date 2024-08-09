import time
from src.mqtt_utils import MQTTClient

# Initialize MQTT client with default topics
mqtt_client = MQTTClient(pub_topic="pub", sub_topic="sub")


# When you want to publish
def publishEvent():
    message = {"button": "b4pressed", "timemillis": round(time.time() * 1000)}
    mqtt_client.publish(message)


# Subscription message handler
def handle_incoming_message(topic, message):
    print("Got Mesasge::::")
    print(message)
    print("Sub Topic", topic)
    # if message.get("ledon"):
    #     print("Turning on the LED: ", message)
    #     # GPIO.output(18, GPIO.HIGH)  # Uncomment when using GPIO
    # else:
    #     print("Turning off the LED")
    #     # GPIO.output(18, GPIO.LOW)  # Uncomment when using GPIO


# Subscribe to the default topic
mqtt_client.subscribe(handle_incoming_message)

# Main loop to simulate button press events
while True:
    time.sleep(10)  # Sleep to keep the component running
    # Mock invoke assuming an event happened
    publishEvent()  # Calling publish event every 10seconds
