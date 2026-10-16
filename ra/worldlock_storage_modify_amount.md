The **Add** and **Withdraw** buttons of the world-lock storage balance screen.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `amount` | the amount on the screen (a 64-bit value, model+0x60) |
| `type` | `1` = add, `-1` = withdraw |

- The amount is reset to 0 and the screen closes after sending.

<small>Builders: `0x1d6f0d4` (Add), `0x1d6f2a8` (Withdraw).</small>
