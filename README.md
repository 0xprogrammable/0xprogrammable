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
  A token launchpad and public review platform for Uniswap v4 hooks and launch models.
</p>

<p align="center">
  <a href="https://programmable.family"><strong>Launch&nbsp;a&nbsp;token</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/blob/main/BUILDER_PROGRAM.md">Submit&nbsp;a&nbsp;hook</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/tree/main/submissions">Browse&nbsp;reviews</a>
</p>

## What Programmable does

Uniswap v4 hooks can change how a market handles swaps, fees, value flows, liquidity and permissions. Programmable
makes those mechanics easier to build, review and use without treating every project as the same contract.

Creators launch through versioned models in the [Programmable interface](https://programmable.family). Builders can
bring an idea, a hook or an existing public project to the
[Programmable v4 Builder](https://github.com/0xprogrammable/programmable/tree/main/skills/programmable-v4-hook-builder).
The complete project stays in the builder's own public repository. A small application pull request identifies one
exact revision and keeps the public review trail in GitHub.

## Submit a hook or project

Install the Builder with:

```bash
gh skill install \
  0xprogrammable/programmable \
  programmable-v4-hook-builder
```

Then:

1. Build the project in a builder-controlled public GitHub repository.
2. Run the published `doctor`, `check`, `package` and `prepare-pr` operations for one clean, pushed revision. Use
   `scaffold` only when starting a new project.
3. Open one small draft pull request against `0xprogrammable/programmable:main` with the generated application record
   and public evidence.
4. Keep architecture discussion, findings and repairs in the same pull request. A code change creates a new review
   target and requires the checks to run again.

[Read the Builder program](https://github.com/0xprogrammable/programmable/blob/main/BUILDER_PROGRAM.md) ·
[Follow the complete submission guide](https://github.com/0xprogrammable/programmable/blob/main/docs/builder/PUBLIC_GITHUB_PR_BETA.md) ·
[Check the current intake status](https://github.com/0xprogrammable/programmable/blob/main/docs/builder/intake-status.json)

## What review covers

Review is tied to the exact public repository id, commit, tree and evidence named by the application. Reviewers examine:

- what the project does and why it uses Uniswap v4;
- source, tests, dependency locks, licensing and provenance;
- assets, value-moving paths, fees, rounding, accounting and custody;
- hook permissions, callbacks and return deltas;
- privileged roles, upgrades, keepers, oracles and autonomous actions;
- external contracts, services, routing and indexing assumptions; and
- failure behavior, expected invariants, known limitations and unresolved questions.

An unfamiliar mechanic starts an architecture discussion. It is not rejected because it lacks a known category. An
objective finding identifies the affected revision, reproducible evidence, applicable rule, practical impact, repair
path and check that must run again.

[Read the submission requirements](https://github.com/0xprogrammable/programmable/blob/main/BUILDER_PROGRAM.md#builder-responsibilities) ·
[Read the reviewer process](https://github.com/0xprogrammable/programmable/blob/main/docs/builder/PUBLIC_GITHUB_PR_BETA.md#reviewer-journey)

## Public review records

GitHub commits, checks, reviews, requested changes and pull-request history form the public review record. Every
conclusion applies only to the exact revision it names. A later commit is a new review target; an earlier conclusion
does not transfer automatically.

- [Browse merged application records](https://github.com/0xprogrammable/programmable/tree/main/submissions)
- [Follow Builder Beta pull requests](https://github.com/0xprogrammable/programmable/issues?q=is%3Apr+%22%5BBuilder+Beta%5D%22)
- [Inspect the canonical model registry](https://github.com/0xprogrammable/programmable/blob/main/models/registry.json)
- [Read published independent reviews](https://github.com/0xprogrammable/programmable/tree/main/audits)

A completed public review means that the review record for the named revision is complete. It is not an independent
audit, a safety or rug-free certification, model acceptance, deployment authorization, provider support or Uniswap
endorsement. Candidate selection, integration, deployment, runtime verification and release are separate decisions
with separate evidence.

## Repository and documentation

- [Programmable repository](https://github.com/0xprogrammable/programmable)
- [Model library](https://github.com/0xprogrammable/programmable/blob/main/MODELS.md)
- [Security assumptions and reporting](https://github.com/0xprogrammable/programmable/blob/main/SECURITY.md)
- [Release requirements](https://github.com/0xprogrammable/programmable/blob/main/RELEASING.md)
- [Builder guide for coding agents](https://github.com/0xprogrammable/programmable/blob/main/docs/builder/AGENT_SKILL.md)

<p align="center">
  <a href="https://programmable.family">Website</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable">GitHub</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/0xProgrammable">X</a>
</p>
