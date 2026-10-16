# action|update_weather_machine

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|update_weather_machine
jsonStr|{}
```

## Fields

| Field | Meaning |
|---|---|
| `jsonStr` | Weather machine settings as JSON. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The settings screen of a weather machine with custom colours (the concert lights one) saves its values.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `jsonStr` | one-line JSON: `Name` (`"CONCERT_LIGHTS"`), `MapIndex`, `RayColor1`, `RayColor2`, `DotsColor`, `GradientColor1`, `GradientColor2` (colours as strings, as the screen holds them) |

<small>Builder: `0x1cb3188`; called from `0x1cb38c8`, `0x1cb396c`.</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|update_weather_machine\njsonStr|0\n");
```

<small>Client function: `0x1cb3188` in libgrowtopia.so 5.60.</small>
