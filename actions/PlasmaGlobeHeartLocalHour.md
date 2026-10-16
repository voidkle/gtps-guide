# action|PlasmaGlobeHeartLocalHour

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|PlasmaGlobeHeartLocalHour
localHour|{}
```

## Fields

| Field | Meaning |
|---|---|
| `localHour` | The device's local hour. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The answer to [OnRequestPlasmaGlobeHeartLocalHour](/functions/OnRequestPlasmaGlobeHeartLocalHour).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `localHour` | the device's local hour (from `0x14224b8`, the local date/time) |

<small>Builder: `0x1382228`; called from `0x12f6d78`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|PlasmaGlobeHeartLocalHour\nlocalHour|0\n");
```

<small>Client function: `0x1382228` in libgrowtopia.so 5.60.</small>
