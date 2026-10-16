Sent when your own avatar spawns ([OnSpawn](/functions/OnSpawn) with `type|local`) if a saved int setting
(probably `seed_diary_hash_dirty`) is above 0. The answer is [OnSendSeedDiaryData](/functions/OnSendSeedDiaryData).

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|get_seed_diary_data\n` |

<small>Builder: `0x136accc` (OnSpawn).</small>
