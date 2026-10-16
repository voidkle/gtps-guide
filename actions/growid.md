# action|growid

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|growid
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **growID** button in the pause menu (create or manage a GrowID). The server answers with a dialog.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|growid\n` |

<small>Builder: `0x17289bc` (pause menu, entity `growID`).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

"Create GrowID" from the pause menu.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|growid\n");
```

<small>Client function: `0x17289bc` in libgrowtopia.so 5.60.</small>
