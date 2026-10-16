Changes named variables of an item's configurable render object on a player (the player in the
CALL_FUNCTION header's `netID`): items whose look is driven by a config with variables (C++ class
`ItemConfigRenderObject`). Other items ignore it.

| # | Type | Meaning |
|---|---|---|
| 1 | int | item id; ignored if the item has no `ItemConfigRenderObject` behaviour |
| 2 | string | the variables, see below |

Format of argument 2: its **first character is the separator** for the entries, and each entry is
`type/name/value`:

```text
|type/name/value|type/name/value
```

- Empty entries are skipped.
- `type` is looked up in a global table of names (`0x2af9cf0`); unknown types are skipped. Probably value
  types such as a color or a number; the table's contents weren't dumped.
- `name` must match a variable of that item's render config (looked up at config+0xf0); otherwise skipped.
- `value` is converted by `type` and stored in the variable (`0x1a523d8`).

The player's own renderer state (avatar+0x330) selects which instance of the item is changed.

### Decompiled handler

```c
void NetAvatar::OnItemVariablesHasChanged(VariantList *args) {     // 0x12f957c
    ItemBehaviour *b = ItemBehaviours()->Find(args->GetInt(0));     // 0x11f5fac, 0x11f60d8
    if (auto *cfg = dynamic_cast<ItemConfigRenderObject *>(b))
        cfg->SetVariables(args->GetString(1), &this->renderer);     // 0xebe5d4
}

void ItemConfigRenderObject::SetVariables(std::string &s, AvatarRenderer *r) {   // 0xebe5d4
    auto inst = this->GetInstance(r);                                // vtable +0x448
    if (!inst) return;
    for (std::string e : Split(s, s[0])) {                           // 0x1e6b024
        if (e.empty()) continue;
        std::string type = PopToken(e, "/");                         // 0x1e6adac
        if (!VarTypes.contains(type)) continue;                      // 0x2af9cf0
        int typeId = VarTypes[type];
        std::string name  = PopToken(e, "/");
        std::string value = PopToken(e, "/");
        if (Var *v = FindVar(inst->config->vars, name))              // config+0xf0, 0xed7118
            SetVarValue(typeId, &v->value, value);                   // v+0xb8, 0x1a523d8
    }
}
```

<small>Handler: `0x12f957c` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0x11f60d8`, `0xebe5d4`, `0x1e6b024`, `0x1e6adac`.</small>

<!-- args: int,string -->
