# action|setOnlyFriendsChat

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|setOnlyFriendsChat
show|{}
```

## Fields

| Field | Meaning |
|---|---|
| `show` | `1` on, `0` off. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Saving **Personal Settings** with the "only friends" chat option.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `show` | the saved `onlyFriendsChat` setting (uint, 0/1) |

<small>Builder: `0x13829d8`; called from `0x1bd9a28`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|setOnlyFriendsChat\nshow|0\n");
```

<small>Client function: `0x13829d8` in libgrowtopia.so 5.60.</small>
