# diagnose-codex-proxy

中文名：**Codex 代理自检**

Read-only Windows diagnostics for the situation where a browser can reach the internet but Codex Desktop, Codex CLI, VS Code, or a terminal keeps reconnecting. The Skill follows a fixed five-step order and does not change proxy settings, environment variables, proxy applications, or application state.

## Public source and search names

- Canonical slug: `diagnose-codex-proxy`
- 中文搜索名：`Codex代理自检`
- 其他描述：`浏览器能上网但Codex一直重连`
- Public source: <https://github.com/HeyDachui/ai-skills/tree/main/diagnose-codex-proxy>
- Instructions: [SKILL.md](SKILL.md)
- MIT license: [LICENSE](LICENSE)

## Install and run

Clone or download the public repository, then copy this directory into the Skills directory used by your AI client. From this Skill directory, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Diagnose-CodexProxy.ps1"
```

Add `-Json` for machine-readable output or `-SkipNetworkTest` to skip the proxy-chain test. The diagnostic output is not a repair or a guarantee that every application will use the same proxy context.

## Scope

This public package contains the diagnostic instructions, PowerShell script, agent metadata, and MIT license. It does not include credentials, private proxy values, internal task records, or machine-specific secrets.
