# Message types

Every ENet packet starts with a little-endian `u32` message type:

| Value | Name | Direction | Body |
|---|---|---|---|
| 1 | [SERVER_HELLO](/messages/1-server-hello) | server → client | nothing: "send your login" |
| 2 | [GENERIC_TEXT](/messages/2-generic-text) | client → server | login text |
| 3 | [GAME_MESSAGE](/messages/3-game-message) | both | `action|...` text |
| 4 | [GAME_PACKET](/messages/4-game-packet) | both | 56-byte header + extra data |
| 5–8 | ERROR, TRACK, CLIENT_LOG_REQUEST/RESPONSE | | unused by both servers |

## Text messages (types 2 and 3)

```text
[u32 type][key|value\nkey|value\n ...][\0]
```

- Lines are `key|value`, separated by `\n`.
- One trailing NUL byte. gurotopia drops the last byte (`receive.cpp`: `data.end() - 1`), so leaving it
  out cuts off your last character.
- gurotopia turns every `\n` into `|` and reads the result as pairs, so `action|drop\n|itemID|2\n`
  and `action|drop\nitemID|2\n` mean the same thing. The client uses both styles; each action page
  shows the exact one.

```cpp
void send_text(int type, const std::string &text)
{
    std::vector<unsigned char> data(4 + text.size() + 1, 0);
    memcpy(data.data(), &type, 4);
    memcpy(data.data() + 4, text.data(), text.size());
    enet_peer_send(server, 0, enet_packet_create(data.data(), data.size(), ENET_PACKET_FLAG_RELIABLE));
}
```
