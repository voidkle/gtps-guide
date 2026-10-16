# action|worldlock_storage_modify_amount

<Badge type="info" text="GENERIC_TEXT (2)" /> <Badge type="info" text="client → server" /> <Badge type="warning" text="not in gurotopia" />

## Format

Exactly as the 5.60 client formats it (`{}` is filled in):

```text
action|worldlock_storage_modify_amount
amount|{}
type|{}
```

## Fields

| Field | Meaning |
|---|---|
| `amount` | Amount of locks. |
| `type` | Which tab or type was picked. |

## When the client sends it

<Badge type="tip" text="decompiled from the 5.60 client" />

The **Add** and **Withdraw** buttons of the world-lock storage balance screen.

| Field | Value |
|---|---|
| message | message type 2 (GENERIC_TEXT) |
| `amount` | the amount on the screen (a 64-bit value, model+0x60) |
| `type` | `1` = add, `-1` = withdraw |

- The amount is reset to 0 and the screen closes after sending.

<small>Builders: `0x1d6f0d4` (Add), `0x1d6f2a8` (Withdraw).</small>

## Server

gurotopia doesn't handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.

## Send it yourself

With `send_text()` from [Talk to the server](/guide/talk-to-server):

```cpp
send_text(2, "action|worldlock_storage_modify_amount\namount|0\ntype|0\n");
```

<small>Client function: `0x1d6f0d4` in libgrowtopia.so 5.60.</small>
