""" module:: GammaHeatingControl.protocol
    :platform: Any
    :synopsis: The protocol description used by EBC Gamma RS-485 bus.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3

    Note: This work is based on https://github.com/bogeyman/gamma/wiki/Protokoll ,
          Not everything there is correct though.
          In my case the communication has 0xFF on every second byte
"""
import logging
from datetime import datetime
from enum import IntEnum, IntFlag
from queue import Queue
from typing import Union, Optional

from crccheck.crc import CrcKermit

LOGGER = logging.getLogger(__name__)


class FrameType(IntEnum):
    BusClaim = 0
    UnknownType1 = 1
    UnknownType2 = 2
    UnknownType3NeverSeen = 3
    HeaterInfo = 4
    TimeAndDate = 5
    RoomStationInfo = 6


class BusAddress(IntEnum):
    Master = 0x10
    Heater = 0x20
    RoomStation1 = 0x21
    Unknown0xAA = 0xAA


class InfoFlags(IntFlag):
    Unkown0x01 = 1
    Unkown0x02 = 2
    Unkown0x04 = 4
    Unkown0x08 = 8
    Unkown0x10 = 0x10
    Unkown0x20 = 0x20
    Unkown0x40 = 0x40
    Unkown0x80 = 0x80


class InfoFlags2(IntFlag):
    Unkown0x01 = 1
    Unkown0x02 = 2
    Unkown0x04 = 4
    Unkown0x08 = 8
    Unkown0x10 = 0x10
    Unkown0x20 = 0x20
    Unkown0x40 = 0x40
    Unkown0x80 = 0x80


def parse_time_and_date_frame_data(data: bytes) -> dict:
    """
    Parse the Time and Date Frame.

    Format
    * 1st byte flags
    * 2nd byte seconds BCD format
    * 3rd byte minute BCD format
    * 4th byte hour BCD format
    * 5th byte day of month BCD format
    * 6th byte high nibble month (single digit 1=January up to 0xC=December)
    * 6th byte low nibble day of week (0=Monday up to 6=Sunday)
    * 7th byte year + 2000
    * 8th byte day of week (0=Sunday up to 6 Saturday)
    * 9th byte month BCD format

    Example:
    00 03 56 17 19 71 22 02 07 -->  17:56:03 19.07.2022

    Special Version, 6 bytes longer, if RS10 is installed, 6 unknown bytes trailing:
    00 58 28 11 16 95 23 06 09 40 00 81 97 64 64 55

    :param data: The Data in proprietary format.
    :return: A dictionary with keys info_flags and time
    """
    info_flags = InfoFlags(data[0])
    seconds = int(data[1:2].hex())
    minute = int(data[2:3].hex())
    hour = int(data[3:4].hex())
    day = int(data[4:5].hex())
    month = int(data[8:9].hex())
    year = int(data[6:7].hex()) + 2000
    day_of_week = data[7]

    result = {"info_flags": info_flags,
              "time": datetime(year=year,
                               month=month,
                               day=day,
                               hour=hour,
                               minute=minute,
                               second=seconds
                               ),
              }

    if len(data) > 9:
        info_flags2 = InfoFlags2(data[9])
        unknown_value11 = data[11]  # seen change 0x6E -> 0x6D
        unknown_value12 = data[12]  # seen increasing 113 -> 114 presumable after target room temperature reached
        result.update({"info_flags2": info_flags2,
                       "heating_curve_offset?": unknown_value11,
                       "heating_curve_offset?": unknown_value12})

    return result


def parse_heater_info_frame_data(data: bytes) -> dict:
    """
    Parse the Heater Info Frame.

    Format
    * 1st byte environment temperature, scaling 0.5 degC, offset 52
    * 15th byte mixer measured temperature, scaling 0.5 degC
    * 16th byte heater target temperature, scaling 0.5 degC
    * 17th byte burner enabled flag, bool
    * 26th byte burner error flag, bool, correlates with the red error indicator
      does indicate a failure of the real burning control unit,
      https://drive.google.com/file/d/1W70URIbawd4oCCIZWKSd3RKz2qO3TbzM/view
      is needed to figure out what the problem is
    * 31st byte heater measured temperature, scaling 0.5 degC

    :param data: The Data in proprietary format.
    :return: A dictionary with the parsed values.
    """

    environment_temperature = (data[0] / 2) - 52
    mixer_measured_temperature = (data[15] / 2) - 16  # 'mixer_measured_temperature': -16.0} ?! something wrong here
    burner_enabled = bool(data[17])
    burner_error = bool(data[26])
    heater_measured_temperature = (data[30] / 2)

    return {"environment_temperature": environment_temperature,
            "mixer_measured_temperature": mixer_measured_temperature,
            "burner_enabled": burner_enabled,
            "burner_error": burner_error,
            "heater_measured_temperature": heater_measured_temperature,
            }


