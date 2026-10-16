# OnFailedToEnterWorld

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Tells the client that joining a world failed, so it stays in the world-select menu. The handler removes the
dim layers of open pop-ups (`pop_up_darken`, `error_pop_up_darken`, `friend_list_darken`; `0x1dd3278`). It also
removes a child of `GameMenu` whose name is a global string (probably the "entering world" overlay;
`0x177b53c`).

No arguments are read. Send the reason first, with [OnConsoleMessage](./OnConsoleMessage) or a dialog.

### Decompiled handler

```c
void OnFailedToEnterWorld(GameLogic *self) {
    RemovePopUpDarkeners();                                    // 0x1dd3278, 400 ms fade
    Entity *menu = FindEntity(GetEntityRoot(), "GameMenu");
    if (menu) {                                                // 0x177b53c
        Entity *e = FindEntity(menu, g_29dff30);
        if (e) KillEntity(e);                                  // 0x1dbde04
    }
}
```

<small>Handler: `0x136ed48` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1dd3278`, `0x177b53c`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnFailedToEnterWorld"` |

The client stays in the world menu.

gurotopia: `include/action/join_request.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnFailedToEnterWorld" });
```
