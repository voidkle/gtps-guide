Starts the PvE enemy manager for the current world (the manager at GameLogic+0x4d8 that [PVE_NPC (0x29)](/packets/29-pve-npc)
drives). It removes any enemies it had and creates one for every enemy-spawner tile in the world, from the tile's extra
data.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | stored as a flag on the manager (+0xb8d); its meaning wasn't traced |

**It only runs when the server's `proto` (from the login settings string) is 999999 or more**, so with the values servers
normally send, PvE is switched off in 5.60. It also needs a loaded world.

### Decompiled handler

```c
// v[n] = argument n
void OnActivatePVENPCManager(GameLogic *self, VariantList *v) {
    if (!self->pve || GetApp()->proto < 999999) return;          // +0x4d8, app+0xc08
    self->pve->Activate(v[1].GetUINT() != 0);                    // 0x14c0258
}

// 0x14c0258
void PveManager::Activate(bool flag) {
    if (GetApp()->proto < 999999 || !GetGameLogic()->world) return;
    Init(world);                                                  // 0x14bfc10
    active = 1; f_b8d = flag;                                     // +0xb8c, +0xb8d
    npcs.clear();
    for (Tile *t : world->npcSpawnerTiles)                        // list at world+0x116e8
        if (t->extra) npcs.push_back(Npc(t->extra->f_d8, t ...)); // 0x14beae8
}
```

<small>Handler: `0x1371870` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x14c0258`, `0x117e8cc`.</small>

<!-- args: uint -->
