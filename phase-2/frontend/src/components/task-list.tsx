'use client';

import { Task } from '@/types';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (id: string, completed: boolean) => void;
  onDelete: (id: string) => void;
}

export default function TaskList({ tasks, onToggleComplete, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No tasks yet. Add your first task!</p>
      </div>
    );
  }

  return (
    <ul className="space-y-4">
      {tasks.map((task) => (
        <li
          key={task.id}
          className="bg-white shadow rounded-lg p-4 flex justify-between items-center hover:shadow-md transition-shadow"
        >
          <div className="flex items-center">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggleComplete(task.id, task.completed)}
              className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
            />
            <span className={`ml-3 ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </span>
            {task.description && (
              <span className="ml-2 text-sm text-gray-500">- {task.description}</span>
            )}
          </div>
          <button
            onClick={() => onDelete(task.id)}
            className="ml-4 px-3 py-1 text-sm text-red-600 hover:text-red-900 hover:bg-red-50 rounded"
          >
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}