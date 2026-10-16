/*
    The smallest client that talks to gurotopia directly: log in, join a world, say hello, print
    every packet the server sends.

    build (from the repo root):
        g++ -std=c++20 -Iinclude docs/examples/hello.cpp -Linclude/enet/lib -lenet -lcrypto -o hello
    run (the server must be running):
        ./hello <growid> <password> [world=START] [ip=127.0.0.1] [port=17091]
*/
#include "enet/enet.h"
#include <openssl/evp.h> // @note base64 for the ltoken
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <format>
#include <string>
#include <vector>

ENetPeer *server{};
int user_id{};

/* message types 2 and 3: [u32 type][text][\0] */
void send_text(int type, const std::string &text)
{
    std::vector<unsigned char> data(4 + text.size() + 1, 0);
    memcpy(data.data(), &type, 4);
    memcpy(data.data() + 4, text.data(), text.size());
    enet_peer_send(server, 0, enet_packet_create(data.data(), data.size(), ENET_PACKET_FLAG_RELIABLE));
}

/* reads the variant list of a CALL_FUNCTION game packet into strings, ints as text */
std::vector<std::string> read_variants(const unsigned char *p, size_t n)
{
    std::vector<std::string> out;
    size_t o = 1;
    for (int k = 0; k < p[0] && o + 2 <= n; ++k)
    {
        unsigned idx = p[o], type = p[o + 1];
        o += 2;
        if (out.size() <= idx) out.resize(idx + 1);
        if (type == 2) // @note string: u32 length + bytes
        {
            unsigned len{};
            memcpy(&len, p + o, 4);
            out[idx].assign(reinterpret_cast<const char*>(p + o + 4), len);
            o += 4 + len;
        }
        else if (type == 5 || type == 9) { int v{}; memcpy(&v, p + o, 4); out[idx] = std::to_string(v); o += 4; }
        else if (type == 1) { float v{}; memcpy(&v, p + o, 4); out[idx] = std::to_string(v); o += 4; }
        else if (type == 3) o += 8;
        else if (type == 4) o += 12;
        else break;
    }
    return out;
}

int main(int argc, char **argv)
{
    if (argc < 3) { puts("usage: ./hello <growid> <password> [world] [ip] [port]"); return 1; }
    const std::string growid = argv[1], password = argv[2], world = argc > 3 ? argv[3] : "START";

    enet_initialize();
    ENetHost *host = enet_host_create(ENET_ADDRESS_TYPE_IPV4, nullptr, 1, 2, 0, 0);
    host->usingNewPacket = 1;                       // @note the three Growtopia changes to ENet:
    host->checksum = enet_crc32;                    //       new header, CRC32 checksums,
    enet_host_compress_with_range_coder(host);      //       range coder compression

    ENetAddress address{ .type = ENET_ADDRESS_TYPE_IPV4, .port = static_cast<enet_uint16>(argc > 5 ? atoi(argv[5]) : 17091) };
    enet_address_set_host_ip(&address, argc > 4 ? argv[4] : "127.0.0.1");
    server = enet_host_connect(host, &address, 2, 0);

    for (int ticks = 0; ticks < 100; ++ticks) // @note ~10 seconds
    {
        ENetEvent event{};
        while (enet_host_service(host, &event, 100) > 0)
        {
            if (event.type == ENET_EVENT_TYPE_DISCONNECT) { puts("disconnected"); return 0; }
            if (event.type != ENET_EVENT_TYPE_RECEIVE) continue;

            const unsigned char *d = event.packet->data;
            const size_t n = event.packet->dataLength;
            int type{};
            memcpy(&type, d, 4);

            if (type == 1) // @note SERVER_HELLO: send the login
            {
                const std::string token = std::format("growId={}&password={}", growid, password);
                std::string b64(4 * ((token.size() + 2) / 3) + 1, '\0');
                b64.resize(EVP_EncodeBlock(reinterpret_cast<unsigned char*>(b64.data()), reinterpret_cast<const unsigned char*>(token.data()), token.size()));
                puts("<- SERVER_HELLO, sending login");
                send_text(2, std::format("protocol|225\nltoken|{}\n", b64));
            }
            else if (type == 2 || type == 3) printf("<- text: %.*s\n", static_cast<int>(n - 4), d + 4);
            else if (type == 4 && n >= 60)
            {
                const unsigned char tank = d[4];
                if (tank != 0x01) { printf("<- game packet 0x%02x (%zu bytes)\n", tank, n); continue; }

                const std::vector<std::string> v = read_variants(d + 60, n - 60);
                if (v.empty()) continue;
                printf("<- %s %s\n", v[0].c_str(), v[0] == "OnConsoleMessage" && v.size() > 1 ? v[1].c_str() : "");

                if (v[0] == "OnSendToServer" && v.size() > 3) // @note step 2 of the login: tankIDName
                {
                    std::string login = std::format("tankIDName|{}\nprotocol|225\ncountry|us\nuser|{}\n", growid, v[3]);
                    for (int i = 0; i < 20; ++i) login += std::format("pad{}|0\n", i); // @note gurotopia wants >= 41 fields
                    send_text(2, login);
                }
                else if (v[0].starts_with("OnSuperMainStartAcceptLogon"))
                {
                    send_text(3, "action|enter_game\n");
                    send_text(3, std::format("action|join_request\nname|{}\ninvitedWorld|0\n", world));
                }
                else if (v[0] == "OnSpawn" && v.size() > 1 && v[1].find("type|local") != std::string::npos)
                {
                    send_text(3, "action|input\n|text|hello from hello.cpp\n");
                }
            }
            enet_packet_destroy(event.packet);
        }
    }
    enet_peer_disconnect_now(server, 0);
    enet_host_destroy(host);
    enet_deinitialize();
}
