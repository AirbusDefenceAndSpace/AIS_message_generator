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


# https://gpsd.gitlab.io/gpsd/AIVDM.html#_type_5_static_and_voyage_related_data
@dataclass
class Payload:
    message_type: int
    repeat_indicator: int
    mmsi: int
    ais_version: int
    imo_number: int
    call_sign: str
    vessel_name: str
    ship_type: int
    dimensions_to_bow: int
    dimensions_to_stern: int
    dimensions_to_port: int
    dimensions_to_starboard: int
    position_fix_type: int
    # 1-12, 0=N/A (default)
    eta_month_utc: int
    # 1-31, 0=N/A (default)
    eta_day_utc: int
    # 0-23, 24=N/A (default)
    eta_hour_utc: int
    # 0-59, 60=N/A (default)
    eta_minute_utc: int
    draught: int
    destination: str
    dte: int
    spare: int

    # sizes of the different fields in bits
    size_dict = {
        "message_type": 6,
        "repeat_indicator": 2,
        "mmsi": 30,
        "ais_version": 2,
        "imo_number": 30,
        "call_sign": 42,
        "vessel_name": 120,
        "ship_type": 8,
        "dimensions_to_bow": 9,
        "dimensions_to_stern": 9,
        "dimensions_to_port": 6,
        "dimensions_to_starboard": 6,
        "position_fix_type": 4,
        "eta_month_utc": 4,
        "eta_day_utc": 5,
        "eta_hour_utc": 5,
        "eta_minute_utc": 6,
        "draught": 8,
        "destination": 120,
        "dte": 1,
        "spare": 1,
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

    # splits bitstring into 6 bit nibblets and converts them based on the lookup table
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
    # https://gpsd.gitlab.io/gpsd/AIVDM.html#_type_5_static_and_voyage_related_data
    @staticmethod
    def create_payload(mmsi: int, imo_number: int, call_sign: str, ship_name: str, dimensions_to_bow: int = 10,
                       dimensions_to_stern: int = 10,
                       dimensions_to_port: int = 10, dimensions_to_starboard: int = 10, ship_type: int = 0,
                       destination: str = "Mallorca",
                       draught: int = 10):
        now = datetime.datetime.now()
        p = Payload(
            message_type=5,
            repeat_indicator=1,
            mmsi=mmsi,
            ais_version=0,
            imo_number=imo_number,
            call_sign=call_sign,
            vessel_name=ship_name,
            ship_type=ship_type,
            dimensions_to_bow=dimensions_to_bow,
            dimensions_to_stern=dimensions_to_stern,
            dimensions_to_port=dimensions_to_port,
            dimensions_to_starboard=dimensions_to_starboard,
            position_fix_type=0,
            eta_month_utc=int(now.month),
            eta_day_utc=int(now.day),
            eta_hour_utc=int(now.hour),
            eta_minute_utc=int(now.minute),
            draught=draught,
            destination=destination,
            dte=0,
            spare=0
        )

        return p.bits_to_nibblets(p.to_bits_str())

    @staticmethod
    def create_NMEA(mmsi: int, imo_number: int, call_sign: str, ship_name: str, dimensions_to_bow: int = 10,
                    dimensions_to_stern: int = 10,
                    dimensions_to_port: int = 10, dimensions_to_starboard: int = 10, ship_type: int = 0,
                    destination: str = "Mallorca",
                    draught: int = 10):
        msg = "!AIVDM,1,1,,A,"

        pyld = NmeaMessage.create_payload(mmsi, imo_number, call_sign, ship_name, dimensions_to_bow,
                                          dimensions_to_stern, dimensions_to_port,
                                          dimensions_to_starboard, ship_type, destination, draught)

        msg += pyld
        msg += ",0*"

        msg += pynmeagps.nmeahelpers.calc_checksum(msg.replace("!", "$"))

        return msg
