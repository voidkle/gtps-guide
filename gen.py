"""
Writes one Markdown page per packet (messages/, packets/, actions/, functions/) and the sidebar
(.vitepress/sidebar.json) from the tables below. Edit the tables, then run:  python3 docs/gen.py

Sources: gurotopia (this repo), GrowServer 4.0.0, and static analysis of the Growtopia 5.60 Android
client (libgrowtopia.so). "client fn" values are function addresses in that libgrowtopia.so.
"""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- message types (first 4 bytes)
MESSAGES = [
    (1, 'SERVER_HELLO', 'server → client',
     'Sent by the server as soon as an ENet connection is up. The body is empty; it means "send your login now".',
     'include/eventType/connect.cpp', '01 00 00 00 00'),
    (2, 'GENERIC_TEXT', 'client → server',
     'Text from the client: the two login messages and most `action|...` messages (each action page says which type it uses). See the two login pages.',
     'include/eventType/receive.cpp', None),
    (3, 'GAME_MESSAGE', 'both',
     'Text actions. The client sends a few actions as type 3 (`join_request`, `quit`, ...); the server sends commands such as `action|log` and `action|play_sfx`, listed on [Text commands from the server](/guide/server-text).',
     'include/eventType/receive.cpp', None),
    (4, 'GAME_PACKET', 'both',
     'Binary game packets: the 56-byte header plus optional extra data. See [Game packet header](/guide/game-packet) and the Game packets section.',
     'include/eventType/receive.cpp', None),
    (5, 'ERROR', 'server → client', 'Error text. The client passes it to a signal nothing listens to. Not used by gurotopia or GrowServer.', None, None),
    (6, 'TRACK', 'server → client', 'Analytics: the server asks the client to log an event. The client never sends it. gurotopia only prints "received unqiue" if one arrives.', None, None),
    (7, 'CLIENT_LOG_REQUEST', 'server → client', 'The client only logs the name. Not used by either server.', None, None),
    (8, 'CLIENT_LOG_RESPONSE', '-', 'Not handled and never sent by the 5.60 client.', None, None),
    (9, 'NETSTATE_SNAPSHOT', 'server → client', 'A binary state snapshot for the client\'s "NetState" system, used only in some worlds (probably PvE / dungeon). The name is this site\'s; the client has none.', None, None),
    (10, 'NETSTATE_FRAME', 'both', 'Binary "NetState" frames, used only in some worlds (probably PvE / dungeon). The two directions have different bodies. The name is this site\'s.', None, None),
    (11, 'NETSTATE_RAW', 'client → server', '8 raw bytes, sent unreliable from the same world tick as type 10. The name is this site\'s.', None, None),
]

# ---------------------------------------------------------------- shared field descriptions
FIELDS = {
    'name': 'World name. Letters and digits only, at most 24 characters. gurotopia uppercases it.',
    'invitedWorld': '`1` if joining from an invite, otherwise `0`.',
    'tileX': 'Tile column (0-99).', 'tileY': 'Tile row (0-59).',
    'text': 'Chat text. Starts with `/` for commands.',
    'netid': 'The player\'s `netID` in the current world (from their `OnSpawn`).',
    'growid': 'A GrowID.', 'delay': 'Delay value from the UI.', 'type': 'Which tab or type was picked.',
    'location': 'Where the menu was opened from: `gem`, `bottommenu`, `pausemenu`, ...',
    'item': 'Store item or category id.', 'selection': 'Store entry inside `item`.',
    'itemID': 'Item id from items.dat.', 'count': 'Amount of the item.',
    'status': '`1` to set, `0` to undo.', 'color': 'Skin color as an unsigned 32-bit number.',
    'roleType': 'Role skin or icon index.', 'animDeath': 'Death animation id.', 'animRespawn': 'Respawn animation id.',
    'localHour': 'The device\'s local hour.', 'filtering': '`1` on, `0` off.', 'cbits': 'Client setting bits.',
    'show': '`1` on, `0` off.', 'GDPR': '`1` if accepted.', 'answer': 'Survey answer.', 'adName': 'Ad placement name.',
    'jsonStr': 'Weather machine settings as JSON.', 'pageIndex': 'Page number.', 'sortType': 'Sort order.',
    'searchItem': 'Search text.', 'bidAmount': 'Bid in World Locks.', 'price': 'Price.', 'duration': 'Auction length.',
    'state': 'Auction tile state.', 'startIndex': 'First row.', 'endIndex': 'Last row.', 'relative': 'Rows relative to you.',
    'chalid': 'Challenge id.', 'questid': 'Quest id.', 'isChal': '`1` for a challenge.', 'participantIndex': 'Who you vote for.',
    'messageID': 'Mailbox message id.', 'listIDs': 'Comma-separated message ids.', 'preset': 'Wardrobe preset slot.',
    'amount': 'Amount of locks.', 'dialog_name': 'The name from the dialog\'s `end_dialog|<name>|...` line.',
}

# ---------------------------------------------------------------- actions (GAME_MESSAGE, client → server)
# (name, group, exact format, client fn, gurotopia handler or None, what gurotopia sends back, note)
A = []
def act(name, group, fmt, fn, handler=None, reply=None, note=None):
    A.append(dict(name=name, group=group, fmt=fmt, fn=fn, handler=handler, reply=reply, note=note))

W, S, C, I, T, D, ST, E = 'World', 'Session', 'Chat & players', 'Inventory & items', 'Trading', 'Dialogs', 'Store', 'Events & extras'
act('join_request', W, 'action|join_request\nname|{}\ninvitedWorld|{}\n', '0x1383e28, 0x1c1653c', 'join_request.cpp',
    '`SEND_MAP_DATA` (0x04), `OnEmoticonDataChanged`, `OnSpawn` for every player (yours has `type|local`), `OnSetPos`, `OnConsoleMessage`, `OnSetClothing`, `OnCountryState`. On a bad name: `OnFailedToEnterWorld`.')
act('quit_to_exit', W, 'action|quit_to_exit', '0x1c10eb8', 'quit_to_exit.cpp', '`OnRemove` to the others in the world, then the world menu.')
act('validate_world', W, 'action|validate_world\nname|{}\n', '0x1c163d0', note='Sent while typing a world name in the world menu.')
act('world_button', W, 'action|world_button\nname|{}\n', '0x1c16adc', note='A category button in the world menu.')
act('gohomeworld', W, 'action|gohomeworld\n', '0x1c1730c')
act('respawn', W, 'action|respawn\n', '0x17289bc', 'respawn.cpp', '`OnKilled`, `OnSetFreezeState`, then `OnSetPos` at the world spawn.')
act('respawn_spike', W, 'action|respawn_spike\ntileX|{}\ntileY|{}\n', '0x12f9a18', 'respawn.cpp', 'Same as `respawn`; gurotopia ignores the tile.')
act('on_use_door_tutorial', W, 'action|on_use_door_tutorial\n', '0x197b92c')
act('update_weather_machine', W, 'action|update_weather_machine\njsonStr|{}\n', '0x1cb3188')

