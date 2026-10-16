# action|killstore

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|killstore
item|{}
```

## Fields

| Field | Meaning |
|---|---|
| `item` | Store item or category id. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Closing the store (Back / `close_` buttons) while a store page is open; probably tells the server the store screen is gone.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `item` | the last opened store entry (may be empty) |

<small>Builder: `0x175dcdc`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|killstore\nitem|main\n");
```

<small>Client function: `0x175dcdc` in libgrowtopia.so 5.60.</small>
