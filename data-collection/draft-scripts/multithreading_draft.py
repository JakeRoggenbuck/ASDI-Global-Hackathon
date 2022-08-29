from datetime import date, timedelta
from queue import Queue
from threading import Thread
import httpx
from dataclasses import dataclass


@dataclass
class NCFile:
    year: int
    month: int
    day: int

    hour: int
    min: int

    def fileurl(self):
        return (
            "https://noaa-ghe-pds.s3.amazonaws.com/rain_rate/"
            + f"{self.year}/{str(self.month).zfill(2)}/{str(self.day).zfill(2)}/NPR.GEO.GHE.v1.S"
            + f"{self.year}{str(self.month).zfill(2)}{str(self.day).zfill(2)}"
            + f"{str(self.hour).zfill(2)}{str(self.min).zfill(2)}.nc.gz"
        )

    def filename(self):
        return (
            f"{self.year}{self.month}{self.day}"
            + f"{str(self.hour).zfill(2)}{str(self.min).zfill(2)}.nc.gz"
        )

    def __repr__(self):
        return f"{self.filename()} @ {self.fileurl()}"

    @staticmethod
    def from_date(d: date, hour: int, min: int):
        return NCFile(d.year, d.month, d.day, hour, min)


class Calendar:
    """
    for x in Calendar(date(2020, 1, 1), date(2022, 1, 1)):
        print(x)

    """

    def __init__(
        self,
        start_date: date,
        end_date: date,
        delta: timedelta = timedelta(days=1),
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.delta = delta

        self.current = start_date
        self.current_min = 0
        self.current_hour = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_min + 15 == 60:
            self.current_min = 0

            if self.current_hour + 1 == 24:

                if self.current + self.delta > self.end_date:
                    raise StopIteration

                else:
                    self.current += self.delta
                    self.current_hour = 0
            else:
                self.current_hour += 1
        else:
            self.current_min += 15

        nc = NCFile.from_date(
            self.current,
            self.current_hour,
            self.current_min,
        )

        return nc


def producer(queue, start, end):
    for day in Calendar(start, end):
        queue.put(day)


def consumer(queue):
    while True:
        if queue.empty():
            break

        item = queue.get()

        dirpath = "data/"
        with open(dirpath + item.filename(), "wb") as download_file:
            with httpx.stream("GET", item.fileurl()) as response:
                for chunk in response.iter_bytes():
                    download_file.write(chunk)
                print(f"Downloaded {item.filename()}")


def main():
    queue = Queue()

    start, end = date(2020, 1, 1), date(2020, 1, 5)
    producer(queue, start, end)

    threads = []
    for _ in range(8):
        consumer_thread = Thread(
            target=consumer,
            args=(queue,),
            daemon=True,
        )
        threads.append(consumer_thread)
        consumer_thread.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
