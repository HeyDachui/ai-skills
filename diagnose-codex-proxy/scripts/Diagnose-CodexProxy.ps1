[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$SkipNetworkTest,
    [string]$TestUrl = "https://chatgpt.com/"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-EnvironmentSnapshot {
    param([ValidateSet("User", "Machine", "Process")][string]$Scope)

    [pscustomobject]@{
        scope       = $Scope
        HTTP_PROXY  = [Environment]::GetEnvironmentVariable("HTTP_PROXY", $Scope)
        HTTPS_PROXY = [Environment]::GetEnvironmentVariable("HTTPS_PROXY", $Scope)
        lower_http_proxy  = [Environment]::GetEnvironmentVariable("http_proxy", $Scope)
        lower_https_proxy = [Environment]::GetEnvironmentVariable("https_proxy", $Scope)
    }
}

function Select-ProxyPart {
    param([AllowNull()][string]$Value, [ValidateSet("http", "https")][string]$Kind = "https")

    if ([string]::IsNullOrWhiteSpace($Value)) { return $null }
    $trimmed = $Value.Trim()
    if ($trimmed -notmatch ";" -and $trimmed -notmatch "^(?i:http|https|socks|socks5)=") {
        return $trimmed
    }

    $parts = @{}
    foreach ($part in ($trimmed -split ";")) {
        if ($part -match "^\s*([^=]+)=(.+)$") {
            $parts[$matches[1].Trim().ToLowerInvariant()] = $matches[2].Trim()
        }
    }
    if ($parts.ContainsKey($Kind)) { return $parts[$Kind] }
    if ($parts.ContainsKey("http")) { return $parts["http"] }
    if ($parts.ContainsKey("https")) { return $parts["https"] }
    return $null
}

function ConvertTo-ProxyEndpoint {
    param([AllowNull()][string]$Value, [string]$Source)

    if ([string]::IsNullOrWhiteSpace($Value)) { return $null }
    $candidate = $Value.Trim()
    if ($candidate -notmatch "://") { $candidate = "http://$candidate" }

    try {
        $uri = [Uri]$candidate
        if ([string]::IsNullOrWhiteSpace($uri.Host) -or $uri.Port -le 0) { return $null }
        $hostForUri = $uri.Host
        if ($hostForUri -match ":" -and $hostForUri -notmatch "^\[") { $hostForUri = "[$hostForUri]" }
        [pscustomobject]@{
            source     = $Source
            scheme     = $uri.Scheme.ToLowerInvariant()
            host       = $uri.Host.ToLowerInvariant()
            port       = [int]$uri.Port
            normalized = ("{0}:{1}" -f $uri.Host.ToLowerInvariant(), $uri.Port)
            safe_uri   = ("{0}://{1}:{2}" -f $uri.Scheme.ToLowerInvariant(), $hostForUri, $uri.Port)
            has_secret = -not [string]::IsNullOrWhiteSpace($uri.UserInfo)
        }
    } catch {
        return $null
    }
}

function ConvertTo-SafeProxyDisplay {
    param(
        [AllowNull()][string]$Value,
        [ValidateSet("http", "https")][string]$Kind = "https"
    )

    if ([string]::IsNullOrWhiteSpace($Value)) { return $null }
    $part = Select-ProxyPart $Value $Kind
    $endpoint = ConvertTo-ProxyEndpoint $part "Safe display"
    if ($null -eq $endpoint) { return "[present_but_unparseable]" }
    return $endpoint.safe_uri
}

function Get-SafeEnvironmentSnapshot {
    param($Snapshot)

    [pscustomobject]@{
        scope             = $Snapshot.scope
        HTTP_PROXY        = ConvertTo-SafeProxyDisplay $Snapshot.HTTP_PROXY "http"
        HTTPS_PROXY       = ConvertTo-SafeProxyDisplay $Snapshot.HTTPS_PROXY "https"
        lower_http_proxy  = ConvertTo-SafeProxyDisplay $Snapshot.lower_http_proxy "http"
        lower_https_proxy = ConvertTo-SafeProxyDisplay $Snapshot.lower_https_proxy "https"
    }
}

function Test-SameEndpoint {
    param($Left, $Right)
    if ($null -eq $Left -or $null -eq $Right) { return $false }
    return ($Left.host -eq $Right.host -and [int]$Left.port -eq [int]$Right.port)
}

function Test-TcpEndpoint {
    param([string]$HostName, [int]$Port, [int]$TimeoutMs = 1500)

    $client = [Net.Sockets.TcpClient]::new()
    try {
        $pending = $client.BeginConnect($HostName, $Port, $null, $null)
        if (-not $pending.AsyncWaitHandle.WaitOne($TimeoutMs, $false)) { return $false }
        $client.EndConnect($pending)
        return $client.Connected
    } catch {
        return $false
    } finally {
        $client.Dispose()
    }
}

function Get-ListeningPorts {
    $rows = @()
    if (-not (Get-Command Get-NetTCPConnection -ErrorAction SilentlyContinue)) { return $rows }
    try {
        foreach ($item in (Get-NetTCPConnection -State Listen -ErrorAction Stop)) {
            $processName = $null
            try { $processName = (Get-Process -Id $item.OwningProcess -ErrorAction Stop).ProcessName } catch {}
            $rows += [pscustomobject]@{
                address = $item.LocalAddress
                port = [int]$item.LocalPort
                pid = [int]$item.OwningProcess
                process = $processName
            }
        }
    } catch {}
    return $rows
}

function Get-CmdEnvironment {
    $values = @{ HTTP_PROXY = $null; HTTPS_PROXY = $null }
    $raw = @()
    try {
        $raw = @(& $env:ComSpec /d /c "set HTTP" 2>&1)
        foreach ($line in $raw) {
            if ([string]$line -match "^([^=]+)=(.*)$") {
                $name = $matches[1].Trim().ToUpperInvariant()
                if ($values.ContainsKey($name)) { $values[$name] = $matches[2].Trim() }
            }
        }
    } catch {}
    [pscustomobject]@{
        HTTP_PROXY = $values.HTTP_PROXY
        HTTPS_PROXY = $values.HTTPS_PROXY
        raw = @($raw | ForEach-Object { [string]$_ })
    }
}

$internetKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings"
$internet = $null
try { $internet = Get-ItemProperty -LiteralPath $internetKey -ErrorAction Stop } catch {}

$proxyEnabled = $false
$proxyServer = $null
$autoConfigUrl = $null
if ($null -ne $internet) {
    if ($internet.PSObject.Properties.Name -contains "ProxyEnable") {
        $proxyEnabled = ([int]$internet.ProxyEnable -eq 1)
    }
    if ($internet.PSObject.Properties.Name -contains "ProxyServer") {
        $proxyServer = [string]$internet.ProxyServer
    }
    if ($internet.PSObject.Properties.Name -contains "AutoConfigURL") {
        $autoConfigUrl = [string]$internet.AutoConfigURL
    }
}

$winInetHttp = ConvertTo-ProxyEndpoint (Select-ProxyPart $proxyServer "http") "Windows manual proxy (HTTP)"
$winInetHttps = ConvertTo-ProxyEndpoint (Select-ProxyPart $proxyServer "https") "Windows manual proxy (HTTPS)"

$userEnv = Get-EnvironmentSnapshot "User"
$processEnv = Get-EnvironmentSnapshot "Process"
$machineEnv = Get-EnvironmentSnapshot "Machine"

$userHttp = ConvertTo-ProxyEndpoint $userEnv.HTTP_PROXY "User HTTP_PROXY"
$userHttps = ConvertTo-ProxyEndpoint $userEnv.HTTPS_PROXY "User HTTPS_PROXY"
$processHttp = ConvertTo-ProxyEndpoint $processEnv.HTTP_PROXY "Process HTTP_PROXY"
$processHttps = ConvertTo-ProxyEndpoint $processEnv.HTTPS_PROXY "Process HTTPS_PROXY"
$machineHttp = ConvertTo-ProxyEndpoint $machineEnv.HTTP_PROXY "Machine HTTP_PROXY"
$machineHttps = ConvertTo-ProxyEndpoint $machineEnv.HTTPS_PROXY "Machine HTTPS_PROXY"
$safeUserEnv = Get-SafeEnvironmentSnapshot $userEnv
$safeProcessEnv = Get-SafeEnvironmentSnapshot $processEnv
$safeMachineEnv = Get-SafeEnvironmentSnapshot $machineEnv

$listeners = @(Get-ListeningPorts)
$likelyProxyPattern = "(?i)(clash|mihomo|v2ray|xray|sing-box|singbox|hiddify|nekoray|shadowsocks|ss-local|trojan|surge|proxifier|outline|warp|proxy)"
$likelyProxyListeners = @($listeners | Where-Object { $_.process -and $_.process -match $likelyProxyPattern })

$expected = $null
if ($proxyEnabled -and $null -ne $winInetHttps) { $expected = $winInetHttps }
elseif ($proxyEnabled -and $null -ne $winInetHttp) { $expected = $winInetHttp }
elseif ($null -ne $userHttps) { $expected = $userHttps }
elseif ($null -ne $userHttp) { $expected = $userHttp }
elseif ($null -ne $processHttps) { $expected = $processHttps }
elseif ($null -ne $processHttp) { $expected = $processHttp }
elseif (@($likelyProxyListeners | Select-Object -ExpandProperty port -Unique).Count -eq 1) {
    $only = $likelyProxyListeners | Select-Object -First 1
    $expected = ConvertTo-ProxyEndpoint ("http://127.0.0.1:{0}" -f $only.port) ("Listening proxy process: {0}" -f $only.process)
}

$portReachable = $null
if ($null -ne $expected) { $portReachable = Test-TcpEndpoint $expected.host $expected.port }

$userPairPresent = ($null -ne $userHttp -and $null -ne $userHttps)
$userPairSame = ($userPairPresent -and (Test-SameEndpoint $userHttp $userHttps))
$userMatchesExpected = ($userPairSame -and $null -ne $expected -and (Test-SameEndpoint $userHttp $expected))

$processPairPresent = ($null -ne $processHttp -and $null -ne $processHttps)
$processPairSame = ($processPairPresent -and (Test-SameEndpoint $processHttp $processHttps))
$processMatchesUser = ($processPairSame -and $userPairSame -and (Test-SameEndpoint $processHttp $userHttp))

$runningApps = @(Get-Process -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessName -match "(?i)^(codex|codexdesktop|code|windowsterminal|cmd|powershell|pwsh)$"
} | Select-Object ProcessName, Id, StartTime -ErrorAction SilentlyContinue)

