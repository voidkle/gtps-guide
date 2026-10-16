# action|requestAccountDelete

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|requestAccountDelete
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **deleteAccount** button in the options menu (only when no pop-up is open). The server is expected to
answer with a confirmation dialog.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|requestAccountDelete\n` |

<small>Builder: `0x1383d60`; called from `0x1bbea6c` (options menu).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|requestAccountDelete\n");
```

<small>Client function: `0x1383d60` in libgrowtopia.so 5.60.</small>
