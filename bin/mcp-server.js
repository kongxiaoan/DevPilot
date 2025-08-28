#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Python 脚本的路径
const pythonScript = path.join(__dirname, '..', 'src', 'mcp_architecture_generate.py');

// 启动 Python MCP 服务器
const child = spawn('uv', ['run', pythonScript], {
  stdio: 'inherit',
  cwd: path.dirname(pythonScript)
});

child.on('error', (error) => {
  console.error('Failed to start MCP server:', error);
  process.exit(1);
});

child.on('exit', (code) => {
  process.exit(code);
});

// 处理进程信号
process.on('SIGINT', () => {
  child.kill('SIGINT');
});

process.on('SIGTERM', () => {
  child.kill('SIGTERM');
});