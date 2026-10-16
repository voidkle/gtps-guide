# action|dailyrewardmenu

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|dailyrewardmenu
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **DAILYREWARD** button of the inventory item bar. The server answers with
[OnDailyRewardRequest](/functions/OnDailyRewardRequest).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|dailyrewardmenu\n` |

- Not sent while the options or pause menu is open.

<small>Builder: `0x16f7ab0`; called from `0x16f6aa0`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|dailyrewardmenu\n");
```

<small>Client function: `0x16f7ab0` in libgrowtopia.so 5.60.</small>
