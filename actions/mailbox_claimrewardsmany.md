# action|mailbox_claimrewardsmany

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|mailbox_claimrewardsmany
listIDs|{}
```

## Fields

| Field | Meaning |
|---|---|
| `listIDs` | Comma-separated message ids. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **Claim all** button of the mailbox (`mailbox.OnClaimAll`).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `listIDs` | comma-separated ids of every unread message that has rewards (no trailing comma) |

- All those messages are marked read locally and the unread count becomes 0.

<small>Builder: `0x1d0fab8`; called from `0x1d101bc`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|mailbox_claimrewardsmany\nlistIDs|0\n");
```

<small>Client function: `0x1d0fab8` in libgrowtopia.so 5.60.</small>
