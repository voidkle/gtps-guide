# action|setGDPR

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|setGDPR
GDPR|{}
```

## Fields

| Field | Meaning |
|---|---|
| `GDPR` | `1` if accepted. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sends the GDPR / Apple consent state after the consent screen.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `GDPR` | app+0xc2c as an int (the consent value the login message also sends as `GDPR`) |

<small>Builder: `0x1382be4`; called from `0x1b94b2c` (consent screen, `AppleConsent`).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|setGDPR\nGDPR|0\n");
```

<small>Client function: `0x1382be4` in libgrowtopia.so 5.60.</small>
