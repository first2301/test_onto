"""
하이브리드 매핑 모듈
규칙 기반 + 시맨틱 매핑을 조합한 통합 매핑 전략
"""

import pandas as pd
from typing import List

from backend.services.ontology_services.config import HIGH_CONFIDENCE, MEDIUM_CONFIDENCE, LOW_CONFIDENCE
from backend.services.ontology_services.models import MappingResult
from backend.services.ontology_services.rule_based_mapper import RuleBasedMapper
from backend.services.ontology_services.semantic_mapper import SemanticMapper


class HybridMapper:
    """하이브리드 매핑: 규칙 + 시맨틱 (파일명만 사용)"""
    
    def __init__(self, ontology_classes: List[str], model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.rule_mapper = RuleBasedMapper()
        self.semantic_mapper = SemanticMapper(model_name)
        self.ontology_classes = ontology_classes
        
        # 신뢰도 임계값 설정
        self.HIGH_CONFIDENCE = HIGH_CONFIDENCE
        self.MEDIUM_CONFIDENCE = MEDIUM_CONFIDENCE
        self.LOW_CONFIDENCE = LOW_CONFIDENCE
    
    def map_file(self, filename: str) -> MappingResult:
        """
        단일 파일 매핑 (하이브리드 로직 - 파일명만 사용)
        
        우선순위:
        1. 규칙 기반 매칭 (고신뢰도)
        2. 시맨틱 매칭
        3. Unclassified
        """
        # Step 1: 규칙 기반 매칭 시도
        rule_result = self.rule_mapper.match_by_keywords(filename)
        if rule_result and rule_result[1] >= self.HIGH_CONFIDENCE:
            return MappingResult(
                filename=filename,
                mapped_class=rule_result[0],
                confidence=rule_result[1],
                method="rule",
                interpreted_as=self.rule_mapper.preprocess_filename(filename)
            )
        
        # Step 2: 시맨틱 매칭
        semantic_df = self.semantic_mapper.map_semantic([filename], self.ontology_classes)
        semantic_score = semantic_df.iloc[0]['Confidence']
        semantic_class = semantic_df.iloc[0]['Mapped_Class']
        
        if semantic_score >= self.MEDIUM_CONFIDENCE:
            return MappingResult(
                filename=filename,
                mapped_class=semantic_class,
                confidence=semantic_score,
                method="semantic",
                interpreted_as=semantic_df.iloc[0]['Interpreted_As']
            )
        
        # Step 3: 모든 방법 실패 시 Unclassified
        return MappingResult(
            filename=filename,
            mapped_class="Unclassified",
            confidence=0.0,
            method="unclassified",
            interpreted_as=self.rule_mapper.preprocess_filename(filename)
        )
    
    def map_files(self, filenames: List[str]) -> pd.DataFrame:
        """
        여러 파일 일괄 매핑
        
        Args:
            filenames: 파일명 리스트
        """
        results = []
        
        for filename in filenames:
            result = self.map_file(filename)
            
            results.append({
                "Filename": result.filename,
                "Interpreted_As": result.interpreted_as,
                "Mapped_Class": result.mapped_class,
                "Confidence": round(result.confidence, 3),
                "Method": result.method
            })
        
        return pd.DataFrame(results)

