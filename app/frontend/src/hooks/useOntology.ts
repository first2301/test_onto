/**
 * 온톨로지 관련 React Query 훅
 * 서버 상태 관리 및 캐싱
 */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { message } from 'antd';
import {
  getHybridOntology,
  listOntologies,
  getOntologyGraph,
  getMergedOntologyGraph,
  uploadData,
} from '../api/ontology';
import type {
  GetHybridOntologyResponse,
  ListOntologiesResponse,
  OntologyGraphResponse,
  UploadDataResponse,
} from '../types/ontology';

/**
 * 온톨로지 조회 Query 훅
 * 
 * @param ontologyId 온톨로지 ID
 * @param enabled 쿼리 활성화 여부 (기본값: false)
 * @returns query 객체 (data, isLoading, error 등)
 */
export const useGetOntology = (
  ontologyId: string | null,
  enabled: boolean = false
) => {
  return useQuery({
    queryKey: ['ontology', ontologyId],
    queryFn: () => {
      if (!ontologyId) {
        throw new Error('온톨로지 ID가 필요합니다.');
      }
      return getHybridOntology(ontologyId);
    },
    enabled: enabled && !!ontologyId,
    retry: 1,
    staleTime: 5 * 60 * 1000, // 5분간 캐시 유지
  });
};

/**
 * 온톨로지 목록 조회 Query 훅
 * 
 * @returns query 객체 (data, isLoading, error 등)
 */
export const useListOntologies = () => {
  return useQuery({
    queryKey: ['ontologies', 'list'],
    queryFn: () => listOntologies(),
    retry: 1,
    staleTime: 1 * 60 * 1000, // 1분간 캐시 유지
    refetchOnWindowFocus: true, // 창 포커스 시 재조회
  });
};

/**
 * 온톨로지 그래프 데이터 조회 Query 훅
 * 
 * @param ontologyId 온톨로지 ID
 * @param enabled 쿼리 활성화 여부 (기본값: false)
 * @returns query 객체 (data, isLoading, error 등)
 */
export const useGetOntologyGraph = (
  ontologyId: string | null,
  enabled: boolean = false
) => {
  return useQuery({
    queryKey: ['ontology', 'graph', ontologyId],
    queryFn: () => {
      if (!ontologyId) {
        throw new Error('온톨로지 ID가 필요합니다.');
      }
      return getOntologyGraph(ontologyId);
    },
    enabled: enabled && !!ontologyId,
    retry: 1,
    staleTime: 5 * 60 * 1000, // 5분간 캐시 유지
  });
};

/**
 * 통합 온톨로지 그래프 조회 Query 훅
 * 모든 온톨로지를 통합한 그래프 데이터를 조회
 * 
 * @returns query 객체 (data, isLoading, error 등)
 */
export const useGetMergedOntologyGraph = () => {
  return useQuery({
    queryKey: ['ontology', 'merged', 'graph'],
    queryFn: () => getMergedOntologyGraph(),
    staleTime: 5 * 60 * 1000, // 5분간 캐시 유지
    refetchOnWindowFocus: false,
    retry: 1,
  });
};

/**
 * 데이터 업로드 Mutation 훅
 * 
 * @returns mutation 객체 (mutate, isLoading, error 등)
 */
export const useUploadData = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (params: {
      file: File;
      ontologyClasses: string[];
      options?: {
        ontologyId?: string;
        relationType?: string;
        sourceColumn?: string;
        targetColumn?: string;
        modelName?: string;
      };
    }) => uploadData(params.file, params.ontologyClasses, params.options || {}),
    onSuccess: (data: UploadDataResponse) => {
      message.success(data.message || '데이터 업로드가 완료되었습니다.');
      // 관련 쿼리 무효화
      queryClient.invalidateQueries({ queryKey: ['ontology'] });
      queryClient.invalidateQueries({ queryKey: ['ontologies', 'list'] });
      queryClient.invalidateQueries({ queryKey: ['ontology', 'merged', 'graph'] });
    },
    onError: (error: Error) => {
      message.error(error.message || '데이터 업로드 중 오류가 발생했습니다.');
    },
  });
};

