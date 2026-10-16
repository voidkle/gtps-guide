# action|setchatFilter

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|setchatFilter
filtering|{}
```

## Fields

| Field | Meaning |
|---|---|
| `filtering` | `1` on, `0` off. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The chat-tab filter menu (`CustomLogFilterMenu`: global, world, private, friend, guild, gameplay check boxes) saves its bits.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `filtering` | the filter bit mask as an unsigned int (`0x10846a8`) |

<small>Builder: `0x1382894`; called from `0x175002c`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|setchatFilter\nfiltering|0\n");
```

<small>Client function: `0x1382894` in libgrowtopia.so 5.60.</small>
