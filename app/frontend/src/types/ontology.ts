/**
 * 온톨로지 관련 TypeScript 타입 정의
 * 백엔드 스키마와 일치하도록 정의
 */

/**
 * 온톨로지 조회 요청 타입
 */
export interface GetHybridOntologyRequest {
  /** 온톨로지 ID */
  ontology_id: string;
}

/**
 * 온톨로지 조회 응답 타입
 */
export interface GetHybridOntologyResponse {
  /** 응답 메시지 */
  message: string;
  /** 온톨로지 ID */
  ontology_id: string;
  /** 생성일시 */
  created_at: string;
  /** 온톨로지 클래스 목록 */
  ontology_classes: string[];
  /** 매핑 개수 */
  mapping_count: number;
  /** 매핑 결과 DataFrame (레코드 배열) */
  mapping_df: Array<Record<string, any>>;
  /** RDF Graph (Turtle 형식) */
  g: string;
}

/**
 * 온톨로지 목록 아이템 타입
 */
export interface OntologyListItem {
  /** 온톨로지 ID */
  ontology_id: string;
  /** 생성일시 */
  created_at: string;
  /** 온톨로지 클래스 목록 */
  ontology_classes: string[];
  /** 매핑 개수 */
  mapping_count: number;
}

/**
 * 온톨로지 목록 조회 응답 타입
 */
export interface ListOntologiesResponse {
  /** 응답 메시지 */
  message: string;
  /** 전체 개수 */
  total: number;
  /** 온톨로지 목록 */
  ontologies: OntologyListItem[];
}

/**
 * 그래프 노드 타입
 */
export interface OntologyGraphNode {
  /** 노드 ID */
  id: string;
  /** 노드 라벨 */
  label: string;
  /** 노드 타입 (class, dataset) */
  type: string;
}

/**
 * 그래프 엣지 타입
 */
export interface OntologyGraphEdge {
  /** 시작 노드 ID */
  source: string;
  /** 종료 노드 ID */
  target: string;
  /** 관계 타입 */
  relation: string;
}

/**
 * 온톨로지 그래프 응답 타입
 */
export interface OntologyGraphResponse {
  /** 응답 메시지 */
  message: string;
  /** 온톨로지 ID */
  ontology_id: string;
  /** 노드 목록 */
  nodes: OntologyGraphNode[];
  /** 엣지 목록 */
  edges: OntologyGraphEdge[];
}

/**
 * 데이터 업로드 응답 타입
 */
export interface UploadDataResponse {
  /** 응답 메시지 */
  message: string;
  /** 온톨로지 ID (기존 또는 새로 생성) */
  ontology_id: string;
  /** 업로드된 파일명 */
  file_name: string;
  /** 파일 크기 (bytes) */
  file_size: number;
  /** 처리된 레코드 수 */
  records_processed: number;
  /** 추가된 관계 수 */
  relations_added: number;
  /** 매핑 결과 DataFrame */
  mapping_df: Array<Record<string, any>>;
  /** RDF Graph (Turtle 형식) */
  g: string;
}

