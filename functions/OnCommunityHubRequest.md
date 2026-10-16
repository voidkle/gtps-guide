# OnCommunityHubRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Opens the community hub menu (`CommunityHubMenu`, under `WorldSpecificGUI`), built from argument 1
(`0x165f81c` → `0x165fc40`). The text may hold a `community_hub_type|<type>` line, and the client keeps that
value in a global (0x29d9260).

| # | Type | Meaning |
|---|---|---|
| 1 | string | dialog text (the OnDialogRequest format), optionally with `community_hub_type|…` |

These types are world lists: `community_communityworlds`, `communityworlds_toprated`, `communityworlds_toptoday`,
`communityworlds_topoverall` and `communityworlds_topyesterday`. For them, after building, the client fades
in the menu's `scroll_child` items and sets up its tab row (`0x16b7560`). Other types just build the menu.

Unlike the other menu requests, this handler doesn't check whether another menu is open.

### Decompiled handler

```c
void OnCommunityHubRequest(GameLogic *self, VariantList *args) {
    OpenCommunityHub(FindEntity(GetEntityRoot(), "WorldSpecificGUI"), arg1.str);   // 0x165f81c
}

Entity *OpenCommunityHub(Entity *gui, std::string text) {           // 0x165f81c
    GetField(text, "community_hub_type|", &g_hubType);
    Entity *m = BuildCommunityHub(gui, text);                       // 0x165fc40
    if (IsWorldListType(g_hubType)) {
        Entity *hub = FindEntity(gui, "CommunityHubMenu");
        for (child in FindEntity(hub, "scroll_child")->children) FadeIn(child);
        SetUpTabs(hub, text, ...);                                  // 0x16b7560
    }
    return m;
}
```

<small>Handler: `0x136ebcc` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x165f81c`, `0x165fc40`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnCommunityHubRequest", "..." });
```