act('enter_game', S, 'action|enter_game\n', '0x1ba7aac, 0x1ba6598', 'enter_game.cpp',
    'Welcome `OnConsoleMessage`s, `SEND_INVENTORY_STATE` (0x09), `OnSetBux`, `SetHasGrowID`, `OnTodaysDate`, `OnRequestWorldSelectMenu`, the gazette `OnDialogRequest`, `PING_REQUEST` (0x16), `OnSetFeatureEnableFlags`.',
    'The client may add `crossplaySetting|{}`.')
act('refresh_item_data', S, 'action|refresh_item_data\n', '0x1ba6598', 'refresh_item_data.cpp', '`SEND_ITEM_DATABASE_DATA` (0x10) with the whole items.dat.',
    'Sent when the items.dat hash in `OnSuperMainStartAcceptLogon...` doesn\'t match the client\'s copy.')
act('refresh_player_tribute_data', S, 'action|refresh_player_tribute_data\n', '0x1ba6598')
act('quit', S, 'action|quit', '0x11424bc', 'quit.cpp', 'The server disconnects the peer.')
act('growid', S, 'action|growid\n', '0x17289bc', note='"Create GrowID" from the pause menu.')
act('requestAccountDelete', S, 'action|requestAccountDelete\n', '0x1383d60')
act('AccountSecurity', S, 'action|AccountSecurity\nlocation|pausemenu\n', '0x17289bc')
act('setGDPR', S, 'action|setGDPR\nGDPR|{}\n', '0x1382be4')

act('input', C, 'action|input\n|text|{}', '0x1682f84, 0x1c2477c', 'input.cpp',
    'Chat: `OnTalkBubble` and `OnConsoleMessage` to everyone in the world. Commands (`/...`): handled in `include/commands/`.',
    'The client sometimes appends `\\n|[FT##]|1`. gurotopia rate-limits 5 messages in 6 seconds.')
act('wrench', C, 'action|wrench\n|netid|{}\n', '0x13a6864, 0x1c61ca4', 'wrench.cpp', '`OnDialogRequest` with the player\'s wrench menu (yours or someone else\'s).')
act('pveprofile', C, 'action|pveprofile\n|growid|{}\n', '0x1720730')
act('friends', C, 'action|friends\ndelay|{}\n', '0x1663bb4, 0x1c60de0', 'friends.cpp', '`OnDialogRequest` with the friends menu.',
    'From the pause menu it\'s `action|friends\\nlocation|pausemenu\\n` instead.')
act('communitytabs', C, 'action|communitytabs\ntype|{}\n', '0x1663bb4')
act('setchatFilter', C, 'action|setchatFilter\nfiltering|{}\n', '0x1382894')
act('setFilter', C, 'action|setFilter\nfiltering|{}\ncbits|{}\n', '0x1382570', note='The swear filter.')
act('setOnlyFriendsChat', C, 'action|setOnlyFriendsChat\nshow|{}\n', '0x13829d8')

act('drop', I, 'action|drop\n|itemID|{}\n', '0x16f6ed4', 'drop.cpp', '`OnDialogRequest` asking how many (dialog `drop_item`), or `OnTextOverlay` "You can\'t drop that."')
act('trash', I, 'action|trash\n|itemID|{}\n', '0x16f71a8', 'trash.cpp', '`OnDialogRequest` asking how many to destroy (dialog `trash_item`).')
act('info', I, 'action|info\n|itemID|{}\n|count|{}\n', '0x16f73e0', 'info.cpp', '`OnDialogRequest` with the item\'s description and rarity.')
act('itemfavourite', I, 'action|itemfavourite\n|itemID|{}\n', '0x16f7c64', 'itemfavourite.cpp', '`OnFavItemUpdated`. At most 20 favourites.')
act('inventoryfavuitrigger', I, 'action|inventoryfavuitrigger\n', '0x13940cc', 'inventoryfavuitrigger.cpp', '`OnDialogRequest`.')
act('setSkin', I, 'action|setSkin\ncolor|{}\n', '0x13774e0', 'setSkin.cpp', '`OnSetClothing` with the new skin color.')
act('setRoleSkin', I, 'action|setRoleSkin\nroleType|{}\n', '0x13776c4')
act('setRoleIcon', I, 'action|setRoleIcon\nroleType|{}\n', '0x13778a8')
act('setDeath', I, 'action|setDeath\nanimDeath|{}\n', '0x1382044')
act('setRespawn', I, 'action|setRespawn\nanimRespawn|{}\n', '0x1382384')
act('PlasmaGlobeHeartLocalHour', I, 'action|PlasmaGlobeHeartLocalHour\nlocalHour|{}\n', '0x1382228')
act('wardrobe_save_ui', I, 'action|wardrobe_save_ui\npreset|{}\n', '0x1d68d64', note='The client formats `action|wardrobe_{}_ui` with `save` or `load`.')
act('wardrobe_load_ui', I, 'action|wardrobe_load_ui\npreset|{}\n', '0x1d68d64', note='The client formats `action|wardrobe_{}_ui` with `save` or `load`.')
act('wardrobe_preset_load', I, 'action|wardrobe_preset_load\n', '0x1d683d8')
act('wardrobe_purchase_slot', I, 'action|wardrobe_purchase_slot\n', '0x1d68c00')
act('wardrobe_unequip_all', I, 'action|wardrobe_unequip_all\n', '0x1d55908')
act('worldlock_storage_getpage', I, 'action|worldlock_storage_getpage\npageIndex|{}\n', '0x1d7d084')
act('worldlock_storage_modify_amount', I, 'action|worldlock_storage_modify_amount\namount|{}\ntype|{}\n', '0x1d6f0d4')

TN = 'The client opens the trade window with `trade_started`, then sends `mod_trade`/`rem_trade` as items change, `trade_lock` and `trade_accept` with `status`, and `trade_cancel` when closed. The server side is `OnStartTrade`, `OnTradeStatus` and `OnForceTradeEnd`. gurotopia doesn\'t implement trading yet.'
act('trade_started', T, 'action|trade_started\nnetid|{}\n', '0x178cd48', note=TN)
act('mod_trade', T, 'action|mod_trade\nitemID|{}\n', '0x178e3b4', note=TN)
act('rem_trade', T, 'action|rem_trade\nitemID|{}\n', '0x178e3b4', note=TN)
act('trade_lock', T, 'action|trade_lock\nstatus|{}\n', '0x178aeec', note=TN)
act('trade_accept', T, 'action|trade_accept\nstatus|{}\n', '0x178aeec', note=TN)
act('trade_check_price', T, 'action|trade_check_price\n', '0x178aeec', note=TN)
act('trade_cancel', T, 'action|trade_cancel\n', '0x178aeec', note=TN)

