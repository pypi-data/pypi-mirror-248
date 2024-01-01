""" module:: tests.test_adapter
    :synopsis: Tests for logging_dlt.adapter in logging-logging_dlt package.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: CC-BY-NC
"""
import time
from pathlib import Path
from queue import Queue, Empty

import pytest

from logging_dlt.adapter import SerialDltStreamLogAdapter, SocketDltStreamLogAdapter
from logging_dlt.protocol import DltRecordType, DEFAULT_DLT_PORT
from tests.mocks import SerialDltMock, SocketDltMock

from logging import LogRecord, getLogger, Filter, Formatter
from logging.handlers import QueueHandler


@pytest.fixture(scope="session")
def mock_dlt_socket() -> SocketDltMock:
    mock = SocketDltMock()
    yield mock


@pytest.fixture(scope="session")
def mock_dlt_serial() -> SerialDltMock:
    mock = SerialDltMock()
    yield mock


@pytest.fixture(scope="session")
def dlt_serial_adapter(mock_dlt_serial) -> SerialDltStreamLogAdapter:
    dlt_adapter = SerialDltStreamLogAdapter(ser=mock_dlt_serial)
    yield dlt_adapter


@pytest.fixture(scope="session")
def dlt_socket_adapter() -> SocketDltStreamLogAdapter:
    dlt_adapter = SocketDltStreamLogAdapter(host="localhost", port=3490)
    yield dlt_adapter


# @pytest.fixture(scope="session")
# def traffic_file():
#     filename = "traffic.bin"
#     with open(filename, "wb") as f:
#         for idx in range(100):
#             f.write(DLT_MAGIC_SERIAL)
#             f.write(generate_dlt_log_record(payload_text="message NO {0}".format(idx),
#                                             ecuid="ECU1",
#                                             sessionid="SESS",
#                                             timestamp=0.1,
#                                             applicationid="APP1",
#                                             contextid="CONT",
#                                             endianess="little"))
#     yield filename


class TestConstructorErrors:
    def test_value_errors(self):
        with pytest.raises(ValueError):
            SocketDltStreamLogAdapter(host="localhost")
        with pytest.raises(ValueError):
            SocketDltStreamLogAdapter(port=DEFAULT_DLT_PORT)
        with pytest.raises(ValueError):
            SerialDltStreamLogAdapter()


class TestDltSerialLogAdapter:
    def test_obj_gen(self, mock_dlt_serial, dlt_serial_adapter):
        mock_dlt_serial.cause_resync_to_dlt_magic()
        mock_dlt_serial.cause_incomplete_record_read()
        mock_dlt_serial.cause_invalid_record_read()
        mock_dlt_serial.cause_invalid_payload_read()
        logger = getLogger("logging_dlt")
        filter_ = Filter(name="logging_dlt.ECU1")
        q = Queue()
        handler = QueueHandler(queue=q)
        handler.addFilter(filter=filter_)
        logger.addHandler(handler)
        result: LogRecord = q.get(timeout=1)
        print(result)
        assert result
        assert result.getMessage() == "some_test"
        assert result.levelname == "INFO"
        time.sleep(1)

    def test_level_none(self, mock_dlt_serial, dlt_serial_adapter):
        logger = getLogger("logging_dlt")
        mock_dlt_serial.cause_silence()
        filter_ = Filter(name="logging_dlt.ECU1")
        q = Queue()
        handler = QueueHandler(queue=q)
        handler.addFilter(filter=filter_)
        logger.addHandler(handler)

        with pytest.raises(Empty):
            q.get_nowait()

        dlt_serial_adapter.handle({"record_type": DltRecordType.LOG,
                                   "payload_text": "defect_message",
                                   })


class TestDltSocketLogAdapter:
    def test_obj_gen(self, mock_dlt_socket, dlt_socket_adapter):
        mock_dlt_socket.cause_resync_to_dlt_magic()
        mock_dlt_socket.cause_incomplete_record_read()
        logger = getLogger("logging_dlt")
        filter_ = Filter(name="logging_dlt.ECU1")
        q = Queue()
        handler = QueueHandler(queue=q)
        handler.addFilter(filter=filter_)
        logger.addHandler(handler)
        result: LogRecord = q.get(timeout=1)
        print(result)
        assert result
        assert result.getMessage() == "some_test"
        assert result.levelname == "INFO"

    def test_level_none(self, mock_dlt_socket, dlt_socket_adapter):
        logger = getLogger("logging_dlt")
        mock_dlt_socket.cause_silence()
        filter_ = Filter(name="logging_dlt.ECU1")
        q = Queue()
        handler = QueueHandler(queue=q)
        handler.addFilter(filter=filter_)
        logger.addHandler(handler)

        with pytest.raises(Empty):
            q.get_nowait()

        dlt_socket_adapter.handle({"record_type": DltRecordType.LOG,
                                   "payload_text": "defect_message",
                                   })

    def test_with_formatter(self, mock_dlt_socket, dlt_socket_adapter):
        """
        A simple test for using a formatter with a logging_dlt adapter
        :param mock_dlt_socket: fixture
        :param dlt_socket_adapter: fixture
        :return: Nothing.
        """
        formatter = Formatter('%(asctime)s - %(timestamp)s - %(levelname)s - %(message)s')
        logger = getLogger("logging_dlt")
        filter_ = Filter(name="logging_dlt.ECU1")
        q = Queue()
        handler = QueueHandler(queue=q)
        handler.addFilter(filter=filter_)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        result: LogRecord = q.get(timeout=1)
        print(result)

    @pytest.mark.parametrize("filename,expected", [
        ("message_100.bin", 100),
        # ("traffic_last_message_incomplete.bin", 100),
    ])
    def test_with_file(self, filename, expected):
        formatter = Formatter('%(asctime)s - %(timestamp)s - %(levelname)s - %(message)s')
        logger = getLogger("logging_dlt")
        q = Queue()
        handler = QueueHandler(queue=q)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        file_obj = list(Path(".").glob("**/data/{0}".format(filename)))[0]
        mock = SerialDltMock(file=file_obj)
        adapter = SerialDltStreamLogAdapter(ser=mock)
        actual = 0
        for i in range(expected):
            try:
                result: LogRecord = q.get(timeout=.01)
                actual += 1
            except Empty:
                pass
        assert actual == expected
