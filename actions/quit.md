# action|quit

<Badge type="info" text="GAME_MESSAGE (3)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|quit
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** the client sends `action|quit` with **no** trailing `\n`, as message type 3 (GAME_MESSAGE).

Sent by the network client's disconnect routine just before it closes the connection on purpose: logging out,
switching to beta mode, the world screen's Back button, returning to the main menu.

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| text | `action\|quit` |

- Only if a peer exists; the connection state then becomes 5 (closing) and the peer is dropped 500 ms later.

<small>Builder: `0x11424bc`; called from `0x11422cc`, `0x136b858` (OnLogout), `0x1370668` (OnSetBetaMode), `0x1372d28`, `0x1ba33d4`, `0x1c16adc`.</small>

## Server

gurotopia: [`include/action/quit.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/quit.cpp).

Reply: The server disconnects the peer.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(3, "action|quit");
```

<small>Client function: `0x11424bc` in libgrowtopia.so 5.60.</small>
