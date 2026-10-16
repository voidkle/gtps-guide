Sends the GDPR / Apple consent state after the consent screen.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `GDPR` | app+0xc2c as an int (the consent value the login message also sends as `GDPR`) |

<small>Builder: `0x1382be4`; called from `0x1b94b2c` (consent screen, `AppleConsent`).</small>
