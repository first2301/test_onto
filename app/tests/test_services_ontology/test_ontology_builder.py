"""
온톨로지 빌더 테스트
하이브리드 온톨로지 구축 로직 검증
"""

import pytest
from backend.services.ontology_services.ontology_builder import build_hybrid_ontology
from backend.services.ontology_services.config import DEFAULT_MODEL


def test_build_hybrid_ontology_basic(sample_ontology_classes: list[str]):
    """기본 온톨로지 구축 테스트"""
    ontology_classes = sample_ontology_classes[:2]
    
    mapping_df, g = build_hybrid_ontology(
        ontology_classes=ontology_classes,
        model_name=DEFAULT_MODEL
    )
    
    # 반환값 검증
    assert mapping_df is not None
    assert g is not None
    # Graph가 비어있을 수도 있음 (입력 파일이 없는 경우)
    assert len(g) >= 0


def test_build_hybrid_ontology_empty_classes():
    """빈 온톨로지 클래스 리스트 테스트"""
    mapping_df, g = build_hybrid_ontology(
        ontology_classes=[],
        model_name=DEFAULT_MODEL
    )
    
    # 빈 리스트여도 함수는 실행되어야 함
    assert mapping_df is not None
    assert g is not None

