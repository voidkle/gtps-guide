# 0x2a PVPCARD_BATTLE

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1373f18`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

PvP card battles: the client's name for this type is `NET_GAME_PACKET_PVPCARD_BATTLE`. The client keeps a list of card battles (0x6770 bytes each), keyed by an id in `tileX`. Each battle has two players (0 and 1), and each player has a queue of animations (`PvpCard…Action` objects) that play one after another. The server sends the results, and the client only queues the animations. `buildRange` is the sub-command; nothing happens when you're not in a world. Sub-commands 1-6 need the battle to exist and be running (battle+0x6761).

| Field | Used as |
|---|---|
| `tileX` | card battle id |
| `buildRange` | the sub-command (below) |
| `netID` | the player index in the battle, 0 or 1 (for 99: a player's netID) |
| `targetNetID` | the element of the attack (1): 0-4 |
| `tileY` | the player's new HP (1, 3), a card item id (2, 99), or the number of buffs (4) |
| `itemID` | 1: > 0 = the attack hit (damage animation and new HP); 2 and 99: ≥ 1 picks the success effect |
| `extraDataLength` | the battle setup (0) or the buff list (4) |

### Sub-commands
`buildRange` selects what happens:

| Value | Effect | Fields used |
|---|---|---|
| 0 | Create (or reuse) card battle `tileX` from the extra data (`sub_1837f64`). If you're one of the two players: `audio/gong.wav` and the music `audio/mp3/theme4.mp3`. | `tileX`, extra data |
| 1 | Attack on player `netID`: queue a `PvpCardElementalAction` that plays the element effect for `targetNetID` (0 → 0x16d, 1 → 0x16a, 2 → 0x16c, 3 → 0x16e, 4 → 0x16b; others nothing). When `itemID` > 0, also queue a `PvpCardDamageAction`: effect 0x168, then the player's HP becomes `tileY`. | `netID`, `targetNetID`, `tileY`, `itemID` |
| 2 | Player `netID` plays card `tileY` (an item id): effect 0x169 80 px above them showing that item's icon, then effect 0x161 if `itemID` ≥ 1 or 0x170 otherwise. | `netID`, `tileY`, `itemID` |
| 3 | Player `netID` heals: effects 0x163 and 0x162, then their HP becomes `tileY`, capped at their max HP. `itemID` is stored but not used. | `netID`, `tileY` |
| 4 | Queue `tileY` buffs for player `netID` from the extra data, each (a, b, c). Entries with a ≤ 0 are skipped. When played, a buff with c > 0 shows effect 0x164 if b ≠ 0 or 0x165 if b = 0; a itself isn't used by the animation. | `netID`, `tileY`, extra data |
| 5 | End the battle once both players' animation queues are empty (battle+0x6760). Ending (`0x183899c`) clears both players' card-battle id, and if you were in it, stops the music and returns the camera. | |
| 6 | Hides player `netID`'s HP bar (side+0x33a8 = 0; sub-command 0 turns both on). | `netID` |
| 99 | Player `netID` (a real netID; logs "player not found" otherwise) gets avatar+0x3588 = `tileY`, the battle pet drawn on their Battle Leash (the same field as [0x21](./21-pet-battle) sub-command 0). Effect 0x169 then shows item `tileY`'s icon over them, followed by effect 0x161 if `itemID` ≥ 1, or 0x170 otherwise. | `netID`, `tileY`, `itemID` |

### Extra data
Sub-command 0, for player 0 and then player 1 (strings are `u16 length` + bytes):

| Type | Meaning |
|---|---|
| string | the player's name |
| `i32` | the player's netID (if not in the world, the battle is dropped) |
| `u16` | skipped (nothing reads it) |
| `i32`, `i32` | the player's HP and max HP |

Sub-command 4: `tileY` entries of three `i32` (a, b, c).

### Animations and the HP bars

Each player has a queue of actions. The battle update (`0x18384cc`) plays up to two actions from each player's
queue every half second (front of queue 0, queue 1, then again), so the server can send a whole turn at once. While a player's HP bar is on, the battle draws it
over their head (`0x1838f44`): a black bar with a green part HP / max HP wide. The actions change the HP shown:
damage sets it, heal sets it (capped at the max). Effects are particle/sprite effects (`sub_1912570` with
the id) played at the player.

### Decompiled handler

```c
void PvpCardBattle(GameLogic *self, packet *pkt)            // 0x137b93c
{
    CardBattle *b = FindCardBattle(pkt->tileX);             // sub_1838324
    if (!self->world) return;
    int p = pkt->netID;
    switch (pkt->buildRange) {
    case 0:  if (pkt->extraDataLength) LoadCardBattle(pkt->tileX, GetExtra(pkt)); break;   // sub_1837db0 -> sub_1837f64
    case 1:  if (b && b->running) {                          // sub_1838adc
                 Queue(b, p, new PvpCardElementalAction(pkt->targetNetID, pkt->tileY, p));
                 if (pkt->itemID > 0) Queue(b, p, new PvpCardDamageAction(pkt->targetNetID, pkt->tileY, p));
             } break;
    case 2:  if (b && b->running) Queue(b, p, new PvpCardActivateCardAction(pkt->tileY, pkt->itemID, p)); break;  // sub_1838c48
    case 3:  if (b && b->running) Queue(b, p, new PvpCardHealAction(pkt->tileY, pkt->itemID, p)); break;          // sub_1838e64
    case 4:  if (b && b->running) {                          // sub_1838d30
                 int32_t *e = GetExtra(pkt);
                 for (int i = 0; i < pkt->tileY; i++, e += 3)
                     if (e[0] > 0) Queue(b, p, new PvpCardBuffAction(e[0], e[1], p, e[2]));
             } break;
    case 5:  if (b && b->running) b->endWhenIdle = 1; break;            // +0x6760
    case 6:  if (b && b->running) b->side[p].showHpBar = 0; break;     // +0x33a8
    case 99: {
        NetAvatar *a = GetAvatar(pkt->netID);
        if (!a) LogError("player not found");
        else { a->battlePetShown = pkt->tileY; RefreshLook(&a->look); }   // avatar+0x3588, sub_1098f88
        Effect *fx = AddEffect(self->renderer + 0x178, 0x169, a->pos, 0);        // sub_1912570
        if (fx) fx->icon = ItemIcon(pkt->tileY);            // texture cell of item tileY
        AddEffect(self->renderer + 0x178, pkt->itemID >= 1 ? 0x161 : 0x170, a->pos, 0);
        break;
    }
    }
}

