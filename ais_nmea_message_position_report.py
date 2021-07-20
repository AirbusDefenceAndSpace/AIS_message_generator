import datetime
import struct
from dataclasses import dataclass

import pynmeagps

# Construction of the "Payload Armoring" lookup table:
# https://gpsd.gitlab.io/gpsd/AIVDM.html#_aivdmaivdo_payload_armoring
numbers = [chr(l) for l in range(ord("0"), ord("9") + 1)]
special_characters = [chr(l) for l in range(58, 64 + 1)]
upper_case_letters = [chr(l) for l in range(ord("A"), ord("W") + 1)]
back_tick = chr(96)
lower_case_letters = [chr(l) for l in range(ord("a"), ord("w") + 1)]
niblets = numbers + special_characters + upper_case_letters + [back_tick] + lower_case_letters


# https://gpsd.gitlab.io/gpsd/AIVDM.html#_types_1_2_and_3_position_report_class_a
@dataclass
class Payload:
    message_type: int
    repeat_indicator: int
    mmsi: int
    # 15 = Not defined (default)
    navigation_status: int
    rate_of_turn: int
    speed_over_ground: int
    position_accuracy: bool
    longitude: int
    latitude: int
    course_over_ground: int
    true_heading: int
    # Seconds of UTC timestamp
    time_stamp: int
    # 0 = Not available (default)
    maneuver_indicator: int
    spare: int
    raim_flag: bool
    radio_status: int

    # sizes of the different fields in bits
    size_dict = {
        "message_type": 6,
        "repeat_indicator": 2,
        "mmsi": 30,
        "navigation_status": 4,
        "rate_of_turn": 8,
        "speed_over_ground": 10,
        "position_accuracy": 1,
        "longitude": 28,
        "latitude": 27,
        "course_over_ground": 12,
        "true_heading": 9,
        "time_stamp": 6,
        "maneuver_indicator": 2,
        "spare": 3,
        "raim_flag": 1,
        "radio_status": 19
    }

    # Converts all the fields to bits and gives them back as a concatenated string
    def to_bits_str(self):
        # Determines correct bits for a character based on:
        # https://gpsd.gitlab.io/gpsd/AIVDM.html#_ais_payload_data_types
        # only uppercase characters can be encoded, so this automatically converts lowercase to uppercase
        def six_bit_lookup(char: str) -> str:
            char = char.upper()
            if 64 <= ord(char) <= 95:
                return "{0:b}".format(ord(char) - 64)
            elif 32 <= ord(char) <= 63:
                return "{0:b}".format(ord(char))
            else:
                raise Exception("received char that cant be encoded")

        # determines bits based on the datatype
        def to_bits(val):
            if isinstance(val, int):
                return "{0:b}".format(val)

            if isinstance(val, str):
                out = ""
                for char in val:
                    txt = six_bit_lookup(char)
                    for i in range(6 - len(txt)):
                        txt = "0" + txt
                    print(f"val: {char}, txt: {txt}")
                    out += txt
                return out

            if isinstance(val, bool):
                if val:
                    return "1"
                else:
                    return "0"

            if isinstance(val, float):
                return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', val))

            return False

        out = ""
        for key, val in self.__dict__.items():
            # Strings have to be filled up with trailing @'s
            if isinstance(val, str):
                for i in range(self.size_dict[key] - len(val)):
                    val += "@"

            bits = to_bits(val)

            # Makes sure bits take up correct size
            if len(bits) < self.size_dict[key]:
                padding = "0" * (self.size_dict[key] - len(bits))
                bits = padding + bits
            elif len(bits) > self.size_dict[key]:
                bits = bits[:self.size_dict[key]]
            out += bits

        return out

    def bits_to_nibblets(self, bits: str):
        sections = []
        while len(bits) >= 6:
            sections.append(bits[:6])
            bits = bits[6:]

        out = ""

        for bit_num in sections:
            num = int(bit_num, 2)
            out += niblets[num]

        return out


class NmeaMessage:
    # https://gpsd.gitlab.io/gpsd/AIVDM.html#_types_1_2_and_3_position_report_class_a
    @staticmethod
    def create_payload(mmsi: int, lat: float, lon: float, speed: float, heading: float):
        now = datetime.datetime.now()
        p = Payload(
            message_type=1,
            repeat_indicator=1,
            mmsi=mmsi,
            navigation_status=15,
            rate_of_turn=0,
            speed_over_ground=int(speed * 10),
            position_accuracy=True,
            longitude=int(lon * 600000),
            latitude=int(lat * 600000),
            course_over_ground=(int(heading * 10) + 3600) % 3600,
            true_heading=(int(heading) + 360) % 360,
            time_stamp=int(now.strftime("%S")),
            maneuver_indicator=0,
            spare=0,
            raim_flag=False,
            radio_status=0
        )

        return p.bits_to_nibblets(p.to_bits_str())

    @staticmethod
    def create_NMEA(mmsi: int, lat: float, lon: float, speed: float, heading: float):
        start = "!AIVDM,1,1,,A,"

        pyld = NmeaMessage.create_payload(mmsi, lat, lon, speed, heading)

        start += pyld
        start += ",0*"

        start += pynmeagps.nmeahelpers.calc_checksum(start.replace("!", "$"))

        return start
