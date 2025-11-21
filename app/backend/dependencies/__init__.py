"""
의존성 주입 모듈
FastAPI Depends에서 사용할 의존성 함수들을 제공
"""

from backend.dependencies.services import get_ontology_service

__all__ = [
    "get_ontology_service",
]

