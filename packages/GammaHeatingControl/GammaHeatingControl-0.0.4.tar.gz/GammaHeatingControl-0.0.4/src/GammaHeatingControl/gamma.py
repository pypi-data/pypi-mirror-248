""" module:: GammaHeatingControl.gamma
    :platform: Any
    :synopsis: The Reader object.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from queue import Empty
from threading import Thread

from GammaHeatingControl.protocol import FrameExtractor
from serial import Serial

logging.basicConfig(
    handlers=[
        RotatingFileHandler(filename=Path.home() / "gamma_heating_control.log",
                            maxBytes=5 * 1024 * 1024,  # 5MiB
                            backupCount=2)],
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    level=logging.DEBUG)


class GammaBaseReader:

    def __init__(self, ser: Serial):
        self._ser = ser
        self._logger = logging.getLogger(__name__)
        self._frame_extractor = FrameExtractor()
        self._rx_queue_handler = Thread(target=self.handle_rx)
        self._rx_queue_handler.daemon = True
        self._rx_queue_handler.start()

    def handle_rx(self):
        while True:
            buff = bytearray()
            data = self._ser.read(1)
            if len(data) > 0:
                buff.extend(data)
                buff.extend(self._ser.read(self._ser.inWaiting()))
                self._frame_extractor.put(buff)

    def get(self, timeout: float):
        return self._frame_extractor.get(timeout=timeout)

    def get_no_wait(self):
        return self._frame_extractor.get_no_wait()


class GammaFrameLogger(GammaBaseReader):

    def __init__(self, ser: Serial):
        super().__init__(ser)
        self._log_writer = Thread(target=self.write_log)
        self._log_writer.daemon = True
        self._log_writer.start()

    def write_log(self):
        last_frame_data = None
        while True:
            try:
                frame = self.get(timeout=1.0)
            except Empty:
                pass
            else:
                if frame.get("raw") != last_frame_data:
                    last_frame_data = frame.get("raw")
                    self._logger.info(last_frame_data.hex())