// the queued actions; the update runs up to two per player every 0.5 s (vtable +0x10)
void PvpCardElementalAction::Run() { static const int fx[] = {0x16d, 0x16a, 0x16c, 0x16e, 0x16b};
                                    if (element >= 0 && element <= 4) AddEffect(fx[element], PlayerPos(player)); }
void PvpCardDamageAction::Run()    { AddEffect(0x168, PlayerPos(player)); side->hp = newHp; }
void PvpCardHealAction::Run()      { AddEffect(0x163, ...); AddEffect(0x162, ...); side->hp = min(newHp, side->maxHp); }
void PvpCardActivateCardAction::Run() { Effect *fx = AddEffect(0x169, PlayerPos(player) - (0, 80)); fx->icon = ItemIcon(card);
                                        AddEffect(success >= 1 ? 0x161 : 0x170, PlayerPos(player) - (0, 80)); }
void PvpCardBuffAction::Run()      { if (c > 0) AddEffect(b ? 0x164 : 0x165, PlayerPos(player)); }
```

<small>Handler: `0x137b93c` (called from the switch at `0x1373f18`) in the 5.60 arm64 client; callees read: `0x1838324`, `0x1837db0`, `0x1837f64`, `0x1838adc`, `0x1838c48`, `0x1838e64`, `0x1838d30`, `0x1912570`; action `Run` methods `0x18393d4`, `0x18392b4`, `0x1839778`, `0x1839578`, `0x18398c4`; update `0x18384cc`, end `0x183899c`, HP bars `0x1838f44`. Action class names from RTTI. Packet name from the client's packet-type string table (`0x108ea9c`).</small>

## Official client

**Received:** handled at `0x1373f18` in the incoming switch (`0x1373e20`).