$restartState = "WAITING_FOR_ENV_FIX"
if ($userPairSame) {
    if ($processMatchesUser) { $restartState = "CURRENT_HOST_MATCHES_USER_ENV" }
    else { $restartState = "NEEDS_RESTART" }
}

$cmdEnv = Get-CmdEnvironment
$cmdHttp = ConvertTo-ProxyEndpoint $cmdEnv.HTTP_PROXY "Fresh CMD HTTP_PROXY"
$cmdHttps = ConvertTo-ProxyEndpoint $cmdEnv.HTTPS_PROXY "Fresh CMD HTTPS_PROXY"
$cmdPairPresent = ($null -ne $cmdHttp -and $null -ne $cmdHttps)
$cmdPairSame = ($cmdPairPresent -and (Test-SameEndpoint $cmdHttp $cmdHttps))
$cmdMatchesExpected = ($cmdPairSame -and $null -ne $expected -and (Test-SameEndpoint $cmdHttp $expected))
$safeCmdHttp = ConvertTo-SafeProxyDisplay $cmdEnv.HTTP_PROXY "http"
$safeCmdHttps = ConvertTo-SafeProxyDisplay $cmdEnv.HTTPS_PROXY "https"

$allEndpoints = @($winInetHttp, $winInetHttps, $userHttp, $userHttps, $processHttp, $processHttps, $machineHttp, $machineHttps) | Where-Object { $null -ne $_ }
$distinctEndpoints = @($allEndpoints | Group-Object normalized | ForEach-Object {
    [pscustomobject]@{ endpoint = $_.Name; sources = @($_.Group.source) }
})

