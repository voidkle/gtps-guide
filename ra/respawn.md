The **Respawn** button in the pause menu.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| text | `action\|respawn\n` |

- Only sent while your avatar exists and isn't already respawning (avatar+0x128 == 0).

```c
// pause menu click handler 0x17289bc
if (name == "Respawn" && LocalAvatar() && LocalAvatar()->respawnState == 0)
    SendText(2, "action|respawn\n");
```

<small>Builder: `0x17289bc` (pause menu, entity `Respawn`).</small>
