# action|get_seed_diary_data

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|get_seed_diary_data
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sent when your own avatar spawns ([OnSpawn](/functions/OnSpawn) with `type|local`) if a saved int setting
(probably `seed_diary_hash_dirty`) is above 0. The answer is [OnSendSeedDiaryData](/functions/OnSendSeedDiaryData).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|get_seed_diary_data\n` |

<small>Builder: `0x136accc` (OnSpawn).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|get_seed_diary_data\n");
```

<small>Client function: `0x136accc` in libgrowtopia.so 5.60.</small>
