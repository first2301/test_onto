/**
 * 온톨로지 조회 페이지
 * 온톨로지 ID로 조회
 */

import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Card, Form, Input, Button, Space, Divider, Tag } from 'antd';
import { BarChartOutlined } from '@ant-design/icons';
import Layout from '../components/common/Layout/Layout';
import LoadingSpinner from '../components/common/Loading/LoadingSpinner';
import ErrorMessage from '../components/common/Error/ErrorMessage';
import MappingResultTable from '../components/ontology/MappingResultTable';
import RDFGraphViewer from '../components/ontology/RDFGraphViewer';
import { useGetOntology } from '../hooks/useOntology';

const ViewOntology = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const urlOntologyId = searchParams.get('ontology_id');
  const [ontologyId, setOntologyId] = useState<string | null>(urlOntologyId);
  const { data, isLoading, error, refetch } = useGetOntology(ontologyId, !!ontologyId);

  // URL 파라미터에서 ID를 가져와서 폼에 설정
  useEffect(() => {
    if (urlOntologyId) {
      form.setFieldsValue({ ontology_id: urlOntologyId });
      setOntologyId(urlOntologyId);
    }
  }, [urlOntologyId, form]);

  const handleSubmit = (values: { ontology_id: string }) => {
    setOntologyId(values.ontology_id);
    refetch();
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
        title="온톨로지 조회"
        style={cardStyle}
        headStyle={{
          background: 'var(--gradient-card)',
          borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
          borderRadius: '16px 16px 0 0',
        }}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{ ontology_id: '' }}
        >
          <Form.Item
            name="ontology_id"
            label="온톨로지 ID"
            rules={[
              {
                required: true,
                message: '온톨로지 ID를 입력해주세요.',
              },
            ]}
          >
            <Input
              placeholder="온톨로지 ID를 입력하세요"
              size="large"
            />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button
                type="primary"
                htmlType="submit"
                size="large"
                loading={isLoading}
                style={{
                  background: 'var(--gradient-primary)',
                  border: 'none',
                }}
              >
                조회
              </Button>
              <Button
                onClick={() => {
                  form.resetFields();
                  setOntologyId(null);
                }}
                size="large"
              >
                초기화
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>

      {isLoading && (
        <Card style={{ marginTop: 24, ...cardStyle }}>
          <LoadingSpinner message="온톨로지를 조회하는 중입니다..." />
        </Card>
      )}

      {error && (
        <Card style={{ marginTop: 24, ...cardStyle }}>
          <ErrorMessage
            message="온톨로지 조회 중 오류가 발생했습니다."
            description={error.message}
          />
        </Card>
      )}

      {data && !isLoading && (
        <>
          <Card
            title="조회 결과"
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
              <Button
                type="primary"
                icon={<BarChartOutlined />}
                onClick={() => navigate(`/visualize?ontology_id=${data.ontology_id}`)}
                style={{
                  background: '#FFFFFF',
                  color: 'var(--primary-color)',
                  border: 'none',
                }}
              >
                시각화
              </Button>
            }
          >
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <div>
                <strong>메시지:</strong> {data.message}
              </div>
              <div>
                <strong>온톨로지 ID:</strong>{' '}
                <Tag color="blue" style={{ fontFamily: 'monospace' }}>
                  {data.ontology_id}
                </Tag>
              </div>
              <div>
                <strong>생성일시:</strong> {new Date(data.created_at).toLocaleString('ko-KR')}
              </div>
              <div>
                <strong>온톨로지 클래스:</strong>
                <Space wrap style={{ marginLeft: 8 }}>
                  {data.ontology_classes.map((cls) => (
                    <Tag key={cls} color="green">
                      {cls}
                    </Tag>
                  ))}
                </Space>
              </div>
              <div>
                <strong>매핑 개수:</strong>{' '}
                <Tag color={data.mapping_count > 0 ? 'success' : 'default'}>
                  {data.mapping_count}개
                </Tag>
              </div>
            </Space>
          </Card>

          {data.mapping_df && data.mapping_df.length > 0 && (
            <>
              <Divider />
              <Card
                title="매핑 결과"
                style={{ marginTop: 24, ...cardStyle }}
                headStyle={{
                  background: 'var(--gradient-card)',
                  borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
                  borderRadius: '16px 16px 0 0',
                }}
              >
                <MappingResultTable data={data.mapping_df} loading={false} />
              </Card>
            </>
          )}

          {data.g && (
            <Card
              style={{ marginTop: 24, ...cardStyle }}
              headStyle={{
                background: 'var(--gradient-card)',
                borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
                borderRadius: '16px 16px 0 0',
              }}
            >
              <RDFGraphViewer graph={data.g} title="RDF Graph (Turtle 형식)" />
            </Card>
          )}
        </>
      )}
    </Layout>
  );
};

export default ViewOntology;

