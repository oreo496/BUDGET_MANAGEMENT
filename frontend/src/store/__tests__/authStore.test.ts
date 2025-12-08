import { renderHook, act } from '@testing-library/react';
import { useAuthStore } from '../authStore';

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('Auth Store', () => {
  beforeEach(() => {
    localStorageMock.clear();
    // Reset store state
    useAuthStore.setState({
      user: null,
      token: null,
      isAuthenticated: false,
    });
  });

  it('initializes with empty state', () => {
    const { result } = renderHook(() => useAuthStore());
    
    expect(result.current.user).toBeNull();
    expect(result.current.token).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('logs in user and sets token', () => {
    const { result } = renderHook(() => useAuthStore());
    
    const user = {
      id: '123',
      email: 'test@example.com',
      firstName: 'Test',
      lastName: 'User',
    };
    
    act(() => {
      result.current.login('test-token', user);
    });
    
    expect(result.current.token).toBe('test-token');
    expect(result.current.user).toEqual(user);
    expect(result.current.isAuthenticated).toBe(true);
    expect(localStorage.getItem('token')).toBe('test-token');
  });

  it('logs out user and clears token', () => {
    const { result } = renderHook(() => useAuthStore());
    
    // First login
    act(() => {
      result.current.login('test-token', {
        id: '123',
        email: 'test@example.com',
        firstName: 'Test',
        lastName: 'User',
      });
    });
    
    // Then logout
    act(() => {
      result.current.logout();
    });
    
    expect(result.current.token).toBeNull();
    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
    expect(localStorage.getItem('token')).toBeNull();
  });
});

