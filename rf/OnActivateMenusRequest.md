Does nothing in the 5.60 client: the registered handler is a bare `ret`. The name is still registered, so
sending it is harmless.

No arguments are read.

### Decompiled handler

```c
void OnActivateMenusRequest(GameLogic *self, VariantList *args) { }
```

<small>Handler: `0x135d128` (dispatcher `0x135e25c`) in the 5.60 arm64 client.</small>

<!-- args: -->
