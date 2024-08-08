import sys
import time
import datetime
from src.hello_client import HelloClient


def main():
    args = sys.argv[1:]
    client = HelloClient(args[0])
    times = 5
    print("Started ::::", datetime.datetime.now(tz=None))

    while times > 0:
        client.tick()
        time.sleep(5)
        times = times - 1


if __name__ == "__main__":
    main()
