'use client';

import { useState } from 'react';
import { Task } from '@/types';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (id: string, completed: boolean) => void;
  onDelete: (id: string) => void;
  onEdit?: (task: Task) => void;
}

export default function EnhancedTaskList({ tasks, onToggleComplete, onDelete, onEdit }: TaskListProps) {
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [sortBy, setSortBy] = useState<'date' | 'priority' | 'title'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  // Sort tasks based on selected criteria
  const sortedTasks = [...filteredTasks].sort((a, b) => {
    let comparison = 0;

    if (sortBy === 'date') {
      // Sort by creation date
      comparison = new Date(a.created_at || '').getTime() - new Date(b.created_at || '').getTime();
    } else if (sortBy === 'title') {
      comparison = a.title.localeCompare(b.title);
    }
    // For priority, we would need to add priority field to Task type

    return sortOrder === 'asc' ? comparison : -comparison;
  });

  if (sortedTasks.length === 0) {
    return (
      <div className="text-center py-12">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
        <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filters and Sorting Controls */}
      <div className="flex flex-col sm:flex-row gap-4 justify-between items-center">
        <div className="flex space-x-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 text-sm rounded-full ${
              filter === 'all'
                ? 'bg-indigo-100 text-indigo-800'
                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('active')}
            className={`px-3 py-1 text-sm rounded-full ${
              filter === 'active'
                ? 'bg-indigo-100 text-indigo-800'
                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
            }`}
          >
            Active
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-3 py-1 text-sm rounded-full ${
              filter === 'completed'
                ? 'bg-indigo-100 text-indigo-800'
                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
            }`}
          >
            Completed
          </button>
        </div>

        <div className="flex space-x-2">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'date' | 'priority' | 'title')}
            className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            <option value="date">Sort by Date</option>
            <option value="title">Sort by Title</option>
          </select>

          <button
            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            className="px-3 py-2 text-sm bg-gray-100 text-gray-800 rounded-md hover:bg-gray-200"
          >
            {sortOrder === 'asc' ? '↑' : '↓'}
          </button>
        </div>
      </div>

      {/* Task List */}
      <ul className="space-y-3">
        {sortedTasks.map((task) => (
          <li
            key={task.id}
            className="bg-white shadow rounded-lg p-4 flex justify-between items-start group hover:shadow-md transition-shadow"
          >
            <div className="flex items-start space-x-3 flex-1 min-w-0">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => onToggleComplete(task.id, task.completed)}
                className="h-5 w-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 mt-0.5"
              />
              <div className="min-w-0 flex-1">
                <p className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                  {task.title}
                </p>
                {task.description && (
                  <p className={`text-sm ${task.completed ? 'text-gray-400' : 'text-gray-500'} mt-1`}>
                    {task.description}
                  </p>
                )}
                {task.created_at && (
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(task.created_at).toLocaleDateString()}
                  </p>
                )}
              </div>
            </div>

            <div className="flex space-x-2 ml-4">
              {onEdit && (
                <button
                  onClick={() => onEdit(task)}
                  className="text-indigo-600 hover:text-indigo-900 text-sm font-medium"
                >
                  Edit
                </button>
              )}
              <button
                onClick={() => onDelete(task.id)}
                className="text-red-600 hover:text-red-900 text-sm font-medium"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}