"""
시맨틱 매퍼 테스트
임베딩 기반 시맨틱 매핑 로직 검증
"""

import pytest
from backend.services.ontology_services.semantic_mapper import SemanticMapper


@pytest.fixture
def semantic_mapper() -> SemanticMapper:
    """시맨틱 매퍼 인스턴스"""
    return SemanticMapper(model_name="sentence-transformers/all-MiniLM-L6-v2")


def test_semantic_mapper_initialization(semantic_mapper: SemanticMapper):
    """시맨틱 매퍼 초기화 테스트"""
    assert semantic_mapper is not None
    assert semantic_mapper.model is not None


def test_semantic_mapper_map_semantic(semantic_mapper: SemanticMapper, sample_ontology_classes: list[str]):
    """시맨틱 매핑 테스트"""
    test_filenames = ["manufacturing_data.csv", "production_data.csv"]
    
    result_df = semantic_mapper.map_semantic(test_filenames, sample_ontology_classes)
    
    assert result_df is not None
    assert len(result_df) == len(test_filenames)
    assert "Filename" in result_df.columns
    assert "Mapped_Class" in result_df.columns
    assert "Confidence" in result_df.columns
    assert "Interpreted_As" in result_df.columns
    
    # 각 행의 신뢰도 확인
    for _, row in result_df.iterrows():
        assert 0.0 <= row["Confidence"] <= 1.0
        assert row["Mapped_Class"] in sample_ontology_classes


def test_semantic_mapper_preprocess_filename(semantic_mapper: SemanticMapper):
    """파일명 전처리 테스트"""
    test_cases = [
        ("test_file.csv", "test file"),
        ("injection-molding_data.CSV", "injection molding data"),
        ("CNC_Machine_123.csv", "CNC Machine 123"),
    ]
    
    for input_name, expected_contains in test_cases:
        processed = semantic_mapper.preprocess_filename(input_name)
        assert isinstance(processed, str)
        assert len(processed) > 0

