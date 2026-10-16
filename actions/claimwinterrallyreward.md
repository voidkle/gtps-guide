# action|claimwinterrallyreward

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|claimwinterrallyreward
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The claim button of the winter rally menu ([OnWinterRallyRequest](/functions/OnWinterRallyRequest)); the menu closes after sending.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|claimwinterrallyreward\n` |

<small>Builder: `0x17957c4` (callback set up in `0x17952bc`).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|claimwinterrallyreward\n");
```

<small>Client function: `0x17957c4` in libgrowtopia.so 5.60.</small>
