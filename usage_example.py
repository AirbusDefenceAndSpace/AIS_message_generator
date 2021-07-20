# Used to verify the resulting NMEA message
import pyais

# https://gpsd.gitlab.io/gpsd/AIVDM.html#_types_1_2_and_3_position_report_class_a
# Type 1/2/3 message:
import ais_nmea_message_position_report

message = ais_nmea_message_position_report.NmeaMessage.create_NMEA(mmsi=1234, lat=26.46, lon=19.27, speed=11.67,
                                                                   heading=155.55)
print(message)

# Verification:
print(pyais.decode_msg(message))

print("\n---------------------------------------------\n")

# https://gpsd.gitlab.io/gpsd/AIVDM.html#_type_5_static_and_voyage_related_data
# Type 5 message:
import ais_nmea_message_static_and_voyage

message = ais_nmea_message_static_and_voyage.NmeaMessage.create_NMEA(mmsi=1234,
                                                                     imo_number=1234,
                                                                     call_sign="Carl",
                                                                     ship_name="Frederic",
                                                                     dimensions_to_bow=10,
                                                                     dimensions_to_stern=10,
                                                                     dimensions_to_port=10,
                                                                     dimensions_to_starboard=10,
                                                                     ship_type=0,
                                                                     destination="Mallorca",
                                                                     draught=10)
print(message)

# Verification:
print(pyais.decode_msg(message))
