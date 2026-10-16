**Format correction:** the client sends `action|quit` with **no** trailing `\n`, as message type 3 (GAME_MESSAGE).

Sent by the network client's disconnect routine just before it closes the connection on purpose: logging out,
switching to beta mode, the world screen's Back button, returning to the main menu.

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| text | `action\|quit` |

- Only if a peer exists; the connection state then becomes 5 (closing) and the peer is dropped 500 ms later.

<small>Builder: `0x11424bc`; called from `0x11422cc`, `0x136b858` (OnLogout), `0x1370668` (OnSetBetaMode), `0x1372d28`, `0x1ba33d4`, `0x1c16adc`.</small>
