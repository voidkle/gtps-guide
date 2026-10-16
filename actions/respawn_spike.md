# action|respawn_spike

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="tip" text="handled by gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|respawn_spike
tileX|{}
tileY|{}
```

## Fields

| Field | Meaning |
|---|---|
| `tileX` | Tile column (0-99). |
| `tileY` | Tile row (0-59). |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

**Format correction:** there are two forms. With a tile: `action|respawn_spike\ntileX|x\ntileY|y\n`.
Without one (death not caused by a tile): `action|respawn_spike\n`.

Sent by your own avatar when it dies on a deadly tile (spikes, lava and similar) or from another death source.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `tileX`, `tileY` | the tile that killed you (tile+0x54, +0x55), when there is one |

- Ignored if the avatar is already respawning (avatar+0x128 != 0); otherwise sets it to 2 and starts the death animation (`0x12f5620`).
- On a Starship Airlock (item 6398) it also triggers that tile's effect first.

```c
void Avatar::DieOnTile(Tile *t) {                             // 0x12f9a18
    if (self->respawnState) return;
    self->respawnState = 2; PlayDeath(self);
    if (!t) SendText(2, "action|respawn_spike\n");
    else    SendText(2, "action|respawn_spike\ntileX|" + to_string(t->x) + "\ntileY|" + to_string(t->y) + "\n");
}
```

<small>Builder: `0x12f9a18`; called from `0x12f8e64`, `0x12f99a4`, `0x13002b4`, `0x131029c`, `0x131092c`, `0x137bd14`, `0x1816ee8`, `0x193f3c0`, `0x1944868`.</small>

## Server

gurotopia: [`include/action/respawn.cpp`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/respawn.cpp).

Reply: Same as `respawn`; gurotopia ignores the tile.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|respawn_spike\ntileX|25\ntileY|37\n");
```

<small>Client function: `0x12f9a18` in libgrowtopia.so 5.60.</small>
