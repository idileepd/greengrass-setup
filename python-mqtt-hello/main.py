import time
from src.mqtt_utils import GreengrassTopicPublisher, GreengrassTopicSubscriber
from src.rasp_utils import RaspberryPiUtils


print(f"MAC::: {RaspberryPiUtils.get_mac_address()}")
print(f"Serial Number::: {RaspberryPiUtils.get_serial_number()}")


# Initialize MQTT Publisher with a default topic
publisher = GreengrassTopicPublisher(topic="mypi/button")

# Initialize MQTT Subscriber with a default topic
subscriber1 = GreengrassTopicSubscriber(topic="mypi/mqtt1")
subscriber2 = GreengrassTopicSubscriber(topic="mypi/mqtt2")


# Button press callback
def button4pressed():
    message = {"button": "b4pressed", "timemillis": round(time.time() * 1000)}
    publisher.publish(message)


# Subscription message handler for topic 1
def handle_incoming_message1(topic, message):
    print(f"Message from {topic}: {message}")


# Subscription message handler for topic 2
def handle_incoming_message2(topic, message):
    print(f"Message from {topic}: {message}")


# Subscribe to multiple topics
subscriber1.subscribe(handle_incoming_message1)
subscriber2.subscribe(handle_incoming_message2)


# Main loop to simulate button press events for every 10 seconds
while True:
    time.sleep(10)  # Sleep to keep the component running
    button4pressed()
