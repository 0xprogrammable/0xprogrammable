<p align="center">
  <picture>
    <source
      media="(prefers-reduced-motion: reduce)"
      srcset="./assets/profile/programmable-profile-ecosystem.jpg"
    />
    <img
      src="./assets/profile/programmable-profile-ecosystem.gif"
      alt="Programmable's pink loop mark framed by a quiet paper-floral garden"
      width="100%"
    />
  </picture>
</p>

<h1 align="center">Programmable</h1>

<p align="center">
  An interface and public model library for launching tokens whose market behavior is defined by Uniswap v4 on Ethereum.
</p>

<p align="center">
  <a href="https://programmable.family"><strong>Open the launch interface</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/blob/main/MODELS.md">Read the model library</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/tree/main/skills/programmable-v4-hook-builder">Build a model</a>
</p>

## Why Programmable exists

Most launch interfaces let someone choose a name, ticker and supply. The market underneath is usually treated as a fixed template. Uniswap v4 changes that. A hook can shape swap fees, value flows, liquidity rules and other parts of the market itself.

That makes new kinds of launches possible, but it also introduces decisions that a conventional token form was never designed to explain. A creator now has to think about contract behavior, fee accounting, liquidity custody, permissions, dependencies and failure cases. Those questions matter, but they should not force every good idea to begin with a custom frontend and a team of Solidity specialists.

Programmable separates the launch experience from the underlying model. The interface asks for the choices that belong to a particular launch. The selected model contains the contracts and rules that determine how the token is created, how its Uniswap v4 pool is initialized, where fees move, how liquidity is held and what the hook can do.

The interface is meant to make those choices understandable. It does not hide the contracts behind them.

## Different mechanics remain different models

There is no universal Uniswap v4 token. A directional fee hook, a liquidity mechanism and a new market design can have completely different accounting paths, authorities and failure modes. Treating all of them as options inside one mutable contract would make those differences harder to understand and review.

Programmable therefore versions every launch model independently. Adding a new model does not alter a release that has already been deployed.

Each model moves through a public lifecycle:

1. **Design** records the intended behavior and unresolved risks.
2. **Candidate** means that source, tests and fixed parameters exist, but the model is not available for production launches.
3. **Available** means that the exact Ethereum release, runtime hashes and security status have been published.
4. **Retired** closes a release to new launches while preserving its public record.

