"""
데이터 모델 정의
매핑 결과 및 관련 데이터 구조 정의
"""

from dataclasses import dataclass


@dataclass
class MappingResult:
    """매핑 결과 데이터 클래스"""
    filename: str
    mapped_class: str
    confidence: float
    method: str  # "rule", "semantic", "unclassified"
    interpreted_as: str

