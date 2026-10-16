# action|setFilter

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|setFilter
filtering|{}
cbits|{}
```

## Fields

| Field | Meaning |
|---|---|
| `filtering` | `1` on, `0` off. |
| `cbits` | Client setting bits. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Saving **Personal Settings** (the parental menu) sends the swear-filter state together with the client bits.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `filtering` | the saved `swearFilter` setting (uint) |
| `cbits` | the client bit field (`0x1084584`), the same value the login message sends as `cbits` |

<small>Builder: `0x1382570`; called from `0x1bd9a28` (Personal Settings save).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Notes

The swear filter.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|setFilter\nfiltering|0\ncbits|0\n");
```

<small>Client function: `0x1382570` in libgrowtopia.so 5.60.</small>
