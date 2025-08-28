#!/usr/bin/env node
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import path from "path";

// 找到 Python 脚本路径
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const scriptPath = path.join(__dirname, "..", "src", "mcp_architecture_generate.py");

// 调用 uv 运行 Python MCP Provider
const child = spawn("uv", ["run", scriptPath], {
  stdio: "inherit",
  shell: true
});

child.on("exit", (code) => {
  process.exit(code ?? 0);
});
