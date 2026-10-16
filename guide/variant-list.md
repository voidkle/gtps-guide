# Variant lists

The server calls functions on the client with a [CALL_FUNCTION (0x01)](/packets/01-call-function) game
packet. Its extra data is a variant list:

```text
u8 count
repeat count times:
  u8 index      0 = function name, 1.. = arguments
  u8 type
  data
```

| Type | Name | Data |
|---|---|---|
| 1 | float | 4 bytes |
| 2 | string | u32 length + bytes (no NUL) |
| 3 | vec2 | 2 × f32 |
| 4 | vec3 | 3 × f32 |
| 5 | uint32 | 4 bytes |
| 9 | int32 | 4 bytes |

In the game packet header around it:

- `netID` says which player the call is about (`OnSetPos`, `OnSetClothing`, ...), or -1.
- `itemID` is a delay in milliseconds before the client runs it.
- `flags` has S_EXTENDED (0x08).

Each function with known arguments has its own page under **Server functions**.

## Reading one

```cpp
std::vector<std::string> read_variants(const unsigned char *p, size_t n)
{
    std::vector<std::string> out;
    size_t o = 1;
    for (int k = 0; k < p[0] && o + 2 <= n; ++k)
    {
        unsigned idx = p[o], type = p[o + 1];
        o += 2;
        if (out.size() <= idx) out.resize(idx + 1);
        if (type == 2) { unsigned len; memcpy(&len, p + o, 4); out[idx].assign((const char*)p + o + 4, len); o += 4 + len; }
        else if (type == 5 || type == 9) { int v; memcpy(&v, p + o, 4); out[idx] = std::to_string(v); o += 4; }
        else if (type == 1) { float v; memcpy(&v, p + o, 4); out[idx] = std::to_string(v); o += 4; }
        else if (type == 3) o += 8;
        else if (type == 4) o += 12;
        else break;
    }
    return out;
}
```

Call it with `data + 60` and `length - 60` (skip the message type and header).

## Writing one (server side)

gurotopia's `send_varlist()` (`include/proton/Variant.cpp`) builds the packet:

```cpp
send_varlist(peer, { "OnConsoleMessage", "hello" });
send_varlist(peer, { "OnSetPos", CL_Vec2f{ 672.f, 1152.f } }, netid); // netid goes in the header
```
