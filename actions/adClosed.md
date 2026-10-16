# action|adClosed

<Badge type="info" text="GAME_MESSAGE (3)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|adClosed
adName|{}
```

## Fields

| Field | Meaning |
|---|---|
| `adName` | Ad placement name. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** lines end with `\r\n`: `action|adClosed\r\nadName|<name>\r\n`, sent as message type 3 (GAME_MESSAGE).

Sent when a rewarded video ad closes.

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| `adName` | the ad placement name |

- The client also reports the ad (type, provider, seconds watched, capped at 1200) to its analytics.

<small>Builder: `0x1f245e8`; called from `0x1f28f10`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(3, "action|adClosed\r\nadName|0\r\n");
```

<small>Client function: `0x1f245e8` in libgrowtopia.so 5.60.</small>
