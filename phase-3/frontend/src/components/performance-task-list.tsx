'use client';

import { memo, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { CheckCircle, Circle, AlertCircle, Pencil, Trash2 } from 'lucide-react';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  createdAt: string;
}

interface PerformanceTaskListProps {
  tasks: Task[];
  onToggleComplete: (id: string, completed: boolean) => void;
  onDelete: (id: string) => void;
  onEdit: (task: Task) => void;
}

const TaskItem = memo(({ task, onToggleComplete, onDelete, onEdit }: {
  task: Task;
  onToggleComplete: (id: string, completed: boolean) => void;
  onDelete: (id: string) => void;
  onEdit: (task: Task) => void;
}) => {
  const handleToggle = useCallback(() => {
    onToggleComplete(task.id, task.completed);
  }, [task, onToggleComplete]);

  const handleDelete = useCallback(() => {
    onDelete(task.id);
  }, [task, onDelete]);

  const handleEdit = useCallback(() => {
    onEdit(task);
  }, [task, onEdit]);

  const priorityColors = {
    low: 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30',
    medium: 'text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30',
    high: 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      layout
      className="group"
    >
      <Card className="p-4 hover:shadow-md transition-shadow">
        <div className="flex items-start gap-3">
          <button
            onClick={handleToggle}
            className="mt-0.5 flex-shrink-0"
            aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
          >
            {task.completed ? (
              <CheckCircle className="w-5 h-5 text-green-500" />
            ) : (
              <Circle className="w-5 h-5 text-neutral-400 dark:text-neutral-500" />
            )}
          </button>

          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <h3 className={`font-medium truncate ${task.completed ? 'line-through text-neutral-500 dark:text-neutral-400' : 'text-neutral-900 dark:text-white'}`}>
                {task.title}
              </h3>
              <span className={`text-xs px-2 py-0.5 rounded-full ${priorityColors[task.priority]}`}>
                {task.priority}
              </span>
            </div>

            {task.description && (
              <p className="text-sm text-neutral-600 dark:text-neutral-300 truncate">
                {task.description}
              </p>
            )}
          </div>

          <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleEdit}
              className="h-8 w-8 p-0"
              aria-label="Edit task"
            >
              <Pencil className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleDelete}
              className="h-8 w-8 p-0 text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
              aria-label="Delete task"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </Card>
    </motion.div>
  );
});

TaskItem.displayName = 'TaskItem';

const PerformanceTaskList = ({ tasks, onToggleComplete, onDelete, onEdit }: PerformanceTaskListProps) => {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-neutral-500 dark:text-neutral-400">No tasks found</p>
      </div>
    );
  }

  return (
    <motion.div layout className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </motion.div>
  );
};

PerformanceTaskList.displayName = 'PerformanceTaskList';

export default PerformanceTaskList;