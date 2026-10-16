Sent when you close the options menu in a world after changing the chosen role icon.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `roleType` | the saved setting (`role icon`) as an unsigned int |

- Sent by the options menu's close button only if the matching "changed" flag is set (`changedSkin`, `changedDeath`,
  `changedRespawn`, or the role flags) and the menu wasn't opened from the main menu.
- When the change was made outside a world, the client keeps a `send…` setting instead and sends this after the
  next world loads ([0x04](/packets/04-send-map-data)).

<small>Builder: `0x13778a8`; called from `0x1bbea6c` (options menu), `0x1373e20` (after a world loads).</small>
