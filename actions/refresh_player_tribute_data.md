# action|refresh_player_tribute_data

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|refresh_player_tribute_data
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Same as [refresh_item_data](./refresh_item_data) for `player_tribute.dat`: sent when OnSuperMain's argument 6 is not 0 and
differs from the hash of the local file. The answer is [SEND_PLAYER_TRIBUTE_DATA (0x27)](/packets/27-send-player-tribute-data).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|refresh_player_tribute_data\n` |

<small>Builder: `0x1ba6598`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|refresh_player_tribute_data\n");
```

<small>Client function: `0x1ba6598` in libgrowtopia.so 5.60.</small>
