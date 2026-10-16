Sent when you close the options menu in a world after changing the chosen death animation.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `animDeath` | the saved setting (`deathAnim`) as an unsigned int |

- Sent by the options menu's close button only if the matching "changed" flag is set (`changedSkin`, `changedDeath`,
  `changedRespawn`, or the role flags) and the menu wasn't opened from the main menu.


<small>Builder: `0x1382044`; called from `0x1bbea6c` (options menu).</small>
