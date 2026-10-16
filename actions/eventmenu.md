# action|eventmenu

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|eventmenu
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** from the pause menu it is `action|eventmenu\nlocation|pausemenu\n`.

Opens the events menu.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `location` | only from the pause menu's **EventMenu** button: `pausemenu` |

- The world UI events button (`0x1c6105c`) sends the short form and does nothing while the options or pause menu is open.

<small>Builders: `0x1c6105c` (world UI, via `0x1c62254`), `0x17289bc` (pause menu).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|eventmenu\n");
```

<small>Client function: `0x1c6105c` in libgrowtopia.so 5.60.</small>
