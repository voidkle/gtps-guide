# OnSetRoleSkinsAndTitles

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="info" text="global: header netID -1" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Sets which role skins and role titles are unlocked for each of the six roles (probably Farmer, Builder, Surgeon, Fisher, Chef
and Startopian, in the client's role order). Each string has one character per role; missing characters leave that role's
flag unchanged.

| # | Type | Meaning |
|---|---|---|
| 1 | string | role skins: character *i* = `1` unlocks role *i*'s skin, anything else locks it (GameLogic+0x3b2…0x3b7) |
| 2 | string | role titles: character *i* = `2` unlocks role *i*'s title, anything else locks it (GameLogic+0x3b8…0x3bd) |

Both are read without a type check, so they must be strings. Example: `"110000"`, `"200000"`. The skin flags fill the
"Select a role skin:" menu (`0x15a185c` lists the unlocked roles).

### Decompiled handler

```c
// v[n] = argument n
void OnSetRoleSkinsAndTitles(GameLogic *self, VariantList *v) {
    std::string skins = v[1].s, titles = v[2].s;
    for (int i = 0; i < 6; i++) {
        if (skins.size()  > i) self->roleSkin[i]  = skins[i]  == '1';     // +0x3b2 + i
        if (titles.size() > i) self->roleTitle[i] = titles[i] == '2';     // +0x3b8 + i
    }
}
```

<small>Handler: `0x1371058` (dispatcher `0x135e25c`) in the 5.60 arm64 client; reader: `0x15a185c`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnSetRoleSkinsAndTitles", "...", "..." });
```