act('dialog_return', D, 'action|dialog_return\ndialog_name|{}\n', '0x16690ac, 0x169000c, 0x1693460', 'dialog_return.cpp',
    'Depends on the dialog; gurotopia\'s handlers are in `include/action/dialog_return/`.',
    'After `dialog_name`, the client adds every `embed_data` as `key|value`, every text input as `name|value`, checkboxes as `name|0` or `name|1`, and `buttonClicked|<id>` for the button pressed. The `end_dialog` OK button adds no `buttonClicked` line (except for a few built-in dialogs), and Cancel sends nothing; see [Dialog elements](/guide/dialog-elements). Example:\n\n```text\naction|dialog_return\ndialog_name|drop_item\nitemID|2|\ncount|5\n```')

act('store', ST, 'action|store\nlocation|{}\n', '0x1c6120c, 0x16f774c, 0x17289bc', 'store.cpp', '`OnStoreRequest` with the store page.')
act('storenavigate', ST, 'action|storenavigate\nitem|{}\nselection|{}\n', '0x16a2f7c, 0x1773c00', 'storenavigate.cpp', '`OnStoreRequest` for that tab.')
act('buy', ST, 'action|buy\nitem|{}\n', '0x175dcdc, 0x176791c', 'buy.cpp', '`OnStorePurchaseResult` and an updated `OnStoreRequest`.')
act('killstore', ST, 'action|killstore\nitem|{}\n', '0x175dcdc')
act('chaching', ST, 'action|chaching\r\n', '0x1083db8')
act('houston_validation_done', ST, 'action|houston_validation_done\npackageName|{}\nproductId|{}\npurchaseTime|{}\npurchaseState|{}\ndeveloperPayload|{}\npurchaseToken|{}\ncurrency|{}\nprice|{}\nhoustonTransId|{}\norderId|{}\nhoustonresult|{}\n', '0x16dfbd0',
    note='The receipt of a real-money purchase. A private server has no reason to accept these.')

act('dailyrewardmenu', E, 'action|dailyrewardmenu\n', '0x16f7ab0')
act('claimdailyreward', E, 'action|claimdailyreward\n', '0x167c1ac')
act('resetclaimdailyreward', E, 'action|resetclaimdailyreward\n', '0x167bf60')
act('eventmenu', E, 'action|eventmenu\n', '0x1c6105c')
act('UbiclubMenu', E, 'action|UbiclubMenu\nlocation|pausemenu\n', '0x17289bc')
act('claimwinterrallyreward', E, 'action|claimwinterrallyreward\n', '0x17957c4')
act('surveyanswer', E, 'action|surveyanswer\nanswer|{}\n', '0x1782600')
act('adClosed', E, 'action|adClosed\r\nadName|{}\r\n', '0x1f245e8')
act('get_seed_diary_data', E, 'action|get_seed_diary_data\n', '0x136accc')
act('complete_seeddiary_tutorial', E, 'action|complete_seeddiary_tutorial\n', '0x1d3252c')
act('tutorialTaskQuestClicked', E, 'action|tutorialTaskQuestClicked\n', '0x1c5ad7c')
act('tutorialTaskPhoneClicked', E, 'action|tutorialTaskPhoneClicked\n', '0x1d24498')
act('fashion_show_join_to_room', E, 'action|fashion_show_join_to_room\n', '0x1ce4ae8')
act('fashion_show_vote', E, 'action|fashion_show_vote\nparticipantIndex|{}\n', '0x1cf4d0c')
act('mailbox_getpage', E, 'action|mailbox_getpage\npageIndex|{}\n', '0x1d0e738')
act('mailbox_readmessage', E, 'action|mailbox_readmessage\nmessageID|{}\n', '0x1d1049c')
act('mailbox_claimreward', E, 'action|mailbox_claimreward\nmessageID|{}\n', '0x1d10240')
act('mailbox_claimrewardsmany', E, 'action|mailbox_claimrewardsmany\nlistIDs|{}\n', '0x1d0fab8')
act('auction_getpage', E, 'action|auction_getpage\npageIndex|{}\nsortType|{}\nsearchItem|{}\n', '0x1c90084')
act('auction_place_bid', E, 'action|auction_place_bid\nbidAmount|{}\n', '0x1c518fc')
act('set_auction_tile', E, 'action|set_auction_tile\nitem|{}|price|{}|duration|{}|state|{}', '0x1c80b20', note='Unusually, the fields share one line.')
act('startdungeonbtn', E, 'action|startdungeonbtn\n', '0x1cd3574')
act('showdungeoninvitefriends', E, 'action|showdungeoninvitefriends\n', '0x1cd342c')
act('purchase_dungeon_pass', E, 'action|purchase_dungeon_pass\n', '0x1cd36c4')
act('purchase_dungeon_scroll', E, 'action|purchase_dungeon_scroll\n', '0x1cd3814')
act('dungeonBackpackClicked', E, 'action|dungeonBackpackClicked\n', '0x1c3ef70')
act('activatedungeonchallenge', E, 'action|activatedungeonchallenge\n|chalid|{}\n', '0x1cd416c')
act('giveupdungeonchallenge', E, 'action|giveupdungeonchallenge\n|chalid|{}\n', '0x1cd416c')
act('claimdungeonchallengerewards', E, 'action|claimdungeonchallengerewards\n|questid|{}\n|isChal|{}\n', '0x1cd416c')
act('dungeonleaderboard_getrange', E, 'action|dungeonleaderboard_getrange\nstartIndex|{}\nendIndex|{}\nrelative|{}\n', '0x1cc00c4')

# ---------------------------------------------------------------- game packets (GAME_PACKET, type byte)
# (type, name, direction, status, fields used [(header field, meaning)], extra data, gurotopia, client evidence, example)
P = []
def pkt(t, name, direction, status, fields=(), extra=None, gt=None, client=None, example=None):
    P.append(dict(t=t, name=name, direction=direction, status=status, fields=list(fields), extra=extra, gt=gt, client=client, example=example))

pkt(0x00, 'STATE', 'both', 'confirmed', [('netID', 'who moved (set by the server when it re-broadcasts)'), ('flags', '`S_MOVE_LEFT` / `S_MOVE_RIGHT` (facing), `S_JUMP`, `S_LAVA_HIT`...'), ('pos', 'position in pixels (tile × 32)'), ('speed', 'velocity')],
    gt='`include/gamePacket/movement.cpp`: stores your position and facing, takes damage on `S_LAVA_HIT`, then re-broadcasts the packet to the world with your `netID`.',
    example='send_packet(gamePacket{ .type = 0x00, .netid = my_netid, .state = 0x20 /*S_MOVE_RIGHT*/, .pos = {22 * 32.0f, 36 * 32.0f} });')
