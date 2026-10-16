**Format correction:** lines end with `\r\n`: `action|adClosed\r\nadName|<name>\r\n`, sent as message type 3 (GAME_MESSAGE).

Sent when a rewarded video ad closes.

| Field | Value |
|---|---|
| message | message type 3 (GAME_MESSAGE) |
| `adName` | the ad placement name |

- The client also reports the ad (type, provider, seconds watched, capped at 1200) to its analytics.

<small>Builder: `0x1f245e8`; called from `0x1f28f10`.</small>
