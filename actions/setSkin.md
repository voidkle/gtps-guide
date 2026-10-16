# action|setSkin

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|setSkin
color|{}
```

## Fields

| Field | Meaning |
|---|---|
| `color` | Skin color as an unsigned 32-bit number. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sent when you close the options menu in a world after changing the skin colour.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `color` | the saved setting (`skinColor`) as an unsigned int |

- Sent by the options menu's close button only if the matching "changed" flag is set (`changedSkin`, `changedDeath`,
  `changedRespawn`, or the role flags) and the menu wasn't opened from the main menu.
- When the change was made outside a world, the client keeps a `send…` setting instead and sends this after the
  next world loads ([0x04](/packets/04-send-map-data)).

<small>Builder: `0x13774e0`; called from `0x1bbea6c` (options menu), `0x1373e20` (after a world loads).</small>

## Server

gurotopia: [`include/action/setSkin.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/setSkin.cpp).

Reply: `OnSetClothing` with the new skin color.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|setSkin\ncolor|0\n");
```

<small>Client function: `0x13774e0` in libgrowtopia.so 5.60.</small>
