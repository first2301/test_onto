/**
 * 레이아웃 컴포넌트
 * 전체 페이지 레이아웃 구조
 */

import { ReactNode } from 'react';
import Header from './Header';

interface LayoutProps {
  /** 자식 컴포넌트 */
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'var(--bg-secondary)',
        position: 'relative',
      }}
    >
      <Header />
      <div
        style={{
          maxWidth: 1200,
          margin: '0 auto',
          padding: '24px 24px 48px',
        }}
        className="fade-in"
      >
        {children}
      </div>
    </div>
  );
};

export default Layout;

