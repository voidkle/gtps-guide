# 0x18 APP_CHECK_RESPONSE

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="inferred" />

## Header fields used

Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.

| Field | Meaning |
|---|---|
| `netID` | 1-based position of the last listed app that is installed, or -1 if none is |
| `itemID` | sum of `HashString(name)` over the listed apps that are **not** installed |

## Official client

**Received:** ignored (falls to the switch's default).

**Sent:** Sent once after [OnSuperMainStartAcceptLogon…](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a#the-app-check) when its argument 4 is a string: a space-separated list of Android package names the client checks for.
