Does nothing useful in the 5.60 client. The handler only checks whether it could open the Ubisoft Club menu.
If the `UbiclubMenu` isn't open and another menu or dialog is, it logs "Ignoring dialog request". No menu is
built and no argument is read.

### Decompiled handler

```c
void OnUbiclubRequest(GameLogic *self, VariantList *args) {
    if (!FindEntity(GetEntityRoot(), "UbiclubMenu") && IsAnyMenuOpen())
        Log("Ignoring dialog request");
}
```

<small>Handler: `0x136ec7c` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: -->
