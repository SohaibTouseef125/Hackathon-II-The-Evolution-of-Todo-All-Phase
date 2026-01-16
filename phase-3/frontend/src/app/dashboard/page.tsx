'use client';

import { useState, useEffect, memo } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { apiClient } from '@/lib/api';
import { Task, TaskCreateData, TaskUpdateData } from '@/types';
import DashboardLayout from '@/components/dashboard-layout';
import EnhancedTaskForm from '@/components/enhanced-task-form';
import EnhancedTaskList from '@/components/enhanced-task-list';
import PerformanceTaskList from '@/components/performance-task-list';
import Modal from '@/components/ui/modal';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import LoadingSpinner from '@/components/ui/loading-spinner';
import { DashboardSkeleton } from '@/components/ui/dashboard-skeleton';
import { useToast } from '@/hooks/use-toast';
import { Plus, CheckCircle, Circle, AlertCircle, Calendar, TrendingUp, Users, Target } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Advanced3DCard from '@/components/advanced-3d-card';
import TaskAnalytics from '@/components/task-analytics';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const router = useRouter();
  const { user, logout } = useAuth();
  const { toast } = useToast();

  // Fetch tasks when component mounts
  useEffect(() => {
    const fetchTasks = async () => {
      if (!user) {
        setLoading(false);
        return;
      }

      try {
        const tasks = await apiClient.getTasks('all', 'created', true); // Show toast on error
        setTasks(tasks);
      } catch (err: any) {
        toast({
          title: 'Error',
          description: err.message || 'Error fetching tasks',
          variant: 'destructive'
        });
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [user]);

  const handleAddTask = async (taskData: TaskCreateData) => {
    if (!user) return;

    try {
      const createdTask = await apiClient.createTask(taskData, true); // Show toast on error
      setTasks([createdTask, ...tasks]);
      toast({
        title: 'Success',
        description: 'Task created successfully!',
        variant: 'success'
      });
    } catch (err: any) {
      toast({
        title: 'Error',
        description: err.message || 'Error creating task',
        variant: 'destructive'
      });
      console.error(err);
    }
  };

  const handleUpdateTask = async (taskData: TaskCreateData | TaskUpdateData) => {
    if (!editingTask || !user) return;

    try {
      const updatedTask = await apiClient.updateTask(editingTask.id, taskData, true); // Show toast on error
      setTasks(tasks.map(task => task.id === editingTask.id ? updatedTask : task));
      setEditingTask(null);
      toast({
        title: 'Success',
        description: 'Task updated successfully!',
        variant: 'success'
      });
    } catch (err: any) {
      toast({
        title: 'Error',
        description: err.message || 'Error updating task',
        variant: 'destructive'
      });
      console.error(err);
    }
  };

  const handleToggleComplete = async (taskId: string, completed: boolean) => {
    if (!user) return;

    try {
      const updatedTask = await apiClient.toggleTaskCompletion(taskId, !completed, true); // Show toast on error
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
      toast({
        title: 'Success',
        description: completed ? 'Task marked as incomplete' : 'Task marked as complete',
        variant: 'success'
      });
    } catch (err: any) {
      toast({
        title: 'Error',
        description: err.message || 'Error updating task',
        variant: 'destructive'
      });
      console.error(err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!user) return;

    if (!confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
      return;
    }

    try {
      await apiClient.deleteTask(taskId, true); // Show toast on error
      setTasks(tasks.filter(task => task.id !== taskId));
      toast({
        title: 'Success',
        description: 'Task deleted successfully!',
        variant: 'success'
      });
    } catch (err: any) {
      toast({
        title: 'Error',
        description: err.message || 'Error deleting task',
        variant: 'destructive'
      });
      console.error(err);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (err) {
      console.error('Error during logout:', err);
      // Even if API logout fails, clear local token and redirect
      localStorage.removeItem('access_token');
      router.push('/login');
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <DashboardSkeleton />
      </DashboardLayout>
    );
  }

  // Calculate stats
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const highPriorityTasks = tasks.filter(task => task.priority === 'high').length;

  return (
    <DashboardLayout>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="space-y-6"
      >
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-neutral-900 dark:text-white">Dashboard</h1>
            <p className="text-neutral-600 dark:text-neutral-200 mt-1">Manage your tasks and boost productivity</p>
          </div>
          <Button
            onClick={() => setEditingTask({} as Task)}
            className="flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            New Task
          </Button>
        </div>

        {/* Stats Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          <Advanced3DCard className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950/30 dark:to-blue-900/30 border-blue-200 dark:border-blue-800">
            <Card className="bg-transparent border-0 shadow-none">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-blue-800 dark:text-blue-200">Total Tasks</CardTitle>
                <Target className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-900 dark:text-blue-100">{totalTasks}</div>
                <p className="text-xs text-blue-600 dark:text-blue-400">All tasks assigned</p>
              </CardContent>
            </Card>
          </Advanced3DCard>

          <Advanced3DCard className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950/30 dark:to-green-900/30 border-green-200 dark:border-green-800">
            <Card className="bg-transparent border-0 shadow-none">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-green-800 dark:text-green-200">Completed</CardTitle>
                <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-900 dark:text-green-100">{completedTasks}</div>
                <p className="text-xs text-green-600 dark:text-green-400">Tasks finished</p>
              </CardContent>
            </Card>
          </Advanced3DCard>

          <Advanced3DCard className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-950/30 dark:to-orange-900/30 border-orange-200 dark:border-orange-800">
            <Card className="bg-transparent border-0 shadow-none">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-orange-800 dark:text-orange-200">Pending</CardTitle>
                <Circle className="w-5 h-5 text-orange-600 dark:text-orange-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-orange-900 dark:text-orange-100">{pendingTasks}</div>
                <p className="text-xs text-orange-600 dark:text-orange-400">Tasks remaining</p>
              </CardContent>
            </Card>
          </Advanced3DCard>

          <Advanced3DCard className="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-950/30 dark:to-red-900/30 border-red-200 dark:border-red-800">
            <Card className="bg-transparent border-0 shadow-none">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-red-800 dark:text-red-200">High Priority</CardTitle>
                <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-red-900 dark:text-red-100">{highPriorityTasks}</div>
                <p className="text-xs text-red-600 dark:text-red-400">Urgent tasks</p>
              </CardContent>
            </Card>
          </Advanced3DCard>
        </motion.div>

        {/* Analytics Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card className="bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800/50 dark:to-neutral-800 border-neutral-200 dark:border-neutral-700">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Task Analytics
              </CardTitle>
            </CardHeader>
            <CardContent>
              <TaskAnalytics tasks={tasks.map(task => ({
                id: task.id,
                title: task.title,
                completed: task.completed,
                priority: task.priority || 'medium', // Default to medium if undefined
                createdAt: task.created_at,
                updatedAt: task.updated_at
              }))} />
            </CardContent>
          </Card>
        </motion.div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Add Task Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="lg:col-span-1"
          >
            <Advanced3DCard>
              <Card className="bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800/50 dark:to-neutral-800 border-neutral-200 dark:border-neutral-700">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <Plus className="w-5 h-5" />
                    Add New Task
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <EnhancedTaskForm
                    onSubmit={handleAddTask}
                    submitButtonText="Create Task"
                  />
                </CardContent>
              </Card>
            </Advanced3DCard>
          </motion.div>

          {/* Task List */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="lg:col-span-2"
          >
            <Advanced3DCard>
              <Card className="bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800/50 dark:to-neutral-800 border-neutral-200 dark:border-neutral-700">
                <CardHeader className="flex flex-row items-center justify-between">
                  <CardTitle className="text-lg flex items-center gap-2">
                    <CheckCircle className="w-5 h-5" />
                    Your Tasks
                  </CardTitle>
                  <div className="text-sm text-neutral-600 dark:text-neutral-400">
                    {pendingTasks} pending, {completedTasks} completed
                  </div>
                </CardHeader>
                <CardContent>
                  <PerformanceTaskList
                    tasks={tasks.map(task => ({
                      id: task.id,
                      title: task.title,
                      description: task.description,
                      completed: task.completed,
                      priority: task.priority || 'medium', // Default to medium if undefined
                      createdAt: task.created_at
                    }))}
                    onToggleComplete={handleToggleComplete}
                    onDelete={handleDeleteTask}
                    onEdit={(transformedTask) => {
                      // Find the original task by ID to pass to the handler
                      const originalTask = tasks.find(t => t.id === transformedTask.id);
                      if (originalTask) {
                        handleEditTask(originalTask);
                      }
                    }}
                  />
                </CardContent>
              </Card>
            </Advanced3DCard>
          </motion.div>
        </div>
      </motion.div>

      {/* Edit Task Modal */}
      <AnimatePresence>
        {editingTask && (
          <Modal
            isOpen={!!editingTask}
            onClose={() => setEditingTask(null)}
            title={editingTask.id ? 'Edit Task' : 'Create New Task'}
          >
            <EnhancedTaskForm
              onSubmit={editingTask.id ? handleUpdateTask : handleAddTask}
              initialData={
                editingTask.id
                  ? {
                      title: editingTask.title,
                      description: editingTask.description || '',
                      priority: editingTask.priority || 'medium'
                    }
                  : undefined
              }
              submitButtonText={editingTask.id ? 'Update Task' : 'Create Task'}
              isEditing={!!editingTask.id}
            />
          </Modal>
        )}
      </AnimatePresence>
    </DashboardLayout>
  );
}