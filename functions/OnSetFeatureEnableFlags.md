# OnSetFeatureEnableFlags

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Tells the client which optional features are switched on. Needed by newer clients (gurotopia sends it after
`enter_game`). The client keeps a set of enabled feature numbers and tells the UI elements that depend on
a feature (`FeatureEnableFlagElement`) when theirs changes.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| 1 | string | base64 of the flag list |

The decoded bytes:

```text
u8 count
u8 feature[count]      feature numbers that are on (0–255)
```

`count` is clipped to the bytes actually present. Every feature not in the list is off. The new set replaces
the old one; for each feature whose state changed, the client notifies the registered elements for that
feature number (`0x17a1944`). The feature numbers' meanings aren't named in the client.

### Decompiled handler

```c
void operator()(VariantList *const &vl) {                       // 0x1ba90ac
    if (!g_featureFlags) g_featureFlags = new FeatureFlags();   // 0x29cdf58
    g_featureFlags->Set(vl->GetString(0));                      // 0x1b2b154
}

void FeatureFlags::Set(const std::string &b64) {                // 0x1b2b154
    std::string d = Base64Decode(b64);                          // 0x1e537d8
    std::set<uint16_t> old = std::move(this->on);               // +8
    if (d.size() >= 2 && d[0] != 0) {
        size_t n = std::min<size_t>((uint8_t)d[0], d.size() - 1);
        for (size_t i = 1; i <= n; i++) this->on.insert((uint8_t)d[i]);
    }
    for (uint16_t f : SymmetricDifference(old, this->on))       // 0x1b2b90c
        for (auto *e : this->listeners[f])                      // +0x20, hash map
            if (auto *el = dynamic_cast<FeatureEnableFlagElement *>(e)) el->Refresh();   // 0x17a1944
}
```

<small>Handler: `0x1ba90ac` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x1b2b154`, `0x1e537d8`, `0x1b2b90c`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnSetFeatureEnableFlags"` |
| 1 | string | base64 flag list |

Needed by 5.47+ clients.

gurotopia: `include/action/enter_game.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnSetFeatureEnableFlags", "..." });
```
