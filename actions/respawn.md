# action|respawn

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|respawn
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **Respawn** button in the pause menu.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|respawn\n` |

- Only sent while your avatar exists and isn't already respawning (avatar+0x128 == 0).

```c
// pause menu click handler 0x17289bc
if (name == "Respawn" && LocalAvatar() && LocalAvatar()->respawnState == 0)
    SendText(2, "action|respawn\n");
```

<small>Builder: `0x17289bc` (pause menu, entity `Respawn`).</small>

## Server

gurotopia: [`include/action/respawn.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/respawn.cpp).

Reply: `OnKilled`, `OnSetFreezeState`, then `OnSetPos` at the world spawn.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|respawn\n");
```

<small>Client function: `0x17289bc` in libgrowtopia.so 5.60.</small>