pkt(0x01, 'CALL_FUNCTION', 'server → client', 'confirmed', [('netID', 'the player the call is about, or -1'), ('flags', '`S_EXTENDED` (0x08)'), ('itemID', 'delay in milliseconds before the client runs it'), ('extraDataLength', 'size of the variant list')],
    extra='A variant list. Variant 0 is the function name. See [Variant lists](/guide/variant-list) and the Server functions section.',
    gt='Built by `send_varlist()` in `include/proton/Variant.cpp`.')
pkt(0x02, 'UPDATE_STATUS', '-', 'unused')
pkt(0x03, 'TILE_CHANGE_REQUEST', 'both', 'confirmed', [('itemID', '18 = punch, 32 = wrench, anything else = the item to place'), ('pos', 'your position in pixels'), ('tileX / tileY', 'the tile')],
    gt='`include/gamePacket/tile_change.cpp`. Punching sends `TILE_APPLY_DAMAGE` (0x08) until the block breaks; then this packet comes back with `itemID` 18. Placing echoes this packet with the placed item. Doors, signs, locks and seeds also get a `SEND_TILE_UPDATE_DATA` (0x05).',
    client='helper `0x1381530` (7 callers) fills `itemID` and the tile from the player\'s selected tile.',
    example='send_packet(gamePacket{ .type = 0x03, .netid = my_netid, .id = 18 /*fist*/, .pos = my_pos, .punch = {25, 37} });')
pkt(0x04, 'SEND_MAP_DATA', 'server → client', 'confirmed', [('flags', '`S_EXTENDED`'), ('extraDataLength', 'size of the world')],
    extra='The whole world. See [World data](/guide/world-data).', gt='`include/action/join_request.cpp` with `world::serialize()`.')
pkt(0x05, 'SEND_TILE_UPDATE_DATA', 'server → client', 'confirmed', [('tileX / tileY', 'the tile'), ('flags', '`S_EXTENDED`')],
    extra='`i16 fg, i16 bg, u8 state[4]`, a tile-extra type byte, then that type\'s extra data (door label, sign text, lock owner, seed age).',
    gt='`send_tile_update()` in `include/database/world.cpp`.')
pkt(0x06, 'SEND_TILE_UPDATE_DATA_MULTIPLE', '-', 'unused')
pkt(0x07, 'TILE_ACTIVATE_REQUEST', 'client → server', 'confirmed', [('tileX / tileY', 'the tile you activated (door, portal, ...)')],
    gt='`include/gamePacket/tile_activate.cpp`: doors and portals warp you.', client='`0x1381790` sets the type to 7.')
pkt(0x08, 'TILE_APPLY_DAMAGE', 'server → client', 'confirmed', [('buildRange (4th type byte)', 'damage/random value (dice, roshambo)'), ('netID', 'who punched'), ('itemID', '6'), ('tileX / tileY', 'the tile')],
    gt='`tile_apply_damage()` in `include/database/world.cpp`, sent when a punch lands but the block doesn\'t break yet.')
pkt(0x09, 'SEND_INVENTORY_STATE', 'server → client', 'confirmed', [('netID', 'you'), ('flags', '`S_EXTENDED`')],
    extra='`u8 1, i32 slot_count, i16 item_count`, then per item `i16 id, i16 count`.', gt='`send_inventory_state()` in `include/database/peer.cpp`, sent after `enter_game`.')
pkt(0x0a, 'ITEM_ACTIVATE_REQUEST', 'client → server', 'confirmed', [('itemID', 'the item to use or wear')],
    gt='`include/gamePacket/item_activate.cpp`: clothing toggles on or off (`OnEquipNewItem`, `OnSetClothing`); some items have special effects.', client='`0x1381810` sets the type to 0x0a and `itemID` from its argument.',
    example='send_packet(gamePacket{ .type = 0x0a, .netid = my_netid, .id = item_id });')
pkt(0x0b, 'ITEM_ACTIVATE_OBJECT_REQUEST', 'client → server', 'confirmed', [('itemID', 'the dropped object\'s uid (not its item id)'), ('pos', 'your position')],
    gt='`include/gamePacket/item_activate_object.cpp`: picks up the drop (gems go to `OnSetBux`), then `ITEM_CHANGE_OBJECT` removes it for everyone.', client='`0x1381c98` sets the type to 0x0b.',
    example='send_packet(gamePacket{ .type = 0x0b, .netid = my_netid, .id = object_uid, .pos = my_pos });')
pkt(0x0c, 'SEND_TILE_TREE_STATE', '-', 'unused by gurotopia')
pkt(0x0d, 'MODIFY_ITEM_INVENTORY', 'server → client', 'confirmed', [('itemID', 'the item'), ('buildRange (4th type byte)', 'amount added'), ('jumpCount (3rd type byte)', 'amount removed')],
    gt='`modify_item_inventory()` in `include/database/world.cpp`.')
pkt(0x0e, 'ITEM_CHANGE_OBJECT', 'server → client', 'confirmed', [('netID', '-1 new drop, -3 count changed, otherwise the player who picked it up'), ('targetNetID', 'object uid, or -1 when picked up'), ('itemID', 'item id, or the object uid when picked up'), ('float_var', 'count'), ('pos', 'where it lies')],
    gt='`add_object()`, `merge_object()` and `remove_object()` in `include/database/world.cpp`.')
pkt(0x0f, 'SEND_LOCK', 'server → client', 'confirmed', [('netID', 'the owner\'s user id'), ('itemID', 'the lock'), ('tileX / tileY', 'where it was placed'), ('flags', '`S_EXTENDED`')],
    gt='`include/gamePacket/tile_change.cpp`, after a World Lock is placed.')
pkt(0x10, 'SEND_ITEM_DATABASE_DATA', 'server → client', 'confirmed', [('flags', '`S_EXTENDED`'), ('extraDataLength', 'size of items.dat')],
    extra='The raw items.dat.', gt='Built once by `decode_items()` in `include/database/items.cpp`; sent for `refresh_item_data`.')
pkt(0x11, 'SEND_PARTICLE_EFFECT', 'server → client', 'confirmed', [('pos', 'where'), ('...', 'effect parameters')], gt='`include/database/world.cpp`.')
pkt(0x12, 'SET_ICON_STATE', 'client → server', 'inferred', [], client='`0x12ecafc` sets the type to 0x12 and sends it.')
pkt(0x13, 'ITEM_EFFECT', '-', 'unused')
pkt(0x14, 'SET_CHARACTER_STATE', 'server → client', 'confirmed', [('type bytes 2-4', '`0x8080` + punch effect id'), ('netID', 'the player'), ('float_var', '125 (water speed)'), ('itemID', 'character state bits (invisible, frozen, halo, ...)'), ('pos / speed', 'movement constants'), ('tileX', 'hair color')],
    gt='`include/onVariant/SetClothing.cpp`, sent with every `OnSetClothing`.')