$conflicts = @()
if ($userPairPresent -and -not $userPairSame) { $conflicts += "User HTTP_PROXY and HTTPS_PROXY point to different endpoints." }
if ($proxyEnabled -and $null -ne $winInetHttps -and $userPairSame -and -not (Test-SameEndpoint $winInetHttps $userHttp)) {
    $conflicts += "Windows manual proxy and user environment variables point to different endpoints."
}
if ($userPairSame -and $processPairPresent -and -not $processMatchesUser) {
    $conflicts += "The current process inherited a different proxy endpoint than the user environment."
}
if ($distinctEndpoints.Count -gt 1) { $conflicts += "More than one proxy endpoint is present across Windows and environment settings." }
$proxyProcessNames = @($likelyProxyListeners | Select-Object -ExpandProperty process -Unique)
if ($proxyProcessNames.Count -gt 1) { $conflicts += "More than one likely proxy application has a listening port." }

$networkTest = [pscustomobject]@{
    attempted = $false
    url = $TestUrl
    proxy = if ($null -ne $expected) { $expected.safe_uri } else { $null }
    curl_exit = $null
    http_status = $null
    passed = $null
    note = $null
}

if (-not $SkipNetworkTest -and $null -ne $expected -and $portReachable -eq $true) {
    if ($expected.has_secret) {
        $networkTest.note = "Skipped because the proxy URI contains credentials."
    } elseif (Get-Command curl.exe -ErrorAction SilentlyContinue) {
        $networkTest.attempted = $true
        $status = & curl.exe -o NUL -sS -w "%{http_code}" --max-time 8 --proxy $expected.safe_uri $TestUrl 2>$null
        $networkTest.curl_exit = $LASTEXITCODE
        $networkTest.http_status = ([string]$status).Trim()
        $networkTest.passed = ($LASTEXITCODE -eq 0 -and $networkTest.http_status -match "^[1-5][0-9][0-9]$")
        if ($networkTest.passed -and $networkTest.http_status -ne "200") {
            $networkTest.note = "The proxy reached the remote HTTP service; this status may reflect login or page policy rather than a proxy failure."
        }
    } else {
        $networkTest.note = "curl.exe is unavailable; skipped the external proxy-path test."
    }
}

