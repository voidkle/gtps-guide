The dungeon leaderboard asks for a range of entries.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `startIndex` | first entry |
| `endIndex` | last entry; must be greater than `startIndex` or nothing is sent |
| `relative` | probably 1 for a range around your own rank |

- The client waits up to 5 s for the answer.

<small>Builder: `0x1cc00c4`; called from `0x1cbf6b4`, `0x1cc045c`, `0x1cc0590`, `0x1cc347c`.</small>
