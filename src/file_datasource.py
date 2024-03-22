from __future__ import annotations

from datetime import datetime
from typing import TextIO

import config
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking


class FileDatasource:
    accelerometer_file: TextIO
    gps_file: TextIO
    parking_file: TextIO

    accelerometer_filename: str
    gps_filename: str
    parking_filename: str

    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        self.accelerometer_file, acc_data = FileDatasource.__get_next_line(self.accelerometer_file, int)
        self.gps_file, gps_data = FileDatasource.__get_next_line(self.gps_file, float)
        self.parking_file, parking_data = FileDatasource.__get_next_line(self.parking_file, float)

        return AggregatedData(
            Accelerometer(acc_data[0], acc_data[1], acc_data[2]),
            Gps(gps_data[0], gps_data[1]),
            Parking(int(parking_data[0]), Gps(parking_data[1], parking_data[2])),
            datetime.now(),
            config.USER_ID,
        )

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        self.parking_file = open(self.parking_filename, 'r')

        self.accelerometer_file.readline()
        self.gps_file.readline()
        self.parking_file.readline()

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        self.accelerometer_file.close()
        self.gps_file.close()
        self.parking_file.close()

    @staticmethod
    def __get_next_line(file: TextIO, datatype: type) -> tuple[TextIO, list[float|int]]:
        line = file.readline()
        if not line or len(line) == 0:
            fl_name = file.name
            file.close()
            file = open(fl_name, 'r')

            file.readline()
            line = file.readline()

        return file, [datatype(num) for num in line.split(',')]
