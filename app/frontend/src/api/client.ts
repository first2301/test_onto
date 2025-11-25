/**
 * Axios 클라이언트 설정
 * API 요청의 기본 설정 및 인터셉터 관리
 */

import axios from 'axios';
import type { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

// 환경 변수에서 API Base URL 가져오기
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Axios 인스턴스 생성
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30초 타임아웃
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 요청 인터셉터
 * 요청 전 공통 처리 (인증 토큰 추가 등)
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 요청 로깅 (개발 환경)
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error: AxiosError) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

/**
 * 응답 인터셉터
 * 응답 후 공통 처리 및 에러 처리
 */
apiClient.interceptors.response.use(
  (response) => {
    // 응답 로깅 (개발 환경)
    if (import.meta.env.DEV) {
      console.log(`[API Response] ${response.config.url}`, response.data);
    }
    return response;
  },
  (error: AxiosError) => {
    // 에러 처리
    if (error.response) {
      // 서버가 응답했지만 에러 상태 코드
      const status = error.response.status;
      const data = error.response.data as { detail?: string };
      
      console.error(`[API Error] ${status}:`, data);
      
      // 에러 메시지 추출
      const errorMessage = data?.detail || error.message || '알 수 없는 오류가 발생했습니다.';
      
      // 에러 객체에 메시지 추가
      error.message = errorMessage;
    } else if (error.request) {
      // 요청은 보냈지만 응답을 받지 못함
      console.error('[API Error] No response received:', error.request);
      error.message = '서버에 연결할 수 없습니다. 네트워크를 확인해주세요.';
    } else {
      // 요청 설정 중 오류 발생
      console.error('[API Error] Request setup error:', error.message);
      error.message = error.message || '요청 중 오류가 발생했습니다.';
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;

