# 0x1b BATTLE_JOIN

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1373f5c`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Puts a player on a team (team battles, capture the flag) and prints who joined which team in the console log. The player's score is reset to 0 and any flag/egg they carried is cleared.

| Field | Used as |
|---|---|
| `netID` | the player joining; `-1` or a player not in the world does nothing |
| `tileX` | the team: 0 Red Rabbits, 1 Blue Bombers, 2 Yellow Yaks, 3 Purple Penguins; 4 or more means "joined the game" (no team name shown) |

### Decompiled handler

```c
case 0x1b: // BATTLE_JOIN
    if (pkt->netID == -1) break;
    NetAvatar *p = GetAvatar(pkt->netID);
    if (!p) break;
    p->team = (uint8_t)pkt->tileX;          // avatar+0x26d
    SetBattleScore(p, 0);                   // sub_1313674: avatar+0x270 = 0, refreshes the scoreboard
    p->carried = 0xff;                      // avatar+0x26e: carries no flag/egg

    std::string msg;
    if (pkt->tileX < 4) {
        if (p == self->localPlayer)
            msg = "You joined the " + TeamName(pkt->tileX, /*colored*/true) + "!";
        else
            msg = p->name + " joined the " + TeamName(pkt->tileX, true) + "!";
    } else {
        msg = (p == self->localPlayer) ? "You joined the game!"
                                       : p->name + " joined the game!";
    }
    AddToLog(msg);                          // sub_1716724: "LogDisplayEntity" console log
    break;

// sub_14db034 TeamName(team, colored)
//   0 "`4Red Rabbits``", 1 "`1Blue Bombers``", 2 "`6Yellow Yaks``", 3 "`#Purple Penguins``",
//   anything else "`bSpooky Skulls``" (without the color codes when colored == false)
```

<small>Handler: inline in the switch at `0x1373f5c` in the 5.60 arm64 client; callees read: `0x14db034`, `0x13785e4`, `0x1313674`, `0x1716724`.</small>

## Official client

**Received:** handled at `0x1373f5c` in the incoming switch (`0x1373e20`).
