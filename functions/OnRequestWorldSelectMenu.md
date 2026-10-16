# OnRequestWorldSelectMenu

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Opens the world-select menu (the world list). Two handlers run for a call with header `netID == -1`. The
menu-flow listener runs first: it pushes the world-menu screen, which keeps argument 1 as the menu
description and argument 2 as a flag, unless that screen is already showing. GameLogic's handler then
leaves the game view: it closes the in-game menu and removes the arcade touch handler.

| # | Type | Meaning |
|---|---|---|
| 1 | string | the world-menu description (the text that lays out the world list; gurotopia builds it in `RequestWorldSelectMenu.cpp`) |
| 2 | int | optional; non-zero sets a flag on the world-menu screen (screen+0x40). What it changes wasn't traced. Missing = 0 |

### Decompiled handler

```c
// menu flow (0x1ba1ec8), lambda 0x1ba8308 -> 0x1ba360c
void OnRequestWorldSelectMenu_menu(MenuFlow *m, VariantList *args) {
    if (m->current && dynamic_cast<WorldMenuState *>(m->current)) return;   // already open
    bool flag = arg2.type != 0 && arg2.i != 0;
    WorldMenuState *s = NewWorldMenuState(...);    // 0x1994be4
    s->description = arg1.str;                     // +0x28
    s->flag = flag;                                // +0x40
    m->Push(s);                                    // 0x1ba9c34, 0x1b72ee4
}

// GameLogic (0x135e25c), arguments not read
void OnRequestWorldSelectMenu(GameLogic *self) {
    sub_1dd3278();
    CloseGameMenu(FindEntity(GetEntityRoot(), "GameMenu"));            // 0x177b53c
    sub_135ccc8(GetApp()->gameLogicEntity, 0);                         // app+0xfd8
    RemoveEntity(GetApp()->gameLogicEntity->entity, "TouchHandlerArcade");
}
```

<small>Handler: `0x136bb64` (dispatcher `0x135e25c`) and `0x1ba8308` → `0x1ba360c` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x1994be4`, `0x177b53c`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnRequestWorldSelectMenu"` |
| 1 | string | world menu description |

Shows the world list.

gurotopia: `include/onVariant/RequestWorldSelectMenu.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnRequestWorldSelectMenu", "...", 1 });
```
