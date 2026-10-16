Stores the new level in the client's Ubisoft services adapter (a singleton created on first use, logged as
`UbiServicesAdapter : `). The handler shows nothing by itself; the level-up effects come from the
`OnParticleEffect` and `OnTalkBubble` calls the server sends with it.

| # | Type | Meaning |
|---|---|---|
| 1 | uint | the player's new level |

Global function: send it with `netID` -1 in the [CALL_FUNCTION](/packets/01-call-function) header.

### Decompiled handler

```c
void GameLogic::OnPlayerLeveledUp(GameLogic *self, VariantList *vl) {
    UbiServicesAdapter *ubi = UbiServicesAdapter::Get();          // 0x29af3c0, created here if null
    ubi->playerLevel = vl[1].u;                                    // +0x4c
}
```

<small>Handler: `0x1372780` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: uint -->