$verdict = "PASS"
$summary = "代理端口、两个环境变量、当前进程和新CMD均指向同一地址，未发现明显冲突。"
$actions = @()

if ($null -eq $expected) {
    $verdict = "INCONCLUSIVE"
    $summary = "没有找到可确认的代理IP和端口，暂时不能判断环境变量应该指向哪里。"
    $actions += "先在代理软件或Windows手动代理中确认本地代理IP和端口。"
} elseif ($portReachable -ne $true) {
    $verdict = "NEEDS_FIX_PROXY_PORT"
    $summary = "已经找到代理地址，但对应端口没有监听或无法连接。"
    $actions += "先确认代理软件正在运行，并核对当前实际端口。"
} elseif (-not $userPairPresent -or -not $userPairSame -or -not $userMatchesExpected) {
    $verdict = "NEEDS_FIX_ENV"
    $summary = "代理端口可用，但用户HTTP_PROXY和HTTPS_PROXY缺失、不一致或没有指向该端口。"
    $actions += ("把用户HTTP_PROXY和HTTPS_PROXY都设置为 {0}。" -f $expected.safe_uri)
} elseif ($restartState -eq "NEEDS_RESTART" -or -not $cmdMatchesExpected) {
    $verdict = "NEEDS_RESTART"
    $summary = "用户环境变量已经正确，但当前进程或新CMD仍没有继承同一代理地址。"
    $actions += "完全关闭Codex、终端和VS Code，再重新打开后运行 set HTTP。"
} elseif ($conflicts.Count -gt 0) {
    $verdict = "NEEDS_FIX_CONFLICT"
    $summary = "基本设置存在，但发现多个代理来源或端口不一致。"
    $actions += "只保留正在使用的代理路径，并让系统代理与两个环境变量全部指向同一个端口。"
} elseif ($networkTest.attempted -and $networkTest.passed -eq $false) {
    $verdict = "INCONCLUSIVE"
    $summary = "本地代理配置一致，但通过该代理访问测试地址失败，需要继续区分代理上游与外部网络问题。"
    $actions += "检查代理软件的节点、规则和上游连接，不要继续重复修改同一个环境变量。"
}

