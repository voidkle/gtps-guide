The world-lock storage screen asks for a page of its list (opening, "next page").

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `pageIndex` | the page (≥ -1; smaller values are ignored) |

- Marks a request as pending and remembers the time (the answer is `OnWorldLockStorageResponse`).

<small>Builder: `0x1d7d084`; called from `0x1d7cb38`, `0x1d7daa4`.</small>
