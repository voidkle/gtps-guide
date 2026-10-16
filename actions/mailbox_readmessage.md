# action|mailbox_readmessage

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|mailbox_readmessage
messageID|{}
```

## Fields

| Field | Meaning |
|---|---|
| `messageID` | Mailbox message id. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Opening a message in the mailbox (`mailbox.OnMessage`).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `messageID` | the message's id |

- Only sent for an **unread** message **without** rewards; the client marks it read and lowers the unread count.
  Messages with rewards are marked read by [mailbox_claimreward](./mailbox_claimreward). The message view opens either way.

<small>Builder: `0x1d1049c`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|mailbox_readmessage\nmessageID|0\n");
```

<small>Client function: `0x1d1049c` in libgrowtopia.so 5.60.</small>
