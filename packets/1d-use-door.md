# 0x1d USE_DOOR

<Badge type="info" text="GAME_PACKET (4)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="not implemented" />

The 5.60 client has its own handler for this type (`0x1374bf0`), so the official server sends it. Neither gurotopia nor GrowServer does yet.

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Player `netID` went through a door or portal. The client moves the avatar to `posX`/`posY` with the same code as
the `OnSetPos` function. It unfreezes the avatar with `OnSetFreezeState(0)` and plays a sound at the new
position. When the avatar is your own, it also calls `OnZoomCamera(10000, 1000)`, which moves the camera there.

| Field | Used as |
|---|---|
| `netID` | the player who moved; ignored if not in the world |
| `posX`, `posY` | the new position, in pixels; also where the sound plays |
| `itemID` | sound: 0 = `audio/door_open.wav`, 1 = `audio/teleport.wav`, anything else = silent |

### Decompiled handler

```c
case 0x1d: // USE_DOOR
    NetAvatar *avatar = GetAvatar(GetNetObjectManager(), pkt->netID);
    if (!avatar) break;

    VariantList args;
    args[0] = vec2{ pkt->posX, pkt->posY };
    Avatar_OnSetPos(avatar, args);                 // FUN_012f5158: the OnSetPos function

    if (avatar->controller == NULL) {              // avatar+0x110 is null for your own player
        args.clear();
        args[0] = 10000.0f;
        args[1] = 1000;
        OnZoomCamera(self, args);                  // FUN_0135dec8 ("rememberZoom")
    }
    args.clear();
    args[0] = 0;
    Avatar_OnSetFreezeState(avatar, args);         // FUN_012f54a0: the OnSetFreezeState function

    vec2 pos = { pkt->posX, pkt->posY };
    if (pkt->itemID == 1)      PlaySoundAt(self, pos, "audio/teleport.wav");
    else if (pkt->itemID == 0) PlaySoundAt(self, pos, "audio/door_open.wav");
    break;
```

<small>Handler: inline in the switch at `0x1374bf0`; callees read: `0x12f5158` (registered as `OnSetPos`), `0x12f54a0` (`OnSetFreezeState`), `0x135dec8` (`OnZoomCamera`), `0x1376ccc`.</small>

## Official client

**Received:** handled at `0x1374bf0` in the incoming switch (`0x1373e20`).
