"""
RDF Graph 파서
Turtle 형식의 RDF Graph를 노드/엣지 구조로 변환
"""

import logging
from typing import List, Dict, Set
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF

logger = logging.getLogger(__name__)


def parse_rdf_graph(turtle_string: str) -> Dict[str, List]:
    """
    Turtle 형식의 RDF Graph를 노드/엣지 구조로 파싱
    
    Args:
        turtle_string: Turtle 형식의 RDF Graph 문자열
        
    Returns:
        {
            "nodes": [{"id": str, "label": str, "type": str}, ...],
            "edges": [{"source": str, "target": str, "relation": str}, ...]
        }
    """
    try:
        # 입력 검증
        if not turtle_string:
            logger.warning("빈 RDF Graph 문자열")
            return {"nodes": [], "edges": []}
        
        # dict 타입 체크 및 처리
        if isinstance(turtle_string, dict):
            logger.error(f"RDF Graph가 dict 타입입니다. 문자열이 필요합니다. dict keys: {list(turtle_string.keys())}")
            # dict를 문자열로 변환 시도 (일반적으로 실패할 것)
            # 하지만 안전하게 처리
            try:
                # dict가 serialize된 형태인지 확인
                if 'nodes' in turtle_string or 'edges' in turtle_string:
                    # 이미 파싱된 형태인 경우
                    logger.warning("이미 파싱된 그래프 데이터입니다.")
                    return {
                        "nodes": turtle_string.get("nodes", []),
                        "edges": turtle_string.get("edges", [])
                    }
                else:
                    # 알 수 없는 dict 형태
                    logger.error(f"알 수 없는 dict 형태: {turtle_string}")
                    return {"nodes": [], "edges": []}
            except Exception as e:
                logger.error(f"dict 처리 중 오류: {str(e)}")
                return {"nodes": [], "edges": []}
        
        # 문자열이 아닌 경우 문자열로 변환
        if not isinstance(turtle_string, str):
            logger.warning(f"RDF Graph가 문자열이 아닙니다: {type(turtle_string)}")
            # Graph 객체인 경우
            if hasattr(turtle_string, 'serialize'):
                try:
                    turtle_string = turtle_string.serialize(format="turtle")
                    if isinstance(turtle_string, bytes):
                        turtle_string = turtle_string.decode('utf-8')
                    turtle_string = str(turtle_string)
                except Exception as e:
                    logger.error(f"Graph 직렬화 실패: {str(e)}")
                    return {"nodes": [], "edges": []}
            else:
                turtle_string = str(turtle_string)
        
        # 빈 문자열 체크
        turtle_string = turtle_string.strip()
        if not turtle_string:
            logger.warning("빈 RDF Graph 문자열 (공백만 포함)")
            return {"nodes": [], "edges": []}
        
        # RDF Graph 생성 및 파싱
        g = Graph()
        try:
            g.parse(data=turtle_string, format="turtle")
        except Exception as parse_error:
            logger.error(f"RDF 파싱 실패: {str(parse_error)}")
            logger.debug(f"파싱 시도한 데이터 타입: {type(turtle_string)}")
            logger.debug(f"파싱 시도한 데이터 (처음 200자): {turtle_string[:200] if isinstance(turtle_string, str) else str(turtle_string)[:200]}")
            raise ValueError(f"RDF Graph 형식이 올바르지 않습니다: {str(parse_error)}")
        
        nodes: List[Dict[str, str]] = []
        edges: List[Dict[str, str]] = []
        node_ids = set()  # 중복 방지
        
        # 노드 ID 생성 함수
        def get_node_id(uri: URIRef) -> str:
            """URI에서 노드 ID 추출"""
            uri_str = str(uri)
            # 네임스페이스 제거
            if "#" in uri_str:
                return uri_str.split("#")[-1]
            elif "/" in uri_str:
                return uri_str.split("/")[-1]
            return uri_str
        
        def get_node_label(uri: URIRef) -> str:
            """URI에서 노드 라벨 추출"""
            return get_node_id(uri)
        
        def get_node_type(uri: URIRef, predicate: URIRef) -> str:
            """노드 타입 결정"""
            # 관계 타입에 따라 결정
            pred_str = str(predicate).lower()
            if "isdataof" in pred_str or "hasdata" in pred_str:
                # 데이터셋으로 판단
                return "dataset"
            else:
                # 기본적으로 클래스로 판단
                return "class"
        
        # Graph가 비어있는지 확인
        if len(g) == 0:
            logger.warning("RDF Graph가 비어있습니다")
            return {"nodes": [], "edges": []}
        
        # 모든 트리플 순회
        for subject, predicate, obj in g:
            # 주체(Subject) 노드 추가
            if isinstance(subject, URIRef):
                subj_id = get_node_id(subject)
                if subj_id not in node_ids:
                    nodes.append({
                        "id": subj_id,
                        "label": get_node_label(subject),
                        "type": "dataset"  # 기본적으로 데이터셋
                    })
                    node_ids.add(subj_id)
            
            # 객체(Object) 노드 추가
            if isinstance(obj, URIRef):
                obj_id = get_node_id(obj)
                if obj_id not in node_ids:
                    nodes.append({
                        "id": obj_id,
                        "label": get_node_label(obj),
                        "type": "class"  # 기본적으로 클래스
                    })
                    node_ids.add(obj_id)
            
            # 엣지 추가 (같은 객체가 여러 번 타겟으로 나타나도 모든 관계를 캡처)
            if isinstance(subject, URIRef) and isinstance(obj, URIRef):
                subj_id = get_node_id(subject)
                obj_id = get_node_id(obj)
                pred_str = str(predicate)
                # 관계 타입 추출
                if "#" in pred_str:
                    relation = pred_str.split("#")[-1]
                elif "/" in pred_str:
                    relation = pred_str.split("/")[-1]
                else:
                    relation = pred_str
                
                edges.append({
                    "source": subj_id,
                    "target": obj_id,
                    "relation": relation
                })
        
        logger.info(f"RDF Graph 파싱 완료: 노드 {len(nodes)}개, 엣지 {len(edges)}개")
        
        return {
            "nodes": nodes,
            "edges": edges
        }
        
    except Exception as e:
        logger.error(f"RDF Graph 파싱 실패: {str(e)}", exc_info=True)
        raise ValueError(f"RDF Graph 파싱 중 오류가 발생했습니다: {str(e)}")

