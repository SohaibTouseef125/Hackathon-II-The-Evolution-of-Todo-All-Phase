'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/use-auth';
import { apiClient } from '@/lib/api';
import { Task } from '@/types';
import DashboardLayout from '@/components/dashboard-layout';
import PageHeader from '@/components/page-header';
import LoadingSpinner from '@/components/loading-spinner';

export default function CalendarPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    const fetchTasks = async () => {
      if (!user) {
        setLoading(false);
        return;
      }

      try {
        const tasks = await apiClient.getTasks();
        setTasks(tasks);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [user]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" label="Loading calendar..." />
      </div>
    );
  }

  // Group tasks by date
  const tasksByDate: Record<string, Task[]> = {};
  tasks.forEach(task => {
    if (task.due_date) {
      // Assuming ISO string or formatted date
      const date = new Date(task.due_date).toLocaleDateString();
      if (!tasksByDate[date]) {
        tasksByDate[date] = [];
      }
      tasksByDate[date].push(task);
    }
  });

  return (
    <DashboardLayout>
      <PageHeader
        title="Calendar"
        subtitle="View your upcoming tasks by date"
      />

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Upcoming Deadlines</h3>
        </div>
        <ul className="divide-y divide-gray-200">
          {Object.keys(tasksByDate).length === 0 ? (
             <li className="px-4 py-4 sm:px-6 text-center text-gray-500">
               No tasks with due dates found.
             </li>
          ) : (
            Object.keys(tasksByDate).map(date => (
              <li key={date} className="px-4 py-4 sm:px-6">
                <div className="text-sm font-bold text-gray-900 mb-2">{date}</div>
                <ul className="space-y-2">
                  {tasksByDate[date].map(task => (
                    <li key={task.id} className="flex justify-between items-center bg-gray-50 p-2 rounded">
                      <span className={task.completed ? 'line-through text-gray-500' : 'text-gray-700'}>
                        {task.title}
                      </span>
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                        ${task.priority === 'high' ? 'bg-red-100 text-red-800' :
                          task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'}`}>
                        {task.priority || 'medium'}
                      </span>
                    </li>
                  ))}
                </ul>
              </li>
            ))
          )}
        </ul>
      </div>
    </DashboardLayout>
  );
}
