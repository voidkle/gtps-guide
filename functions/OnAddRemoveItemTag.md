# OnAddRemoveItemTag

<Badge type="info" text="CALL_FUNCTION (0x01)" /> <Badge type="info" text="server → client" /> <Badge type="warning" text="runs on the player in the header netID" />

## What the client does with it

<Badge type="tip" text="decompiled from the 5.60 client" />

Adds a text tag to, or removes it from, an item of a player (the player in the CALL_FUNCTION header's
`netID`). Each item id has a list of strings on the player (avatar+0x2c78); where they're shown wasn't traced.

| # | Type | Meaning |
|---|---|---|
| 1 | int | item id |
| 2 | string | the tag |
| 3 | int | non-zero = add the tag to the item's list; 0 = remove it |

Adding doesn't check for duplicates; removing removes matching strings.

### Decompiled handler

```c
void NetAvatar::OnAddRemoveItemTag(VariantList *args) {     // 0x12f9398
    int item = args->GetInt(0);
    std::string tag = args->GetString(1);
    std::list<std::string> &tags = this->itemTags[item];    // avatar+0x2c78, std::map<int, list>
    if (args->GetInt(2) != 0) tags.push_back(tag);
    else RemoveFromList(&tags, tag);                        // 0x1311790
}
```

<small>Handler: `0x12f9398` (dispatcher `0x12ecb2c`) in the 5.60 arm64 client; callees read: `0xefeb64`, `0x1311790`.</small>

## Send it (server side)

```cpp
send_varlist(peer, { "OnAddRemoveItemTag", 1, "...", 1 }, pPeer->netid);
```
