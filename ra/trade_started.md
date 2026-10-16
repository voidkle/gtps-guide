Sent when the trade window has opened after [OnStartTrade](/functions/OnStartTrade) found the other player.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `netid` | the other player's netID (OnStartTrade argument 2) |

- Not sent if the in-world GUI or the other avatar is missing ("other player doesn't exist!").

<small>Builder: `0x178cd48` (TradeMenu::Open); called from `0x136ffa8` (OnStartTrade).</small>
