# action|tutorialTaskQuestClicked

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|tutorialTaskQuestClicked
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The tutorial task button. Without the tutorial flag (`0x1444df4` false) and with no menu open, the client sends this;
with it, it opens the questline screen itself (`OnDialogRequestRML("show_questline_ui")`).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|tutorialTaskQuestClicked\n` |

<small>Builder: `0x1c5ad7c` (`ServerAuthPacketBuilder` table, set up in `0x1864840`).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|tutorialTaskQuestClicked\n");
```

<small>Client function: `0x1c5ad7c` in libgrowtopia.so 5.60.</small>
