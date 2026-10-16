# action|chaching

<Badge type="info" text="GAME_MESSAGE (3)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|chaching
```

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(3, "action|chaching\r\n");
```

<small>Client function: `0x1083db8` in libgrowtopia.so 5.60.</small>
