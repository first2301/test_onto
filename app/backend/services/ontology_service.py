"""
온톨로지 서비스 레이어
비즈니스 로직 및 데이터 변환 처리
"""

import logging
from typing import List, Dict, Any
from rdflib import Graph
from backend.services.ontology_storage import get_ontology_storage
from backend.services.ontology_services.rdf_parser import parse_rdf_graph
from backend.schmas.ontology_schma import (
    GetHybridOntologyResponse,
    ListOntologiesResponse,
    OntologyListItem,
    OntologyGraphResponse,
    OntologyGraphNode,
    OntologyGraphEdge,
)

logger = logging.getLogger(__name__)


class OntologyService:
    """온톨로지 관련 비즈니스 로직 처리"""
    
    def get_hybrid_ontology(self, ontology_id: str) -> GetHybridOntologyResponse:
        """
        온톨로지 조회
        
        Args:
            ontology_id: 온톨로지 ID
            
        Returns:
            GetHybridOntologyResponse: 조회 결과
        """
        storage = get_ontology_storage()
        ontology = storage.get(ontology_id)
        
        if not ontology:
            raise ValueError(f"온톨로지를 찾을 수 없습니다: {ontology_id}")
        
        return GetHybridOntologyResponse(
            message="하이브리드 온톨로지 조회 완료",
            ontology_id=ontology["ontology_id"],
            created_at=ontology["created_at"],
            ontology_classes=ontology["ontology_classes"],
            mapping_count=ontology["mapping_count"],
            mapping_df=ontology["mapping_df"],
            g=ontology["rdf_graph"],
        )
    
    def list_ontologies(self) -> ListOntologiesResponse:
        """
        온톨로지 목록 조회
        
        Returns:
            ListOntologiesResponse: 목록 조회 결과
        """
        storage = get_ontology_storage()
        all_ontologies = storage.list_all()
        
        # 목록 아이템으로 변환
        items = [
            OntologyListItem(
                ontology_id=ont["ontology_id"],
                created_at=ont["created_at"],
                ontology_classes=ont["ontology_classes"],
                mapping_count=ont["mapping_count"],
            )
            for ont in all_ontologies
        ]
        
        return ListOntologiesResponse(
            message="온톨로지 목록 조회 완료",
            total=len(items),
            ontologies=items,
        )
    
    def get_ontology_graph(self, ontology_id: str) -> OntologyGraphResponse:
        """
        온톨로지 그래프 데이터 조회
        
        Args:
            ontology_id: 온톨로지 ID
            
        Returns:
            OntologyGraphResponse: 그래프 데이터
        """
        storage = get_ontology_storage()
        ontology = storage.get(ontology_id)
        
        if not ontology:
            raise ValueError(f"온톨로지를 찾을 수 없습니다: {ontology_id}")
        
        # 저장된 rdf_graph 타입 확인
        rdf_graph = ontology["rdf_graph"]
        logger.debug(f"저장된 RDF Graph 타입: {type(rdf_graph)}")
        
        # Graph 객체인 경우 직렬화
        if isinstance(rdf_graph, Graph):
            logger.warning("저장된 RDF Graph가 Graph 객체입니다. 직렬화합니다.")
            rdf_graph = rdf_graph.serialize(format="turtle")
            if isinstance(rdf_graph, bytes):
                rdf_graph = rdf_graph.decode('utf-8')
            rdf_graph = str(rdf_graph)
        
        # RDF Graph 파싱
        graph_data = parse_rdf_graph(rdf_graph)
        
        # 스키마 객체로 변환
        nodes = [
            OntologyGraphNode(
                id=node["id"],
                label=node["label"],
                type=node["type"]
            )
            for node in graph_data["nodes"]
        ]
        
        edges = [
            OntologyGraphEdge(
                source=edge["source"],
                target=edge["target"],
                relation=edge["relation"]
            )
            for edge in graph_data["edges"]
        ]
        
        return OntologyGraphResponse(
            message="온톨로지 그래프 조회 완료",
            ontology_id=ontology_id,
            nodes=nodes,
            edges=edges,
        )
    
    def get_merged_ontology_graph(self) -> OntologyGraphResponse:
        """
        모든 온톨로지를 통합한 그래프 데이터 조회
        
        Returns:
            OntologyGraphResponse: 통합된 그래프 데이터
        """
        storage = get_ontology_storage()
        all_ontologies = storage.list_all()
        
        if not all_ontologies:
            return OntologyGraphResponse(
                message="통합 온톨로지 그래프 조회 완료 (온톨로지 없음)",
                ontology_id="merged",
                nodes=[],
                edges=[],
            )
        
        # 모든 온톨로지의 노드와 엣지를 병합
        all_nodes: Dict[str, OntologyGraphNode] = {}
        all_edges: List[OntologyGraphEdge] = []
        
        for ontology in all_ontologies:
            rdf_graph = ontology["rdf_graph"]
            
            # Graph 객체인 경우 직렬화
            if isinstance(rdf_graph, Graph):
                logger.debug(f"온톨로지 {ontology['ontology_id']}: Graph 객체를 직렬화합니다.")
                rdf_graph = rdf_graph.serialize(format="turtle")
                if isinstance(rdf_graph, bytes):
                    rdf_graph = rdf_graph.decode('utf-8')
                rdf_graph = str(rdf_graph)
            
            # RDF Graph 파싱
            graph_data = parse_rdf_graph(rdf_graph)
            
            # 노드 병합 (중복 제거 - 같은 ID는 하나만 유지)
            for node in graph_data["nodes"]:
                node_id = node["id"]
                if node_id not in all_nodes:
                    all_nodes[node_id] = OntologyGraphNode(
                        id=node["id"],
                        label=node["label"],
                        type=node["type"]
                    )
            
            # 엣지 추가 (모든 엣지 포함)
            for edge in graph_data["edges"]:
                all_edges.append(OntologyGraphEdge(
                    source=edge["source"],
                    target=edge["target"],
                    relation=edge["relation"]
                ))
        
        logger.info(f"통합 그래프 생성 완료: 노드 {len(all_nodes)}개, 엣지 {len(all_edges)}개 (온톨로지 {len(all_ontologies)}개 병합)")
        
        return OntologyGraphResponse(
            message="통합 온톨로지 그래프 조회 완료",
            ontology_id="merged",
            nodes=list(all_nodes.values()),
            edges=all_edges,
        )

