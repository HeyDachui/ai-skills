---
name: diagnose-codex-proxy
description: "Diagnose Windows proxy mismatches when a browser or ChatGPT can access the internet but Codex Desktop, Codex CLI, VS Code, or a terminal keeps reconnecting or cannot connect. Follow the fixed order: identify the active proxy IP and port, compare HTTP_PROXY and HTTPS_PROXY, determine whether already-open apps inherited stale values, verify from a newly started CMD context, then detect multiple proxy apps or conflicting ports. Use for read-only self-checks before changing proxy settings."
---

# Codex代理自检

在Windows上按固定五步检查“浏览器能上网，但Codex一直重新连接”。默认只检测，不修改环境变量、代理软件或应用状态。

## 运行

在本 Skill 根目录执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\Diagnose-CodexProxy.ps1"
```

需要机器可读结果时增加`-Json`。不希望发起一次代理链路测试时增加`-SkipNetworkTest`。

## 固定检测顺序

严格按以下顺序解释结果，不提前跳到后面的猜测：

1. **确认代理IP和端口**：读取Windows手动代理，识别本地代理监听端口，并检查该端口是否真的可连接。
2. **检查环境变量**：读取用户、当前进程和机器范围的`HTTP_PROXY`、`HTTPS_PROXY`，判断两个变量是否存在、是否指向同一地址、是否与第一步的代理端口一致。
3. **检查重启需求**：比较用户范围和当前诊断进程继承的值；如果用户值已正确、当前进程仍是旧值，判定Codex、终端或VS Code需要完全关闭后重新打开。不要声称能够直接读取其他进程内部的环境块。
4. **用新CMD验证**：执行等价于`cmd /d /c set HTTP`的检查，确认当前新CMD上下文能看到两个变量及正确代理地址。
5. **检查最常见冲突**：最后再比较Windows代理、两个环境变量、当前进程和本地代理进程；发现多个代理软件或不同端口时，明确列出冲突来源。

## 判断与回复

先给一句普通中文结论，再按步骤说明：当前值、预期值、问题层和下一动作。

- `PASS`：代理端口可用，用户变量一致，当前进程与新CMD都看到同一端口，未发现冲突。
- `NEEDS_FIX_PROXY_PORT`：第一步找到的端口没有监听或不可连接。先处理代理软件或端口，不要先改环境变量。
- `NEEDS_FIX_ENV`：端口正常，但两个用户环境变量缺失、彼此不同或没有指向该端口。
- `NEEDS_RESTART`：用户环境变量正确，但当前进程或新CMD仍继承旧值。关闭Codex、终端和VS Code后重新打开。
- `NEEDS_FIX_CONFLICT`：多个代理来源或端口不一致。让系统代理与两个环境变量全部指向同一个实际监听端口。
- `INCONCLUSIVE`：没有找到可确认的代理端口、只使用PAC，或网络测试无法区分本地配置与外部网络问题。保留未知，不冒充代理已修好。

如果需要修复，只在用户明确要求后操作。先保留原值，再设置用户范围变量；不要自动关闭应用、切换代理软件或改变系统代理。

## 边界

- 浏览器能上网不等于Codex已经继承浏览器插件代理。
- 一个HTTP状态码即使不是200，也可以证明HTTPS请求已经经过代理到达远端；不要把登录状态或页面权限误判为代理失败。
- 代理检查全部通过后仍反复重连，停止重复改端口，转查服务状态、登录、证书、客户端版本或其他网络层问题。
- 输出代理地址时隐藏用户名和密码；不把代理凭据写入普通报告。
