# action|mailbox_getpage

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|mailbox_getpage
pageIndex|{}
```

## Fields

| Field | Meaning |
|---|---|
| `pageIndex` | Page number. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The mailbox asks for a page of messages (on open and "next page").

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `pageIndex` | the page (≥ -1) |

- Marks a request as pending and refreshes the list view.

<small>Builder: `0x1d0e738`; called from `0x1d0e0ec` (`MailBoxController::OnActivate`), `0x1d11350`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|mailbox_getpage\npageIndex|0\n");
```

<small>Client function: `0x1d0e738` in libgrowtopia.so 5.60.</small>
