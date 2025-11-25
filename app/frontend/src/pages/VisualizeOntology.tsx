/**
 * 온톨로지 시각화 페이지
 * 모든 온톨로지를 통합한 그래프 시각화
 */

import { Card, Space, Typography, Button, message, Divider } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import Layout from '../components/common/Layout/Layout';
import OntologyGraphViewer from '../components/ontology/OntologyGraphViewer';
import LoadingSpinner from '../components/common/Loading/LoadingSpinner';
import ErrorMessage from '../components/common/Error/ErrorMessage';
import { useGetMergedOntologyGraph, useListOntologies } from '../hooks/useOntology';

const { Title, Text } = Typography;

const VisualizeOntology = () => {
  const { data: listData } = useListOntologies();
  const {
    data: graphData,
    isLoading: graphLoading,
    error: graphError,
    refetch: refetchGraph,
  } = useGetMergedOntologyGraph();

  // 그래프 새로고침
  const handleRefresh = () => {
    refetchGraph();
    message.success('그래프를 새로고침했습니다.');
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
        title={
          <Space split={<Divider type="vertical" />} wrap>
            <Title level={2} style={{ margin: 0, fontSize: 20 }}>
              온톨로지 관계 시각화 (전체)
            </Title>
            {graphData && !graphLoading && (
              <Text type="secondary" style={{ fontSize: 9 }}>
                통합 온톨로지 그래프 (노드: {graphData.nodes.length}개, 엣지: {graphData.edges.length}개)
              </Text>
            )}
          </Space>
        }
        extra={
          <Space>
            {listData && (
              <Text type="secondary">
                총 {listData.total}개 온톨로지 통합
              </Text>
            )}
            <Button
              icon={<ReloadOutlined />}
              onClick={handleRefresh}
              disabled={graphLoading}
              style={{
                background: 'var(--gradient-primary)',
                border: 'none',
                color: '#FFFFFF',
              }}
            >
              새로고침
            </Button>
          </Space>
        }
        style={cardStyle}
        headStyle={{
          background: 'var(--gradient-card)',
          borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
          borderRadius: '16px 16px 0 0',
        }}
        bodyStyle={{
          padding: '24px',
        }}
      >
        {graphLoading && (
          <LoadingSpinner message="통합 그래프 데이터를 불러오는 중..." />
        )}

        {graphError && (
          <ErrorMessage
            message="통합 그래프 데이터를 불러오는 중 오류가 발생했습니다."
            description={graphError.message}
          />
        )}

        {graphData && !graphLoading && !graphError && (
          <OntologyGraphViewer
            nodes={graphData.nodes}
            edges={graphData.edges}
            height={600}
          />
        )}

        {!graphData && !graphLoading && !graphError && (
          <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
            온톨로지가 없습니다. 데이터를 업로드하여 온톨로지를 생성해주세요.
          </div>
        )}
      </Card>
    </Layout>
  );
};

export default VisualizeOntology;

