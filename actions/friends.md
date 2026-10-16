# action|friends

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|friends
delay|{}
```

## Fields

| Field | Meaning |
|---|---|
| `delay` | Delay value from the UI. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** two forms: `action|friends\ndelay|<ms>\n` and `action|friends\nlocation|pausemenu\n`.

Opens the friends list (the server answers with a dialog).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `delay` | `0` from the world UI friends button; `500` from the community hub's Back button when no tab was open |
| `location` | `pausemenu` from the pause menu's **FriendsMenu** button (no `delay` line) |

- The world UI button does nothing while the options or pause menu is open
  ("Options menu already active, not showing friends menu").

<small>Builders: `0x1c60de0` (world UI, via `0x1c621d4`), `0x1663bb4` (community hub Back), `0x17289bc` (pause menu).</small>

## Server

gurotopia: [`include/action/friends.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/friends.cpp).

Reply: `OnDialogRequest` with the friends menu.

## Notes

From the pause menu it's `action|friends\nlocation|pausemenu\n` instead.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|friends\ndelay|0\n");
```

<small>Client function: `0x1663bb4, 0x1c60de0` in libgrowtopia.so 5.60.</small>
