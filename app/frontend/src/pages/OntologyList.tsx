/**
 * 온톨로지 목록 페이지
 * 생성된 온톨로지 목록을 테이블로 표시
 */

import { Card, Table, Tag, Space, Button, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';
import { EyeOutlined, BarChartOutlined } from '@ant-design/icons';
import Layout from '../components/common/Layout/Layout';
import LoadingSpinner from '../components/common/Loading/LoadingSpinner';
import ErrorMessage from '../components/common/Error/ErrorMessage';
import { useListOntologies } from '../hooks/useOntology';
import type { ColumnsType } from 'antd/es/table';
import type { OntologyListItem } from '../types/ontology';

const { Title } = Typography;

const OntologyList = () => {
  const navigate = useNavigate();
  const { data, isLoading, error, refetch } = useListOntologies();

  const handleView = (ontologyId: string) => {
    navigate(`/view?ontology_id=${ontologyId}`);
  };

  const handleVisualize = (ontologyId: string) => {
    navigate(`/visualize?ontology_id=${ontologyId}`);
  };

  const columns: ColumnsType<OntologyListItem> = [
    {
      title: '온톨로지 ID',
      dataIndex: 'ontology_id',
      key: 'ontology_id',
      width: 300,
      render: (text: string) => (
        <Tag color="blue" style={{ fontFamily: 'monospace', fontSize: 12 }}>
          {text.substring(0, 8)}...
        </Tag>
      ),
    },
    {
      title: '생성일시',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 200,
      sorter: (a, b) => a.created_at.localeCompare(b.created_at),
      render: (text: string) => {
        const date = new Date(text);
        return date.toLocaleString('ko-KR');
      },
    },
    {
      title: '온톨로지 클래스',
      dataIndex: 'ontology_classes',
      key: 'ontology_classes',
      render: (classes: string[]) => (
        <Space wrap>
          {classes.map((cls) => (
            <Tag key={cls} color="green">
              {cls}
            </Tag>
          ))}
        </Space>
      ),
    },
    {
      title: '매핑 개수',
      dataIndex: 'mapping_count',
      key: 'mapping_count',
      width: 120,
      sorter: (a, b) => a.mapping_count - b.mapping_count,
      render: (count: number) => (
        <Tag color={count > 0 ? 'success' : 'default'}>{count}개</Tag>
      ),
    },
    {
      title: '액션',
      key: 'action',
      width: 200,
      render: (_: any, record: OntologyListItem) => (
        <Space>
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => handleView(record.ontology_id)}
            size="small"
          >
            조회
          </Button>
          <Button
            type="link"
            icon={<BarChartOutlined />}
            onClick={() => handleVisualize(record.ontology_id)}
            size="small"
          >
            시각화
          </Button>
        </Space>
      ),
    },
  ];

  const cardStyle = {
    borderRadius: 16,
    boxShadow: 'var(--shadow-md)',
    border: '1px solid rgba(0, 0, 0, 0.05)',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  };

  return (
    <Layout>
      <Card
        title={<Title level={2} style={{ margin: 0 }}>온톨로지 목록</Title>}
        extra={
          <Button
            onClick={() => refetch()}
            loading={isLoading}
            style={{
              background: 'var(--gradient-primary)',
              border: 'none',
              color: '#FFFFFF',
            }}
          >
            새로고침
          </Button>
        }
        style={cardStyle}
        headStyle={{
          background: 'var(--gradient-card)',
          borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
          borderRadius: '16px 16px 0 0',
        }}
      >
        {isLoading && <LoadingSpinner message="온톨로지 목록을 불러오는 중..." />}

        {error && (
          <ErrorMessage
            message="온톨로지 목록을 불러오는 중 오류가 발생했습니다."
            description={error.message}
          />
        )}

        {data && !isLoading && (
          <>
            <div style={{ marginBottom: 16 }}>
              <Typography.Text type="secondary">
                총 {data.total}개의 온톨로지가 있습니다.
              </Typography.Text>
            </div>
            <Table
              columns={columns}
              dataSource={data.ontologies}
              rowKey="ontology_id"
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showTotal: (total) => `총 ${total}개`,
              }}
              scroll={{ x: 'max-content' }}
            />
          </>
        )}

        {data && data.total === 0 && !isLoading && (
          <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
            생성된 온톨로지가 없습니다.
            <br />
            <Button
              type="link"
              onClick={() => navigate('/upload')}
              style={{ marginTop: 16 }}
            >
              데이터 업로드하기
            </Button>
          </div>
        )}
      </Card>
    </Layout>
  );
};

export default OntologyList;