pkt(0x15, 'PING_REPLY', 'client → server', 'confirmed', [('netID', 'your state bits'), ('targetNetID', 'hash of the request\'s `itemID` (the challenge)'), ('itemID', 'client tick in ms'), ('pos', 'reach with the Fist (x) and with other items (y), in pixels'), ('speed', 'physics values from the last 0x14'), ('...', 'full layout on [0x16 PING_REQUEST](/packets/16-ping-request#the-reply-the-client-builds)')],
    gt='`include/gamePacket/ping_reply.cpp` only logs it.', client='Sent from inside the client\'s server-packet handler.')
pkt(0x16, 'PING_REQUEST', 'both', 'confirmed', [], gt='Sent by `include/action/enter_game.cpp`.', client='The client also sends 0x16 itself (`0x137c2fc`, `0x1382d90`).')
pkt(0x17, 'GOT_PUNCHED', 'client → server', 'inferred', [], client='`0x130efb8` and `0x130f130` set the type to 0x17.')
pkt(0x18, 'APP_CHECK_RESPONSE', 'client → server', 'inferred', [('netID', '1-based position of the last listed app that is installed, or -1 if none is'), ('itemID', 'sum of `HashString(name)` over the listed apps that are **not** installed')],
    client='Sent once after [OnSuperMainStartAcceptLogon…](/functions/OnSuperMainStartAcceptLogonHrdxs47254722215a#the-app-check) when its argument 4 is a string: a space-separated list of Android package names the client checks for.')
pkt(0x19, 'APP_INTEGRITY_FAIL', 'client → server', 'inferred', [('itemID', 'a reason code, for example 25 from the physics check in [OnSetPos](/functions/OnSetPos), 28 from "Punch hack detected!" in [OnSetClothing](/functions/OnSetClothing)'), ('targetNetID', ''), ('pos', ''), ('speed', '')],
    client='Helper `0x137c374`, called from 24 places in item and movement code (for example the position check in `OnSetPos`): the client reports something it considers impossible.')
pkt(0x1a, 'DISCONNECT', 'client → server', 'confirmed', [], gt='`include/gamePacket/disconnect.cpp`.', client='`0x1ba44a4`.')
for t, n in [(0x1b, 'BATTLE_JOIN'), (0x1c, 'BATTLE_EVENT'), (0x1d, 'USE_DOOR'), (0x1e, 'SEND_PARENTAL'), (0x1f, 'GONE_FISHIN'), (0x20, 'STEAM')]:
    pkt(t, n, '-', 'unused')
pkt(0x21, 'PET_BATTLE', 'client → server', 'unknown', [('buildRange (4th type byte)', 'an argument')], client='Helper `0x1382f78`.')
pkt(0x22, 'NPC', 'client → server', 'unknown', [('pos', ''), ('speed', '')], client='Helper `0x1383008`.')
for t, n in [(0x23, 'SPECIAL'), (0x24, 'SEND_PARTICLE_EFFECT_V2'), (0x25, 'ACTIVE_ARROW_TO_ITEM'), (0x26, 'SELECT_TILE_INDEX'), (0x27, 'SEND_PLAYER_TRIBUTE_DATA'), (0x28, 'FTUE_SET_ITEM_TO_QUICK_INVENTORY')]:
    pkt(t, n, '-', 'unused')
pkt(0x29, 'PVE_NPC', 'server → client', 'unknown')
pkt(0x2a, 'PVPCARD_BATTLE', 'server → client', 'unknown')
pkt(0x2b, 'PVE_APPLY_PLAYER_DAMAGE', '-', 'unused')
pkt(0x2c, 'PVE_NPC_POSITION_UPDATE', '-', 'unused')
pkt(0x2d, 'SET_EXTRA_MODS', 'server → client', 'unknown')
pkt(0x2e, 'ON_STEP_ON_TILE_MOD', 'client → server', 'inferred', [('itemID', '3728 (Ectoplasm Sample)'), ('tileX / tileY', 'the Ghost Block you landed on')], client='`0x13816a0`, when you land on a Ghost Block.')

# the 5.60 client's incoming game packet switch (0x1373e20: `cmp type, #0x2d`, jump table at 0x7fae44):
# type -> handler address. Types 0x00-0x2d not listed here (and anything above 0x2d) go to the default
# at 0x1376388, which does nothing: the client ignores them.
RX_SWITCH = 0x1373e20
RX = {0x00: 0x1373ec0, 0x01: 0x137445c, 0x03: 0x1374588, 0x04: 0x1374730, 0x05: 0x13745b4, 0x06: 0x1374680,
      0x08: 0x1374860, 0x09: 0x137488c, 0x0c: 0x13740d0, 0x0d: 0x1374a7c, 0x0e: 0x13741a0, 0x0f: 0x1374638,
      0x10: 0x1374248, 0x11: 0x1374008, 0x12: 0x13747c4, 0x13: 0x137481c, 0x14: 0x1374ba0, 0x16: 0x1374a98,
      0x1b: 0x1373f5c, 0x1c: 0x13742ac, 0x1d: 0x1374bf0, 0x1f: 0x1373fd8, 0x20: 0x1374204, 0x21: 0x137415c,
      0x22: 0x1374780, 0x23: 0x1374024, 0x24: 0x1374d60, 0x25: 0x1374d1c, 0x26: 0x13741c0, 0x27: 0x13742f0,
      0x28: 0x1374a44, 0x29: 0x1374424, 0x2a: 0x1373f18, 0x2d: 0x1374068}
for p in P:  # a type the client handles but neither server uses isn't "unused": the official server sends it
    if p['t'] in RX and p['status'].startswith('unused'):
        p['status'], p['direction'] = 'not implemented', 'server → client'
    if p['t'] in RX and p['status'] == 'unknown':  # @note decompiled now, see docs/rx/
        p['status'] = 'not implemented'
    if p['t'] in RX and p['direction'] == 'client → server':
        p['direction'] = 'both'

