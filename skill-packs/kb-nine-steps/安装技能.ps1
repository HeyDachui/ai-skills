[CmdletBinding()]
param(
    [ValidateNotNullOrEmpty()]
    [string]$Destination = (Join-Path (Get-Location) '.agents/skills')
)

$ErrorActionPreference = 'Stop'
$items = @(
    @{ Folder = '01_需求访谈'; Name = 'needs-interview' },
    @{ Folder = '02_简单搭建'; Name = 'simple-setup' },
    @{ Folder = '03_卡片模板'; Name = 'card-template' },
    @{ Folder = '04_拆分制卡'; Name = 'card-splitting' },
    @{ Folder = '05_复查周期'; Name = 'review-cycle' },
    @{ Folder = '06_强制检索'; Name = 'required-retrieval' },
    @{ Folder = '07_保真检查'; Name = 'fidelity-check' },
    @{ Folder = '08_卡片评分'; Name = 'card-scoring' },
    @{ Folder = '09_复盘回写'; Name = 'review-writeback' }
)

$installRoot = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Destination)
if ((Test-Path -LiteralPath $installRoot) -and
    -not (Test-Path -LiteralPath $installRoot -PathType Container)) {
    throw "目标必须是文件夹：$installRoot"
}

# 先检查全部来源与目标，再开始复制。
foreach ($item in $items) {
    $source = Join-Path $PSScriptRoot $item.Folder
    foreach ($requiredFile in @('SKILL.md', 'agents/openai.yaml', '提示词.md')) {
        if (-not (Test-Path -LiteralPath (Join-Path $source $requiredFile) -PathType Leaf)) {
            throw "资料包不完整：$($item.Folder)/$requiredFile。尚未安装任何技能。"
        }
    }
    $target = Join-Path $installRoot $item.Name
    if (Test-Path -LiteralPath $target) {
        throw "已存在同名文件或文件夹：$($item.Name)。尚未安装任何技能；请选择其他目标目录。"
    }
}

New-Item -ItemType Directory -Path $installRoot -Force | Out-Null
foreach ($item in $items) {
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot $item.Folder) `
        -Destination (Join-Path $installRoot $item.Name) -Recurse
}
Write-Output "已安装 $($items.Count) 份技能到：$installRoot"
Write-Output '请查看工具的技能列表，确认九份技能都能发现。'
