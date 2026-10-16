# action|wrench

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|wrench
|netid|{}
```

## Fields

| Field | Meaning |
|---|---|
| `netid` | The player's `netID` in the current world (from their `OnSpawn`). |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

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

## Server

gurotopia: [`include/action/wrench.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/wrench.cpp).

Reply: `OnDialogRequest` with the player's wrench menu (yours or someone else's).

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|wrench\n|netid|2\n");
```

<small>Client function: `0x13a6864, 0x1c61ca4` in libgrowtopia.so 5.60.</small>
