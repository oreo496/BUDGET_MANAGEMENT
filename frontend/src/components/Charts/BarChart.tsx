'use client';

interface BarChartProps {
  data: { label: string; value: number; color?: string }[];
  height?: number;
  showValues?: boolean;
}

export default function BarChart({ data, height = 200, showValues = false }: BarChartProps) {
  const maxValue = Math.max(...data.map(d => d.value));

  return (
    <div className="w-full" style={{ height: `${height}px` }}>
      <div className="flex items-end justify-between h-full gap-2">
        {data.map((item, index) => (
          <div key={index} className="flex-1 flex flex-col items-center">
            {showValues && (
              <div className="text-sm font-semibold mb-1">{item.value}</div>
            )}
            <div
              className="w-full rounded-t transition-all hover:opacity-80"
              style={{
                height: `${(item.value / maxValue) * 100}%`,
                backgroundColor: item.color || '#3b82f6',
                minHeight: '4px',
              }}
            />
            <div className="text-xs text-gray-600 mt-2">{item.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

