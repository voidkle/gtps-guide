Sets a player's country flag and badge flags. The flag icon drawn next to the name is
`interface/flags/<name>.rttex`.

| # | Type | Meaning |
|---|---|---|
| 1 | string | `<country>[_suffix]` then optional `|flag` words, e.g. `id|showGuild|maxLevel` |

Player function: the [CALL_FUNCTION](/packets/01-call-function) header's `netID` picks the player; the call is
dropped if that player isn't in the world.

**Parsing** (`0x131123c`):

1. The string is split on `|`. All eight badge flags are cleared, and each word after the first sets one:

   | Word | Flag |
   |---|---|
   | `showGuild` | avatar+0x3619 |
   | `maxLevel` | avatar+0x361a |
   | `master` | avatar+0x361b |
   | `doctor` | avatar+0x361c |
   | `donor` | avatar+0x361d |
   | `ccBadge` | avatar+0x361e |
   | `ttBadge` | avatar+0x361f |
   | `euphoriaTitle` | avatar+0x3620 |

2. The first word is cut at the first `_` (`id_5` → `id`).
3. Some words replace the flag icon. Later steps win:
   - `lg` becomes `us`;
   - `ccBadge` makes it `ccBadge`;
   - `ttBadge` makes it `ttBadge`;
   - a name ending in `` of Legend`` `` makes it `lg`;
   - `master` makes it `master_icon`;
   - `donor` makes it `g4g`.
4. The result is stored at avatar+0x140 and the icon reloads from `interface/flags/<result>.rttex` (`0x1310130`).

So the legend flag `lg` only shows for names ending in `` of Legend`` ``. [OnNameChanged](/functions/OnNameChanged)
runs the same code when a name changes.

### Decompiled handler

```c
void NetAvatar::OnCountryState(NetAvatar *a, VariantList *vl) {
    std::string s = vl[1].s;                                       // read without a type check
    SetCountryState(a, s);                                         // 0x131123c
}

void SetCountryState(NetAvatar *a, std::string &s) {
    std::vector<std::string> w = Split(s, "|");
    if (!w.empty()) s = w[0];
    memset(&a->badge[1], 0, 8);                                    // avatar+0x3619..0x3620
    for (size_t i = 1; i < w.size(); i++) {
        if (w[i] == "donor")         a->donor = 1;                 // +0x361d
        else if (w[i] == "master")   a->master = 1;                // +0x361b
        else if (w[i] == "doctor")   a->doctor = 1;                // +0x361c
        else if (w[i] == "ccBadge")  a->ccBadge = 1;               // +0x361e
        else if (w[i] == "ttBadge")  a->ttBadge = 1;               // +0x361f
        else if (w[i] == "euphoriaTitle") a->euphoriaTitle = 1;    // +0x3620
        else if (w[i] == "showGuild") a->showGuild = 1;            // +0x3619
        else if (w[i] == "maxLevel") a->maxLevel = 1;              // +0x361a
    }
    std::vector<std::string> c = Split(s, "_");
    if (!c.empty()) s = c[0];
    if (s == "lg") s = "us";
    if (a->ccBadge) s = "ccBadge";
    if (a->ttBadge) s = "ttBadge";
    if (a->name.size() >= 14 && a->name.ends_with(" of Legend``")) s = "lg";
    if (a->master) s = "master_icon";
    if (a->donor) s = "g4g";
    a->flagName = s;                                               // avatar+0x140
    a->LoadFlagIcon();                                             // 0x1310130: "interface/flags/" + s + ".rttex"
}
```

<small>Handler: `0x12f7594` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x131123c`, `0x1e6b024`, `0x1310130`.</small>

<!-- args: string -->
