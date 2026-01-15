'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, AreaChart, Area } from 'recharts';

interface TaskAnalyticsProps {
  tasks: Array<{
    id: string;
    title: string;
    completed: boolean;
    priority: 'low' | 'medium' | 'high';
    createdAt: string;
    updatedAt: string;
  }>;
  className?: string;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

export default function TaskAnalytics({ tasks, className = '' }: TaskAnalyticsProps) {
  // Prepare data for charts
  const statusData = [
    { name: 'Completed', value: tasks.filter(t => t.completed).length },
    { name: 'Pending', value: tasks.filter(t => !t.completed).length },
  ];

  const priorityData = [
    { name: 'High', value: tasks.filter(t => t.priority === 'high').length },
    { name: 'Medium', value: tasks.filter(t => t.priority === 'medium').length },
    { name: 'Low', value: tasks.filter(t => t.priority === 'low').length },
  ];

  // Group tasks by creation date for trend analysis
  const taskTrendData = tasks.reduce((acc: Array<{date: string, tasks: number}>, task) => {
    const date = new Date(task.createdAt).toLocaleDateString();
    const existing = acc.find(d => d.date === date);

    if (existing) {
      existing.tasks += 1;
    } else {
      acc.push({ date, tasks: 1 });
    }

    return acc;
  }, []).sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  return (
    <div className={`grid grid-cols-1 lg:grid-cols-3 gap-6 ${className}`}>
      {/* Status Distribution */}
      <div className="lg:col-span-1">
        <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Task Status</h3>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={statusData}
              cx="50%"
              cy="50%"
              labelLine={false}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
              label={({ name, percent }: { name: string, percent: number }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            >
              {statusData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Priority Distribution */}
      <div className="lg:col-span-1">
        <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Task Priority</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart
            data={priorityData}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="name" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1F2937',
                borderColor: '#374151',
                borderRadius: '0.5rem',
                color: '#F9FAFB'
              }}
            />
            <Legend />
            <Bar dataKey="value" fill="#3b82f6" name="Tasks Count" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Task Creation Trend */}
      <div className="lg:col-span-1">
        <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Task Creation Trend</h3>
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart
            data={taskTrendData}
            margin={{
              top: 10,
              right: 30,
              left: 0,
              bottom: 0,
            }}
          >
            <defs>
              <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="date" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1F2937',
                borderColor: '#374151',
                borderRadius: '0.5rem',
                color: '#F9FAFB'
              }}
            />
            <Area type="monotone" dataKey="tasks" stroke="#3b82f6" fillOpacity={1} fill="url(#colorUv)" name="Tasks Created" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}