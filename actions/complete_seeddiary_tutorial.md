# action|complete_seeddiary_tutorial

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|complete_seeddiary_tutorial
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sent once, the first time the seed diary is used while the tutorial flag is on: only if the saved setting
`IsCompletedSeedDiary` is 0. Afterwards the client sets that setting to 1.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|complete_seeddiary_tutorial\n` |

<small>Builder: `0x1d3252c`; called from `0x1d361d8`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|complete_seeddiary_tutorial\n");
```

<small>Client function: `0x1d3252c` in libgrowtopia.so 5.60.</small>
