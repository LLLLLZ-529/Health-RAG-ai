# 🏥 Health-RAG-ai

大学生体质健康智能推荐系统（大创项目）——基于 **RAG（检索增强生成）** 的知识增强评估后端。支持学生数据管理、体质语义分型、知识库增强评估、个性化推荐与 AI 对话。

> 本仓库为**开发版**；干净的重构部署版见 [healthrag-backend](https://github.com/LLLLLZ-529/healthrag-backend)（含 Dockerfile、.gitignore、README），建议部署一律用后者。

## ✨ 功能特性

- 🎓 **学生数据管理**：`/api/students`，学生信息与体质数据的增删查改【接口细节以代码为准】
- 🏷️ **语义分型**：`/api/classify`，按语义对学生体质状况分类
- 📚 **知识增强评估**：`/api/assess`，基于知识库检索 + 大模型生成评估结论
- 🎯 **个性化推荐**：`/api/recommend`，结合分型与评估给出运动/健康建议
- 💬 **AI 对话**：`/api/chat`，RAG 增强的流式/非流式问答
- 🧠 **混合检索**：BM25（默认）+ 可选稠密向量（`bge-large-zh-v1.5`）+ 可选重排（`bge-reranker-large`）
- ☁️ **腾讯云 COS 知识库同步**：云函数环境启动时自动从 COS 拉取知识库分块
- 🔌 **多 LLM 后端**：DashScope（qwen-plus，默认）/ DeepSeek / OpenAI 兼容接口

## 🏗️ 技术栈

- Python 3.10+ / FastAPI / Pydantic v2 / SQLAlchemy / SQLite
- RAG：jieba 分词 + BM25 + （可选）faiss / sentence-transformers + bge 系列模型
- 部署：腾讯云 CloudBase 云函数（SCF）+ COS

## 🚀 快速开始

### 本地运行

```bash
# 1. 安装依赖（开发环境建议用完整依赖）
pip install -r requirements.txt   # 【待确认】仓库暂无 requirements.txt，需自行整理

# 2. 配置环境变量（.env）
# 至少设置：DASHSCOPE_API_KEY（或其他 LLM 密钥），以及本地数据目录
export DATA_DIR=/你的/数据路径
export KNOWLEDGE_DIR=/你的/知识库/chunks
export VECTOR_STORE_DIR=/你的/向量库路径

# 3. 启动
uvicorn app.main:app --reload
```

> ⚠️ 注意：`app/config.py` 的默认数据路径是 Windows 绝对路径（`D:\大创\...`），macOS/Linux 本地运行**必须**用环境变量覆盖，否则启动会报错。

### API 文档

启动后访问 `http://127.0.0.1:8000/docs`（FastAPI 自动生成 Swagger 文档）。

### 健康检查

```bash
curl http://127.0.0.1:8000/api/health
```

## 📁 项目结构

```
Health-RAG-ai/
├── app/
│   ├── main.py           # FastAPI 入口，注册 5 组路由
│   ├── config.py         # 配置（环境变量优先）
│   ├── api/              # 路由层：students / classify / assess / recommend / chat
│   ├── models/           # 数据模型：student / classification / knowledge / recommendation / chat
│   ├── services/         # 业务层：rag_engine / classifier / recommender / chat_engine / hi_engine / cos_sync
│   └── db/               # 数据库（SQLAlchemy）
└── backend/              # ⚠️ 疑似误提交的旧文件（backend/app、healthrag.db）
```

## ⚠️ 已知问题

1. **提交了垃圾文件**：`__pycache__/`、`backend/healthrag.db`、`backend/app`（疑似误提交的二进制/旧目录），应清理并加入 `.gitignore`。
2. **缺少 `requirements.txt`**：本地启动需要先整理依赖清单。
3. **与 `healthrag-backend` 重复**：本仓库是开发版，`healthrag-backend` 是重构部署版，建议本仓库归档。

## 📄 许可

未指定开源许可（默认保留所有权利）。
