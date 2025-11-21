"""
하이브리드 매퍼 테스트
규칙 기반 + 시맨틱 매핑 통합 로직 검증
"""

import pytest
from backend.services.ontology_services.hybrid_mapper import HybridMapper


@pytest.fixture
def hybrid_mapper(sample_ontology_classes: list[str]) -> HybridMapper:
    """하이브리드 매퍼 인스턴스"""
    return HybridMapper(
        ontology_classes=sample_ontology_classes,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def test_hybrid_mapper_initialization(hybrid_mapper: HybridMapper, sample_ontology_classes: list[str]):
    """하이브리드 매퍼 초기화 테스트"""
    assert hybrid_mapper is not None
    assert hybrid_mapper.ontology_classes == sample_ontology_classes
    assert hybrid_mapper.rule_mapper is not None
    assert hybrid_mapper.semantic_mapper is not None


def test_hybrid_mapper_map_file(hybrid_mapper: HybridMapper):
    """단일 파일 매핑 테스트"""
    test_filename = "injection_molding_data.csv"
    
    result = hybrid_mapper.map_file(test_filename)
    
    assert result is not None
    assert result.filename == test_filename
    assert result.mapped_class is not None
    assert 0.0 <= result.confidence <= 1.0
    assert result.method in ["rule", "semantic", "unclassified"]


def test_hybrid_mapper_map_files(hybrid_mapper: HybridMapper):
    """다중 파일 매핑 테스트"""
    test_filenames = [
        "injection_molding_data.csv",
        "welding_robot_data.csv",
        "unknown_data.csv"
    ]
    
    mapping_df = hybrid_mapper.map_files(test_filenames)
    
    assert mapping_df is not None
    assert len(mapping_df) == len(test_filenames)
    assert "Filename" in mapping_df.columns
    assert "Mapped_Class" in mapping_df.columns
    assert "Confidence" in mapping_df.columns
    assert "Method" in mapping_df.columns

