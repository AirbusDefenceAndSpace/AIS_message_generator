# An NMEA / AIS / AIVDO message generator

This was developed as a means to generate AIS messages from DIS simulation data and to display this data in OpenCPN.
This was not a priority during development and as such was developed in quite a hacky fashion. That beeing said, it seems to work quite well and is to my knowledge currently the only AIS message generator in the entire internet.


# Supported message types

This supports the generation of "Position Report Class A" messages, also known as type 1/2/3:
https://gpsd.gitlab.io/gpsd/AIVDM.html#_types_1_2_and_3_position_report_class_a

And "Static and Voyage Related Data" or Type 5:
https://gpsd.gitlab.io/gpsd/AIVDM.html#_type_5_static_and_voyage_related_data


## Credit / Acknowledgements

- All of this was developed based on the knowledge gathered from [Eric S. Raymonds "AIVDM/AIVDO protocol decoding" article](https://gpsd.gitlab.io/gpsd/AIVDM.html) 
- The checksum calculation is done with [pynmeagps](https://pypi.org/project/pynmeagps/)
- The verification of the results seen in the usage examples is done with the help of [pyais](https://pypi.org/project/pyais/)


## Installation

- Clone this repo
- open the cloned folder in your terminal
- run
```shell
$ pip install -r requirements.txt
```


## Usage

```python
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
```


## ToDo / Roadmaps

There are currently no plans to develop this further


## License

```
Copyright (c) 2021 Airbus Defence and Space, Janis Börsig
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```


### Licenses of dependencies

```
bitarray
2.2.2
Python Software Foundation License
PYTHON SOFTWARE FOUNDATION LICENSE
----------------------------------

1. This LICENSE AGREEMENT is between Ilan Schnell, and the Individual or
Organization ("Licensee") accessing and otherwise using this software
("bitarray") in source or binary form and its associated documentation.

2. Subject to the terms and conditions of this License Agreement, Ilan Schnell
hereby grants Licensee a nonexclusive, royalty-free, world-wide
license to reproduce, analyze, test, perform and/or display publicly,
prepare derivative works, distribute, and otherwise use bitarray
alone or in any derivative version, provided, however, that Ilan Schnell's
License Agreement and Ilan Schnell's notice of copyright, i.e., "Copyright (c)
2008 - 2021 Ilan Schnell; All Rights Reserved" are retained in bitarray
alone or in any derivative version prepared by Licensee.

3. In the event Licensee prepares a derivative work that is based on
or incorporates bitarray or any part thereof, and wants to make
the derivative work available to others as provided herein, then
Licensee hereby agrees to include in any such work a brief summary of
the changes made to bitarray.

4. Ilan Schnell is making bitarray available to Licensee on an "AS IS"
basis.  ILAN SCHNELL MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, ILAN SCHNELL MAKES NO AND
DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF BITARRAY WILL NOT
INFRINGE ANY THIRD PARTY RIGHTS.

5. ILAN SCHNELL SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF BITARRAY
FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING BITARRAY,
OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material
breach of its terms and conditions.

7. Nothing in this License Agreement shall be deemed to create any
relationship of agency, partnership, or joint venture between Ilan Schnell
and Licensee.  This License Agreement does not grant permission to use Ilan
Schnell trademarks or trade name in a trademark sense to endorse or promote
products or services of Licensee, or any third party.

8. By copying, installing or otherwise using bitarray, Licensee
agrees to be bound by the terms and conditions of this License
Agreement.

pyais
1.6.1
MIT License
MIT License

Copyright (c) 2019 M0r13n

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


pynmeagps
1.0.2
BSD License
BSD 3-Clause License ("BSD License 2.0", "Revised BSD License", "New BSD License", or "Modified BSD License")

Copyright (c) 2021, SEMU Consulting
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

```
