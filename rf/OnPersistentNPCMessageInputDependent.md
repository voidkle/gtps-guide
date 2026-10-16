Like [OnPersistentNPCMessage](./OnPersistentNPCMessage), but the server sends two texts and the client
picks one by input method. Players using touch controls get argument 3, everyone else argument 2. The box
is always closable by [OnClearNPCMessage](./OnClearNPCMessage).

| # | Type | Meaning |
|---|---|---|
| 1 | uint | tile index (`x + y × width`) |
| 2 | string | text for keyboard / controller players |
| 3 | string | text for touch players |

Argument 3 is used on Android (platform id 4) always, and on other platforms when the saved option `touch`
is non-zero. Otherwise argument 2 is used.

### Decompiled handler

```c
void OnPersistentNPCMessageInputDependent(GameLogic *self, VariantList *args) {
    uint tile = arg1.u;
    std::string keys = arg2.str, touch = arg3.str;
    bool notAndroid = GetPlatform() != 4;                       // 0x14213b0
    if (notAndroid && GetApp()->GetVar("touch")->u == 0)
        self->npcMessage.Show(tile, keys, 1, 1, 1);             // 0x11827a8
    else
        self->npcMessage.Show(tile, touch, 1, 1, 1);
}
```

<small>Handler: `0x136d3c0` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x14213b0`, `0x117ded4`, `0x11827a8`.</small>

<!-- args: uint,string,string -->