# ---------------------------------------------------------------- server functions with known arguments (gurotopia)
# (name, [(variant type, meaning)], uses header netID?, source, note)
F = [
    ('OnSendToServer', [('int', 'port'), ('int', 'token'), ('int', 'user id'), ('string', '"ip|0|0" (gurotopia) or "ip|doorID|uuid"'), ('int', 'logon mode (1 = welcome)'), ('string', 'growid')], False, 'action/protocol.cpp', 'Tells the client which server to (re)connect to. gurotopia lets the client continue on the same connection.'),
    ('OnSuperMainStartAcceptLogonHrdxs47254722215a', [('uint', 'items.dat hash'), ('string', 'CDN host'), ('string', 'CDN path'), ('string', 'blocked app list'), ('string', 'settings: proto|...|active_holiday|...|eventButtons=...')], False, 'action/tankIDName.cpp', 'Login accepted. The client answers with `action|enter_game` (and `refresh_item_data` if its items.dat hash differs).'),
    ('OnOverrideGDPRFromServer', [('int', ''), ('int', ''), ('int', ''), ('int', '')], False, 'action/tankIDName.cpp', None),
    ('OnRequestWorldSelectMenu', [('string', 'world menu description')], False, 'onVariant/RequestWorldSelectMenu.cpp', 'Shows the world list.'),
    ('OnConsoleMessage', [('string', 'text with `` `x `` color codes')], False, 'onVariant/ConsoleMessage.cpp', None),
    ('OnTalkBubble', [('int', 'netID of the speaker'), ('string', 'text'), ('uint', 'optional: 1 = also in console'), ('uint', 'optional')], False, 'action/input.cpp', None),
    ('OnTextOverlay', [('string', 'text')], False, None, 'A short message in the middle of the screen.'),
    ('OnSpawn', [('string', 'spawn|avatar\\nnetID|..\\nuserID|..\\ncolrect|0|0|20|30\\nposXY|x|y\\nname|..\\ncountry|..\\ninvis|0\\nmstate|0\\nsmstate|0\\nonlineID|\\n (+ type|local for yourself)')], False, 'onVariant/Spawn.cpp', 'gurotopia sends `posXY` in tiles; the official server uses pixels.'),
    ('OnRemove', [('string', 'netID|<n>\\n'), ('string', 'pId|<user id>\\n')], False, 'action/quit_to_exit.cpp', 'A player left the world.'),
    ('OnSetPos', [('vec2', 'position in pixels')], True, 'action/join_request.cpp', 'The header `netID` says whose position.'),
    ('OnSetClothing', [('vec3', 'hair, shirt, legs'), ('vec3', 'feet, face, hand'), ('vec3', 'back, head, charm'), ('int/uint', 'skin color (-140 for ghost)'), ('vec3', 'ances, 0, 0')], True, 'onVariant/SetClothing.cpp', 'Followed by a SET_CHARACTER_STATE (0x14) game packet.'),
    ('OnSetBux', [('int', 'gems'), ('int', '1'), ('int', '1')], False, 'onVariant/SetBux.cpp', None),
    ('SetHasGrowID', [('int', '1'), ('string', 'growid'), ('string', 'password (empty)')], False, 'action/enter_game.cpp', 'Matched by the client without the `On` prefix.'),
    ('OnTodaysDate', [('int', 'month'), ('int', 'day'), ('uint', ''), ('uint', '')], False, 'action/enter_game.cpp', None),
    ('OnSetFeatureEnableFlags', [('string', 'base64 flag list')], False, 'action/enter_game.cpp', 'Needed by 5.47+ clients.'),
    ('OnDialogRequest', [('string', 'dialog text')], False, 'tools/create_dialog.cpp', 'See [Dialogs](/guide/dialogs). The client answers with `action|dialog_return`.'),
    ('OnDialogRequestRML', [('string', 'RML (HTML-like) dialog')], False, None, None),
    ('OnFailedToEnterWorld', [], False, 'action/join_request.cpp', 'The client stays in the world menu.'),
    ('OnEmoticonDataChanged', [('int', ''), ('string', 'emoticon list')], False, 'onVariant/EmoticonDataChanged.cpp', None),
    ('OnCountryState', [('string', 'country code + flags')], True, 'onVariant/CountryState.cpp', None),
    ('OnNameChanged', [('string', 'display name with color code')], True, 'onVariant/NameChanged.cpp', 'Used when a world is locked, to show the owner in green.'),
    ('OnEquipNewItem', [('int', 'item id')], True, 'gamePacket/item_activate.cpp', None),
    ('OnSetFreezeState', [('int', 'state (gurotopia sends 1, then 2)')], True, 'action/respawn.cpp', None),
    ('OnKilled', [], True, 'action/respawn.cpp', None),
    ('OnZoomCamera', [('float', 'zoom (10000)'), ('uint', 'duration (1000)')], False, 'gamePacket/tile_activate.cpp', None),
    ('OnSetCurrentWeather', [('int', 'weather id')], False, 'commands/weather.cpp', None),
    ('OnBillboardChange', [('int', 'netID'), ('int', 'item id'), ('string', '"show,isBuying" as 0/1'), ('int', 'price'), ('int', '1 = price per item')], False, 'onVariant/BillboardChange.cpp', None),
    ('OnFavItemUpdated', [('int', 'item id'), ('int', '1 added, 0 removed')], False, 'action/itemfavourite.cpp', None),
    ('OnStoreRequest', [('string', 'store page')], False, 'action/store.cpp', None),
    ('OnStorePurchaseResult', [('string', 'result text')], False, 'action/buy.cpp', None),
    ('OnPlayerLeveledUp', [('int', 'new level')], False, 'database/peer.cpp', 'Sent together with an `OnParticleEffect` and an `OnTalkBubble`.'),
    ('OnParticleEffect', [('uint', 'effect id'), ('vec2', 'position in pixels'), ('float', '0'), ('float', '0')], False, 'database/peer.cpp', None),
    ('OnAction', [('string', '/emote name')], True, 'onVariant/Action.cpp', None),
]

