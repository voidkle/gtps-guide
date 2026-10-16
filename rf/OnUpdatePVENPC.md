Updates the PvE enemies. It only runs while the PvE manager is active (see [OnActivatePVENPCManager](./OnActivatePVENPCManager)),
a world is loaded and the server's `proto` is 999999 or more.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | number of enemy records in argument 2 |
| 2 | string | the records: 12 fields each, all joined with `\|` (record after record, no other separator) |

Fields of one record:

| Field | Type | Used as (manager active) |
|---|---|---|
| 0 | int | enemy id; matched against the enemy's id (+0x2a8), which is its spawner's tile index (x + y × width) |
| 1, 2 | float | not used when updating (when creating an enemy they are stored at +0x278 / +0x27c, probably its home position) |
| 3, 4 | float | position x, y in pixels (+0x280 / +0x284) |
| 5, 6, 7 | int | three flags, non-zero = set (+0x258, +0x259, +0x25a) |
| 8, 9 | | not read |
| 10 | int | stored at +0x2ac |
| 11 | int | flag, non-zero = set (+0x2f5) |

Records whose id matches no enemy are skipped. The same function has a "create" path that runs when the manager isn't
active (it treats field 0 as a tile index and builds the enemy from that tile's extra data), but this handler never reaches it
because it requires an active manager.

### Decompiled handler

```c
// v[n] = argument n
void OnUpdatePVENPC(GameLogic *self, VariantList *v) {
    if (self->pve && self->pve->active && GetApp()->proto > 999998)   // +0x4d8, +0xb8c, app+0xc08
        self->pve->Update(v, self->world);                            // 0x14bf544
}

// 0x14bf544, update path
void PveManager::Update(VariantList *v, World *world) {
    if (!world || GetApp()->proto < 999999 || npcs.empty()) return;
    int count = v[1].GetUINT();
    auto f = Split(v[2].s, '|');
    for (int r = 0; r < count; r++) {
        auto *rec = &f[r * 12];
        for (Npc &n : npcs) if (n.id == atoi(rec[0])) {
            n.x = atof(rec[3]); n.y = atof(rec[4]);                   // +0x280, +0x284
            n.f_258 = atoi(rec[5]) != 0; n.f_259 = atoi(rec[6]) != 0; n.f_25a = atoi(rec[7]) != 0;
            n.f_2ac = atoi(rec[10]);
            n.f_2f5 = atoi(rec[11]) != 0;
            break;
        }
    }
}
```

<small>Handler: `0x1371810` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x14bf544`, `0x14beae8`.</small>

<!-- args: uint,string -->
