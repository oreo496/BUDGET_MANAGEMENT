/**
 * Observer Pattern hooks for React frontend
 * Provides real-time update capabilities using polling
 */

import { useEffect, useState, useCallback } from 'react';
import api from '@/lib/api';

/**
 * Custom hook for observing AI alerts in real-time
 */
export function useAlertObserver(pollingInterval: number = 30000) {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [unreadCount, setUnreadCount] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchAlerts = useCallback(async () => {
    try {
      const response = await api.get('/ai-alerts/');
      const data = Array.isArray(response.data) ? response.data : response.data.results || [];
      setAlerts(data);
      setUnreadCount(data.length);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching alerts:', error);
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAlerts();
    
    // Set up polling
    const interval = setInterval(fetchAlerts, pollingInterval);
    
    return () => clearInterval(interval);
  }, [fetchAlerts, pollingInterval]);

  return { alerts, unreadCount, loading, refresh: fetchAlerts };
}

/**
 * Custom hook for observing budget status
 */
export function useBudgetObserver(pollingInterval: number = 60000) {
  const [budgets, setBudgets] = useState<any[]>([]);
  const [exceededBudgets, setExceededBudgets] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchBudgets = useCallback(async () => {
    try {
      const response = await api.get('/budgets/');
      const data = Array.isArray(response.data) ? response.data : response.data.results || [];
      setBudgets(data);
      
      // Filter exceeded budgets (you'd need backend to provide spending info)
      // For now, this is a placeholder
      setExceededBudgets(data.filter((b: any) => b.is_exceeded));
      setLoading(false);
    } catch (error) {
      console.error('Error fetching budgets:', error);
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchBudgets();
    
    const interval = setInterval(fetchBudgets, pollingInterval);
    
    return () => clearInterval(interval);
  }, [fetchBudgets, pollingInterval]);

  return { budgets, exceededBudgets, loading, refresh: fetchBudgets };
}

/**
 * Custom hook for observing transaction changes
 */
export function useTransactionObserver(pollingInterval: number = 30000) {
  const [transactions, setTransactions] = useState<any[]>([]);
  const [newTransactions, setNewTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchTransactions = useCallback(async () => {
    try {
      const response = await api.get('/transactions/');
      const data = Array.isArray(response.data) ? response.data : response.data.results || [];
      
      // Detect new transactions (compare with previous state)
      if (transactions.length > 0) {
        const existingIds = new Set(transactions.map((t: any) => t.id));
        const newOnes = data.filter((t: any) => !existingIds.has(t.id));
        if (newOnes.length > 0) {
          setNewTransactions(newOnes);
        }
      }
      
      setTransactions(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching transactions:', error);
      setLoading(false);
    }
  }, [transactions]);

  useEffect(() => {
    fetchTransactions();
    
    const interval = setInterval(fetchTransactions, pollingInterval);
    
    return () => clearInterval(interval);
  }, [pollingInterval]); // Only depend on interval, not fetchTransactions

  return { transactions, newTransactions, loading, refresh: fetchTransactions };
}

/**
 * Custom hook for observing goal progress
 */
export function useGoalObserver(pollingInterval: number = 60000) {
  const [goals, setGoals] = useState<any[]>([]);
  const [achievedGoals, setAchievedGoals] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchGoals = useCallback(async () => {
    try {
      const response = await api.get('/goals/');
      const data = Array.isArray(response.data) ? response.data : response.data.results || [];
      setGoals(data);
      
      // Detect newly achieved goals (progress >= 100%)
      const achieved = data.filter((g: any) => {
        const progress = (g.current_amount / g.target_amount) * 100;
        return progress >= 100;
      });
      setAchievedGoals(achieved);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching goals:', error);
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchGoals();
    
    const interval = setInterval(fetchGoals, pollingInterval);
    
    return () => clearInterval(interval);
  }, [fetchGoals, pollingInterval]);

  return { goals, achievedGoals, loading, refresh: fetchGoals };
}

/**
 * Event emitter for client-side events
 */
type EventCallback = (data: any) => void;

class EventEmitter {
  private events: Map<string, EventCallback[]>;

  constructor() {
    this.events = new Map();
  }

  on(event: string, callback: EventCallback) {
    if (!this.events.has(event)) {
      this.events.set(event, []);
    }
    this.events.get(event)?.push(callback);
  }

  off(event: string, callback: EventCallback) {
    const callbacks = this.events.get(event);
    if (callbacks) {
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  emit(event: string, data: any) {
    const callbacks = this.events.get(event);
    if (callbacks) {
      callbacks.forEach(callback => callback(data));
    }
  }
}

export const appEvents = new EventEmitter();

/**
 * Hook to listen to custom app events
 */
export function useEventListener(event: string, callback: EventCallback) {
  useEffect(() => {
    appEvents.on(event, callback);
    
    return () => {
      appEvents.off(event, callback);
    };
  }, [event, callback]);
}