# names the client handles (from the 5.60 dispatchers); their pages come from docs/rf/
CLIENT_ONLY = '''OnAchievementCompleted OnAchievementListLogon OnAchievementProgress OnActivateMenusRequest OnActivatePVENPCManager
OnAddNotification OnAddRemoveItemTag OnAutoSetChatToWorldRequest OnAvatarBePaintBalled OnBalloonBunnyUpdate OnBannerBandolier
OnCaptchaFailed OnCardBattleDialogRequest OnCernuousMask OnChallengeFlags OnChangeAirBalloonStyle OnChangeDeathAnim
OnChangePlasmaGlobeHeartStyle OnChangePureBeingMode OnChangeRespawnAnim OnChangeRoleIcon OnChangeRoleSkin OnChangeSkin
OnClashEventIsActiveChanged OnClearAllTutorialArrows OnClearItemTransforms OnClearNPCMessage OnClearTutorialArrow
OnCommunityHubRequest OnCorrectNPCPos OnCountdownEnd OnCountdownStart OnDailyChallengeRequest OnDailyRewardRequest OnDataConfig
OnDaylightDragon OnDeactivatePVENPCManager OnDisableRemoveIAPScreen OnDisabledParticleList OnDisguiseChanged OnEndMission
OnFTUECameraLock OnFTUEWorldSwitchSetActive OnFactionDataChanged OnFashionShowUpdate OnFlagMay2019 OnFriendOnlineID
OnGuildDataChanged OnHelpRequest OnHideDialogMessage OnHideMenusRequest OnInfinityAura OnInfinityCrown OnInfinityWeapon
OnInitNewWorld OnItemEffect OnItemVariablesHasChanged OnMadHatterUpdate OnMagicCompassTrackingItemIDChanged OnMinokawaWings
OnMusicalMaestro OnOpenTapjoyTV OnPaintTile OnParticleEffectV2 OnPartyUIUpdate OnPaw2018SkinColor1Changed
OnPaw2018SkinColor2Changed OnPersistentNPCMessage OnPersistentNPCMessageInputDependent OnPianoWingsUpdate OnPinchMod
OnPineapplePizzaPaddleUpdate OnPlanterActivated OnPlayPositioned OnRaceEnd OnRaceStart OnReceivedZodiacMode OnReconnect
OnRedirectServer OnRequestHoustonPricing OnRequestNativeAppReview OnRequestPlasmaGlobeHeartLocalHour OnResetInventoryPosRequest
OnRestorePurchases OnRiftCape OnRiftWings OnSDBroadcast OnScarfOfSeasons OnSendFavItemsList OnSendIAPConfirmation
OnSendSeedDiaryData OnSetBaseWeather OnSetBetaMode OnSetBetaSilent OnSetDungeonToken OnSetDungeonWorldInfo
OnSetDungeonXMLIndexes OnSetFriendOfWorldOwner OnSetItemTransform OnSetMissionTimer OnSetNpcXMLIndexes OnSetPearl
OnSetRoleSkinsAndIcons OnSetRoleSkinsAndTitles OnSetSpikeCheck OnSetVouchers OnShowDialogMessage OnStorylineStatsUpdate
OnSuperSupportState OnSurveyRequest OnTeaSoakedUpdate OnThrowToStartMenu OnTileBePaintballed OnToggleBetaMode
OnTransmutateLinkDataModified OnTriggerCrashlyticsNFE OnTutorialArrow OnUbiClubRewardGiven OnUbiclubRequest OnUpdatePVENPC
OnUpdateRespawnTimeout OnUpdateThanksGivingBossUI OnWeatherMachineChanged OnWinterRallyRequest OnWorldMenuFTUEMessageRequest
OnWrongDetails SetRespawnPos'''.split()

# ---------------------------------------------------------------- page writers
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def badge(text, kind='info'): return f'<Badge type="{kind}" text="{text}" />'
def dir_badge(d): return badge(d, 'tip' if d == 'both' else 'info')
STATUS = {'confirmed': ('confirmed', 'tip'), 'inferred': ('inferred', 'warning'), 'unknown': ('unknown', 'danger'), 'unused': ('unused', 'info'),
          'unused by gurotopia': ('not implemented', 'warning'), 'not implemented': ('not implemented', 'warning')}

def frag(path):
    """A hand-written fragment, with bare <...> outside code escaped so Vue doesn't read it as a tag."""
    text = re.sub(r'<!--.*?-->', '', open(path).read(), flags=re.S).strip()
    code = re.compile(r'```.*?```|(`+)[^\n]*?(?<!`)\1(?!`)', re.S)
    out, i = [], 0
    for m in code.finditer(text):
        out += [re.sub(r'<(?!/?small>)', '&lt;', text[i:m.start()]), m.group(0)]; i = m.end()
    return ''.join(out + [re.sub(r'<(?!/?small>)', '&lt;', text[i:])])

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f: f.write(text)

def cpp_string(s): return s.replace('\\', '\\\\').replace('\r', '\\r').replace('\n', '\\n').replace('"', '\\"')

# the 5.60 client sends these as message type 3; every other action is type 2 (docs/ra/)
TYPE3 = {'join_request', 'validate_world', 'world_button', 'gohomeworld', 'quit_to_exit', 'quit', 'chaching', 'adClosed', 'houston_validation_done'}

def action_page(a):
    fmt = a['fmt']
    keys = [k for k in re.findall(r'(?:^|\n|\|)([A-Za-z_]+)\|\{\}', fmt)]
    example = fmt
    for k in keys: example = example.replace(f'{k}|{{}}', f'{k}|' + {'name': 'START', 'invitedWorld': '0', 'itemID': '2', 'count': '1', 'netid': '2', 'text': 'hello', 'status': '1', 'tileX': '25', 'tileY': '37', 'location': 'gem', 'item': 'main', 'selection': 'gems_bundle06', 'dialog_name': 'drop_item'}.get(k, '0'), 1)
    mt = 3 if a['name'] in TYPE3 else 2
    out = [f'# action|{a["name"]}', '', f'{badge("GAME_MESSAGE (3)" if mt == 3 else "GENERIC_TEXT (2)")} {badge("client → server", "info")} ' + (badge('handled by gurotopia', 'tip') if a['handler'] else badge('not in gurotopia', 'warning')), '']
    out += ['## Format', '', 'Exactly as the 5.60 client formats it (`{}` is filled in):', '', '```text', fmt.rstrip('\n'), '```', '']
    if keys:
        out += ['## Fields', '', '| Field | Meaning |', '|---|---|'] + [f'| `{k}` | {FIELDS.get(k, "")} |' for k in keys] + ['']
    ra = os.path.join(ROOT, 'ra', a['name'] + '.md')  # @note hand-written from the decompiled builder
    if os.path.exists(ra):
        out += ['## When the client sends it', '', badge('decompiled from the 5.60 client', 'tip'), '', frag(ra), '']
    out += ['## Server', '']
    if a['handler']:
        out += [f'gurotopia: [`include/action/{a["handler"]}`](https://github.com/gurotopia/Gurotopia/blob/master/include/action/{a["handler"]}).', '']
        if a['reply']: out += [f'Reply: {a["reply"]}', '']
    else:
        out += ['gurotopia doesn\'t handle this action yet (`action_pool` in `include/action/__action.cpp`); the server ignores it.', '']
    if a['note']: out += ['## Notes', '', a['note'], '']
    out += ['## Send it yourself', '', 'With `send_text()` from [Talk to the server](/guide/talk-to-server):', '', '```cpp', f'send_text({mt}, "{cpp_string(example)}");', '```', '',
            f'<small>Client function: `{a["fn"]}` in libgrowtopia.so 5.60.</small>', '']
    return '\n'.join(out)

