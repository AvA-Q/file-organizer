# File Organizer

一个安全的 Python 命令行文件整理工具。它会扫描指定目录，根据文件扩展名生成整理计划，并在用户确认后把文件移动到对应分类目录。

项目默认不会覆盖已有文件，也不会移动无法识别的文件。

## 功能

- 按扩展名分类图片、文档、视频和压缩包。
- 支持 `--dry-run`，只展示计划，不修改文件。
- 执行前默认要求用户确认。
- 支持 `--yes`，跳过确认，适合自动化场景。
- 遇到同名文件时生成 `photo (1).jpg`，避免覆盖。
- 汇总成功数量、失败数量和失败原因。
- 使用确定性的文件顺序，方便测试和对比结果。
- 核心逻辑与命令行界面分离，方便后续增加新界面。

## 分类规则

| 分类 | 扩展名 |
| --- | --- |
| `images` | `.jpg`、`.jpeg`、`.png`、`.gif`、`.webp` |
| `documents` | `.pdf`、`.doc`、`.docx`、`.txt`、`.md` |
| `videos` | `.mp4`、`.mov`、`.avi`、`.mkv` |
| `archives` | `.zip`、`.rar`、`.7z`、`.tar`、`.gz` |

扩展名比较不区分大小写，例如 `.JPG` 和 `.jpg` 会被识别为图片。

## 环境要求

- Python 3.10 或更高版本
- Windows、Linux 或 macOS
- Git，用于版本管理

以下安装和运行命令以 Windows 为例。Linux 或 macOS 用户可以将 `.venv\Scripts\python.exe` 替换为 `.venv/bin/python`。

## 安装

在项目根目录创建虚拟环境：

```text
python -m venv .venv
```

安装项目和开发依赖：

```text
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Windows PowerShell 用户可以激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

## 使用方法

### 预览整理计划

```text
python -m file_organizer.cli "C:\path\to\folder" --dry-run
```

预览模式只打印计划，不会移动任何文件。

### 确认后执行

```text
python -m file_organizer.cli "C:\path\to\folder"
```

程序会展示计划，并询问：

```text
Proceed with these moves? [y/N]
```

输入 `y` 或 `yes` 后才会执行移动。

### 跳过确认直接执行

```text
python -m file_organizer.cli "C:\path\to\folder" --yes
```

执行前建议先使用 `--dry-run` 检查计划。

### 使用已安装的命令

安装完成后也可以运行：

```text
file-organizer "C:\path\to\folder" --dry-run
```

## 命令参数

| 参数 | 作用 |
| --- | --- |
| `directory` | 必填，指定需要整理的目录 |
| `--dry-run` | 只显示移动计划，不修改文件 |
| `--yes` | 不询问确认，直接执行计划 |
| `--help` | 显示命令帮助 |

## 输出示例

```text
Planned moves:
  C:\Downloads\photo.jpg -> C:\Downloads\images\photo.jpg
  C:\Downloads\report.pdf -> C:\Downloads\documents\report.pdf
Moved: 2
Failed: 0
```

如果某个文件移动失败，程序会继续处理后续文件，并在标准错误输出中打印失败原因。

## 开发

安装开发依赖：

```text
.venv\Scripts\python.exe -m pip install --no-build-isolation -e .
```

运行测试：

```text
.venv\Scripts\python.exe -m pytest -q
```

当前测试覆盖分类规则、预览计划、同名保护、确认流程、跳过确认和错误处理。

## 项目结构

```text
file-organizer/
├── src/
│   └── file_organizer/
│       ├── __init__.py
│       ├── cli.py
│       └── organizer.py
├── tests/
│   ├── test_cli.py
│   ├── test_organizer.py
│   └── test_package.py
├── docs/
│   └── PROJECT_GOAL.md
├── .gitignore
├── pyproject.toml
└── README.md
```

## Roadmap

- [ ] 支持配置文件和自定义分类规则。
- [ ] 支持递归整理和目录排除。
- [ ] 支持撤销操作。
- [ ] 支持日志文件。
- [ ] 增加 GitHub Actions 持续集成。


