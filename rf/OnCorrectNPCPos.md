The 5.60 client registers this name, but its handler is a single `ret`: the call is accepted and ignored, whatever the
arguments. It is probably left over from an older version, or the feature moved elsewhere.

### Decompiled handler

```c
void OnCorrectNPCPos(GameLogic *self, VariantList *v) { }
```

<small>Handler: `0x137186c` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: -->
