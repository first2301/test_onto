/**
 * 헤더 컴포넌트
 * 네비게이션 메뉴 포함
 */

import { Menu, Typography } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import { ApartmentOutlined } from '@ant-design/icons';

const { Text } = Typography;

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      label: '홈',
    },
    {
      key: '/upload',
      label: '데이터 업로드',
    },
    {
      key: '/list',
      label: '온톨로지 목록',
    },
    {
      key: '/visualize',
      label: '온톨로지 시각화',
    },
    {
      key: '/view',
      label: '온톨로지 조회',
    },
  ];

  const handleMenuClick = ({ key }: { key: string }) => {
    navigate(key);
  };

  return (
    <div
      style={{
        background: 'var(--gradient-primary)',
        boxShadow: 'var(--shadow-lg)',
        marginBottom: 24,
        position: 'sticky',
        top: 0,
        zIndex: 100,
      }}
    >
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '0 24px' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '20px 0',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              cursor: 'pointer',
            }}
            onClick={() => navigate('/')}
          >
            <ApartmentOutlined
              style={{
                fontSize: 32,
                color: '#FFFFFF',
                filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))',
              }}
            />
            <Text
              style={{
                fontSize: 24,
                fontWeight: 'bold',
                color: '#FFFFFF',
                margin: 0,
                background: 'linear-gradient(135deg, #FFFFFF 0%, #E0E7FF 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
                textShadow: '0 2px 4px rgba(0,0,0,0.1)',
              }}
            >
              OntoMap
            </Text>
          </div>
          <Menu
            mode="horizontal"
            selectedKeys={[location.pathname]}
            items={menuItems}
            onClick={handleMenuClick}
            style={{
              borderBottom: 'none',
              background: 'transparent',
              color: '#FFFFFF',
              flex: 1,
              justifyContent: 'flex-end',
            }}
            theme="dark"
          />
        </div>
      </div>
    </div>
  );
};

export default Header;

