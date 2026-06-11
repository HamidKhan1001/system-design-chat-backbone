import time
import pytest
from chat import WebSocketConnection, ConnectionState


def test_new_connection_is_connected():
    c = WebSocketConnection("c1", "u1")
    assert c.state == ConnectionState.CONNECTED


def test_heartbeat_updates_state():
    c = WebSocketConnection("c1", "u1")
    c.last_heartbeat = time.monotonic() - 100
    c.beat()
    assert not c.is_stale(30.0)


def test_stale_detection():
    c = WebSocketConnection("c1", "u1")
    c.last_heartbeat = time.monotonic() - 60
    assert c.is_stale(30.0) is True


def test_mark_dead():
    c = WebSocketConnection("c1", "u1")
    c.mark_dead()
    assert c.state == ConnectionState.DEAD


def test_fresh_connection_not_stale():
    c = WebSocketConnection("c1", "u1")
    assert c.is_stale(30.0) is False
