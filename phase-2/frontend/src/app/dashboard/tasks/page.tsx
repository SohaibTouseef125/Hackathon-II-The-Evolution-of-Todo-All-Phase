'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { apiClient } from '@/lib/api';
import { Task, TaskCreateData } from '@/types';
import DashboardLayout from '@/components/dashboard-layout';
import EnhancedTaskForm from '@/components/enhanced-task-form';
import EnhancedTaskList from '@/components/enhanced-task-list';
import Modal from '@/components/modal';
import PageHeader from '@/components/page-header';
import Notification from '@/components/notification';
import LoadingSpinner from '@/components/loading-spinner';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showNotification, setShowNotification] = useState(false);
  const [notificationType, setNotificationType] = useState<'success' | 'error' | 'warning' | 'info'>('info');
  const [notificationMessage, setNotificationMessage] = useState('');
  const router = useRouter();
  const { user, logout } = useAuth();

  // Fetch tasks when component mounts
  useEffect(() => {
    const fetchTasks = async () => {
      if (!user) {
        setLoading(false);
        return;
      }

      try {
        const tasks = await apiClient.getTasks();
        setTasks(tasks);
      } catch (err: any) {
        showNotificationMessage('error', err.message || 'Error fetching tasks');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [user]);

  const showNotificationMessage = (type: 'success' | 'error' | 'warning' | 'info', message: string) => {
    setNotificationType(type);
    setNotificationMessage(message);
    setShowNotification(true);
  };

  const handleAddTask = async (taskData: TaskCreateData) => {
    if (!user) return;

    try {
      const createdTask = await apiClient.createTask(taskData);
      setTasks([createdTask, ...tasks]);
      showNotificationMessage('success', 'Task created successfully!');
    } catch (err: any) {
      showNotificationMessage('error', err.message || 'Error creating task');
      console.error(err);
    }
  };

  const handleUpdateTask = async (taskData: TaskCreateData) => {
    if (!editingTask || !user) return;

    try {
      const updatedTask = await apiClient.updateTask(editingTask.id, taskData);
      setTasks(tasks.map(task => task.id === editingTask.id ? updatedTask : task));
      setEditingTask(null);
      showNotificationMessage('success', 'Task updated successfully!');
    } catch (err: any) {
      showNotificationMessage('error', err.message || 'Error updating task');
      console.error(err);
    }
  };

  const handleToggleComplete = async (taskId: string, completed: boolean) => {
    if (!user) return;

    try {
      const updatedTask = await apiClient.toggleTaskCompletion(taskId, !completed);
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
      showNotificationMessage('success', completed ? 'Task marked as incomplete' : 'Task marked as complete');
    } catch (err: any) {
      showNotificationMessage('error', err.message || 'Error updating task');
      console.error(err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!user) return;

    if (!confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
      return;
    }

    try {
      await apiClient.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
      showNotificationMessage('success', 'Task deleted successfully!');
    } catch (err: any) {
      showNotificationMessage('error', err.message || 'Error deleting task');
      console.error(err);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" label="Loading your tasks..." />
      </div>
    );
  }

  return (
    <DashboardLayout>
      {showNotification && (
        <Notification
          type={notificationType}
          message={notificationMessage}
          onClose={() => setShowNotification(false)}
        />
      )}

      <PageHeader
        title="All Tasks"
        subtitle="Manage all your tasks in one place"
        actions={
          <button
            type="button"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            + New Task
          </button>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Add New Task</h2>
            <EnhancedTaskForm
              onSubmit={handleAddTask}
              submitButtonText="Create Task"
            />
          </div>
        </div>

        <div className="lg:col-span-2">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Your Tasks</h2>
            <EnhancedTaskList
              tasks={tasks}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDeleteTask}
              onEdit={handleEditTask}
            />
          </div>
        </div>
      </div>

      {/* Edit Task Modal */}
      {editingTask && (
        <Modal
          isOpen={!!editingTask}
          onClose={() => setEditingTask(null)}
          title="Edit Task"
        >
          <EnhancedTaskForm
            onSubmit={handleUpdateTask}
            initialData={{
              title: editingTask.title,
              description: editingTask.description || '',
              due_date: editingTask.due_date || '',
              priority: editingTask.priority || 'medium'
            }}
            submitButtonText="Update Task"
            isEditing={true}
          />
        </Modal>
      )}
    </DashboardLayout>
  );
}
