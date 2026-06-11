import time
import pytest
from chat import WebSocketConnection, ConnectionHub, Message


def test_connect_increments_count():
    hub = ConnectionHub()
    hub.connect(WebSocketConnection("c1", "u1"))
    assert hub.active_count() == 1


def test_disconnect_decrements_count():
    hub = ConnectionHub()
    hub.connect(WebSocketConnection("c1", "u1"))
    hub.disconnect("c1")
    assert hub.active_count() == 0


def test_heartbeat_returns_true():
    hub = ConnectionHub()
    hub.connect(WebSocketConnection("c1", "u1"))
    assert hub.heartbeat("c1") is True


def test_heartbeat_missing_returns_false():
    hub = ConnectionHub()
    assert hub.heartbeat("missing") is False


def test_prune_dead_connections():
    hub = ConnectionHub(heartbeat_timeout=0.0)
    conn = WebSocketConnection("c1", "u1")
    conn.last_heartbeat = time.monotonic() - 1
    hub.connect(conn)
    pruned = hub.prune_dead()
    assert "c1" in pruned
    assert hub.active_count() == 0


def test_deliver_to_online_user():
    hub = ConnectionHub()
    hub.connect(WebSocketConnection("c1", "u1"))
    msg = Message(room_id="r1", sender_id="u2", body="hi")
    delivered = hub.deliver("u1", msg)
    assert delivered is True


def test_offline_user_gets_queued():
    hub = ConnectionHub()
    msg = Message(room_id="r1", sender_id="u2", body="hi")
    hub.deliver("offline_user", msg)
    assert hub.offline_queue.has_pending("offline_user")