def parse_room_station_info_frame_data(data: bytes) -> dict:
    """
    Parse the Room Station Info Frame.

    Format
    * 1st byte room temperature, scaling 0.5 degC

    When looking at this frame in hex, it is observed that there is some repeating scheme, that could resemble
    a heating time plan
    Time + Duration + Temperature.

    ts: 2023-10-15 08:58:32.226000
    hex: 29002a00000000002a0000000042000a0001112a200000000002002a200000000001002a20000000

    002a00000000
    002a00000000
    42000a000111
    2a20000000000200
    2a20000000000100
    2a20000000

    :param data: The Data in proprietary format.
    :return: A dictionary with the parsed values.
    """
    room_temperature = data[0] / 2

    return {"room_temperature": room_temperature}


def parse_bus_claim_frame_data(data: bytes) -> dict:
    """
    Parse the Bus Claim Frame.

    It is observed that all physical devices send messages of this type
    to a "virtual" device 0xAA and either claim the Bus or not.
    This is a blunt guess for now.

    Format
    * 1st byte Bus Claimed Flag

    :param data: The Data in proprietary format.
    :return: A dictionary with the parsed values.
    """

    bus_claimed = bool(data[0])

    return {"bus_claimed": bus_claimed}


def parse_frame_data(frame_dict: dict) -> dict:
    _mapping_ = {FrameType.HeaterInfo: parse_heater_info_frame_data,
                 FrameType.TimeAndDate: parse_time_and_date_frame_data,
                 FrameType.RoomStationInfo: parse_room_station_info_frame_data,
                 FrameType.BusClaim: parse_bus_claim_frame_data,
                 }
    frame_type = frame_dict.get("type")
    data = frame_dict.get("data")
    parser_function = _mapping_.get(frame_type)
    if parser_function is None:
        raise ValueError("No Parser for FrameType {0}".format(FrameType))
    return parser_function(data=data)


def parse_frame(frame: Union[bytes, bytearray]) -> Optional[dict]:
    """
    Parse a data frame into its contents.

    :param frame: The raw frame data.
    :type frame: bytes,bytearray
    :return: The contents.
    :rtype: dict
    :raises: ValueError
    """
    if not all([frame.startswith(b"\x82"),  # start marker
                frame.endswith(b"\x03"),  # end marker
                (len(frame) > 8),  # absolute minimum, start + dest + src + length + >=1byte of data + 2bytes crc + end
                ]):
        raise ValueError("Broken Envelope on frame {0}".format(frame.hex()))
    frame_without_envelope = frame[1:-1]
    sender, receiver, frame_advertised_length = frame_without_envelope[:3]

    frame_data = frame_without_envelope[4:-2]
    if len(frame_data) != frame_advertised_length:
        raise ValueError("Frame incomplete missing at least {0} bytes".format(
            frame_advertised_length - len(frame_data)))

    frame_crc = int.from_bytes(frame_without_envelope[-2:], "little")
    calc_crc = CrcKermit.calc(data=frame_without_envelope[:-2])
    if frame_crc != calc_crc:
        raise ValueError("Broken CRC exp {0} != {1} act".format(frame_crc, calc_crc))

    try:
        receiver = BusAddress(receiver)
    except ValueError:
        LOGGER.error("Not a known BusAddress 0x{0:X}".format(receiver))

    try:
        sender = BusAddress(sender)
    except ValueError:
        LOGGER.error("Not a known BusAddress 0x{0:X}".format(sender))

    return {"raw": frame,
            "receiver": receiver,
            "sender": sender,
            "type": FrameType(frame_without_envelope[3]),
            "data": frame_data}


class FrameExtractor:

    def __init__(self):
        self._buffer = bytearray()
        self._out_queue = Queue()

    def put(self, data: bytes):
        self._buffer.extend(filter(lambda x: x != 0xFF, data))
        # For whatever reason, the logs recorded on my devices contain 0xFF values
        # which are not shown in bogeyman's logs
        # LOGGER.debug("Added {0} bytes".format(len(data)))
        self._consume_buffer()

    def _consume_buffer(self):
        start_idx = -1
        stop_idx = start_idx
        start_code = 0x82
        stop_code = 0x03
        while start_code in self._buffer[start_idx + 1:]:
            start_idx = self._buffer.index(start_code, start_idx + 1)
            stop_idx = start_idx
            while stop_code in self._buffer[stop_idx + 1:]:
                stop_idx = self._buffer.index(stop_code, stop_idx + 1)
                try:
                    result = parse_frame(self._buffer[start_idx:stop_idx + 1])
                except ValueError:
                    pass
                else:
                    self._out_queue.put(result)
                    break
        self._buffer = self._buffer[stop_idx:]

    def get(self, timeout):
        return self._out_queue.get(timeout=timeout)

    def get_no_wait(self):
        return self._out_queue.get_nowait()
