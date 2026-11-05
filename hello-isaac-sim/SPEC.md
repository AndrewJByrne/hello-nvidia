# Spec: `hello-isaac-sim`, a beginner skill

**Status:** proposal. The skill hasn't been built.

## Goal

A newcomer with an everyday laptop and a fresh Brev L40S machine makes one plain-language request, then watches a robot drive in their browser. No networking knowledge is needed.

## Scope

**In scope:** one setup. A laptop with Chrome (no NVIDIA GPU needed) and a Brev L40S machine in the cloud.

**Out of scope:** other clouds, local GPUs and other browsers. Those setups keep using the existing skills.

I didn't have time to try the existing skills on a laptop with its own NVIDIA GPU, so I can't say how well they cover that setup.

## Why each step exists

Every step answers a problem I hit in the [Brev write-up](../brev-first-simulation/). References such as (#16) are entries in the friction log at the end of that write-up.

| Step | Problem it solves | What the skill does |
| --- | --- | --- |
| 1. Pick the setup | The existing skills cover a browser on the same machine or network, not a laptop with a cloud machine. | Checks that the skill is running on Brev, and stops with a clear message if not. |
| 2. Open the ports | I didn't find the firewall ports mentioned in the skills I used. | Shows the three ports to open for the user's own IP, and waits until they're open. |
| 3. Check prerequisites | On a fresh machine, `acl` is missing and the preflight GPU check fails. The NGC login and license steps come up mid-way (#16, #17). | Checks the GPU, Docker, `acl`, NGC login and license acceptance before starting anything. |
| 4. Start Isaac Sim | One address can't do two jobs, and the viewer doesn't start the control server. | Starts Isaac Sim with separate listen and browser addresses, with the control server already on. |
| 5. Show a demo | The skills stop once Isaac Sim is on screen. | Adds a ground plane and a Jetbot, and drives the Jetbot. |
| 6. Check the demo worked | The agent can't see the stream, and said so. | Reads the robot's position, then asks the user to confirm they can see the robot moving. |
| 7. Point onward | Nothing suggests what to try after a first demo. | Suggests next skills: navigation, sensors, synthetic data. |

## Where the skill fits: the first stop on a getting-started route

The `SKILLS.md` router could offer a getting-started route that begins with `hello-isaac-sim` and continues with the next skills from step 7, such as `isaac-sim-robot-navigation` and `isaac-sim-sensor`. That might give a newcomer a clearer path onward from a first demo.

## Done means all of these pass

1. The skill checks that the machine is a Brev machine, and stops with a clear message on any other setup.
2. Before launching Isaac Sim, the skill tells the user exactly which three ports to open (8210/tcp, 49100/tcp, 47998/udp) for their own IP only, and confirms the ports are open.
3. The skill checks the GPU, Docker, `acl`, the NGC login and license acceptance up front, and names any that are missing.
4. Isaac Sim starts with separate listen and browser addresses, and with the control server on, so no restart is needed.
5. A Jetbot on a ground plane moves, and the skill reports the robot's start and end positions.
6. The user confirms they can see the robot moving. The skill doesn't claim success from the position data alone.
7. The skill ends by suggesting next skills, and tells the user how to stop the machine and what the machine costs while running.

## How to test the skill

- **Fresh-machine run:** a new Brev machine and one prompt, written by someone who hasn't seen the skill. The run passes if criteria 1 to 7 are all met without the tester giving extra hints.
- **Wrong setup:** run the skill on a machine that isn't on Brev, and check that the skill stops with a clear message (criterion 1).
- **Ports closed:** leave the firewall closed, and check that the skill doesn't launch Isaac Sim until the ports are open (criterion 2).
- **Missing prerequisite:** remove `acl`, and check that the skill reports the missing package before launch (criterion 3).
- **Timing:** record the time from a fresh machine to a moving robot, with and without the skill. That first run sets the target. I haven't timed one yet, so I won't guess.

## Risks: an open stream, a dependency on the address fix and closed contribution paths

- The stream has no login or encryption, so the ports must be open to one IP only.
- The skill depends on the address fix landing in `isaac-sim-web-viewer` first.
- Under the IsaacSim [contribution path policy](https://github.com/isaac-sim/IsaacSim/blob/release/6.3/CONTRIBUTING_PATHS.md), outside contributors can't change `skills/`. A new skill would have to be proposed in a GitHub Discussion and built by a maintainer.
