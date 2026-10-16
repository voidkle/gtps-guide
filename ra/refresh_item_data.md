Sent during login when the hash of the local `items.dat` differs from argument 1 of
[OnSuperMainStartAcceptLogon…](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a). The server should answer with
[SEND_ITEM_DATABASE_DATA (0x10)](/packets/10-send-item-database-data).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|refresh_item_data\n` |

- Logs "Need to refresh items data. Request it." and shows a download screen.

<small>Builder: `0x1ba6598`.</small>
