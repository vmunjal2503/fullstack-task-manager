/**
 * API client for the Task Manager backend.
 */

import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

// Attach auth token
api.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ── Projects ──
export const projectsAPI = {
  list: () => api.get("/api/projects"),
  create: (data: { name: string; description?: string }) => api.post("/api/projects", data),
  getBoard: (id: string) => api.get(`/api/projects/${id}/board`),
};

// ── Tasks ──
export const tasksAPI = {
  list: (filters?: Record<string, string>) => api.get("/api/tasks", { params: filters }),
  create: (data: { title: string; project_id: string; column_id: string; priority?: string }) =>
    api.post("/api/tasks", data),
  update: (id: string, data: Record<string, unknown>) => api.patch(`/api/tasks/${id}`, data),
  move: (id: string, data: { column_id: string; position: number }) =>
    api.patch(`/api/tasks/${id}/move`, data),
  delete: (id: string) => api.delete(`/api/tasks/${id}`),
};

// ── Comments ──
export const commentsAPI = {
  list: (taskId: string) => api.get(`/api/tasks/${taskId}/comments`),
  add: (taskId: string, data: { content: string; mentions?: string[] }) =>
    api.post(`/api/tasks/${taskId}/comments`, data),
};

// ── Search ──
export const searchAPI = {
  search: (query: string, projectId?: string) =>
    api.get("/api/search", { params: { q: query, project_id: projectId } }),
};

export default api;
