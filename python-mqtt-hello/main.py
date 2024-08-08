import sys
import time
import datetime
from src.hello_client import HelloClient


def main():
    print("\n\n\n::::: MAIN Started")
    # try:
    #     args = sys.argv[1:]
    #     client = HelloClient(args[0])

    #     print(">>>>> About to sub")
    #     # Subscribe to the 'hello' topic
    #     # client.subscribe()

    #     times = 20
    #     print("Started ::::", datetime.datetime.now(tz=None))
    #     while times > 0:
    #         client.tick()
    #         time.sleep(5)
    #         times = times - 1
    # except Exception as e:
    #     print("ERRORRR :::::: \n\n")
    #     print(e)


if __name__ == "__main__":
    main()
