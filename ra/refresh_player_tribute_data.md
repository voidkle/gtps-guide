Same as [refresh_item_data](./refresh_item_data) for `player_tribute.dat`: sent when OnSuperMain's argument 6 is not 0 and
differs from the hash of the local file. The answer is [SEND_PLAYER_TRIBUTE_DATA (0x27)](/packets/27-send-player-tribute-data).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|refresh_player_tribute_data\n` |

<small>Builder: `0x1ba6598`.</small>
