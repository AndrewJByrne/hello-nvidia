# Isaac Sim on Brev: ports, addresses and the launch command

The setup: a laptop running Chrome, and Isaac Sim on a Brev machine on AWS. The [Brev write-up](../brev-first-simulation/) explains each step.

## Three ports, open to your own IP only

In the Brev console: instance page, **Access** tab, **Cloud Firewall Ports**, dropdown set to **Allow Only My IP**.

| Port | Used for |
| --- | --- |
| 8210/tcp | The web page |
| 49100/tcp | Setting up the stream |
| 47998/udp | The video itself |

The stream has no login or encryption, so never open these ports to everyone. An SSH tunnel can't carry the UDP video, which is why tunnelling gave a page with no picture.

## Two addresses, two jobs

On AWS, the public IP isn't on the machine. AWS translates traffic for the public address to the machine's private `172.31.x` address.

| Variable | Set to | Job |
| --- | --- | --- |
| `ISAACSIM_BIND_HOST` | Private IP (`ip -4 -br addr`) | The address the web viewer listens on, and its health check |
| `ISAACSIM_HOST` | Public IP (Brev console) | The address Isaac Sim gives the browser |

None of the web viewer skill's single `--host` values works on Brev:

| `--host` | Result |
| --- | --- |
| `127.0.0.1` | Works only through an SSH tunnel, which can't carry the UDP video |
| Public IP | The web viewer can't listen on an address the machine doesn't own: `EADDRNOTAVAIL` |
| `auto` | Picks the private address, which the laptop can't reach |
| Brev NetBird IP (`wt0`, 100.x) | The laptop isn't on Brev's private network |

## One-time setup on the machine

```bash
sudo apt-get update -qq && sudo apt-get install -y acl     # provides setfacl
docker login nvcr.io       # username: $oauthtoken, password: NGC API key with the NGC Catalog scope
```

## Launch

`docker-compose.public-ip.yml` is a compose override: a second file that Docker merges with the skill's own file. The override points the web viewer's `vite preview --host` and health check at `ISAACSIM_BIND_HOST`.

```bash
ISAAC_SIM_IMAGE=nvcr.io/nvidia/isaac-sim:6.2.0 \
ISAACSIM_HOST=<PUBLIC_IP> ISAACSIM_BIND_HOST=<PRIVATE_IP> \
docker compose -p isim \
  -f ~/.claude/skills/isaac-sim-web-viewer/docker/docker-compose.yml \
  -f ~/isaac-sim-brev/docker-compose.public-ip.yml up --build -d
```

Then open `http://<PUBLIC_IP>:8210` on the laptop, in one tab.

## To drive a robot

`isaac-sim-remote` needs the Python control server `isaacsim.code_editor.python_server` at `127.0.0.1:8226`, which the web viewer doesn't start. A second override, `docker-compose.python-server.yml`, turns the control server on and needs a restart.

## Finish

```bash
brev stop <name>     # on the laptop
```
