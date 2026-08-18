// Mini Charts Component
// Compact sparkline charts for dashboard
// Shows trends without labels for clean look

import { LineChart, Line, AreaChart, Area, ResponsiveContainer } from 'recharts';

const MiniChart = ({ data, type = 'line', color = '#10b981', height = 60 }) => {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <span className="text-xs text-gray-400">No data</span>
      </div>
    );
  }

  const chartProps = {
    width: '100%',
    height,
    data,
    margin: { top: 5, right: 5, bottom: 5, left: 5 }
  };

  if (type === 'area') {
    return (
      <ResponsiveContainer {...chartProps}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id={`colorGradient-${color}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={color} stopOpacity={0.3} />
              <stop offset="95%" stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>
          <Area
            type="monotone"
            dataKey="value"
            stroke={color}
            strokeWidth={2}
            fill={`url(#colorGradient-${color})`}
            animationDuration={1000}
          />
        </AreaChart>
      </ResponsiveContainer>
    );
  }

  return (
    <ResponsiveContainer {...chartProps}>
      <LineChart data={data}>
        <Line
          type="monotone"
          dataKey="value"
          stroke={color}
          strokeWidth={2}
          dot={false}
          animationDuration={1000}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default MiniChart;
