'use client';

import { memo, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { User, Bot } from 'lucide-react';
import ToolCallActionCard from '@/components/tool-call-action-card';
import type { ChatMessageRecord } from '@/types';

interface PerformanceChatMessagesProps {
  messages: ChatMessageRecord[];
  isSending: boolean;
  error?: string;
  formatTime: (iso: string) => string;
  handleDeleteMessage: (messageId: string) => void;
}

const ChatMessage = memo(({
  message,
  formatTime,
  handleDeleteMessage,
  isLastMessage
}: {
  message: ChatMessageRecord;
  formatTime: (iso: string) => string;
  handleDeleteMessage: (messageId: string) => void;
  isLastMessage: boolean;
}) => {
  const isUser = message.role === 'user';

  return (
    <motion.li
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className="max-w-[90%] sm:max-w-[80%]">
        <div
          className={`group relative rounded-2xl px-4 py-3 text-sm shadow-sm ${
            isUser
              ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white'
              : 'bg-white dark:bg-neutral-700/50 border border-neutral-200 dark:border-neutral-600 text-neutral-900 dark:text-neutral-100'
          }`}
        >
          <div className="flex items-start gap-2">
            <div className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 ${
              isUser
                ? 'bg-white/20'
                : 'bg-neutral-100 dark:bg-neutral-600'
            }`}>
              {isUser ? (
                <User className="w-3 h-3" />
              ) : (
                <Bot className="w-3 h-3" />
              )}
            </div>
            <div className="whitespace-pre-wrap break-words flex-1">
              {message.content}
            </div>
          </div>

          <button
            type="button"
            onClick={() => handleDeleteMessage(message.id)}
            className={`absolute right-2 top-2 hidden rounded-md p-1 text-xs group-hover:block focus:block focus:outline-none focus:ring-2 ${
              isUser
                ? 'text-white/90 hover:bg-white/10 focus:ring-white/60'
                : 'text-neutral-500 dark:text-neutral-400 hover:bg-neutral-200 dark:hover:bg-neutral-600 focus:ring-neutral-400 dark:focus:ring-neutral-500'
            }`}
          >
            <span className="sr-only">Delete message</span>
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Tool call action cards for assistant messages */}
        {!isUser && message.tool_calls && message.tool_calls.map((toolCall, idx) => (
          <motion.div
            key={`${message.id}-${idx}`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mt-2"
          >
            <ToolCallActionCard
              toolCall={toolCall}
              onConfirm={(result) => {
                console.log('Tool call confirmed:', result);
              }}
              onCancel={() => {
                console.log('Tool call cancelled:', toolCall);
              }}
            />
          </motion.div>
        ))}

        <div className={`mt-1 text-xs ${isUser ? 'text-right text-white/70' : 'text-left text-neutral-500 dark:text-neutral-400'}`}>
          {formatTime(message.created_at)}
        </div>
      </div>
    </motion.li>
  );
});

ChatMessage.displayName = 'ChatMessage';

const PerformanceChatMessages = ({
  messages,
  isSending,
  error,
  formatTime,
  handleDeleteMessage
}: PerformanceChatMessagesProps) => {
  const memoizedMessages = useMemo(() => messages.map((msg, index) => (
    <ChatMessage
      key={msg.id}
      message={msg}
      formatTime={formatTime}
      handleDeleteMessage={handleDeleteMessage}
      isLastMessage={index === messages.length - 1}
    />
  )), [messages, formatTime, handleDeleteMessage]);

  return (
    <div className="min-h-0 flex-1 overflow-y-auto space-y-4 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800/50 p-4 mb-4">
      {messages.length === 0 ? (
        <div className="flex h-full flex-col items-center justify-center text-center py-12">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="w-16 h-16 rounded-full bg-gradient-to-r from-primary-500 to-primary-600 flex items-center justify-center mb-4"
          >
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </motion.div>
          <motion.h3
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-lg font-semibold text-neutral-900 dark:text-white mb-2"
          >
            Start a conversation
          </motion.h3>
          <motion.p
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-sm text-neutral-600 dark:text-neutral-300 max-w-sm"
          >
            Try asking me to add, update, or manage your tasks. I'm here to help!
          </motion.p>
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-md"
          >
            {[
              "Add a task to buy groceries",
              "Show my incomplete tasks",
              "Mark rent as completed",
              "Update my workout schedule"
            ].map((suggestion, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => {
                  const event = new CustomEvent('suggestionClick', { detail: suggestion });
                  window.dispatchEvent(event);
                }}
                className="text-left p-3 rounded-lg border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800/50 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700/50 transition-colors"
              >
                {suggestion}
              </motion.button>
            ))}
          </motion.div>
        </div>
      ) : (
        <AnimatePresence>
          <ul className="space-y-4" role="list">
            {memoizedMessages}
          </ul>
        </AnimatePresence>
      )}

      {isSending && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex justify-start"
        >
          <div className="rounded-2xl border border-neutral-200 dark:border-neutral-600 bg-white dark:bg-neutral-700/50 px-4 py-3">
            <div className="flex items-center space-x-2" aria-label="Assistant is typing" role="status">
              <div className="w-2 h-2 rounded-full bg-neutral-400 animate-bounce" />
              <div className="w-2 h-2 rounded-full bg-neutral-400 animate-bounce delay-100" />
              <div className="w-2 h-2 rounded-full bg-neutral-400 animate-bounce delay-200" />
            </div>
          </div>
        </motion.div>
      )}

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700 dark:text-red-300"
        >
          Error: {error}
        </motion.div>
      )}
    </div>
  );
};

PerformanceChatMessages.displayName = 'PerformanceChatMessages';

export default PerformanceChatMessages;