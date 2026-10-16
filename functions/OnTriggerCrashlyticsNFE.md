# OnTriggerCrashlyticsNFE

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sends a test report to Firebase Crashlytics: it sets the custom key `test_key` and records the string as a
non-fatal exception ("NFE") twice. Only works when your own avatar has the second
[OnDataConfig](/functions/OnDataConfig) flag set (avatar+0x162); otherwise it is ignored.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the exception message to record |

Global function: send it with `netID` -1 in the [CALL_FUNCTION](/packets/01-call-function) header.

The bridge is the Java class `com.rtsoft.growtopia.FirebaseCrashlyticsManager`, method `RecordException(String, int)`
(slot 0x18 of the wrapper at `0x29341c8`); the custom key goes through `firebase::crashlytics::SetCustomKey`.

### Decompiled handler

```c
void GameLogic::OnTriggerCrashlyticsNFE(GameLogic *self, VariantList *vl) {
    NetAvatar *me = self->localAvatar;                             // self+0x1a8
    if (!me || !me->dataConfig2) return;                           // avatar+0x162
    std::string msg = vl[1].s;
    Crashlytics()->SetCustomKey("test_key", 1);                    // 0x1f1bb3c (slot 0x38)
    Crashlytics()->RecordException(msg, 0);                        // 0x1f1bafc (slot 0x18)
    Crashlytics()->RecordException(msg, 1);
}
```

<small>Handler: `0x1372aa8` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1f1ba54`, `0x1f1bb3c`, `0x1f1bafc`, `0x1f1c55c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnTriggerCrashlyticsNFE", "..." });
```
