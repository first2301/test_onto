"""
관계 추출 모듈
파싱된 데이터에서 온톨로지 관계 추출
"""

import logging
import polars as pl
from typing import List, Dict, Any, Optional
from backend.services.ontology_services.hybrid_mapper import HybridMapper

logger = logging.getLogger(__name__)


class RelationExtractor:
    """관계 추출기"""
    
    def __init__(self, ontology_classes: List[str], model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        """
        관계 추출기 초기화
        
        Args:
            ontology_classes: 온톨로지 클래스 목록
            model_name: SentenceTransformer 모델명
        """
        self.ontology_classes = ontology_classes
        self.mapper = HybridMapper(ontology_classes, model_name)
    
    def extract_relations(
        self,
        df: pl.DataFrame,
        file_name: str,
        relation_type: str = "isDataOf",
        source_column: Optional[str] = None,
        target_column: Optional[str] = None
    ) -> pl.DataFrame:
        """
        데이터프레임에서 관계 추출
        매핑은 자동으로 처리됩니다:
        - 타겟 컬럼이 있으면 직접 매핑 사용
        - 타겟 컬럼이 없으면 파일명 기반 하이브리드 매핑 사용 (규칙 기반 + 시맨틱)
        
        Args:
            df: 파싱된 데이터프레임
            file_name: 파일명 (데이터셋 전체를 하나의 클래스로 매핑하기 위해 사용)
            relation_type: 관계 타입 (isDataOf, hasPart, etc.)
            source_column: 소스 컬럼명 (None이면 자동 감지, 현재는 사용하지 않음)
            target_column: 타겟 컬럼명 (None이면 자동 감지, 있으면 직접 매핑 사용)
            
        Returns:
            DataFrame: 관계 매핑 결과 (파일명 → 온톨로지 클래스, 1개 관계)
        """
        try:
            # 타겟 컬럼이 있으면 직접 매핑 (기존 로직 유지)
            if target_column and target_column in df.columns:
                # 타겟 컬럼의 고유한 값들 확인
                unique_targets = df[target_column].unique().to_list()
                for target_value in unique_targets:
                    if target_value is not None:
                        target_str = str(target_value).strip()
                        if target_str and target_str in self.ontology_classes:
                            # 파일명을 Source로, 타겟 컬럼 값을 Target으로 사용
                            logger.info(f"타겟 컬럼 기반 직접 매핑: {file_name} → {target_str}")
                            return pl.DataFrame([{
                                "Source": file_name,
                                "Target": target_str,
                                "Relation": relation_type,
                                "Method": "direct",
                                "Confidence": 1.0
                            }])
            
            # 타겟 컬럼이 없으면 파일명 기반 하이브리드 매핑 사용
            # (규칙 기반 + 시맨틱 매핑을 자동으로 조합)
            logger.info(f"파일명 기반 하이브리드 매핑 시작: {file_name}")
            mapping_result = self.mapper.map_file(file_name)
            
            if mapping_result.mapped_class != "Unclassified":
                logger.info(f"매핑 완료: {file_name} → {mapping_result.mapped_class} (신뢰도: {mapping_result.confidence}, 방법: {mapping_result.method})")
                return pl.DataFrame([{
                    "Source": file_name,
                    "Target": mapping_result.mapped_class,
                    "Relation": relation_type,
                    "Method": mapping_result.method,
                    "Confidence": mapping_result.confidence
                }])
            else:
                logger.warning(f"매핑 실패: {file_name}을 온톨로지 클래스로 매핑할 수 없습니다.")
                raise ValueError(f"데이터셋 '{file_name}'을 온톨로지 클래스로 매핑할 수 없습니다.")
            
        except Exception as e:
            logger.error(f"관계 추출 실패: {str(e)}", exc_info=True)
            raise ValueError(f"관계 추출 중 오류가 발생했습니다: {str(e)}")
    
    def _detect_source_column(self, df: pl.DataFrame) -> str:
        """
        소스 컬럼 자동 감지
        
        Args:
            df: 데이터프레임
            
        Returns:
            str: 소스 컬럼명
        """
        # 일반적인 소스 컬럼명 패턴
        source_patterns = [
            'filename', 'file_name', 'file', 'name', 'dataset', 'data',
            'source', 'id', 'identifier', 'key'
        ]
        
        for pattern in source_patterns:
            for col in df.columns:
                if pattern.lower() in col.lower():
                    return col
        
        # 패턴 매칭 실패 시 첫 번째 컬럼 사용
        return df.columns[0]
    
    def _detect_target_column(self, df: pl.DataFrame) -> Optional[str]:
        """
        타겟 컬럼 자동 감지
        
        Args:
            df: 데이터프레임
            
        Returns:
            Optional[str]: 타겟 컬럼명 또는 None
        """
        # 일반적인 타겟 컬럼명 패턴
        target_patterns = [
            'class', 'type', 'category', 'ontology', 'mapped_class',
            'target', 'category', 'classification'
        ]
        
        for pattern in target_patterns:
            for col in df.columns:
                if pattern.lower() in col.lower():
                    return col
        
        return None

