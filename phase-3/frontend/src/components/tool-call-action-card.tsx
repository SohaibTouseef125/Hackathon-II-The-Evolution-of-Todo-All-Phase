'use client';

import { useState } from 'react';
import { Check, X, AlertTriangle, Loader2 } from 'lucide-react';
import { apiClient } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';

interface ToolCallActionCardProps {
  toolCall: {
    name: string;
    arguments: string;
  };
  onConfirm: (result: any) => void;
  onCancel: () => void;
}

export default function ToolCallActionCard({ toolCall, onConfirm, onCancel }: ToolCallActionCardProps) {
  const { toast } = useToast();
  const [isExecuting, setIsExecuting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [argumentsObj, setArgumentsObj] = useState<Record<string, any>>({});

  // Parse arguments string to object
  useState(() => {
    try {
      const parsed = JSON.parse(toolCall.arguments);
      setArgumentsObj(parsed);
    } catch (e) {
      console.error('Failed to parse tool arguments:', e);
    }
  });

  const isDestructive = ['delete_task'].includes(toolCall.name);

  const handleConfirm = async () => {
    setIsExecuting(true);
    try {
      let result;

      switch (toolCall.name) {
        case 'add_task':
          result = await apiClient.createTask({
            title: argumentsObj.title || 'Untitled Task',
            description: argumentsObj.description,
            priority: argumentsObj.priority,
            due_date: argumentsObj.due_date
          }, false); // Don't show toast since we handle it manually
          toast({ title: 'Success', description: 'Task added successfully', variant: 'success' });
          break;
        case 'update_task':
          if (argumentsObj.id) {
            result = await apiClient.updateTask(argumentsObj.id, {
              title: argumentsObj.title,
              description: argumentsObj.description,
              priority: argumentsObj.priority,
              due_date: argumentsObj.due_date
            }, false); // Don't show toast since we handle it manually
            toast({ title: 'Success', description: 'Task updated successfully', variant: 'success' });
          }
          break;
        case 'delete_task':
          if (argumentsObj.id) {
            await apiClient.deleteTask(argumentsObj.id, false); // Don't show toast since we handle it manually
            result = { success: true };
            toast({ title: 'Success', description: 'Task deleted successfully', variant: 'success' });
          }
          break;
        case 'complete_task':
          if (argumentsObj.id) {
            result = await apiClient.toggleTaskCompletion(argumentsObj.id, true, false); // Don't show toast since we handle it manually
            toast({ title: 'Success', description: 'Task marked as complete', variant: 'success' });
          }
          break;
        case 'list_tasks':
          result = await apiClient.getTasks('all', 'created', false); // Don't show toast since we handle it manually
          break;
        default:
          result = { error: `Unknown tool: ${toolCall.name}` };
      }

      setIsSuccess(true);
      onConfirm(result);
    } catch (error: any) {
      const errorMsg = error.message || 'Operation failed';
      toast({ title: 'Error', description: errorMsg, variant: 'destructive' });
      console.error('Tool execution error:', error);
    } finally {
      setIsExecuting(false);
    }
  };

  const getActionText = () => {
    switch (toolCall.name) {
      case 'add_task':
        return `Add task: "${argumentsObj.title}"`;
      case 'update_task':
        return `Update task: "${argumentsObj.title || argumentsObj.id}"`;
      case 'delete_task':
        return `Delete task: "${argumentsObj.title || argumentsObj.id}"`;
      case 'complete_task':
        return `Mark task as complete: "${argumentsObj.title || argumentsObj.id}"`;
      case 'list_tasks':
        return 'List all tasks';
      default:
        return `Execute: ${toolCall.name}`;
    }
  };

  if (isSuccess) {
    return (
      <div className="mt-3 p-4 rounded-xl border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20">
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center flex-shrink-0">
            <Check className="h-4 w-4 text-white" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-green-800 dark:text-green-200">Action completed successfully!</p>
            <p className="text-xs text-green-700 dark:text-green-300 mt-1">{getActionText()}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`mt-3 p-4 rounded-xl border ${isDestructive ? 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800' : 'bg-white dark:bg-neutral-700/50 border-neutral-200 dark:border-neutral-600'}`}>
      <div className="flex items-start gap-3">
        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          isDestructive
            ? 'bg-red-500'
            : 'bg-yellow-500 dark:bg-yellow-600'
        }`}>
          <AlertTriangle className="h-4 w-4 text-white" />
        </div>
        <div className="flex-1">
          <p className="text-sm font-medium text-neutral-900 dark:text-white">{getActionText()}</p>
          {argumentsObj.description && (
            <p className="text-xs text-neutral-600 dark:text-neutral-300 mt-1">{argumentsObj.description}</p>
          )}
        </div>
      </div>

      <div className="flex gap-2 mt-3">
        <Button
          variant={isDestructive ? "destructive" : "default"}
          size="sm"
          onClick={handleConfirm}
          disabled={isExecuting}
          className="flex-1"
        >
          {isExecuting ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin mr-2" />
              Executing...
            </>
          ) : (
            <>
              <Check className="h-4 w-4 mr-2" />
              Confirm
            </>
          )}
        </Button>

        <Button
          variant="outline"
          size="sm"
          onClick={onCancel}
          disabled={isExecuting}
          className="flex-1"
        >
          <X className="h-4 w-4 mr-2" />
          Cancel
        </Button>
      </div>
    </div>
  );
}