/**
 * 홈 페이지
 * 기능 소개 및 빠른 링크
 */

import { Card, Row, Col, Button, Typography, Space } from 'antd';
import { useNavigate } from 'react-router-dom';
import {
  UploadOutlined,
  BarChartOutlined,
  UnorderedListOutlined,
} from '@ant-design/icons';
import Layout from '../components/common/Layout/Layout';

const { Title, Paragraph } = Typography;

const Home = () => {
  const navigate = useNavigate();

  return (
    <Layout>
      {/* 히어로 섹션 */}
      <div
        style={{
          textAlign: 'center',
          marginBottom: 48,
          padding: '32px 24px',
          background: 'var(--bg-primary)',
          borderRadius: 16,
          boxShadow: 'var(--shadow-md)',
          border: '1px solid rgba(0, 0, 0, 0.05)',
          color: 'var(--text-primary)',
        }}
        className="fade-in"
      >
        <Title
          level={1}
          style={{
            color: 'var(--text-primary)',
            fontSize: 36,
            fontWeight: 'bold',
            marginBottom: 12,
          }}
        >
          온톨로지 매핑 시스템
        </Title>
        <Paragraph
          style={{
            fontSize: 18,
            color: 'var(--text-secondary)',
            maxWidth: 600,
            margin: '0 auto',
            lineHeight: 1.6,
          }}
        >
          하이브리드 접근법을 활용한 지능형 온톨로지 구축 및 매핑 도구
        </Paragraph>
        <Space size="large" style={{ marginTop: 24 }}>
          <Button
            type="primary"
            size="large"
            icon={<UploadOutlined />}
            onClick={() => navigate('/upload')}
            style={{
              height: 44,
              padding: '0 28px',
              fontSize: 15,
              fontWeight: 'bold',
              background: 'var(--gradient-primary)',
              color: '#FFFFFF',
              border: 'none',
              boxShadow: 'var(--shadow-md)',
            }}
          >
            데이터 업로드 시작
          </Button>
          <Button
            size="large"
            icon={<UnorderedListOutlined />}
            onClick={() => navigate('/list')}
            style={{
              height: 44,
              padding: '0 28px',
              fontSize: 15,
              fontWeight: 'bold',
              background: 'transparent',
              color: 'var(--primary-color)',
              border: '2px solid var(--primary-color)',
            }}
          >
            온톨로지 목록
          </Button>
        </Space>
      </div>

      {/* 기능 카드 */}
      <Row gutter={[24, 24]} style={{ marginBottom: 48 }}>
        <Col xs={24} md={12} lg={8}>
          <Card
            hoverable
            style={{
              height: '100%',
              borderRadius: 16,
              boxShadow: 'var(--shadow-md)',
              border: '1px solid rgba(0, 0, 0, 0.05)',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              display: 'flex',
              flexDirection: 'column',
            }}
            bodyStyle={{
              padding: 24,
              display: 'flex',
              flexDirection: 'column',
              flex: 1,
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = 'var(--shadow-xl)';
              e.currentTarget.style.transform = 'translateY(-4px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = 'var(--shadow-md)';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            <div style={{ textAlign: 'center', marginBottom: 16 }}>
              <UnorderedListOutlined
                style={{
                  fontSize: 48,
                  color: 'var(--primary-color)',
                  marginBottom: 16,
                }}
              />
            </div>
            <Card.Meta
              style={{ flex: 1, display: 'flex', flexDirection: 'column' }}
              title={
                <Title level={4} style={{ textAlign: 'center', marginBottom: 12 }}>
                  온톨로지 목록
                </Title>
              }
              description={
                <Space direction="vertical" style={{ width: '100%', flex: 1 }}>
                  <Paragraph style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                    생성된 모든 온톨로지 목록을 확인하고 관리할 수 있습니다.
                  </Paragraph>
                  <ul
                    style={{
                      textAlign: 'left',
                      paddingLeft: 20,
                      color: 'var(--text-secondary)',
                      margin: 0,
                      marginBottom: 24,
                    }}
                  >
                    <li>전체 온톨로지 목록 조회</li>
                    <li>온톨로지 상세 정보 확인</li>
                    <li>온톨로지별 통계 확인</li>
                  </ul>
                </Space>
              }
            />
            <Button
              type="primary"
              icon={<UnorderedListOutlined />}
              size="large"
              onClick={() => navigate('/list')}
              style={{
                width: '100%',
                background: 'var(--gradient-primary)',
                border: 'none',
                marginTop: 24,
              }}
            >
              목록 보기
            </Button>
          </Card>
        </Col>
        <Col xs={24} md={12} lg={8}>
          <Card
            hoverable
            style={{
              height: '100%',
              borderRadius: 16,
              boxShadow: 'var(--shadow-md)',
              border: '1px solid rgba(0, 0, 0, 0.05)',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              display: 'flex',
              flexDirection: 'column',
            }}
            bodyStyle={{
              padding: 24,
              display: 'flex',
              flexDirection: 'column',
              flex: 1,
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = 'var(--shadow-xl)';
              e.currentTarget.style.transform = 'translateY(-4px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = 'var(--shadow-md)';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            <div style={{ textAlign: 'center', marginBottom: 16 }}>
              <UploadOutlined
                style={{
                  fontSize: 48,
                  color: 'var(--secondary-color)',
                  marginBottom: 16,
                }}
              />
            </div>
            <Card.Meta
              style={{ flex: 1, display: 'flex', flexDirection: 'column' }}
              title={
                <Title level={4} style={{ textAlign: 'center', marginBottom: 12 }}>
                  데이터 업로드
                </Title>
              }
              description={
                <Space direction="vertical" style={{ width: '100%', flex: 1 }}>
                  <Paragraph style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                    데이터 파일을 업로드하고 온톨로지를 자동으로 구축합니다.
                  </Paragraph>
                  <ul
                    style={{
                      textAlign: 'left',
                      paddingLeft: 20,
                      color: 'var(--text-secondary)',
                      margin: 0,
                      marginBottom: 24,
                    }}
                  >
                    <li>CSV, JSON, Excel 파일 지원</li>
                    <li>자동 관계 추출</li>
                    <li>온톨로지 클래스 지정</li>
                  </ul>
                </Space>
              }
            />
            <Button
              type="primary"
              icon={<UploadOutlined />}
              size="large"
              onClick={() => navigate('/upload')}
              style={{
                width: '100%',
                background: 'var(--gradient-primary)',
                border: 'none',
                marginTop: 24,
              }}
            >
              업로드하기
            </Button>
          </Card>
        </Col>
        <Col xs={24} md={12} lg={8}>
          <Card
            hoverable
            style={{
              height: '100%',
              borderRadius: 16,
              boxShadow: 'var(--shadow-md)',
              border: '1px solid rgba(0, 0, 0, 0.05)',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              display: 'flex',
              flexDirection: 'column',
            }}
            bodyStyle={{
              padding: 24,
              display: 'flex',
              flexDirection: 'column',
              flex: 1,
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = 'var(--shadow-xl)';
              e.currentTarget.style.transform = 'translateY(-4px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = 'var(--shadow-md)';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            <div style={{ textAlign: 'center', marginBottom: 16 }}>
              <BarChartOutlined
                style={{
                  fontSize: 48,
                  color: 'var(--accent-color)',
                  marginBottom: 16,
                }}
              />
            </div>
            <Card.Meta
              style={{ flex: 1, display: 'flex', flexDirection: 'column' }}
              title={
                <Title level={4} style={{ textAlign: 'center', marginBottom: 12 }}>
                  온톨로지 시각화
                </Title>
              }
              description={
                <Space direction="vertical" style={{ width: '100%', flex: 1 }}>
                  <Paragraph style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                    통합된 온톨로지를 그래프 형태로 시각화합니다.
                  </Paragraph>
                  <ul
                    style={{
                      textAlign: 'left',
                      paddingLeft: 20,
                      color: 'var(--text-secondary)',
                      margin: 0,
                      marginBottom: 24,
                    }}
                  >
                    <li>인터랙티브 그래프</li>
                    <li>노드 및 엣지 탐색</li>
                    <li>전체 온톨로지 통합</li>
                  </ul>
                </Space>
              }
            />
            <Button
              type="primary"
              icon={<BarChartOutlined />}
              size="large"
              onClick={() => navigate('/visualize')}
              style={{
                width: '100%',
                background: 'var(--gradient-primary)',
                border: 'none',
                marginTop: 24,
              }}
            >
              시각화하기
            </Button>
          </Card>
        </Col>
      </Row>

      {/* 사용 방법 섹션 */}
      <Card
        style={{
          marginTop: 48,
          borderRadius: 16,
          boxShadow: 'var(--shadow-md)',
          border: '1px solid rgba(0, 0, 0, 0.05)',
        }}
      >
        <Title level={3} style={{ marginBottom: 32 }}>
          사용 방법
        </Title>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div
            style={{
              padding: 24,
              background: 'var(--gradient-card)',
              borderRadius: 12,
              border: '1px solid rgba(102, 126, 234, 0.2)',
            }}
          >
            <Title level={4} style={{ color: 'var(--primary-color)', marginBottom: 12 }}>
              1. 데이터 업로드
            </Title>
            <Paragraph style={{ color: 'var(--text-secondary)', margin: 0 }}>
              데이터 파일을 업로드하고 온톨로지 클래스를 지정하면, 시스템이 자동으로
              관계를 추출하고 온톨로지를 생성합니다.
            </Paragraph>
          </div>
          <div
            style={{
              padding: 24,
              background: 'var(--gradient-card)',
              borderRadius: 12,
              border: '1px solid rgba(102, 126, 234, 0.2)',
            }}
          >
            <Title level={4} style={{ color: 'var(--primary-color)', marginBottom: 12 }}>
              2. 결과 확인
            </Title>
            <Paragraph style={{ color: 'var(--text-secondary)', margin: 0 }}>
              매핑 결과는 테이블 형태로 표시되며, 생성된 RDF Graph는 Turtle 형식으로
              확인하고 다운로드할 수 있습니다.
            </Paragraph>
          </div>
          <div
            style={{
              padding: 24,
              background: 'var(--gradient-card)',
              borderRadius: 12,
              border: '1px solid rgba(102, 126, 234, 0.2)',
            }}
          >
            <Title level={4} style={{ color: 'var(--primary-color)', marginBottom: 12 }}>
              3. 온톨로지 조회
            </Title>
            <Paragraph style={{ color: 'var(--text-secondary)', margin: 0 }}>
              생성된 온톨로지의 ID를 입력하여 이전에 생성한 온톨로지를 조회할 수
              있습니다.
            </Paragraph>
          </div>
        </Space>
      </Card>
    </Layout>
  );
};

export default Home;

