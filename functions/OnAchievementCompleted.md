# OnAchievementCompleted

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Does nothing visible in 5.60. The handler only makes sure argument 1 exists as an int (it sets a missing one to 0) and
returns. Achievements are probably shown through other calls such as [OnAddNotification](./OnAddNotification) or a console
message.

| # | Type | Meaning |
|---|---|---|
| 1 | int | read, not used (probably the achievement id) |

### Decompiled handler

```c
void OnAchievementCompleted(GameLogic *self, VariantList *v) {
    v[1].GetINT32();       // result unused
}
```

<small>Handler: `0x13714bc` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnAchievementCompleted", 1 });
```
