# system-design-chat-backbone

Real-time state synchronization and messaging architecture for massive chat (WhatsApp/Discord scale). Manages millions of persistent WebSocket connections with heartbeat pruning and offline message queuing.

## Architecture

```
Client ──WebSocket──► ConnectionHub
                           │
              ┌────────────┼────────────────┐
              │            │                │
        connect()    heartbeat()       prune_dead()
              │            │           (removes stale connections)
              │            │
         ChatRoom.send()
              │
         ┌───┴───────────────────┐
         │ user online?          │
         │   YES → deliver()     │
         │   NO  → OfflineQueue  │
         └───────────────────────┘
                  │ user reconnects
              drain() → flush pending messages
```

## Deep-dive metrics

| Concern | Solution |
|---------|---------|
| Millions of connections | Per-connection state in dict (O(1) lookup) |
| Dead connection detection | Heartbeat timeout: last_heartbeat > 30s → prune |
| Offline messages | Per-user deque, max 500 msgs, drained on reconnect |
| Message ordering | Timestamps on every Message, history list per room |

## Heartbeat pruning

```python
hub.prune_dead()  # called on schedule (e.g., every 10s)
# removes connections with last_heartbeat > timeout_seconds ago
# marks them ConnectionState.DEAD before deletion
```

## Running tests

```bash
pip install -r requirements.txt
python3 -m pytest tests/ -v   # 22 tests
```