FIELD_ORDER = 'type objectType jumpCount buildRange netID targetNetID flags float_var itemID posX posY speedX speedY particleID tileX tileY extraDataLength'.split()
def packet_page(p):
    st, kind = STATUS[p['status']]
    out = [f'# {p["t"]:#04x} {p["name"]}', '', f'{badge("GAME_PACKET (4)")} {dir_badge(p["direction"])} {badge(st, kind)}', '']
    if p['t'] in RX and p['status'] in ('not implemented', 'unused by gurotopia', 'unknown') and not p['gt']:
        out += [f'The 5.60 client has its own handler for this type (`{RX[p["t"]]:#x}`), so the official server sends it. '
                'Neither gurotopia nor GrowServer does yet.', '']
    rx = os.path.join(ROOT, 'rx', f'{p["t"]:#04x}.md')  # @note hand-written from the decompiled handler
    if os.path.exists(rx):
        out += ['## What the client does with it' if p['t'] in RX else '## What the client sends', '', badge('decompiled from the 5.60 client', 'tip'), '',
                frag(rx), '']
    elif p['status'] == 'unused':
        out += ['The 5.60 client **ignores** this type when it arrives (its switch sends it to the do-nothing default), '
                'no sender was found in the client, and neither server uses it.', '']
    if p['fields']:
        out += ['## Header fields used', '', 'Offsets are from the [game packet header](/guide/game-packet). Fields not listed are 0.', '', '| Field | Meaning |', '|---|---|']
        out += [f'| `{f}` | {m} |' for f, m in p['fields']] + ['']
    if p['extra']: out += ['## Extra data', '', p['extra'], '']
    if p['gt']: out += ['## gurotopia', '', p['gt'], '']
    received = (f'**Received:** handled at `{RX[p["t"]]:#x}` in the incoming switch (`{RX_SWITCH:#x}`).' if p['t'] in RX
                else '**Received:** ignored (falls to the switch\'s default).')
    out += ['## Official client', '', received, ''] + ([f'**Sent:** {p["client"]}', ''] if p['client'] else [])
    if p['example']:
        out += ['## Send it yourself', '', 'Using `compress_state()` from `include/database/peer.cpp` (as `client/main.cpp` does):', '', '```cpp', p['example'], '```', '']
    return '\n'.join(out)

def message_page(m):
    v, name, d, desc, src, raw = m
    out = [f'# {v} {name}', '', f'{badge("message type")} {dir_badge(d) if d != "-" else badge("unused")}', '', desc, '']
    rm = os.path.join(ROOT, 'rm', f'{v}.md')  # @note hand-written from the decompiled dispatcher
    if os.path.exists(rm): out += ['## What the client does with it', '', badge('decompiled from the 5.60 client', 'tip'), '', frag(rm), '']
    out += ['## Layout', '']
    if v in (2, 3): out += ['```text', f'[u32 {v}][key|value\\n ... ][\\0]', '```', '', 'The trailing NUL is required by gurotopia, which drops the last byte (`receive.cpp`).', '']
    elif v == 4: out += ['```text', '[u32 4][56-byte header][extraDataLength bytes]', '```', '']
    else: out += ['```text', f'[u32 {v}]' + ('[u8 0]' if v == 1 else '[...]'), '```', '']
    if raw: out += ['Bytes on the wire:', '', '```text', raw, '```', '']
    if src: out += [f'gurotopia: `{src}`.', '']
    return '\n'.join(out)

def function_page(name, f=None):
    path = os.path.join(ROOT, 'rf', name + '.md')  # @note hand-written from the decompiled handler
    rf = open(path).read() if os.path.exists(path) else None
    scope = ''
    if rf and '0x12ecb2c' in rf: scope = ' ' + badge('runs on the player in the header netID', 'warning')
    elif rf: scope = ' ' + badge('global: header netID -1')
    out = [f'# {name}', '', f'{badge("CALL_FUNCTION (0x01)")} {badge("server → client")}{scope}', '']
    if rf:
        out += ['## What the client does with it', '', badge('decompiled from the 5.60 client', 'tip'), '',
                frag(path), '']
    elif not f:
        out += ['The 5.60 client\'s dispatchers match this name, but its handler isn\'t documented yet.', '']
    if f:
        _, args, uses_netid, src, note = f
        out += ['## As gurotopia sends it' if rf else '## Arguments', '', '| # | Type | Meaning |', '|---|---|---|', f'| 0 | string | `"{name}"` |']
        out += [f'| {i} | {t} | {m} |' for i, (t, m) in enumerate(args, 1)] + ['']
        if uses_netid: out += ['The game packet header\'s `netID` names the player this call is about.', '']
        if note: out += [note, '']
        if src: out += [f'gurotopia: `include/{src}`.', '']
        types = [t for t, _ in args]
    else:
        uses_netid = False; types = []
    m = rf and re.search(r'<!-- args: *([^>]*?) *-->', rf)
    if m: types = [t.strip() for t in m.group(1).split(',') if t.strip()]
    if rf and '0x12ecb2c' in rf: uses_netid = True  # @note NetAvatar dispatcher: runs on the header's netID
    sample = ', '.join(['"' + name + '"'] + [{'string': '"..."', 'vec2': 'CL_Vec2f{x, y}', 'vec3': 'CL_Vec3f{a, b, c}', 'float': '1.0f', 'uint': '1u'}.get(t, '1') for t in types])
    out += ['## Send it (server side)', '', '```cpp', f'send_varlist(peer, {{ {sample} }}{", pPeer->netid" if uses_netid else ""});', '```', '']
    return '\n'.join(out)

def main():
    for d in ('messages', 'packets', 'actions', 'functions'):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    sidebar = {}

    items = []
    for m in MESSAGES:
        write(os.path.join(ROOT, 'messages', f'{m[0]}-{slug(m[1])}.md'), message_page(m))
        items.append({'text': f'{m[0]} {m[1]}', 'link': f'/messages/{m[0]}-{slug(m[1])}'})
    sidebar['messages'] = items

    items = []
    for p in P:
        fn = f'{p["t"]:02x}-{slug(p["name"])}'
        write(os.path.join(ROOT, 'packets', fn + '.md'), packet_page(p))
        items.append({'text': f'{p["t"]:#04x} {p["name"]}', 'link': f'/packets/{fn}'})
    sidebar['packets'] = items

    groups = {}
    for a in A:
        write(os.path.join(ROOT, 'actions', a['name'] + '.md'), action_page(a))
        groups.setdefault(a['group'], []).append({'text': a['name'], 'link': f'/actions/{a["name"]}'})
    sidebar['actions'] = [{'text': g, 'collapsed': True, 'items': v} for g, v in groups.items()]

    items = []
    known = {f[0]: f for f in F}
    rf = {n[:-3] for n in os.listdir(os.path.join(ROOT, 'rf'))} if os.path.isdir(os.path.join(ROOT, 'rf')) else set()
    for name in sorted(set(known) | set(CLIENT_ONLY) | rf, key=str.lower):
        write(os.path.join(ROOT, 'functions', name + '.md'), function_page(name, known.get(name)))
        items.append({'text': name[:32] + ('…' if len(name) > 32 else ''), 'link': f'/functions/{name}'})
    sidebar['functions'] = items

    with open(os.path.join(ROOT, '.vitepress', 'sidebar.json'), 'w') as f: json.dump(sidebar, f, indent=1)
    print(f'{len(MESSAGES)} messages, {len(P)} packets, {len(A)} actions, {len(items)} functions')

if __name__ == '__main__':
    main()
