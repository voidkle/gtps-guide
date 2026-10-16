# action|fashion_show_vote

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|fashion_show_vote
participantIndex|{}
```

## Fields

| Field | Meaning |
|---|---|
| `participantIndex` | Who you vote for. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Voting on the fashion show voting screen (`FashionShowVoteUi.OnVote`).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `participantIndex` | the clicked element's index attribute (`message_index`), 0–4; larger values are ignored |

<small>Builder: `0x1cf4d0c`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|fashion_show_vote\nparticipantIndex|0\n");
```

<small>Client function: `0x1cf4d0c` in libgrowtopia.so 5.60.</small>
