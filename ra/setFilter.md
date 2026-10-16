Saving **Personal Settings** (the parental menu) sends the swear-filter state together with the client bits.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `filtering` | the saved `swearFilter` setting (uint) |
| `cbits` | the client bit field (`0x1084584`), the same value the login message sends as `cbits` |

<small>Builder: `0x1382570`; called from `0x1bd9a28` (Personal Settings save).</small>
