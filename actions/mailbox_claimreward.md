# action|mailbox_claimreward

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|mailbox_claimreward
messageID|{}
```

## Fields

| Field | Meaning |
|---|---|
| `messageID` | Mailbox message id. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The claim button of one mail message (`mailbox.OnClaim` in the list or in the message view).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `messageID` | the message's id |

- The client marks the message read and lowers the unread count before sending.

<small>Builders: `0x1d10240` (list), `0x1d16ddc` (message view).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|mailbox_claimreward\nmessageID|0\n");
```

<small>Client function: `0x1d10240` in libgrowtopia.so 5.60.</small>
