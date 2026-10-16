# OnAction

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Makes a player do an emote: an animation, or a facial expression held for 3 seconds. The argument is the
command text, matched exactly (case-sensitive).

| # | Type | Meaning |
|---|---|---|
| 1 | string | the emote, e.g. `/wave` |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

| Text | Effect |
|---|---|
| `/dab` | animation `0x10d7d84` |
| `/dance` | animation `0x10d2f50` |
| `/dance2` | animation `0x10d7dcc` |
| `/dance3` | animation `0x10d7da8` |
| `/march` | animation `0x10d7df8` |
| `/shower` | animation `0x109b838` |
| `/rolleyes` | animation `0x10d7e5c` |
| `/furious` | animation `0x10d7eb0` |
| `/sleep` | animation `0x10d827c` |
| `/omg` | animation `0x10d84d4` |
| `/yes` | animation `0x10d82c4` |
| `/idk` | animation `0x10d848c` |
| `/fold` | animation `0x10d84b0` |
| `/no` | animation `0x10d851c` |
| `/sassy` | animation `0x10d853c` |
| `/fp` | animation `0x10d855c` |
| `/wave` | animation `0x10d7d64` |
| `/cheer` | animation `0x10d8258` |
| `/smh` | animation `0x10d885c`, only if the server's `proto` (login settings) is above 106 |
| `:P` | face 3 for 3 s |
| `/lol` | face 8 for 3 s |
| `/love` | face 14 for 3 s |
| `/troll` | face 15 for 3 s |
| `/shy` | face 27 for 3 s |
| `/grumpy` | face 28 for 3 s |
| anything else | logs `Unknown action: %s` |

The face is stored at avatar+0x100 and its timer (3.0 s) at avatar+0x104. Every frame the timer drops by the
elapsed time, and the face is cleared when it reaches 0 (`0x1305fd4`). Animation entries call a method on the
avatar's visuals (avatar+0x330); their names aren't known.

### Decompiled handler

```c
void NetAvatar::OnAction(NetAvatar *a, VariantList *vl) {
    std::string s = vl[1].s;
    if (s == "/dab")    { a->visual.Dab();    return; }            // 0x10d7d84
    if (s == "/dance2") { a->visual.Dance2(); return; }            // 0x10d7dcc
    if (s == "/dance3") { a->visual.Dance3(); return; }            // 0x10d7da8
    if (s == "/shower") { a->visual.Shower(); return; }            // 0x109b838
    if (s == "/dance")  { a->visual.Dance();  return; }            // 0x10d2f50
    if (s == "/march")  { a->visual.March();  return; }            // 0x10d7df8
    if (s == "/rolleyes") ...                                      // one call per row of the table above
    ...
    if (s == "/smh" && GetApp()->proto > 106) { a->visual.Smh(); return; }   // 0x10d885c
    int face;
    if      (s == ":P")      face = 3;
    else if (s == "/love")   face = 14;
    else if (s == "/lol")    face = 8;
    else if (s == "/troll")  face = 15;
    else if (s == "/shy")    face = 27;
    else if (s == "/grumpy") face = 28;
    else { Log("Unknown action: %s", s.c_str()); return; }
    a->face = face;                                                // avatar+0x100
    a->faceTimer = 3.0f;                                           // avatar+0x104
}
```

<small>Handler: `0x12f7030` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0xebda10` (string equals); face timer at `0x1305fd4`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnAction"` |
| 1 | string | /emote name |

The game packet header's `netID` names the player this call is about.

gurotopia: `include/onVariant/Action.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnAction", "..." }, pPeer->netid);
```
