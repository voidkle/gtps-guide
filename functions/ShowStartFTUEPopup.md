# ShowStartFTUEPopup

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Shows the "start the tutorial" pop-up. Any earlier `FTUEStartPopup` fades out over 500 ms and is renamed
`FOR_DELETE`. Then a new pop-up is built: it has a **Start the Tutorial** button, the
`interface/large/gui_shop_buybanner.rttex` image and the internal name `tutorial_start_popup`. Afterwards the
client runs its own `HideWorldUI` function.

| # | Type | Meaning |
|---|---|---|
| 1 | string | pop-up title (probably; it is the first text passed to the pop-up builder, before the body) |
| 2 | string | pop-up text |

The pop-up builder (`0x173cd90`) is the generic one with `pop_up_title`, `pop_up_image`, `pop_up_text`, a
close cross and `OnButtonSelected`. What the button sends wasn't traced; `tutorial_start_popup` is probably
the name it reports.

### Decompiled handler

```c
void ShowStartFTUEPopup(GameLogic *self, VariantList *args) {
    Entity *old = FindEntity(GetEntityRoot(), "FTUEStartPopup");
    if (old) { FadeOutAndKill(old, 500); old->SetName("FOR_DELETE"); }
    Entity *e = GetEntityRoot()->AddChild(new Entity("FTUEStartPopup"));
    BuildPopUp(e, arg1.str, arg2.str, "", "Start the Tutorial",
               ..., "interface/large/gui_shop_buybanner.rttex", ..., "tutorial_start_popup", ...);   // 0x173cd90
    CallFunction(self, "HideWorldUI");
}
```

<small>Handler: `0x135d3d4` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x173cd90`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "ShowStartFTUEPopup", "...", "..." });
```
