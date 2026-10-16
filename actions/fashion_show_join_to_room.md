# action|fashion_show_join_to_room

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|fashion_show_join_to_room
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **Join** button of the fashion show screen (`FashionShowUi.OnJoin`); the screen closes after sending.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|fashion_show_join_to_room\n` |

- The screen's **Buy tickets** button sends `action|storenavigate\nitem|main\nselection|fashion_show_ticket\n`.

<small>Builder: `0x1ce4ae8`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|fashion_show_join_to_room\n");
```

<small>Client function: `0x1ce4ae8` in libgrowtopia.so 5.60.</small>
