""" module:: tests.test_protocol
    :synopsis: Tests for logging_dlt.protocol in logging-logging_dlt package.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: CC-BY-NC
"""

import logging
import pytest

from datetime import datetime, timedelta

from logging_dlt.protocol import StorageHeader, DltHeaderBit, generate_standard_header, \
    parse_standard_header, get_standard_header_extra_size, parse_standard_header_extra, generate_standard_header_extra, \
    generate_extended_header, parse_extended_header, DltRecordType, DltTraceType, DltControlType, DltPayloadType, \
    generate_payload, parse_payload, DltLogLevel, generate_dlt_log_record, parse_dlt_record, DltRecordIncomplete, \
    DltRecordInvalid

LOGGER = logging.getLogger(__name__)

class TestStorageHeader:
    @pytest.mark.parametrize("timestamp,ecuid",
                             [(datetime.now(), "BEER"),
                              (datetime.now() - timedelta(days=365 * 42), "COLA"),
                              (datetime.now() + timedelta(days=365 * 42), "Tea"),
                              ])
    def test_storage_header(self,
                            timestamp,
                            ecuid):
        data = StorageHeader(ecuid=ecuid, timestamp=timestamp).to_bytes()
        result = StorageHeader.from_bytes(data=data)
        LOGGER.debug("{0},{1} ?= {2}".format(ecuid, timestamp, result))
        assert result.timestamp == timestamp
        assert result.ecuid == ecuid


    def test_parse_storage_header_error(self):
        with pytest.raises(ValueError):
            StorageHeader.from_bytes(bytes(11))


@pytest.mark.parametrize("flags,record_count,record_length,version",
                         [(DltHeaderBit(0), 0, 0, 1),
                          (DltHeaderBit(1), 2, 5, 1),
                          (DltHeaderBit(3), 1, 100, 1),
                          (DltHeaderBit(31), 5, 0x1234, 1),
                          ])
def test_standard_header(flags,
                         record_count,
                         record_length,
                         version):
    data = generate_standard_header(flags=flags,
                                    record_count=record_count,
                                    record_length=record_length,
                                    version=version)
    result = parse_standard_header(data=data)
    assert result.get("flags") == flags
    assert result.get("record_count") == record_count
    assert result.get("record_length") == record_length
    assert result.get("version") == version


def test_parse_standard_header_error():
    data = bytes(((2 << 5), 0, 0, 0))
    with pytest.raises(NotImplementedError):
        parse_standard_header(data=data)
    data = bytes(3)
    with pytest.raises(DltRecordIncomplete):
        parse_standard_header(data=data)


@pytest.mark.parametrize("flags,expected",
                         [(DltHeaderBit.WITH_ECU_ID, 4),
                          (DltHeaderBit.WITH_ECU_ID | DltHeaderBit.WITH_SESSION_ID, 8),
                          (DltHeaderBit.WITH_ECU_ID | DltHeaderBit.WITH_SESSION_ID | DltHeaderBit.WITH_TIMESTAMP, 12),
                          ])
def test_get_standard_header_extra_size(flags,
                                        expected):
    assert get_standard_header_extra_size(flags=flags) == expected


@pytest.mark.parametrize("flags,data, expected",
                         [(DltHeaderBit.WITH_ECU_ID, b"cola", {"ecuid": "cola"}),
                          (DltHeaderBit.WITH_SESSION_ID, b"sess", {"sessionid": "sess"}),
                          (DltHeaderBit.WITH_TIMESTAMP, int(10245).to_bytes(4, "big"), {"timestamp": 1.0245}),
                          (DltHeaderBit.WITH_ECU_ID | DltHeaderBit.WITH_SESSION_ID, b"colasess", {"ecuid": "cola",
                                                                                                  "sessionid": "sess"},),
                          (DltHeaderBit.WITH_ECU_ID | DltHeaderBit.WITH_SESSION_ID | DltHeaderBit.WITH_TIMESTAMP,
                           b"colasess\x00\x00(\x05", {"ecuid": "cola",
                                                      "sessionid": "sess",
                                                      "timestamp": 1.0245},
                           ),
                          ])
def test_parse_standard_header_extra(flags,
                                     data,
                                     expected):
    assert parse_standard_header_extra(flags=flags,
                                       data=data) == expected


def test_parse_standard_header_extra_error():
    with pytest.raises(DltRecordIncomplete):
        # noinspection PyTypeChecker
        parse_standard_header_extra(
            flags=DltHeaderBit.WITH_ECU_ID | DltHeaderBit.WITH_SESSION_ID | DltHeaderBit.WITH_TIMESTAMP,
            data=bytes(3))


@pytest.mark.parametrize("ecuid,sessionid,timestamp",
                         [("cola", "beer", 42.42),
                          (None, None, 1.2),
                          (None, "tea", None),
                          ("milk", None, None),
                          ])
def test_standard_header_extra(ecuid,
                               sessionid,
                               timestamp):
    flags, data = generate_standard_header_extra(ecuid=ecuid,
                                                 sessionid=sessionid,
                                                 timestamp=timestamp)
    result = parse_standard_header_extra(flags=flags,
                                         data=data)
    assert result.get("ecuid") == ecuid
    assert result.get("sessionid") == sessionid
    assert result.get("timestamp") == timestamp


