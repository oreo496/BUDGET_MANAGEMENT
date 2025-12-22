"use client";

import { useEffect, useState } from "react";
import MainLayout from "@/components/Layout/MainLayout";
import api from "@/lib/api";

interface AlertItem {
  id: string;
  message: string;
  type: string;
  created_at: string;
}

const typeStyles: Record<string, string> = {
  LOAN_REMINDER: "bg-amber-50 border-amber-200 text-amber-800",
  GOAL_RISK: "bg-red-50 border-red-200 text-red-800",
  GOAL_RECOMMENDATION: "bg-blue-50 border-blue-200 text-blue-800",
  FRAUD: "bg-orange-50 border-orange-200 text-orange-800",
  SPENDING_PATTERN: "bg-purple-50 border-purple-200 text-purple-800",
  BUDGET_ALERT: "bg-emerald-50 border-emerald-200 text-emerald-800",
};

export default function NotificationsPage() {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAlerts = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get("/ai-alerts/");
      const data = Array.isArray(res.data) ? res.data : res.data?.results || [];
      setAlerts(data);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          err?.response?.data?.error ||
          "Unable to load notifications. Please ensure you are signed in."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  return (
    <MainLayout title="Notifications">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Notifications</h1>
            <p className="text-sm text-gray-600">Alerts from loans, goals, AI insights, and security.</p>
          </div>
          <button
            onClick={fetchAlerts}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-60"
          >
            {loading ? "Refreshing..." : "Refresh"}
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">{error}</div>
        )}

        {alerts.length === 0 && !loading ? (
          <div className="bg-white border border-dashed border-gray-200 rounded-lg p-8 text-center text-gray-600">
            No notifications yet.
          </div>
        ) : (
          <div className="space-y-3">
            {alerts.map((alert) => {
              const style = typeStyles[alert.type] || "bg-gray-50 border-gray-200 text-gray-800";
              return (
                <div
                  key={alert.id}
                  className={`border rounded-lg p-4 flex items-start gap-3 ${style}`}
                >
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-semibold tracking-wide">{alert.type.replace(/_/g, " ")}</span>
                      <span className="text-xs text-gray-600">
                        {new Date(alert.created_at).toLocaleString()}
                      </span>
                    </div>
                    <p className="mt-1 text-sm leading-relaxed">{alert.message}</p>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </MainLayout>
  );
}
