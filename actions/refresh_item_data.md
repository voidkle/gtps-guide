# action|refresh_item_data

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|refresh_item_data
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sent during login when the hash of the local `items.dat` differs from argument 1 of
[OnSuperMainStartAcceptLogon…](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a). The server should answer with
[SEND_ITEM_DATABASE_DATA (0x10)](/packets/10-send-item-database-data).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|refresh_item_data\n` |

- Logs "Need to refresh items data. Request it." and shows a download screen.

<small>Builder: `0x1ba6598`.</small>

## Server

gurotopia: [`include/action/refresh_item_data.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/refresh_item_data.cpp).

Reply: `SEND_ITEM_DATABASE_DATA` (0x10) with the whole items.dat.

## Notes

Sent when the items.dat hash in `OnSuperMainStartAcceptLogon...` doesn't match the client's copy.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|refresh_item_data\n");
```

<small>Client function: `0x1ba6598` in libgrowtopia.so 5.60.</small>
