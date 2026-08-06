<p align="center">
  <picture>
    <source
      media="(prefers-reduced-motion: reduce)"
      srcset="./assets/profile/programmable-night-garden.jpg"
    />
    <img
      src="./assets/profile/programmable-night-garden.gif"
      alt="Programmable's pink loop mark over a night garden with four flowers moving in subtle stop-motion"
      width="100%"
    />
  </picture>
</p>

<h1 align="center">Programmable</h1>

<p align="center">
  A launchpad for what Uniswap v4 pools can become.
</p>

<p align="center">
  <a href="https://programmable.family"><strong>Launch&nbsp;a&nbsp;token</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/blob/main/BUILDER_PROGRAM.md">Submit&nbsp;a&nbsp;hook</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/tree/main/submissions">Browse&nbsp;reviews</a>
</p>

## The token is only the beginning

A token describes what is being traded. A hook shapes what happens when it moves.

With Uniswap v4, a pool can react when someone trades or moves liquidity. It can change fees, remember earlier activity, decide where revenue goes or refuse an action entirely. Two pools can hold the same assets and still behave as different systems.

Once a pool can remember events, react to information and distribute value according to its own rules, it stops being only a place where two tokens meet. It can become part of a game, a scientific project, a company or a network of physical machines.

## The unfinished space

Programmable is for that unfinished space. We want to explore what trading becomes when a pool can respond to a game, a company, a machine or a scientific question. Putting one more token into the same familiar pool cannot be the limit of programmable liquidity.

An idea can begin in ordinary language, become code and tests, and be examined before it touches real liquidity. Software can shorten the distance between imagination and implementation, but it cannot replace judgment.

Creators launch through versioned models in the [Programmable interface](https://programmable.family). Builders bring an idea, a hook or an existing public project to the [Programmable v4 Builder](https://github.com/0xprogrammable/programmable/tree/main/skills/programmable-v4-hook-builder). The complete project stays in the builder's own public repository. A small application pull request identifies one exact revision and keeps the public review trail in GitHub.

## Submit a hook or project

Use the Builder to prepare one clean, reproducible review target from a public GitHub repository you control.

Install the Builder with:

```bash
gh skill install \
  0xprogrammable/programmable \
  programmable-v4-hook-builder
```

Then:

1. Build the project in a public GitHub repository you control.
2. Run the published `doctor`, `check`, `package` and `prepare-pr` operations for one clean, pushed revision. Use `scaffold` only when starting a new project.
3. Open one small draft pull request against `0xprogrammable/programmable:main` with the generated application record and public evidence.
4. Keep architecture discussion, findings and repairs in the same pull request. A code change creates a new review target and requires the checks to run again.

[Read the Builder program](https://github.com/0xprogrammable/programmable/blob/main/BUILDER_PROGRAM.md) · [Follow the complete submission guide](https://github.com/0xprogrammable/programmable/blob/main/docs/builder/PUBLIC_GITHUB_PR_BETA.md) · [Check the current intake status](https://github.com/0xprogrammable/programmable/blob/main/docs/builder/intake-status.json)

## What review covers

More freedom creates more possibilities, but also more ways for a mechanism to fail. When a contract can change prices or decide where money goes, a mistake is not cosmetic.

Review is tied to the exact public repository ID, commit, tree and evidence named by the application. Reviewers examine:

- what the project does and why it uses Uniswap v4;
- source, tests, dependency locks, licensing and provenance;
- assets, value-moving paths, fees, rounding, accounting and custody;
- hook permissions, callbacks and return deltas;
- privileged roles, upgrades, keepers, oracles and autonomous actions;
- external contracts, services, routing and indexing assumptions; and
- failure behavior, expected invariants, known limitations and unresolved questions.

An unfamiliar mechanic starts an architecture discussion. It is not rejected because it lacks a known category. An objective finding identifies the affected revision, reproducible evidence, applicable rule, practical impact, repair path and check that must run again.

[Read the submission requirements](https://github.com/0xprogrammable/programmable/blob/main/BUILDER_PROGRAM.md#builder-responsibilities) · [Read the reviewer process](https://github.com/0xprogrammable/programmable/blob/main/docs/builder/PUBLIC_GITHUB_PR_BETA.md#reviewer-journey)

## Public review records

Public review makes that judgment inspectable. GitHub commits, checks, reviews, requested changes and pull-request history form the public review record. Every conclusion applies only to the exact revision it names. A later commit is a new review target; an earlier conclusion does not transfer automatically.

- [Browse merged application records](https://github.com/0xprogrammable/programmable/tree/main/submissions)
- [Follow Builder Beta pull requests](https://github.com/0xprogrammable/programmable/issues?q=is%3Apr+%22%5BBuilder+Beta%5D%22)
- [Inspect the canonical model registry](https://github.com/0xprogrammable/programmable/blob/main/models/registry.json)
- [Read published independent reviews](https://github.com/0xprogrammable/programmable/tree/main/audits)

A completed public review means that the review record for the named revision is complete. It is not an independent audit, a safety or rug-free certification, model acceptance, deployment authorization, provider support or Uniswap endorsement. Candidate selection, integration, deployment, runtime verification and release are separate decisions with separate evidence.

## Repository and documentation

- [Programmable repository](https://github.com/0xprogrammable/programmable)
- [Model library](https://github.com/0xprogrammable/programmable/blob/main/MODELS.md)
- [Security assumptions and reporting](https://github.com/0xprogrammable/programmable/blob/main/SECURITY.md)
- [Release requirements](https://github.com/0xprogrammable/programmable/blob/main/RELEASING.md)
- [Builder guide for coding agents](https://github.com/0xprogrammable/programmable/blob/main/docs/builder/AGENT_SKILL.md)

<p align="center">
  <em>The tools already exist. What people will eventually learn to build with them does not.</em>
</p>

<p align="center">
  <a href="https://programmable.family">Website</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable">GitHub</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/0xProgrammable">X</a>
</p>
