Replaces the player's seed diary (which seeds they have recorded) with the server's copy, and saves it. The
server sends it after login when the `seed_diary_hash` from
[OnSuperMainStartAcceptLogonHrdxs47254722215a](./OnSuperMainStartAcceptLogonHrdxs47254722215a) didn't match,
probably.

It is registered by the screen controller (`0x1ba1ec8`) as an extra listener on GameLogic's function of the same name (`0x1be931c` connects it to GameLogic+0x28), so it runs only for calls with the CALL_FUNCTION header `netID` = -1.

| # | Type | Meaning |
|---|---|---|
| 1 | string | binary data: a list of u16 values, little-endian |

Each u16: the low 15 bits are an item id, bit 15 is a second flag.

- If the string's length is odd or 0, nothing is added (the diary is still cleared).
- Ids above 16432 (0x4030) are skipped, and so are ids for which `0x1483b54` returns true (a lookup in a
  global table; probably ids excluded from the diary).
- Every id is added to the first set (diary+0x878 bitset and a hash set at +0x1080). Ids with bit 15 also go
  into the second set (diary+0x48 bitset, hash set at +0x850). Probably "seen/planted" and "completed";
  the UI that shows them wasn't traced.

Afterwards the saved setting `seed_diary_hash_dirty` is set to 0 and the diary is saved to the setting
`seed_diary_data` (`0x1484cd4`, only if it changed).

### Decompiled handler

```c
void operator()(VariantList *const &vl) {                       // 0x1ba8e38
    SeedDiary *d = &GameLogic()->seedDiary;                     // +0x550
    d->Clear();                                                 // 0x1483a7c
    d->Load(vl->GetString(0), /*reset=*/true);                  // 0x14848f8
    GetApp()->Var("seed_diary_hash_dirty")->SetInt(0);
    d->Save(false);                                             // 0x1484cd4 → "seed_diary_data"
}

void SeedDiary::Load(const std::string &s, bool reset) {        // 0x14848f8
    if (reset) { /* clear both bitsets and hash sets */ this->dirty = true; }
    if (s.size() == 0 || s.size() & 1) return;
    for (size_t i = 0; i < s.size(); i += 2) {
        uint16_t v = (uint8_t)s[i] | (uint8_t)s[i + 1] << 8;
        uint id = v & 0x7fff;
        if (id > 0x4030 || IsExcluded(this, id)) continue;      // 0x1483b54
        this->have.set(id);  this->haveSet.insert(id);          // +0x878, +0x1080
        if (v & 0x8000) { this->done.set(id); this->doneSet.insert(id); }   // +0x48, +0x850
    }
}
```

<small>Handler: `0x1ba8e38` (dispatcher `0x1ba1ec8`) in the 5.60 arm64 client; callees read: `0x1483a7c`, `0x14848f8`, `0x1484cd4`.</small>

<!-- args: string -->
