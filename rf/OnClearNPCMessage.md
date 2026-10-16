Closes the NPC message box from [OnPersistentNPCMessage](./OnPersistentNPCMessage). It only acts if the box
was opened as closable (third argument 1, or any [OnPersistentNPCMessageInputDependent](./OnPersistentNPCMessageInputDependent)).
The closable mark is then cleared and the box's line times out 1 second later.

No arguments are read.

### Decompiled handler

```c
void OnClearNPCMessage(GameLogic *self) {
    MessageBox *box = self->npcMessage.box;            // self+0x1b0 +0x30
    if (box && box->closable) {                        // +0x65
        box->closable = 0;
        box->lines.first->expires = GetTick() + 1000;  // +0x2c
    }
}
```

<small>Handler: `0x136d68c` (dispatcher `0x135e25c`) in the 5.60 arm64 client; callees read: `0x1182a6c`, `0x118a114`.</small>

<!-- args: -->
