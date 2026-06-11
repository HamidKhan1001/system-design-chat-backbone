import pytest
from chat import OfflineMessageQueue, Message


def test_enqueue_and_drain():
    q = OfflineMessageQueue()
    msg = Message(room_id="r1", sender_id="u1", body="hello")
    q.enqueue("u2", msg)
    drained = q.drain("u2")
    assert len(drained) == 1
    assert drained[0].body == "hello"


def test_drain_clears_queue():
    q = OfflineMessageQueue()
    q.enqueue("u1", Message("r1", "s1", "m"))
    q.drain("u1")
    assert q.pending_count("u1") == 0


def test_pending_count():
    q = OfflineMessageQueue()
    for i in range(3):
        q.enqueue("u1", Message("r1", "s", f"msg{i}"))
    assert q.pending_count("u1") == 3


def test_has_pending_false_for_new_user():
    q = OfflineMessageQueue()
    assert q.has_pending("new_user") is False


def test_max_per_user_cap():
    q = OfflineMessageQueue(max_per_user=3)
    for i in range(10):
        q.enqueue("u1", Message("r1", "s", f"m{i}"))
    assert q.pending_count("u1") == 3