$result = [pscustomobject]@{
    skill = "diagnose-codex-proxy"
    checked_at = (Get-Date).ToString("o")
    verdict = $verdict
    summary = $summary
    steps = [ordered]@{
        step1_proxy_endpoint = [pscustomobject]@{
            windows_manual_proxy_enabled = $proxyEnabled
            windows_proxy_server = ConvertTo-SafeProxyDisplay $proxyServer "https"
            pac_url_present = -not [string]::IsNullOrWhiteSpace($autoConfigUrl)
            selected_endpoint = $expected
            port_reachable = $portReachable
            likely_proxy_listeners = $likelyProxyListeners
        }
        step2_environment_variables = [pscustomobject]@{
            user = $safeUserEnv
            process = $safeProcessEnv
            machine = $safeMachineEnv
            user_pair_present = $userPairPresent
            user_pair_same = $userPairSame
            user_matches_selected_endpoint = $userMatchesExpected
        }
        step3_restart = [pscustomobject]@{
            state = $restartState
            process_matches_user = $processMatchesUser
            running_affected_apps = $runningApps
            note = "The script can compare inherited values but cannot directly read every other process environment block."
        }
        step4_fresh_cmd = [pscustomobject]@{
            command = "cmd /d /c set HTTP"
            HTTP_PROXY = $safeCmdHttp
            HTTPS_PROXY = $safeCmdHttps
            pair_present = $cmdPairPresent
            pair_same = $cmdPairSame
            matches_selected_endpoint = $cmdMatchesExpected
        }
        step5_conflicts = [pscustomobject]@{
            conflicts = $conflicts
            distinct_endpoints = $distinctEndpoints
            likely_proxy_processes = $proxyProcessNames
        }
    }
    network_test = $networkTest
    next_actions = $actions
}

if ($Json) {
    $result | ConvertTo-Json -Depth 10
    exit 0
}

Write-Output "Codex代理自检"
Write-Output ("结论 [{0}] {1}" -f $result.verdict, $result.summary)
Write-Output ""
Write-Output "1. 确认代理IP和端口"
if ($null -eq $expected) {
    Write-Output "   未找到可确认的代理端口"
} else {
    Write-Output ("   当前选择: {0}  来源: {1}" -f $expected.safe_uri, $expected.source)
    Write-Output ("   端口监听: {0}" -f $portReachable)
}
Write-Output ""
Write-Output "2. 检查HTTP_PROXY和HTTPS_PROXY"
Write-Output ("   用户HTTP_PROXY : {0}" -f $safeUserEnv.HTTP_PROXY)
Write-Output ("   用户HTTPS_PROXY: {0}" -f $safeUserEnv.HTTPS_PROXY)
Write-Output ("   两个变量一致并匹配当前端口: {0}" -f $userMatchesExpected)
Write-Output ""
Write-Output "3. 检查重启需求"
Write-Output ("   状态: {0}" -f $restartState)
if ($runningApps.Count -gt 0) {
    Write-Output ("   当前打开的相关程序: {0}" -f (($runningApps.ProcessName | Sort-Object -Unique) -join ", "))
}
Write-Output ""
Write-Output "4. 新CMD执行 set HTTP"
Write-Output ("   HTTP_PROXY : {0}" -f $safeCmdHttp)
Write-Output ("   HTTPS_PROXY: {0}" -f $safeCmdHttps)
Write-Output ("   新CMD匹配当前端口: {0}" -f $cmdMatchesExpected)
Write-Output ""
Write-Output "5. 多代理与端口冲突"
if ($conflicts.Count -eq 0) { Write-Output "   未发现明显冲突" }
else { foreach ($item in $conflicts) { Write-Output ("   - {0}" -f $item) } }

if ($networkTest.attempted) {
    Write-Output ""
    Write-Output ("代理链路测试: HTTP {0}  通过: {1}" -f $networkTest.http_status, $networkTest.passed)
}

if ($actions.Count -gt 0) {
    Write-Output ""
    Write-Output "下一步"
    foreach ($action in $actions) { Write-Output ("- {0}" -f $action) }
}
