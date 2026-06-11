import pytest
from chat import WebSocketConnection, ConnectionHub, ChatRoom, Message


@pytest.fixture
def hub():
    return ConnectionHub()


@pytest.fixture
def room(hub):
    return ChatRoom("room1", hub)


def test_join_increments_members(room):
    room.join("u1")
    assert room.member_count == 1


def test_leave_decrements_members(room):
    room.join("u1")
    room.leave("u1")
    assert room.member_count == 0


def test_message_stored_in_history(room):
    room.join("u1")
    msg = Message("room1", "u1", "hello")
    room.send(msg)
    assert len(room.history) == 1


def test_sender_not_in_own_delivery(hub, room):
    hub.connect(WebSocketConnection("c1", "u1"))
    room.join("u1")
    msg = Message("room1", "u1", "self msg")
    delivered = room.send(msg)
    assert delivered == 0


def test_deliver_to_online_member(hub, room):
    hub.connect(WebSocketConnection("c1", "u2"))
    room.join("u1")
    room.join("u2")
    msg = Message("room1", "u1", "hi u2")
    delivered = room.send(msg)
    assert delivered == 1
