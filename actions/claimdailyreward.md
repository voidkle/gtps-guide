# action|claimdailyreward

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|claimdailyreward
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The claim button in the daily reward menu. The client closes the menu right after sending.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|claimdailyreward\n` |

<small>Builder: `0x167c1ac` (callback set up in `0x167ba58`).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|claimdailyreward\n");
```

<small>Client function: `0x167c1ac` in libgrowtopia.so 5.60.</small>
