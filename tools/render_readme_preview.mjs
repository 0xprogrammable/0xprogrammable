#!/usr/bin/env node

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const readme = readFileSync(join(root, "README.md"), "utf8");
const payload = JSON.stringify({
  text: readme,
  mode: "gfm",
  context: process.env.PROFILE_MARKDOWN_CONTEXT ?? "0xprogrammable/0xprogrammable",
});

const rendered = spawnSync("gh", ["api", "markdown", "--input", "-"], {
  cwd: root,
  input: payload,
  encoding: "utf8",
});

if (rendered.status !== 0) {
  process.stderr.write(rendered.stderr);
  process.exit(rendered.status ?? 1);
}

const renderedHtml = rendered.stdout.replaceAll('src="./assets/', 'src="/assets/');

const outputDir = join(root, ".artifacts", "profile");
mkdirSync(outputDir, { recursive: true });

const page = String.raw`<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Programmable GitHub profile preview</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/github-markdown-css@5.8.1/github-markdown.min.css"
    />
    <style>
      :root { color-scheme: light dark; }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        min-height: 100vh;
        background: #f6f8fa;
      }
      .profile-shell {
        width: min(896px, 100%);
        margin: 0 auto;
        padding: 32px 24px 64px;
      }
      .markdown-body {
        padding: 32px;
        border: 1px solid #d0d7de;
        border-radius: 6px;
        background: #ffffff;
      }
      @media (prefers-color-scheme: dark) {
        body { background: #0d1117; }
        .markdown-body {
          border-color: #30363d;
          background: #0d1117;
        }
      }
      @media (max-width: 600px) {
        .profile-shell { padding: 16px 0 40px; }
        .markdown-body { padding: 16px; border-left: 0; border-right: 0; border-radius: 0; }
      }
    </style>
  </head>
  <body>
    <main class="profile-shell">
      <article class="markdown-body" data-color-mode="auto" data-light-theme="light" data-dark-theme="dark">
        ${renderedHtml}
      </article>
    </main>
  </body>
</html>`;

writeFileSync(join(outputDir, "readme-preview.html"), page);
process.stdout.write(join(outputDir, "readme-preview.html") + "\n");
