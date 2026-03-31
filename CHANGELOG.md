# Changelog

All notable changes to this project will be documented in this file.

## v2.2.1 (2026-03-31)
- **文档优化**：
  - 更新 `README.md`：在语音处理流程第 1 点添加"**重点注意**"，强调**严禁新开子会话**。
  - 优化 `DESIGN.md`：精简重复内容，补充渠道支持表格，新增注意事项。
  - 更新本 `CHANGELOG.md`。
- **格式修正**：确保流程步骤之间有空行，提升可读性。

## v2.2.0 (2026-03-30)
- 新增 `SOUL.md` 配置最佳实践（动态频道识别）。
- 完善新手前置步骤文档。
- 修复 `config.py` 环境变量验证问题 (`extra = "ignore"`)。
- 优化飞书音频格式 (`.ogg` 容器)。

## v2.1.6 (2026-03-30)
- 新增 Edge TTS 失败自动降级到 `pyttsx3`。
- 发布到 ClawHub，修复 SKILL.md 格式。
- 重构为纯 Skill 架构，移除插件依赖。

## v2.1.5
- 新增 Edge TTS 失败自动降级到 `pyttsx3`。

## v2.1.4
- 发布到 ClawHub，修复 SKILL.md 格式。

## v2.1.0
- 重构为纯 Skill 架构，移除插件依赖。
