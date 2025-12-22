"use client";

import { FormEvent, useEffect, useState } from "react";
import MainLayout from "@/components/Layout/MainLayout";
import api from "@/lib/api";

interface Goal {
  id: string;
  title: string;
  target_amount: string;
  current_amount: string;
  deadline?: string | null;
  progress_percentage: number;
  created_at: string;
}

interface Insight {
  progress_percentage: number;
  monthly_surplus: number;
  required_monthly: number;
  risk: boolean;
  notification_created: boolean;
  days_left: number;
  loading?: boolean;
}

export default function GoalsPage() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [insights, setInsights] = useState<Record<string, Insight>>({});
  const [title, setTitle] = useState("");
  const [targetAmount, setTargetAmount] = useState("");
  const [currentAmount, setCurrentAmount] = useState("");
  const [deadline, setDeadline] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchGoals = async () => {
    setError(null);
    try {
      const res = await api.get("/goals/");
      const data = Array.isArray(res.data) ? res.data : res.data?.results || [];
      setGoals(data);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          err?.response?.data?.error ||
          "Unable to load goals. Make sure you are signed in."
      );
    }
  };

  useEffect(() => {
    fetchGoals();
  }, []);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await api.post("/goals/", {
        title,
        target_amount: parseFloat(targetAmount),
        current_amount: currentAmount ? parseFloat(currentAmount) : 0,
        deadline: deadline || null,
      });
      setTitle("");
      setTargetAmount("");
      setCurrentAmount("");
      setDeadline("");
      await fetchGoals();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to create goal");
    } finally {
      setLoading(false);
    }
  };

  const runInsight = async (goalId: string) => {
    setError(null);
    if (typeof window !== "undefined" && !localStorage.getItem("token")) {
      setError("Please sign in to fetch goal insights.");
      return;
    }

    setInsights((prev) => ({ ...prev, [goalId]: { ...(prev[goalId] || {} as Insight), loading: true } }));
    try {
      const res = await api.post(`/goals/${goalId}/insights/`);
      setInsights((prev) => ({ ...prev, [goalId]: res.data }));
    } catch (err: any) {
      const detail =
        err?.response?.data?.detail ||
        err?.response?.data?.error ||
        err?.message ||
        "Unable to fetch insight";
      setError(detail);
    } finally {
      setInsights((prev) => ({ ...prev, [goalId]: { ...(prev[goalId] || {} as Insight), loading: false } }));
    }
  };

  return (
    <MainLayout title="Goals">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">Goals</h1>
              <p className="text-sm text-gray-600">Track savings goals and request AI insights when you are off-track.</p>
            </div>
            <button
              onClick={fetchGoals}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg"
            >
              Refresh
            </button>
          </div>

          {error && <div className="bg-red-50 border border-red-200 text-red-700 p-3 rounded-lg">{error}</div>}

          {goals.length === 0 ? (
            <div className="bg-white border border-dashed border-gray-200 rounded-lg p-8 text-center text-gray-600">
              No goals yet. Create one to get started.
            </div>
          ) : (
            <div className="space-y-4">
              {goals.map((goal) => {
                const insight = insights[goal.id];
                const progress = Math.min(goal.progress_percentage ?? 0, 100);
                return (
                  <div key={goal.id} className="bg-white rounded-lg shadow-sm border border-gray-100 p-5">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{goal.title}</h3>
                        <p className="text-sm text-gray-600">
                          Target ${goal.target_amount} • Current ${goal.current_amount}
                          {goal.deadline ? ` • Deadline ${new Date(goal.deadline).toLocaleDateString()}` : ""}
                        </p>
                      </div>
                      <button
                        onClick={() => runInsight(goal.id)}
                        className="px-3 py-2 text-sm bg-indigo-600 text-white rounded-lg"
                      >
                        Get AI Insight
                      </button>
                    </div>
                    <div className="mt-3">
                      <div className="flex justify-between text-xs text-gray-600 mb-1">
                        <span>{Number(progress || 0).toFixed(1)}% complete</span>
                        {goal.deadline && <span>Due {new Date(goal.deadline).toLocaleDateString()}</span>}
                      </div>
                      <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-blue-600"
                          style={{ width: `${progress}%` }}
                        />
                      </div>
                    </div>
                    {insight && !insight.loading && (
                      <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                        <div className="p-3 bg-gray-50 rounded-lg">
                          <div className="text-gray-500">Monthly surplus</div>
                          <div className="font-semibold">${Number(insight.monthly_surplus ?? 0).toFixed(2)}</div>
                        </div>
                        <div className="p-3 bg-gray-50 rounded-lg">
                          <div className="text-gray-500">Needed monthly</div>
                          <div className={`font-semibold ${insight.risk ? "text-red-600" : "text-green-600"}`}>
                            ${Number(insight.required_monthly ?? 0).toFixed(2)}
                          </div>
                        </div>
                        <div className="p-3 bg-gray-50 rounded-lg">
                          <div className="text-gray-500">Days left</div>
                          <div className="font-semibold">{insight.days_left}</div>
                        </div>
                        <div className="p-3 bg-gray-50 rounded-lg">
                          <div className="text-gray-500">Risk status</div>
                          <div className={`font-semibold ${insight.risk ? "text-red-600" : "text-green-600"}`}>
                            {insight.risk ? "At risk" : "On track"}
                          </div>
                        </div>
                        {insight.notification_created && (
                          <div className="col-span-2 text-sm text-blue-700 bg-blue-50 border border-blue-200 rounded-lg p-3">
                            Notification sent to your inbox for this goal.
                          </div>
                        )}
                      </div>
                    )}
                    {insight?.loading && (
                      <div className="mt-3 text-sm text-gray-600">Calculating insight...</div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-5">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">Create a goal</h2>
          <form className="space-y-4" onSubmit={handleCreate}>
            <div>
              <label className="block text-sm text-gray-700">Title</label>
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full border px-3 py-2 rounded"
                required
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm text-gray-700">Target amount</label>
                <input
                  type="number"
                  step="0.01"
                  value={targetAmount}
                  onChange={(e) => setTargetAmount(e.target.value)}
                  className="w-full border px-3 py-2 rounded"
                  required
                />
              </div>
              <div>
                <label className="block text-sm text-gray-700">Current amount</label>
                <input
                  type="number"
                  step="0.01"
                  value={currentAmount}
                  onChange={(e) => setCurrentAmount(e.target.value)}
                  className="w-full border px-3 py-2 rounded"
                  placeholder="0"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm text-gray-700">Deadline (optional)</label>
              <input
                type="date"
                value={deadline}
                onChange={(e) => setDeadline(e.target.value)}
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg disabled:opacity-60"
            >
              {loading ? "Saving..." : "Create goal"}
            </button>
          </form>
        </div>
      </div>
    </MainLayout>
  );
}