The current status of every model is maintained in the [model library](https://github.com/0xprogrammable/programmable/blob/main/MODELS.md).

Classic is the model currently marked Available on Ethereum. It creates a fixed-supply token, initializes its native ETH pool, permanently locks the complete launch position and completes the creator's initial buy in one transaction. Creators can select separate immutable buy and sell fees, direct ETH rewards to as many as five beneficiaries, and choose whether their initial-buy tokens remain unlocked, locked or vested.

[Read how Classic works](https://github.com/0xprogrammable/programmable/blob/main/models/classic/README.md)

## The website and the repository have different jobs

[programmable.family](https://programmable.family) is where a creator chooses an available model, reviews the launch and signs the transaction. Using the interface does not require the creator to write Solidity.

The [Programmable repository](https://github.com/0xprogrammable/programmable) is the public record behind that interface. It keeps the model definition, source, tests, parameters, security record and Ethereum evidence tied to one exact release.

This distinction matters. A polished interface is not proof of onchain behavior. A passing test suite is not proof of deployment. A verified contract is not proof that the complete launch lifecycle was reviewed. Programmable keeps those states separate instead of presenting them as the same thing.

## Building a new launch model

A new model can begin with a plain-language idea or an existing public Uniswap v4 project. The Programmable v4 Builder is a portable skill for compatible coding agents. It helps the agent understand the proposed mechanic, identify value flows and trust boundaries, inspect the project, run the published checks and prepare an application for one exact public revision.

<p align="center">
  <picture>
    <source
      media="(prefers-reduced-motion: reduce)"
      srcset="./assets/profile/programmable-builder-skill.jpg"
    />
    <img
      src="./assets/profile/programmable-builder-skill.gif"
      alt="The Programmable and GitHub marks above a restrained paper-floral garden"
      width="100%"
    />
  </picture>
</p>

Install the Builder with:

```bash
gh skill install \
  0xprogrammable/programmable \
  programmable-v4-hook-builder
```

Then give the agent the idea you want to explore:

```text
Use the Programmable v4 Builder
skill.

Help me turn this idea into a
public GitHub project.

Prepare it for the Public
GitHub PR Builder Beta.

<idea>
```

The process keeps the complete project in the builder's own public repository:

1. Explain what the market should do and why the mechanic needs Uniswap v4.
2. Build and check the project in the repository that the builder controls.
3. Bind one clean, pushed revision to its exact commit, tree and public evidence.
4. Submit a small application pull request to Programmable for discussion and review.

A mutable branch name is never treated as the reviewed source. When the project changes, the builder pushes a new commit and updates the same application with new evidence.

The Builder makes the process more consistent, but it does not turn generated code into an approved release. Maintainer review, security work, deployment evidence and production activation remain separate steps. The skill also does not publish source, push a branch, deploy contracts or open a pull request without permission.

<p>
  <a href="https://github.com/0xprogrammable/programmable/blob/main/docs/builder/AGENT_SKILL.md">Read the Builder guide</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/blob/main/BUILDER_PROGRAM.md">Read the submission requirements</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/blob/main/docs/builder/intake-status.json">Check the current intake status</a>
</p>

## Available means there is a public record

For a model marked Available, the canonical repository publishes the material needed to identify and inspect that exact release:

- Contract source, tests and fixed parameters are published together.
- Security assumptions, known limitations and review status are stated without turning them into a safety promise.
- Ethereum addresses, deployment transactions and runtime hashes identify the deployed code.
- Release and interface records show which exact version was activated for new launches.

<p>
  <a href="https://github.com/0xprogrammable/programmable/actions/workflows/verify.yml">
    <img src="https://github.com/0xprogrammable/programmable/actions/workflows/verify.yml/badge.svg" alt="Build and test status" />
  </a>
  <a href="https://github.com/0xprogrammable/programmable/actions/workflows/security.yml">
    <img src="https://github.com/0xprogrammable/programmable/actions/workflows/security.yml/badge.svg" alt="Security checks status" />
  </a>
  <a href="https://github.com/0xprogrammable/programmable/actions/workflows/mainnet-evidence.yml">
    <img src="https://github.com/0xprogrammable/programmable/actions/workflows/mainnet-evidence.yml/badge.svg" alt="Ethereum evidence status" />
  </a>
  <a href="https://github.com/0xprogrammable/programmable/actions/workflows/verify-hook-builder.yml">
    <img src="https://github.com/0xprogrammable/programmable/actions/workflows/verify-hook-builder.yml/badge.svg" alt="Builder intake status" />
  </a>
</p>

<p>
  <a href="https://github.com/0xprogrammable/programmable/blob/main/MODELS.md">Model status</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/blob/main/deployments/ethereum.json">Ethereum deployment evidence</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/blob/main/SECURITY.md">Security assumptions and limitations</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/blob/main/RELEASING.md">Release requirements</a>
</p>

Open source code makes behavior inspectable. It does not remove smart-contract risk, replace an independent audit or imply endorsement by Uniswap.

<details>
<summary><strong>How a model reaches Available</strong></summary>

<br />

A candidate does not become Available because its code compiles or because a deployment transaction exists. The exact release must have its source, parameters, tests and security properties fixed; its Ethereum transactions and runtime hashes recorded; its deployed source verified; its lifecycle behavior checked; and the interface configured for that same release.

Passing CI, a local fork or a testnet deployment does not satisfy this gate.

[Read the complete release process](https://github.com/0xprogrammable/programmable/blob/main/RELEASING.md)

</details>

<details>
<summary><strong>How Builder review stays tied to exact code</strong></summary>

<br />

The application identifies the builder's public repository by its immutable GitHub numeric id and binds one full commit, its exact tree and the public check evidence for that revision. Review conclusions apply only to that code. Updates remain in the same pull request, but each new project revision receives a new evidence package.

[Read the Public GitHub PR Builder Beta](https://github.com/0xprogrammable/programmable/blob/main/docs/builder/PUBLIC_GITHUB_PR_BETA.md)

</details>

## Start with the part you need

If you want to launch a token, begin with the [Programmable interface](https://programmable.family) and read the model before signing. If you have a new market mechanic, bring the idea or an existing public project to the [Programmable v4 Builder](https://github.com/0xprogrammable/programmable/tree/main/skills/programmable-v4-hook-builder).

The interface is for released models. The Builder is for mechanics that do not belong in the interface yet. The repository keeps the distinction visible while both sides of the project continue to grow.

<p align="center">
  <a href="https://programmable.family">Website</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable">Repository</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/0xprogrammable/programmable/blob/main/MODELS.md">Models</a>
  &nbsp;·&nbsp;
  <a href="https://x.com/0xProgrammable">X</a>
</p>
