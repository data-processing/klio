# Copyright 2020 Spotify AB

import logging

import pytest

from klio_core.proto import klio_pb2

import transforms


@pytest.fixture
def caplog(caplog):
    """Set global test logging levels."""
    caplog.set_level(logging.DEBUG)
    return caplog


@pytest.fixture
def klio_msg():
    element = b"s0m3_tr4ck_1d"
    msg = klio_pb2.KlioMessage()
    msg.data.element = element
    msg.version = klio_pb2.Version.V2
    return msg


@pytest.fixture
def expected_log_messages(klio_msg):
    return [
        "Received element {}".format(klio_msg.data.element),
        "Received payload {}".format(klio_msg.data.payload),
    ]


def test_process(klio_msg, expected_log_messages, caplog):
    helloklio_fn = transforms.LogKlioMessage()
    output = helloklio_fn.process(klio_msg.SerializeToString())

    assert klio_msg.SerializeToString() == list(output)[0]

    for index, record in enumerate(caplog.records):
        assert "INFO" == record.levelname
        assert expected_log_messages[index] == record.message