# OnPersistentNPCMessage

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Shows an NPC-style message box at a tile. There is only one such box at a time: a new call replaces its text.
The box sits near the given tile; if that tile's foreground is item 10924 (Pineapple Guzzler) it gets other
colors (`0x7e1e84ff` / `0xd733e1ff`) and sits on the tile.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | tile index in the current world (`x + y × width`); keep it inside the world: outside, the placement code (`0x11833a4`) gets a null tile |
| 2 | string | the text |
| 3 | uint | 1 = the box can be closed by [OnClearNPCMessage](./OnClearNPCMessage) (it then fades out after 1 s); anything else = OnClearNPCMessage has no effect. Missing = 0 |

When the server's `proto` (login settings) is 41 or higher, emoticon codes in the text are replaced. The box
is created on first use with default colors `0x9f7d27ff` / `0xfbe3a5ff`. Where it sits depends on the camera
zoom: it moves `3 / zoom + 2` tiles down from the given tile, if that tile is still inside the world. Whether
it also expires on its own wasn't traced: the line gets a 1000 ms timing value, the same as a talk-bubble line
of style 1.

The position is only updated while the world renderer exists (GameLogic+0xe0).

### Decompiled handler

```c
void OnPersistentNPCMessage(GameLogic *self, VariantList *args) {
    uint tile = arg1.u;  std::string text = arg2.str;  uint closable = arg3.u;
    self->npcMessage.Show(tile, text, closable == 1, 1, 1);          // 0x11827a8, self+0x1b0
}

void NPCMessage::Show(uint tile, std::string text, bool closable, bool lowered, int timing) {   // 0x11827a8
    if (!box) { box = new MessageBox(); box->lowered = lowered; box->colors = {0x9f7d27ff, 0xfbe3a5ff}; }
    if (GetApp()->proto >= 41) text = ReplaceEmoticons(text);
    box->SetSingleLine(text, timing);                               // 0x1189f04: keep one line, 1000 ms
    if (closable) box->closable = 1;                                // +0x65
    box->tile = tile;                                               // +0x1c
    if (GameLogic()->worldRenderer)
        PlaceAtTile(GameLogic(), box, GetTileByIndex(world, tile)); // 0x11833a4
}
```

<small>Handler: `0x136d210` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x11827a8`, `0x1189f04`, `0x11833a4`, `0x118a150`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnPersistentNPCMessage", 1u, "...", 1u });
```
