/**
 * 로딩 스피너 컴포넌트
 * Ant Design Spin 컴포넌트를 사용한 로딩 표시
 */

import { Spin } from 'antd';

interface LoadingSpinnerProps {
  /** 로딩 메시지 */
  message?: string;
  /** 전체 화면 로딩 여부 */
  fullScreen?: boolean;
  /** 크기 */
  size?: 'small' | 'default' | 'large';
}

const LoadingSpinner = ({
  message = '로딩 중...',
  fullScreen = false,
  size = 'default',
}: LoadingSpinnerProps) => {
  if (fullScreen) {
    return (
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
        }}
      >
        <Spin size={size} tip={message} />
      </div>
    );
  }

  return <Spin size={size} tip={message} />;
};

export default LoadingSpinner;

