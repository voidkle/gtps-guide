# action|pveprofile

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|pveprofile
|growid|{}
```

## Fields

| Field | Meaning |
|---|---|
| `growid` | A GrowID. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The three tab buttons of the PvE profile screen. Each selects a tab locally (`0x14cf178(pve+0x440, tab)`) and
sends the number that call returns.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `growid` | an int returned by `0x14cf178` for tab 0, 1 or 2 (despite the name; probably an id of that profile tab, not traced) |

- Not sent while another menu is open (`0x137d330`).

<small>Builder: `0x1720730` (button callback set up in `0x1720e3c`).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|pveprofile\n|growid|0\n");
```

<small>Client function: `0x1720730` in libgrowtopia.so 5.60.</small>
