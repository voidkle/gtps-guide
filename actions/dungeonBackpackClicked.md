# action|dungeonBackpackClicked

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|dungeonBackpackClicked
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The backpack button of the in-dungeon UI (`dungeon_ui.backpack_click`), when no other menu is open.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|dungeonBackpackClicked\n` |

<small>Builder: `0x1c3ef70` (`DungeonWorldUIController` lambda).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|dungeonBackpackClicked\n");
```

<small>Client function: `0x1c3ef70` in libgrowtopia.so 5.60.</small>
