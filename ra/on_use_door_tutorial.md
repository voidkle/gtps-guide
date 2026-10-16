Tutorial progress: sent when you use a door during the tutorial and the client has no local tutorial
step for that door.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|on_use_door_tutorial\n` |

- Only while the tutorial is active (`0x1444df4`) and connected. If the current tutorial step lists the door, the
  client advances the step itself instead; if the step is in its "skip" list nothing is sent.
- The pause menu's Quit button calls the same function and shows "You must complete the tutorial first!" when it returns false.

<small>Builder: `0x197b92c`; called from `0x13035e4`, `0x17289bc`.</small>
