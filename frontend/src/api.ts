import axios from 'axios';

// Auto-detect API URL based on current hostname
const getApiBaseUrl = () => {
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // If accessing from remote IP, use the same hostname with backend port
  const hostname = window.location.hostname;
  if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
    return `http://${hostname}:5001/api`;
  }
  
  // Default to localhost for local development
  return 'http://localhost:5001/api';
};

const API_BASE_URL = getApiBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
});

export interface SummaryStats {
  totalRetailOrders: number;
  totalRetailSpending: number;
  totalDigitalOrders: number;
  totalDigitalSpending: number;
  totalOrders: number;
  totalSpending: number;
  dateRange: { start: string | null; end: string | null };
  averageOrderValue: number;
}

export interface SpendingOverTime {
  labels: string[];
  values: number[];
  orderCounts: number[];
}

export interface TopProduct {
  name: string;
  quantity: number;
  spending: number;
  orders: number;
}

export interface Category {
  name: string;
  spending: number;
}

export interface PaymentMethod {
  method: string;
  spending: number;
}

export interface ReturnStats {
  totalReturns: number;
  returnRate: number;
  returnsOverTime: { labels: string[]; values: number[] };
}

export interface DigitalVsRetail {
  retail: { orders: number; spending: number };
  digital: { orders: number; spending: number };
}

export const getSummary = async (): Promise<SummaryStats> => {
  const response = await api.get('/stats/summary');
  return response.data;
};

export const getSpendingOverTime = async (period: 'monthly' | 'yearly'): Promise<SpendingOverTime> => {
  const response = await api.get('/stats/spending-over-time', { params: { period } });
  return response.data;
};

export const getTopProducts = async (limit: number = 20, by: 'quantity' | 'spending' = 'quantity'): Promise<{ products: TopProduct[] }> => {
  const response = await api.get('/stats/top-products', { params: { limit, by } });
  return response.data;
};

export const getCategories = async (): Promise<{ categories: Category[] }> => {
  const response = await api.get('/stats/categories');
  return response.data;
};

export const getPaymentMethods = async (): Promise<{ paymentMethods: PaymentMethod[] }> => {
  const response = await api.get('/stats/payment-methods');
  return response.data;
};

export const getReturns = async (): Promise<ReturnStats> => {
  const response = await api.get('/stats/returns');
  return response.data;
};

export const getDigitalVsRetail = async (): Promise<DigitalVsRetail> => {
  const response = await api.get('/stats/digital-vs-retail');
  return response.data;
};
