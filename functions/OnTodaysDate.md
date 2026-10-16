# OnTodaysDate

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Gives the client the server's date and two more numbers. Month and day drive date-based visuals (many item and weather
effects compare them, for example to pick a season or zodiac sign).

| # | Type | Meaning |
|---|---|---|
| 1 | int | month, 1-12 (GameLogic+0x13c) |
| 2 | int | day of the month (GameLogic+0x134) |
| 3 | uint | GameLogic+0x144, also copied to the UbiServices adapter (+0x28) |
| 4 | uint | GameLogic+0x138, also copied to the UbiServices adapter (+0x4c) |

Arguments 3 and 4 are compared (≥) against two minimum values in a requirement check that a script binding registers next
to `MinPlayTimeRequirementInDays` and `IsPlayTimeRequirementsMet`. So they are probably play-time values, such as the
account's age in days, and the analytics adapter gets them too. gurotopia sends 0 for both.

### Decompiled handler

```c
// v[n] = argument n
void OnTodaysDate(GameLogic *self, VariantList *v) {
    self->month = v[1].GetINT32();          // +0x13c
    self->day   = v[2].GetINT32();          // +0x134
    self->f_144 = v[3].GetUINT();
    self->f_138 = v[4].GetUINT();
    UbiServicesAdapter *u = UbiServicesAdapter::Get();     // created on first use ("UbiServicesAdapter : ")
    u->f_28 = v[3].GetUINT();
    u->f_4c = v[4].GetUINT();
}

// 0x1cda634, the requirement check
bool IsPlayTimeRequirementsMet(Req *r) {
    return GetGameLogic()->f_138 >= r->f_1c && GetGameLogic()->f_144 >= r->f_18;
}
```

<small>Handler: `0x13718f8` (dispatcher `0x135e25c`) in the 5.60 arm64 client; reader: `0x1cda634`.</small>

## As gurotopia sends it

| # | Type | Meaning |
|---|---|---|
| 0 | string | `"OnTodaysDate"` |
| 1 | int | month |
| 2 | int | day |
| 3 | uint |  |
| 4 | uint |  |

gurotopia: `include/action/enter_game.cpp`.

## Send it (server side)

```cpp
send_varlist(peer, { "OnTodaysDate", 1, 1, 1u, 1u });
```
