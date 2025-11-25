/**
 * 데이터 업로드 페이지
 * 파일 업로드 및 온톨로지 관계 추가
 */

import { useState } from 'react';
import { Card, Divider, Space, Typography, Button, Tag, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { CopyOutlined, SearchOutlined } from '@ant-design/icons';
import Layout from '../components/common/Layout/Layout';
import UploadDataForm from '../components/upload/UploadDataForm';
import MappingResultTable from '../components/ontology/MappingResultTable';
import RDFGraphViewer from '../components/ontology/RDFGraphViewer';
import LoadingSpinner from '../components/common/Loading/LoadingSpinner';
import ErrorMessage from '../components/common/Error/ErrorMessage';
import { useUploadData, useListOntologies } from '../hooks/useOntology';
import type { UploadDataResponse } from '../types/ontology';

const { Text } = Typography;

const UploadData = () => {
  const [result, setResult] = useState<UploadDataResponse | null>(null);
  const uploadMutation = useUploadData();
  const { data: listData } = useListOntologies();
  const navigate = useNavigate();

  // 기존 온톨로지 목록 준비
  const existingOntologies =
    listData?.ontologies.map((ont) => ({
      id: ont.ontology_id,
      label: `${ont.ontology_id.substring(0, 8)}... (${ont.mapping_count}개 매핑)`,
    })) || [];

  const handleSubmit = async (params: {
    file: File;
    ontologyClasses: string[];
    options: {
      ontologyId?: string;
      relationType?: string;
      sourceColumn?: string;
      targetColumn?: string;
      modelName?: string;
    };
  }) => {
    try {
      const response = await uploadMutation.mutateAsync(params);
      setResult(response);
    } catch (error) {
      // 에러는 useUploadData 훅에서 처리됨
      setResult(null);
    }
  };

  const handleCopyId = async () => {
    if (result?.ontology_id) {
      try {
        await navigator.clipboard.writeText(result.ontology_id);
        message.success('온톨로지 ID가 클립보드에 복사되었습니다.');
      } catch (error) {
        message.error('복사에 실패했습니다.');
      }
    }
  };

  const handleViewOntology = () => {
    if (result?.ontology_id) {
      navigate(`/view?ontology_id=${result.ontology_id}`);
    }
  };

  const cardStyle = {
    borderRadius: 16,
    boxShadow: 'var(--shadow-md)',
    border: '1px solid rgba(0, 0, 0, 0.05)',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  };

  return (
    <Layout>
      <Card
        title="데이터 업로드 및 온톨로지 관계 추가"
        style={cardStyle}
        headStyle={{
          background: 'var(--gradient-card)',
          borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
          borderRadius: '16px 16px 0 0',
        }}
      >
        <UploadDataForm
          onSubmit={handleSubmit}
          loading={uploadMutation.isPending}
          existingOntologies={existingOntologies}
        />
      </Card>

      {uploadMutation.isPending && (
        <Card style={{ marginTop: 24, ...cardStyle }}>
          <LoadingSpinner message="데이터를 업로드하고 온톨로지를 구축하는 중입니다. 잠시만 기다려주세요..." />
        </Card>
      )}

      {uploadMutation.isError && (
        <Card style={{ marginTop: 24, ...cardStyle }}>
          <ErrorMessage
            message="데이터 업로드 중 오류가 발생했습니다."
            description={uploadMutation.error?.message}
          />
        </Card>
      )}

      {result && !uploadMutation.isPending && (
        <>
          <Divider />
          <Card
            title="업로드 완료"
            style={{
              marginTop: 24,
              ...cardStyle,
              background: 'var(--gradient-card)',
            }}
            headStyle={{
              background: 'var(--gradient-primary)',
              color: '#FFFFFF',
              borderRadius: '16px 16px 0 0',
            }}
            extra={
              <Space>
                <Button
                  icon={<CopyOutlined />}
                  onClick={handleCopyId}
                  style={{
                    background: 'rgba(255, 255, 255, 0.2)',
                    color: '#FFFFFF',
                    border: '1px solid rgba(255, 255, 255, 0.3)',
                  }}
                >
                  ID 복사
                </Button>
                <Button
                  type="primary"
                  icon={<SearchOutlined />}
                  onClick={handleViewOntology}
                  style={{
                    background: '#FFFFFF',
                    color: 'var(--primary-color)',
                    border: 'none',
                  }}
                >
                  조회하기
                </Button>
              </Space>
            }
          >
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <div>
                <Text strong>온톨로지 ID: </Text>
                <Tag color="blue" style={{ fontSize: 14, padding: '4px 12px' }}>
                  {result.ontology_id}
                </Tag>
              </div>
              <div>
                <Text strong>파일명: </Text>
                <Text>{result.file_name}</Text>
              </div>
              <div>
                <Text strong>파일 크기: </Text>
                <Text>{(result.file_size / 1024).toFixed(2)} KB</Text>
              </div>
              <div>
                <Text strong>처리된 레코드: </Text>
                <Tag color="green">{result.records_processed}개</Tag>
              </div>
              <div>
                <Text strong>추가된 관계: </Text>
                <Tag color="success">{result.relations_added}개</Tag>
              </div>
            </Space>
          </Card>

          {result.mapping_df && result.mapping_df.length > 0 && (
            <Card
              title="매핑 결과"
              style={{ marginTop: 24, ...cardStyle }}
              headStyle={{
                background: 'var(--gradient-card)',
                borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
                borderRadius: '16px 16px 0 0',
              }}
            >
              <MappingResultTable data={result.mapping_df} loading={false} />
            </Card>
          )}

          <Card
            style={{ marginTop: 24, ...cardStyle }}
            headStyle={{
              background: 'var(--gradient-card)',
              borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
              borderRadius: '16px 16px 0 0',
            }}
          >
            <RDFGraphViewer graph={result.g} title="RDF Graph (Turtle 형식)" />
          </Card>
        </>
      )}
    </Layout>
  );
};

export default UploadData;

