# OnDailyChallengeRequest

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets the daily-challenge state that the HUD shows. Argument 1 is a `|`-separated list, and the handler only
stores the values. Nothing is opened. Where the HUD reads them back wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | string | `active|value1|value2|itemID` |

| Field | Stored at (GameLogic) | Meaning |
|---|---|---|
| `active` | +0x504 | non-zero = a challenge is running |
| `value1` | +0x508 | an int; probably the progress or goal |
| `value2` | +0x510 | an int; probably a time in seconds, since the client stores the current time next to it (+0x50c) |
| `itemID` | +0x514 | the challenge item; its icon's sprite cell is stored at +0x518/+0x51c (`0x1166780`). An unknown id is ignored |

Fields are read with `atoi`, so a missing field reads as 0.

### Decompiled handler

```c
void OnDailyChallengeRequest(GameLogic *self, VariantList *args) {
    std::string s = arg1.str;
    self->challengeActive = atoi(NextToken(&s, "|")) != 0;      // 0x1e6adac
    self->challengeValue1 = atoi(NextToken(&s, "|"));
    self->challengeValue2 = atoi(NextToken(&s, "|"));
    self->challengeTime   = GetTimeNow();                       // 0x1422568, +0x50c
    ItemInfo *it = GetItem(atoi(NextToken(&s, "|")));
    if (it) {
        GetItemIconCell(it, &self->challengeIconX, &self->challengeIconY);   // 0x1166780
        self->challengeItem = it->id;                           // +0x514
    }
}
```

<small>Handler: `0x136ded4` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1e6adac`, `0x1564a48`, `0x1166780`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnDailyChallengeRequest", "..." });
```
