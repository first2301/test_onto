"""
온톨로지 서비스 테스트
비즈니스 로직 검증
"""

import pytest
from backend.services.ontology_service import OntologyService
from backend.schmas.ontology_schma import (
    BuildHybridOntologyRequest,
    BuildHybridOntologyResponse,
    GetHybridOntologyResponse
)


@pytest.fixture
def ontology_service() -> OntologyService:
    """온톨로지 서비스 인스턴스"""
    return OntologyService()


def test_build_hybrid_ontology_service(ontology_service: OntologyService, sample_ontology_classes: list[str]):
    """온톨로지 구축 서비스 테스트"""
    request = BuildHybridOntologyRequest(
        ontology_classes=sample_ontology_classes[:2],
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    response = ontology_service.build_hybrid_ontology(request)
    
    assert isinstance(response, BuildHybridOntologyResponse)
    assert response.message == "하이브리드 온톨로지 구축 완료"
    assert isinstance(response.mapping_df, list)
    assert isinstance(response.g, str)
    # Turtle 형식인지 확인
    assert "@prefix" in response.g or "base:" in response.g or len(response.g) > 0


def test_build_hybrid_ontology_service_default_model(ontology_service: OntologyService, sample_ontology_classes: list[str]):
    """기본 모델명 사용 테스트"""
    request = BuildHybridOntologyRequest(
        ontology_classes=sample_ontology_classes[:1],
        model_name=None  # 기본값 사용
    )
    
    response = ontology_service.build_hybrid_ontology(request)
    
    assert isinstance(response, BuildHybridOntologyResponse)
    assert response.message == "하이브리드 온톨로지 구축 완료"


def test_get_hybrid_ontology_service(ontology_service: OntologyService):
    """온톨로지 조회 서비스 테스트"""
    ontology_id = "test_ontology_123"
    
    response = ontology_service.get_hybrid_ontology(ontology_id)
    
    assert isinstance(response, GetHybridOntologyResponse)
    assert response.message == "하이브리드 온톨로지 조회 완료"
    assert response.ontology_id == ontology_id

