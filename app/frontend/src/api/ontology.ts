/**
 * 온톨로지 관련 API 함수
 * 백엔드 API 엔드포인트와 통신
 */

import apiClient from './client';
import type {
  GetHybridOntologyResponse,
  ListOntologiesResponse,
  OntologyGraphResponse,
  UploadDataResponse,
} from '../types/ontology';

/**
 * 온톨로지 조회
 * 
 * @param ontologyId 온톨로지 ID
 * @returns 조회 결과
 */
export const getHybridOntology = async (
  ontologyId: string
): Promise<GetHybridOntologyResponse> => {
  const response = await apiClient.get<GetHybridOntologyResponse>(
    '/api/v1/get_hybrid_ontology',
    {
      params: {
        ontology_id: ontologyId,
      },
    }
  );
  return response.data;
};

/**
 * 온톨로지 목록 조회
 * 
 * @returns 목록 조회 결과
 */
export const listOntologies = async (): Promise<ListOntologiesResponse> => {
  const response = await apiClient.get<ListOntologiesResponse>(
    '/api/v1/list_ontologies'
  );
  return response.data;
};

/**
 * 온톨로지 그래프 데이터 조회
 * 
 * @param ontologyId 온톨로지 ID
 * @returns 그래프 데이터
 */
export const getOntologyGraph = async (
  ontologyId: string
): Promise<OntologyGraphResponse> => {
  const response = await apiClient.get<OntologyGraphResponse>(
    `/api/v1/get_ontology_graph/${ontologyId}`
  );
  return response.data;
};

/**
 * 모든 온톨로지를 통합한 그래프 데이터 조회
 * 
 * @returns 통합된 그래프 데이터
 */
export const getMergedOntologyGraph = async (): Promise<OntologyGraphResponse> => {
  const response = await apiClient.get<OntologyGraphResponse>(
    '/api/v1/get_merged_ontology_graph'
  );
  return response.data;
};

/**
 * 데이터 파일 업로드 및 온톨로지 관계 추가
 * 
 * @param file 업로드할 파일
 * @param ontologyClasses 온톨로지 클래스 목록
 * @param options 업로드 옵션
 * @returns 업로드 결과
 */
export const uploadData = async (
  file: File,
  ontologyClasses: string[],
  options: {
    ontologyId?: string;
    relationType?: string;
    sourceColumn?: string;
    targetColumn?: string;
    modelName?: string;
  } = {}
): Promise<UploadDataResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('ontology_classes', ontologyClasses.join(','));
  
  if (options.ontologyId) {
    formData.append('ontology_id', options.ontologyId);
  }
  if (options.relationType) {
    formData.append('relation_type', options.relationType);
  }
  if (options.sourceColumn) {
    formData.append('source_column', options.sourceColumn);
  }
  if (options.targetColumn) {
    formData.append('target_column', options.targetColumn);
  }
  if (options.modelName) {
    formData.append('model_name', options.modelName);
  }
  
  const response = await apiClient.post<UploadDataResponse>(
    '/api/v1/upload_data',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );
  return response.data;
};

