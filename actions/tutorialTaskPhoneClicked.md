# action|tutorialTaskPhoneClicked

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|tutorialTaskPhoneClicked
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The daily quests button of the questline screen (`questline.OnDailyQuests`); the screen closes first.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|tutorialTaskPhoneClicked\n` |

<small>Builder: `0x1d24498` (`QuestlineController` lambda).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|tutorialTaskPhoneClicked\n");
```

<small>Client function: `0x1d24498` in libgrowtopia.so 5.60.</small>
