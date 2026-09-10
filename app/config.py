# -*- coding: utf-8 -*-
"""HealthRAG 后端配置"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置，优先读取环境变量"""

    # --- 基础 ---
    APP_NAME: str = "HealthRAG"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    RUN_ENV: str = ""
    DATA_ROOT: str = ""

    # --- 数据库 ---
    # 云上由环境变量 DATABASE_URL 覆盖（如 sqlite:////tmp/healthrag/healthrag.db）
    DATABASE_URL: str = "sqlite:///./healthrag.db"

    # --- 数据路径 ---
    # 以下默认值仅供本地开发；SCF 部署时请用环境变量覆盖（知识库放 COS → /tmp）
    DATA_DIR: str = r"D:\大创\实验"
    KNOWLEDGE_DIR: str = r"D:\大创\知识库\chunks"
    VECTOR_STORE_DIR: str = r"D:\大创\实验\vector_store"

    # --- RAG ---
    USE_DENSE: bool = False
    USE_RERANKER: bool = False
    BM25_TOP_K: int = 30
    DENSE_TOP_K: int = 10
    RERANK_TOP_K: int = 5
    HYBRID_ALPHA: float = 0.5  # BM25 权重
    EMBED_MODEL: str = "BAAI/bge-large-zh-v1.5"
    RERANK_MODEL: str = "BAAI/bge-reranker-large"

    # --- LLM ---
    LLM_PROVIDER: str = "dashscope"
    LLM_MODEL: str = "qwen-plus"
    DASHSCOPE_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    # DeepSeek（OpenAI 兼容接口），provider=deepseek 时使用
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"

    # --- COS ---
    COS_BUCKET: str = ""
    COS_REGION: str = ""
    COS_KNOWLEDGE_PREFIX: str = "chunks/"
    COS_SECRET_ID: str = ""
    COS_SECRET_KEY: str = ""
    COS_TOKEN: str = ""

    # --- CORS ---
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        # .env.example 为前后端共用，含 NEXT_PUBLIC_API_URL 等前端变量，需忽略多余字段
        "extra": "ignore",
    }


settings = Settings()


def llm_client_credentials() -> tuple:
    """OpenAI 兼容通道凭据 (api_key, base_url)。
    provider=deepseek 走 DeepSeek，否则走 OpenAI。"""
    if settings.LLM_PROVIDER == "deepseek":
        return settings.DEEPSEEK_API_KEY, settings.DEEPSEEK_BASE_URL
    return settings.OPENAI_API_KEY, settings.OPENAI_BASE_URL
