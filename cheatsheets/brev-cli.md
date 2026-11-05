# Brev CLI cheatsheet

Commands I used on the laptop, with the surprises I hit. Numbers like #33 point to the friction log in the [Brev write-up](../brev-first-simulation/).

## Find and create a machine

```bash
brev search --gpu-name L40S --min-disk 150 --stoppable --flex-ports --wide
brev create <name> --type g6e.2xlarge --min-disk 150
brev ls            # wait for RUNNING / COMPLETED / READY
brev refresh       # writes the SSH alias, so `ssh <name>` works
```

| Flag | Why |
| --- | --- |
| `--gpu-name L40S` | An L40S has RTX, which Isaac Sim needs |
| `--stoppable` | You can pause the machine and resume later without losing work |
| `--flex-ports` | You can open your own network ports, which the browser stream needs |
| `--wide` | Shows the RAM and CPU columns, hidden by default (#13, #14) |

## Watch out for

- **Underscores are dropped from names without warning.** `ab_isaac_sim` became `abisaacsim` (#33).
- **SSH before `brev refresh` fails with a DNS error,** not "machine not ready".
- **Stop, restart and recreate change the SSH proxy ports.** Run `brev refresh` again (#20).
- **`--min-disk 150` didn't change the 117 GB root disk on `g6e.2xlarge`.** A 419 GB drive was mounted at `/opt/dlami/nvme`, but that drive is wiped whenever the machine stops (#29, #34). I saw this once, so it needs reproducing.
- **`brev copy ./skills <name>:~/skills` reported no error but left no folder.** Cloning on the machine worked (#30). Also seen once.
- **`brev delete` doesn't ask for confirmation** (#9).
- **Don't install a second VPN such as Tailscale.** Tailscale and Brev's own NetBird network both use 100.64.0.0/10, and the clash broke SSH (#27).

## Stop paying

```bash
brev stop <name>     # about $2.71 an hour while running; my notes recorded $0.02 an hour stopped (#26)
brev start <name>    # then: brev refresh
```

The public IP can change after a restart. Check the IP in the Brev console before launching anything that uses the IP.
