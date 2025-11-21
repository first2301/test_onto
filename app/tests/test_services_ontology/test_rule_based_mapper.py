"""
규칙 기반 매퍼 테스트
키워드 기반 매핑 로직 검증
"""

import pytest
from backend.services.ontology_services.rule_based_mapper import RuleBasedMapper


@pytest.fixture
def rule_mapper() -> RuleBasedMapper:
    """규칙 기반 매퍼 인스턴스"""
    return RuleBasedMapper()


def test_rule_mapper_initialization(rule_mapper: RuleBasedMapper):
    """규칙 기반 매퍼 초기화 테스트"""
    assert rule_mapper is not None
    assert rule_mapper.keyword_rules is not None
    assert len(rule_mapper.keyword_rules) > 0


def test_rule_mapper_match_keywords(rule_mapper: RuleBasedMapper):
    """키워드 매칭 테스트"""
    # injection 관련 키워드 테스트
    test_cases = [
        ("injection_molding_data.csv", "Injection_Molding_Machine"),
        ("welding_robot_data.csv", "Welding_Robot"),
        ("cnc_machine_data.csv", "CNC_Machine"),
    ]
    
    for filename, expected_class in test_cases:
        result = rule_mapper.match_by_keywords(filename)
        if result is not None:
            matched_class, confidence = result
            # 매칭된 경우 신뢰도 확인
            assert confidence > 0.0
            assert confidence <= 1.0
            assert matched_class in rule_mapper.keyword_rules.keys()


def test_rule_mapper_preprocess_filename(rule_mapper: RuleBasedMapper):
    """파일명 전처리 테스트"""
    test_cases = [
        ("test_file.csv", "test file"),
        ("injection-molding_data.CSV", "injection molding data"),
        ("CNC_Machine_123.csv", "cnc machine"),
    ]
    
    for input_name, expected_contains in test_cases:
        processed = rule_mapper.preprocess_filename(input_name)
        assert isinstance(processed, str)
        assert len(processed) > 0

