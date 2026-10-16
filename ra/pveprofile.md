The three tab buttons of the PvE profile screen. Each selects a tab locally (`0x14cf178(pve+0x440, tab)`) and
sends the number that call returns.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `growid` | an int returned by `0x14cf178` for tab 0, 1 or 2 (despite the name; probably an id of that profile tab, not traced) |

- Not sent while another menu is open (`0x137d330`).

<small>Builder: `0x1720730` (button callback set up in `0x1720e3c`).</small>
