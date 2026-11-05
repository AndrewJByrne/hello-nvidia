# Notes on the human-facing docs

Before I touched the agent skills, I started where a newcomer would: a Google search. These are the questions I had along the way. They're observations from one person on one day, not a review of the docs.

## Finding the right version

- The search landed on the **5.1.0** quick-install page. Nothing on that page said a newer version existed.
- I only noticed after starting the install. For an install page in particular, a "this isn't the latest version" banner would have saved me time.
- The version picker lists **7.0.0.a1**. I didn't know what that version was, or whether a newcomer should use it.
- A note on the page starts with **"On Linux"**, which made me skim past the note.

## Downloading

- The [download page](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/download.html#latest-release) doesn't show download sizes.
- The page offers three downloads. It isn't clear whether all three are needed to get started.
- I couldn't tell whether the "download helper" and the "Bash helper" in the next sentence are the same thing, or whether the Bash helper fetches Isaac Sim itself or only the assets.
- The assets download was about 70 to 80 MiB, and fetched only the assets.

## Learning the basics

- The docs don't say early on what an **asset** is.
- I got a room and a robot loaded on my laptop.
- The [Basic Usage tutorial](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/introduction/quickstart_isaacsim.html) didn't leave me understanding much more. The tutorial doesn't explain the terms it uses or what's on screen. The tutorial's videos are a good idea, but I couldn't get them to play.

## Trying the cloud route

- I went back to Brev to compare speeds with the same tutorial, but the launchable gave errors when starting.
- That's what led me to set up a Brev machine from scratch, which the [Brev write-up](../brev-first-simulation/) covers.

## The common thread

These are the same first-time gaps I later found in the skills: missing sizes and costs, terms used before they're defined, and no clear starting point. The only difference is that these gaps slow down people instead of agents.
