# action|worldlock_storage_getpage

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|worldlock_storage_getpage
pageIndex|{}
```

## Fields

| Field | Meaning |
|---|---|
| `pageIndex` | Page number. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The world-lock storage screen asks for a page of its list (opening, "next page").

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `pageIndex` | the page (≥ -1; smaller values are ignored) |

- Marks a request as pending and remembers the time (the answer is `OnWorldLockStorageResponse`).

<small>Builder: `0x1d7d084`; called from `0x1d7cb38`, `0x1d7daa4`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|worldlock_storage_getpage\npageIndex|0\n");
```

<small>Client function: `0x1d7d084` in libgrowtopia.so 5.60.</small>
