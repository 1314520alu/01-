# JLCEDA MCP 配置与修复

## 链路

```
嘉立创 EDA (MCP Bridge)  ←ws→  Cursor (JLCEDA MCP Hub)  ←MCP→  Agent
```

| 侧 | 地址 |
|----|------|
| EDA Bridge | `ws://127.0.0.1:8760/bridge/ws` |
| HTTP MCP（可选） | `http://127.0.0.1:7655/mcp` |

## 正常配置

### Cursor

1. 安装扩展 **JLCEDA MCP Hub**（`chengbin.jlceda-mcp-hub`）
2. Settings 中确认：
   - `jlcMcpServer.port`: **8760**
   - `jlcMcpServer.httpPort`: **7655**
3. **Settings → MCP** → `jlceda-mcp-hub` 应为 **Connected**

### 嘉立创 EDA

1. 只启用 **MCP Bridge (Lion)**，禁用 Run API Gateway / 重复 Bridge
2. **MCP Bridge → 连接设置** → `ws://127.0.0.1:8760/bridge/ws`
3. 必须在 **原理图或 PCB 页** 才能连接

## 根因（Connection closed）

Cursor 下 Hub 扩展用 `Cursor.exe` 启动 MCP 运行时，导致参数 `--storage-directory` 等被当成 Electron 开关，进程秒退。

**已修复**：`getRuntimeCommand()` 改为使用 Cursor 自带 `node.exe`。

扩展路径：

```
%USERPROFILE%\.cursor\extensions\chengbin.jlceda-mcp-hub-1.5.4-universal\out\extension.js
```

> 扩展升级后若复发，重新应用该 patch，或运行下方手动启动脚本。

## 手动启动（备用）

```powershell
powershell -ExecutionPolicy Bypass -File G:\soft\01飞控\tools\start_jlceda_mcp.ps1
```

验证：

```powershell
netstat -ano | findstr 8760
```

应看到 `LISTENING`。

## 8765 端口冲突

GCS COM bridge（`G:\soft\GCS\legacy\web\tools\com-bridge\server.py`）占用 **8765**，因此 Hub 端口改为 **8760**。不要用 8765，除非先停 GCS bridge。

## 验收

1. `netstat` 见 8760 **LISTENING**
2. Cursor Hub：**EDA 连接 → 桥接客户端已连接**
3. EDA：**桥接连接 → 已连接**（非「等待 stdio 启动」）
