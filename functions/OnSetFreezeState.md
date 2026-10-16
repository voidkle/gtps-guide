# OnSetFreezeState

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets a player's freeze state. Any value other than 0 freezes the player. The movement and drawing code tests
for 1 separately, so 1 and 2 behave differently; how wasn't traced. gurotopia sends 1 when you die and 2 when you respawn.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | 0 = not frozen; 1 or 2 = frozen (see above) |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

- When the state goes from **2 to 0**, the client plays the respawn effects:
  - your own avatar gets flags 0x2800 added to avatar+0x124;
  - if the player's respawn tile is a Starship Transporter (6392), particle 254 plays on it;
  - the respawn animation starts at the checkpoint, or at the main door if there's none.
- Whenever the new state is 0, the `LoadingMessage` overlay fades out (600 ms) and avatar+0x18a is cleared.

### Decompiled handler

```c
void NetAvatar::OnSetFreezeState(NetAvatar *a, VariantList *vl) {
    int old = a->freezeState;                                      // avatar+0x128
    a->freezeState = vl[1].u;
    if (a->freezeState == 0 && old == 2) {
        if (!a->controller) {
            a->flags |= 0x2800;                                    // avatar+0x124
            if (a->physics) a->physics->dirty = 1;
        }
        PlayTransporterRespawnParticle(a);                         // 0x1311a2c: tile a->respawnTile is 6392 → particle 254
        a->visual.StartRespawnAnim();                              // 0x10d7978 (avatar+0x330)
    }
    if (a->freezeState == 0) {
        FadeOutLoadingMessage(NULL);                               // 0x1713d24: "LoadingMessage", "AboutToBeDeleted", 600 ms
        a->f_18a = 0;
    }
}
```

<small>Handler: `0x12f54a0` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x1311a2c`, `0x10d7978`, `0x1713d24`; readers of the state: `0x1306900`, `0x1307040`, `0x1335648`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnSetFreezeState"` |
| 1 | int | state (gurotopia sends 1, then 2) |

The game packet header's `netID` names the player this call is about.

gurotopia: `include/action/respawn.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnSetFreezeState", 1u }, pPeer->netid);
```
