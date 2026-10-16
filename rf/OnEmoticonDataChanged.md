Replaces the client's emoticon table (the chat shortcuts like `(wl)` and the character each one turns into).

| # | Type | Meaning |
|---|---|---|
| 1 | int | stored next to the table (a global at `0x29b5fa8`); not used in this path, probably a version or count |
| 2 | string | the emoticon list (see below) |

The list is split on `&` into entries, and each entry on `|` into exactly three fields; entries with a different number of
fields, or an empty name or code, are skipped:

```text
<name>|<code>|<enabled>&<name>|<code>|<enabled>&...
(wl)|ā|1&(yes)|Ă|1&(no)|ă|0
```

`name` is what the player types, `code` is the replacement character, and `enabled` (`atoi` ≠ 0) is stored per name,
probably "the player owns it". The old table is cleared first.

### Decompiled handler

```c
// v[n] = argument n
void OnEmoticonDataChanged(GameLogic *self, VariantList *v) {
    if (!v) return;
    int n = v[1].GetINT32();
    std::string list = v[2].s;
    g_emoticons.f_50 = n;                                  // DAT_029b5fa8 (static object at 0x29b5f58)
    g_emoticons.Load(list);                                // 0x1e64ee8
}

// 0x1e64ee8
void Emoticons::Load(std::string list) {
    names.clear(); enabled.clear();
    for (std::string e : Split(list, '&')) {
        auto f = Split(e, '|');
        if (f.size() != 3 || f[0].empty() || f[1].empty()) continue;
        AddPair(f[0], f[1]);                               // 0x1e65ab8
        enabled[f[0]] = atoi(f[2].c_str()) != 0;           // 0x1e65f2c
    }
}
```

<small>Handler: `0x1370d78` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1e64ee8`.</small>

<!-- args: int,string -->
