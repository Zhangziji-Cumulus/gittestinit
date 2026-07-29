# GitGUI Tool 配置目录（.GGT）

本目录 `.GGT` 是 **GitGUI Tool** 的仓库级配置目录，用于存放本仓库的图形界面相关设置。

## 目录内容

- `ggt_config.ggt`：配置文件（JSON 格式）。当前字段：
  - `version`：配置结构版本号（整数）。
  - `icon`：FontAwesome 图标类名（如 `fas fa-folder`），用于侧边栏中本仓库的图标。
- `GGT_README.md`：本说明文件。

## 说明

- 本目录随仓库通过 git 传播，**任何人在任何机器上打开该仓库，都能看到设置好的图标**。
- 你可以**安全删除整个 `.GGT` 目录**：删除后仓库图标将恢复为自动识别；下次在 GitGUI Tool 中重新设置图标时会自动重新生成。
- 请勿手动修改 `ggt_config.ggt`，以免配置损坏（除非你清楚其 JSON 格式）。
- 本文件（`GGT_README.md`）仅在不存在时由程序写入，你对其所做的编辑不会被覆盖。
