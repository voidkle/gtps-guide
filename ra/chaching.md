**Format correction:** the format is `action|chaching\r\n` followed by saved purchase data, as message type 3 (GAME_MESSAGE).

Re-sends a pending in-app purchase. The client keeps unconfirmed orders as saved settings named `order_<number>`;
when this runs it takes the first one and sends its stored text after the header.

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| body | the saved value of the first `order_<n>` setting (purchase data) |

- Only while connected (app client +0xa5) and when such a setting exists. Called after a world loads
  ([0x04](/packets/04-send-map-data)), on [OnReconnect](/functions/OnReconnect) and a few other places.

```c
void MaybeSendChaching() {                                    // 0x1083db8
    if (!client->connected) return;
    int n; std::string data;
    if (FindSetting("order_", &n, &data))                     // 0x16e1e1c
        SendText(3, "action|chaching\r\n" + data);
}
```

<small>Builder: `0x1083db8`; called from `0x135ccc8`, `0x136abf8`, `0x136cf9c`, `0x1373be4`, `0x1373e20`.</small>
