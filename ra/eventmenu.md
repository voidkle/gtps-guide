**Format correction:** from the pause menu it is `action|eventmenu\nlocation|pausemenu\n`.

Opens the events menu.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `location` | only from the pause menu's **EventMenu** button: `pausemenu` |

- The world UI events button (`0x1c6105c`) sends the short form and does nothing while the options or pause menu is open.

<small>Builders: `0x1c6105c` (world UI, via `0x1c62254`), `0x17289bc` (pause menu).</small>
