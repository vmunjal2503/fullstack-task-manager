/**
 * WebSocket hook for real-time Kanban board updates.
 * Automatically reconnects on disconnect.
 */

import { useEffect, useRef, useCallback, useState } from "react";

interface WSMessage {
  event: string;
  payload: Record<string, unknown>;
  sender: string;
}

export function useWebSocket(projectId: string, onMessage: (msg: WSMessage) => void) {
  const wsRef = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const reconnectTimeout = useRef<NodeJS.Timeout>();

  const connect = useCallback(() => {
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";
    const ws = new WebSocket(`${wsUrl}/ws/${projectId}`);

    ws.onopen = () => {
      setConnected(true);
      console.log(`[WS] Connected to board ${projectId}`);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (err) {
        console.error("[WS] Failed to parse message:", err);
      }
    };

    ws.onclose = () => {
      setConnected(false);
      console.log("[WS] Disconnected. Reconnecting in 3s...");
      reconnectTimeout.current = setTimeout(connect, 3000);
    };

    ws.onerror = (err) => {
      console.error("[WS] Error:", err);
      ws.close();
    };

    wsRef.current = ws;
  }, [projectId, onMessage]);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      wsRef.current?.close();
    };
  }, [connect]);

  const send = useCallback((event: string, payload: Record<string, unknown>) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ event, payload, user_id: "current_user" }));
    }
  }, []);

  return { connected, send };
}
