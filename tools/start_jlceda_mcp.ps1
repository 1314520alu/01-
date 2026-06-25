# 手动启动 JLCEDA MCP Hub 运行时（Cursor 兼容修复）
# 当 Cursor MCP 显示 Connection closed 时，可先运行本脚本，再在 EDA 连接 ws://127.0.0.1:8760/bridge/ws

$ErrorActionPreference = "Stop"

$Node = "$env:LOCALAPPDATA\Programs\cursor\resources\app\resources\helpers\node.exe"
if (-not (Test-Path $Node)) {
    $Node = "$env:LOCALAPPDATA\Programs\cursor\_\resources\app\resources\helpers\node.exe"
}
if (-not (Test-Path $Node)) {
    throw "未找到 Cursor 自带 node.exe，请确认 Cursor 已安装"
}

$ExtRoot = "$env:USERPROFILE\.cursor\extensions\chengbin.jlceda-mcp-hub-1.5.4-universal"
$Runtime = Join-Path $ExtRoot "out\server\runtime.js"
$Storage = "$env:APPDATA\Cursor\User\globalStorage\chengbin.jlceda-mcp-hub"

if (-not (Test-Path $Runtime)) {
    throw "未找到 JLCEDA MCP Hub 扩展，请先在 Cursor 安装 chengbin.jlceda-mcp-hub"
}

# 读取 Cursor settings 中的端口配置
$SettingsPath = "$env:APPDATA\Cursor\User\settings.json"
$Port = 8760
$HttpPort = 7655
if (Test-Path $SettingsPath) {
    $settings = Get-Content $SettingsPath -Raw | ConvertFrom-Json
    if ($settings.'jlcMcpServer.port') { $Port = [int]$settings.'jlcMcpServer.port' }
    if ($null -ne $settings.'jlcMcpServer.httpPort') { $HttpPort = [int]$settings.'jlcMcpServer.httpPort' }
}

# 使用最新 session 目录中的 status 文件推断 session-id
$StatusFiles = Get-ChildItem $Storage -Filter "jlceda-mcp-hub-runtime-status-*-$Port.json" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending
$SessionId = "manual-session"
if ($StatusFiles) {
    if ($StatusFiles[0].Name -match 'runtime-status-([0-9a-f-]+)-') {
        $SessionId = $Matches[1]
    }
}

$StatusFile = Join-Path $Storage "jlceda-mcp-hub-runtime-status-$SessionId-127.0.0.1-$Port.json"

Write-Host "Node:    $Node"
Write-Host "Bridge:  ws://127.0.0.1:$Port/bridge/ws"
Write-Host "HTTP:    http://127.0.0.1:$HttpPort/mcp"
Write-Host "Status:  $StatusFile"
Write-Host "按 Ctrl+C 停止"
Write-Host ""

& $Node $Runtime `
    --storage-directory $Storage `
    --session-id $SessionId `
    --host 127.0.0.1 `
    --port $Port `
    --status-file $StatusFile `
    --extension-version 1.5.4 `
    --enable-system-log false `
    --enable-connection-list false `
    --http-port $HttpPort
