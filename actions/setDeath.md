# action|setDeath

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|setDeath
animDeath|{}
```

## Fields

| Field | Meaning |
|---|---|
| `animDeath` | Death animation id. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sent when you close the options menu in a world after changing the chosen death animation.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `animDeath` | the saved setting (`deathAnim`) as an unsigned int |

- Sent by the options menu's close button only if the matching "changed" flag is set (`changedSkin`, `changedDeath`,
  `changedRespawn`, or the role flags) and the menu wasn't opened from the main menu.


<small>Builder: `0x1382044`; called from `0x1bbea6c` (options menu).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|setDeath\nanimDeath|0\n");
```

<small>Client function: `0x1382044` in libgrowtopia.so 5.60.</small>
