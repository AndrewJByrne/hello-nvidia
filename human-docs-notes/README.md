# First impressions of the Isaac Sim docs

Before trying the agent skills, I installed Isaac Sim the way a newcomer might: a Google search, the download page, then the quickstart tutorial. I started on my Windows laptop, an Asus G14, and got Isaac Sim running there, though I didn't take many notes. I then moved to a small Linux laptop. These are the questions I had along the way, from one person's first attempt.

## The search landed on an old version with no warning

- The search landed on the **5.1.0** quick-install page. Nothing on that page said a newer version existed. In a later search I did see an "older version" banner, so the docs have one, but the page where I first landed didn't show it.
- I only noticed after starting the install. For an install page in particular, a "this isn't the latest version" banner would have saved me time.
- The version picker lists **7.0.0.a1**. I didn't know what that version was, or whether a newcomer should use it.
- A note on the page starts with **"On Linux"**. I was on Windows at the time, so I skimmed past the note.

## Downloads show no sizes and don't say which ones are needed

- The [download page](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/download.html#latest-release) doesn't show download sizes.
- The page offers three downloads. It isn't clear whether all three are needed to get started.
- I couldn't tell whether the "download helper" and the "Bash helper" in the next sentence are the same thing, or whether the Bash helper fetches Isaac Sim itself or only the assets.
- I confirmed that the helper fetches only the assets, not Isaac Sim itself. The assets download was about 70 to 80 MiB.

## The basics tutorial doesn't explain its terms

- The docs don't say early on what an **asset** is.
- I got a room and a robot loaded on my laptop.
- The [Basic Usage tutorial](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/introduction/quickstart_isaacsim.html) didn't leave me understanding much more. The tutorial doesn't explain the terms it uses or what's on screen. The tutorial's videos help, but I couldn't follow what they showed well enough to repeat the steps on my laptop.

## The Brev launchable failed to start, and the error was hard to find

- I went back to Brev to compare speeds with the same tutorial, but the launchable failed to start. Looking back, the cause may have been a temporary capacity problem.
- I didn't realise at the time that clicking the red "last start attempt failed" label shows the actual error. I assumed the error would be in the logs.
- That's what led me to set up a Brev machine from scratch, which the [Brev write-up](../brev-first-simulation/) covers.

## These gaps match the ones in the skills

These are the same first-time gaps I later found in the skills: missing sizes and costs, terms used before they're defined, and no clear starting point. The only difference is that these gaps slow down people instead of agents.
