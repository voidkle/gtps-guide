# action|startdungeonbtn

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|startdungeonbtn
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **Start** button of the dungeon start screen (`DungeonStartUi.OnStart`); the screen closes after sending.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|startdungeonbtn\n` |

<small>Builder: `0x1cd3574` (`DungeonStartUiController` lambda).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|startdungeonbtn\n");
```

<small>Client function: `0x1cd3574` in libgrowtopia.so 5.60.</small>
