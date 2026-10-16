# action|gohomeworld

<Badge type="info" text="GAME_MESSAGE (3)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|gohomeworld
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The home-world button on the world-select screen.

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| text | `action\|gohomeworld\n` |

- Needs the GUI and a GameLogic; then shows the "Entering world" loading message.

<small>Builder: `0x1c1730c`; called from `0x1c182f0`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(3, "action|gohomeworld\n");
```

<small>Client function: `0x1c1730c` in libgrowtopia.so 5.60.</small>
