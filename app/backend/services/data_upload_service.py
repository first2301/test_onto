"""
데이터 업로드 서비스
파일 업로드 및 온톨로지 관계 추가 처리
"""

import logging
import uuid
import urllib.parse
from typing import Optional, List, Dict, Any
from rdflib import Graph, Literal, RDF, Namespace
from backend.services.data_parser import get_parser
from backend.services.relation_extractor import RelationExtractor
from backend.services.ontology_storage import get_ontology_storage
from backend.services.ontology_services.config import BASE_URI, FACT_URI, DEFAULT_MODEL
from backend.schmas.ontology_schma import UploadDataResponse

logger = logging.getLogger(__name__)


class DataUploadService:
    """데이터 업로드 서비스"""
    
    def upload_and_build_ontology(
        self,
        file_content: bytes,
        file_name: str,
        file_type: str,
        ontology_classes: List[str],
        ontology_id: Optional[str] = None,
        relation_type: str = "isDataOf",
        source_column: Optional[str] = None,
        target_column: Optional[str] = None,
        model_name: str = DEFAULT_MODEL
    ) -> UploadDataResponse:
        """
        파일 업로드 및 온톨로지 구축
        매핑은 자동으로 처리됩니다: 타겟 컬럼이 있으면 직접 매핑, 없으면 파일명 기반 하이브리드 매핑 사용
        
        Args:
            file_content: 파일 내용 (bytes)
            file_name: 파일명
            file_type: 파일 타입 (csv, json, excel)
            ontology_classes: 온톨로지 클래스 목록
            ontology_id: 기존 온톨로지 ID (None이면 새로 생성)
            relation_type: 관계 타입
            source_column: 소스 컬럼명 (None이면 자동 감지)
            target_column: 타겟 컬럼명 (None이면 자동 감지, 있으면 직접 매핑 사용)
            model_name: 모델명
            
        Returns:
            UploadDataResponse: 업로드 결과
        """
        try:
            # 1. 파일 파싱
            logger.info(f"파일 파싱 시작: {file_name}, 타입: {file_type}")
            parser = get_parser(file_type)
            df = parser.parse(file_content, file_name)
            
            if len(df) == 0:
                raise ValueError("파일이 비어있거나 파싱할 데이터가 없습니다.")
            
            logger.info(f"파싱 완료: {len(df)}개 행")
            
            # 2. 관계 추출
            logger.info("관계 추출 시작")
            extractor = RelationExtractor(ontology_classes, model_name)
            relations_df = extractor.extract_relations(
                df=df,
                file_name=file_name,  # 파일명 전달 (데이터셋 전체를 하나의 클래스로 매핑)
                relation_type=relation_type,
                source_column=source_column,
                target_column=target_column
            )
            
            if len(relations_df) == 0:
                raise ValueError("추출된 관계가 없습니다.")
            
            logger.info(f"관계 추출 완료: {len(relations_df)}개 관계")
            
            # 3. RDF Graph 생성 또는 병합
            if ontology_id:
                # 기존 온톨로지에 관계 추가
                logger.info(f"기존 온톨로지에 관계 추가: {ontology_id}")
                g = self._add_relations_to_existing_ontology(
                    ontology_id=ontology_id,
                    relations_df=relations_df,
                    relation_type=relation_type
                )
            else:
                # 새 온톨로지 생성
                logger.info("새 온톨로지 생성")
                ontology_id = str(uuid.uuid4())
                g = self._build_new_ontology(
                    relations_df=relations_df,
                    relation_type=relation_type
                )
            
            # 4. Graph 직렬화
            graph_turtle = g.serialize(format="turtle")
            if isinstance(graph_turtle, bytes):
                graph_turtle = graph_turtle.decode('utf-8')
            graph_turtle = str(graph_turtle)
            
            # 5. 응답 생성
            mapping_dict = relations_df.to_dicts()
            
            response = UploadDataResponse(
                message="데이터 업로드 및 온톨로지 구축 완료",
                ontology_id=ontology_id,
                file_name=file_name,
                file_size=len(file_content),
                records_processed=len(df),
                relations_added=len(relations_df),
                mapping_df=mapping_dict,
                g=graph_turtle
            )
            
            # 6. 저장소에 저장 (기존 온톨로지 업데이트 또는 새로 저장)
            storage = get_ontology_storage()
            if ontology_id in storage._storage:
                # 기존 온톨로지 업데이트
                existing = storage.get(ontology_id)
                existing["rdf_graph"] = graph_turtle
                existing["mapping_df"].extend(mapping_dict)
                existing["mapping_count"] = len(existing["mapping_df"])
            else:
                # 새 온톨로지 저장
                from backend.schmas.ontology_schma import BuildHybridOntologyResponse
                build_response = BuildHybridOntologyResponse(
                    message=response.message,
                    ontology_id=ontology_id,
                    mapping_df=mapping_dict,
                    g=graph_turtle
                )
                storage.save(build_response, ontology_classes)
            
            logger.info(f"데이터 업로드 완료: ontology_id={ontology_id}, 관계={len(relations_df)}개")
            
            return response
            
        except Exception as e:
            logger.error(f"데이터 업로드 실패: {str(e)}", exc_info=True)
            raise
    
    def _build_new_ontology(
        self,
        relations_df,
        relation_type: str
    ) -> Graph:
        """
        새 온톨로지 Graph 생성
        
        Args:
            relations_df: 관계 DataFrame
            relation_type: 관계 타입
            
        Returns:
            Graph: RDF Graph
        """
        META = Namespace(BASE_URI)
        FACT = Namespace(FACT_URI)
        g = Graph()
        g.bind("meta", META)
        g.bind("fact", FACT)
        
        for row in relations_df.iter_rows(named=True):
            source = str(row['Source'])
            target = str(row['Target'])
            
            # URI 생성
            source_uri = FACT[urllib.parse.quote(source)]
            target_uri = FACT[urllib.parse.quote(target)]
            
            # 관계 추가
            relation_predicate = FACT[relation_type]
            g.add((source_uri, relation_predicate, target_uri))
        
        return g
    
    def _add_relations_to_existing_ontology(
        self,
        ontology_id: str,
        relations_df,
        relation_type: str
    ) -> Graph:
        """
        기존 온톨로지에 관계 추가
        
        Args:
            ontology_id: 온톨로지 ID
            relations_df: 관계 DataFrame
            relation_type: 관계 타입
            
        Returns:
            Graph: 병합된 RDF Graph
        """
        storage = get_ontology_storage()
        existing = storage.get(ontology_id)
        
        if not existing:
            raise ValueError(f"온톨로지를 찾을 수 없습니다: {ontology_id}")
        
        # 기존 Graph 로드
        from rdflib import Graph
        from backend.services.ontology_services.rdf_parser import parse_rdf_graph
        
        existing_graph_str = existing["rdf_graph"]
        
        # 기존 Graph가 문자열인 경우 파싱
        if isinstance(existing_graph_str, str):
            g = Graph()
            g.parse(data=existing_graph_str, format="turtle")
        else:
            g = existing_graph_str
        
        # 새 관계 추가
        FACT = Namespace(FACT_URI)
        
        for row in relations_df.iter_rows(named=True):
            source = str(row['Source'])
            target = str(row['Target'])
            
            # URI 생성
            source_uri = FACT[urllib.parse.quote(source)]
            target_uri = FACT[urllib.parse.quote(target)]
            
            # 관계 추가
            relation_predicate = FACT[relation_type]
            g.add((source_uri, relation_predicate, target_uri))
        
        return g

