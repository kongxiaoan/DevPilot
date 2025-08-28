import os
from pathlib import Path
from mcp.server import FastMCP

# 初始化 MCP 服务
app = FastMCP("devpilot-architecture")


# 一个简单的工具：根据用户输入生成项目架构
@app.tool("generate_architecture")
async def generate_architecture(
        platform: str,
        use_case: bool = True,
        repository: bool = True,
) -> dict:
    """
    生成应用架构基础骨架。

    Args:
        platform: 平台类型 ("ios", "android", "react-native", "flutter")
        use_case: 是否使用 UseCase 层
        repository: 是否使用 Repository 层

    Returns:
        dict: 包含生成的文件/目录结构
    """
    base_path = Path(f"./generated/{platform}_app")
    os.makedirs(base_path, exist_ok=True)

    structure = {
        "platform": platform,
        "directories": [],
    }

    # 公共目录
    common_dirs = ["core", "ui", "data"]
    structure["directories"].extend(common_dirs)

    if use_case:
        structure["directories"].append("domain/usecases")
        (base_path / "domain/usecases").mkdir(parents=True, exist_ok=True)

    if repository:
        structure["directories"].append("data/repository")
        (base_path / "data/repository").mkdir(parents=True, exist_ok=True)

    # Flutter 特殊处理
    if platform == "flutter":
        structure["directories"].append("lib")
        (base_path / "lib").mkdir(exist_ok=True)

    # React Native 特殊处理
    if platform == "react-native":
        structure["directories"].append("src")
        (base_path / "src").mkdir(exist_ok=True)

    # iOS / Android 可以加上默认 module 结构
    if platform in ["ios", "android"]:
        structure["directories"].append("modules")
        (base_path / "modules").mkdir(exist_ok=True)

    return {
        "message": f"Generated base architecture for {platform}",
        "structure": structure,
        "path": str(base_path.resolve())
    }


# 启动 MCP Provider
if __name__ == "__main__":
    app.run()
