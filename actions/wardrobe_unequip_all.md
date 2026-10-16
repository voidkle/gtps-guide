# action|wardrobe_unequip_all

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|wardrobe_unequip_all
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **UnequipAll** button on the wardrobe screen.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|wardrobe_unequip_all\n` |

- Not sent while a flag on the wardrobe model (+0x518 bit 0) is set (probably "busy").

<small>Builder: `0x1d55908`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|wardrobe_unequip_all\n");
```

<small>Client function: `0x1d55908` in libgrowtopia.so 5.60.</small>
