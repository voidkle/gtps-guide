Opens a player's wrench menu (profile). The server answers with a dialog.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `netid` | the player's netID |

When it is sent:

- You tap another player while the Wrench (item 32, action type 1) is selected and no generic dialog is open
  (`0x13a6864`); the client plays `audio/tile_removed.wav`.
- You tap your own avatar in the world UI (`world_ui.avatar_click`) → your own netID (`0x1c61ca4`).
- **Back** in the wardrobe (`WardrobeMain.OnBack`) and world-lock storage (`worldLockStorage.OnBack`) screens,
  and selecting a non-item entry in the seed diary → your own netID, to return to your profile.

```c
SendText(2, "action|wrench\n|netid|" + to_string(avatar->netID) + "\n");
```

<small>Builders: `0x13a6864`, `0x1c61ca4`, `0x1d556e0`, `0x1d7db8c`, `0x1d35724`.</small>
