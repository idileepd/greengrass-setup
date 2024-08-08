import sys
import time
import datetime
from src.hello_client import HelloClient
import logging


def main():
    try:
        args = sys.argv[1:]
        client = HelloClient(args[0])

        print("")
        # Subscribe to the 'hello' topic
        client.subscribe()

        times = 5
        print("Started ::::", datetime.datetime.now(tz=None))
        while times > 0:
            client.tick()
            time.sleep(5)
            times = times - 1
    except Exception as e:
        logging.error("\n\n>>>error:::", e)


if __name__ == "__main__":
    main()