@pytest.mark.parametrize("record_type,number_of_arguments,applicationid,contextid,log_level,command,verbose",
                         [(DltRecordType.LOG, 1, "beer", "bar", DltLogLevel.INFO, None, True),
                          (DltRecordType.LOG, 1, "beer", "bar", DltLogLevel.ERROR, None, True),
                          (DltRecordType.LOG, 1, "beer", "bar", DltLogLevel.DEBUG, None, True),
                          (DltRecordType.APP_TRACE, 2, "tea", "prty", None, DltTraceType.VARIABLE, False),
                          (DltRecordType.CONTROL, 255, "gin", "bar", None, DltControlType.REQUEST, True),
                          (DltRecordType.NW_TRACE, 4, "wine", "home", None, None, True),
                          ])
def test_extended_header(record_type,
                         number_of_arguments,
                         applicationid,
                         contextid,
                         log_level,
                         command,
                         verbose):
    data = generate_extended_header(record_type=record_type,
                                    number_of_arguments=number_of_arguments,
                                    applicationid=applicationid,
                                    contextid=contextid,
                                    log_level=log_level,
                                    command=command,
                                    verbose=verbose
                                    )
    result = parse_extended_header(data)
    assert result.get("record_type") == record_type
    assert result.get("number_of_arguments") == number_of_arguments
    assert result.get("applicationid") == applicationid
    assert result.get("contextid") == contextid
    assert result.get("command") == command
    assert result.get("verbose") == verbose


def test_parse_extended_header_error():
    with pytest.raises(DltRecordIncomplete):
        parse_extended_header(data=bytes(9))

    data = generate_extended_header(record_type=DltRecordType.LOG,
                                    number_of_arguments=4,
                                    applicationid="wine",
                                    contextid="home",
                                    log_level=None,
                                    command=None,
                                    verbose=True)
    data = bytearray(data)
    data[0] |= 0x70  # make subtype invalid
    with pytest.raises(DltRecordInvalid):
        parse_extended_header(data=bytes(data))


@pytest.mark.parametrize("payload_type,payload_text,endianess",
                         [(DltPayloadType.STRING, "HELLO WORLD", "little"),
                          (DltPayloadType.STRING, "HELLO WORLD", "big")
                          ])
def test_payload(payload_type,
                 payload_text,
                 endianess):
    record_type, msb_first, data = generate_payload(payload_type=payload_type,
                                                     payload_text=payload_text,
                                                     endianess=endianess)
    LOGGER.debug(data.hex())
    result = parse_payload(record_type=record_type,
                           msb_first=msb_first,
                           data=data)
    assert result.get("payload_type") == payload_type
    assert result.get("payload_text") == payload_text


def test_payload_error():
    with pytest.raises(ValueError):
        generate_payload(payload_type=DltPayloadType.STRING,
                         payload_text="HELLO WORLD",
                         endianess="someunknownendianess")

    with pytest.raises(NotImplementedError):
        generate_payload(payload_type=DltPayloadType.FLOAT,
                         payload_text="HELLO WORLD",
                         endianess="big")

    record_type, msb_first, data = generate_payload(payload_type=DltPayloadType.STRING,
                                                     payload_text="HELLO WORLD",
                                                     endianess="big")
    with pytest.raises(DltRecordIncomplete):
        parse_payload(record_type=record_type,
                      msb_first=msb_first,
                      data=data[:-2])

    with pytest.raises(NotImplementedError):
        parse_payload(record_type=DltRecordType.CONTROL,
                      msb_first=msb_first,
                      data=data)

    data = bytearray(data)
    data[:4] = (DltPayloadType.FLOAT << 4).to_bytes(4, "big")
    with pytest.raises(NotImplementedError):
        parse_payload(record_type=DltRecordType.LOG,
                      msb_first=msb_first,
                      data=bytes(data))

    data = bytearray(data)
    data[:4] = (0xFFFFFFFF).to_bytes(4, "big")
    with pytest.raises(DltRecordInvalid):
        parse_payload(record_type=DltRecordType.LOG,
                      msb_first=msb_first,
                      data=bytes(data))


@pytest.mark.parametrize("payload_text,ecuid,sessionid,timestamp,applicationid,contextid,endianess",
                         [("Hello World", "ECU1", "SESS", 42.42, "DLT", "INIT", "little"),
                          ("Hello Myself", "ECU2", "SS", 1.0, "DLT", "OUT", "big"),
                          ])
def test_generate_dlt_log_record(payload_text,
                                  ecuid,
                                  sessionid,
                                  timestamp,
                                  applicationid,
                                  contextid,
                                  endianess):
    data = generate_dlt_log_record(payload_text=payload_text,
                                   ecuid=ecuid,
                                   sessionid=sessionid,
                                   timestamp=timestamp,
                                   applicationid=applicationid,
                                   contextid=contextid,
                                   endianess=endianess)
    result = parse_dlt_record(data=data)
    assert result.get("payload_text") == payload_text
    assert result.get("ecuid") == ecuid
    assert result.get("sessionid") == sessionid
    assert result.get("timestamp") == timestamp
    assert result.get("applicationid") == applicationid
    assert result.get("contextid") == contextid
