'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { Menu, Plus, Search, Trash2, X, Bot, User, Send, Sparkles, MessageSquarePlus } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { useAuth } from '@/hooks/use-auth';
import { useToast } from '@/hooks/use-toast';
import { chatApiClient } from '@/lib/api';
import ToolCallActionCard from '@/components/tool-call-action-card';
import PerformanceChatMessages from '@/components/performance-chat-messages';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { ChatMessageRecord, Conversation, ChatToolCall } from '@/types';


const LAST_CONVERSATION_KEY = 'chat_last_conversation_id';
const CONVERSATION_LABELS_KEY = 'chat_conversation_labels_v1';

function safeParseJson<T>(value: string | null, fallback: T): T {
  if (!value) return fallback;
  try {
    return JSON.parse(value) as T;
  } catch {
    return fallback;
  }
}

function formatTime(iso: string) {
  const d = new Date(iso);
  return d.toLocaleString(undefined, {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function deriveConversationLabel(messages: ChatMessageRecord[]): string {
  const firstUser = messages.find((m) => m.role === 'user');
  if (!firstUser) return 'New conversation';

  const trimmed = firstUser.content.trim().replace(/\s+/g, ' ');
  return trimmed.length > 48 ? `${trimmed.slice(0, 48)}…` : trimmed;
}

export default function ChatPage() {
  const { user, loading: authLoading, isAuthenticated } = useAuth();
  const { toast } = useToast();

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [conversationSearch, setConversationSearch] = useState('');

  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessageRecord[]>([]);

  const [labels, setLabels] = useState<Record<string, string>>(() => {
    if (typeof window === 'undefined') return {};
    return safeParseJson<Record<string, string>>(localStorage.getItem(CONVERSATION_LABELS_KEY), {});
  });

  const [input, setInput] = useState('');
  const [isLoadingConversations, setIsLoadingConversations] = useState(false);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | undefined>(undefined);
  const [pendingToolCalls, setPendingToolCalls] = useState<{[key: string]: ChatToolCall[]}>({});

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isSending]);

  const filteredConversations = useMemo(() => {
    const q = conversationSearch.trim().toLowerCase();
    if (!q) return conversations;

    return conversations.filter((c) => {
      const label = (labels[c.id] || '').toLowerCase();
      return c.id.toLowerCase().includes(q) || label.includes(q);
    });
  }, [conversationSearch, conversations, labels]);

  const persistLabels = (next: Record<string, string>) => {
    setLabels(next);
    try {
      localStorage.setItem(CONVERSATION_LABELS_KEY, JSON.stringify(next));
    } catch {
      // ignore
    }
  };

  const selectConversation = async (conversationId: string) => {
    setActiveConversationId(conversationId);
    try {
      localStorage.setItem(LAST_CONVERSATION_KEY, conversationId);
    } catch {
      // ignore
    }
    setSidebarOpen(false);
  };

  const loadConversations = async () => {
    if (!user) return;

    setIsLoadingConversations(true);
    setError(undefined);

    try {
      const list = await chatApiClient.listConversations(user.id, true); // Show toast on error
      setConversations(list);

      const lastId = typeof window === 'undefined' ? null : localStorage.getItem(LAST_CONVERSATION_KEY);
      const preferred = lastId && list.some((c) => c.id === lastId) ? lastId : null;

      if (preferred) {
        setActiveConversationId(preferred);
        return;
      }

      if (list.length > 0) {
        setActiveConversationId(list[0].id);
        return;
      }

      const created = await chatApiClient.createConversation(user.id, true); // Show toast on error
      setConversations([created]);
      setActiveConversationId(created.id);
      try {
        localStorage.setItem(LAST_CONVERSATION_KEY, created.id);
      } catch {
        // ignore
      }
    } catch (err: any) {
      const msg = err?.message || 'Failed to load conversations';
      setError(msg);
      toast({
        title: 'Error',
        description: msg,
        variant: 'destructive'
      });
    } finally {
      setIsLoadingConversations(false);
    }
  };

  const loadMessages = async (conversationId: string) => {
    if (!user) return;

    setIsLoadingMessages(true);
    setError(undefined);

    try {
      const msgs = await chatApiClient.getConversationMessages(user.id, conversationId, undefined, true); // Show toast on error

      // tool_calls is already an array of ChatToolCall objects, no parsing needed
      const parsedMsgs = msgs;

      setMessages(parsedMsgs);

      if (!labels[conversationId]) {
        persistLabels({
          ...labels,
          [conversationId]: deriveConversationLabel(parsedMsgs),
        });
      }

      // Set any pending tool calls for this conversation
      if (pendingToolCalls[conversationId]) {
        // Tool calls have been processed, remove them
        setPendingToolCalls(prev => {
          const newState = {...prev};
          delete newState[conversationId];
          return newState;
        });
      }
    } catch (err: any) {
      const msg = err?.message || 'Failed to load messages';
      setError(msg);
      toast({
        title: 'Error',
        description: msg,
        variant: 'destructive'
      });
    } finally {
      setIsLoadingMessages(false);
    }
  };

  useEffect(() => {
    if (!isAuthenticated || !user) return;
    void loadConversations();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated, user?.id]);

  useEffect(() => {
    if (!isAuthenticated || !user || !activeConversationId) return;
    void loadMessages(activeConversationId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeConversationId, isAuthenticated, user?.id]);

  const handleNewConversation = async () => {
    if (!user) return;

    try {
      const created = await chatApiClient.createConversation(user.id, true); // Show toast on error
      setConversations((prev) => [created, ...prev]);
      await selectConversation(created.id);
      setMessages([]);
      toast({
        title: 'Success',
        description: 'New conversation created!',
        variant: 'success'
      });
    } catch (err: any) {
      const msg = err?.message || 'Failed to create conversation';
      toast({
        title: 'Error',
        description: msg,
        variant: 'destructive'
      });
    }
  };

  const handleDeleteConversation = async () => {
    if (!user || !activeConversationId) return;

    const ok = window.confirm('Delete this conversation? This cannot be undone.');
    if (!ok) return;

    try {
      await chatApiClient.deleteConversation(user.id, activeConversationId, true); // Show toast on error
      toast({
        title: 'Success',
        description: 'Conversation deleted',
        variant: 'success'
      });

      setConversations((prev) => prev.filter((c) => c.id !== activeConversationId));
      setMessages([]);

      const next = conversations.find((c) => c.id !== activeConversationId)?.id || null;
      setActiveConversationId(next);
      if (next) {
        try {
          localStorage.setItem(LAST_CONVERSATION_KEY, next);
        } catch {
          // ignore
        }
      }
    } catch (err: any) {
      const msg = err?.message || 'Failed to delete conversation';
      toast({
        title: 'Error',
        description: msg,
        variant: 'destructive'
      });
    }
  };

  const handleClearConversation = async () => {
    if (!user || !activeConversationId) return;

    const ok = window.confirm('Clear all messages in this conversation?');
    if (!ok) return;

    try {
      await chatApiClient.clearConversationMessages(user.id, activeConversationId, true); // Show toast on error
      toast({
        title: 'Success',
        description: 'Conversation cleared',
        variant: 'success'
      });
      setMessages([]);
    } catch (err: any) {
      const msg = err?.message || 'Failed to clear conversation';
      toast({
        title: 'Error',
        description: msg,
        variant: 'destructive'
      });
    }
  };

  const handleDeleteMessage = async (messageId: string) => {
    if (!user || !activeConversationId) return;

    const ok = window.confirm('Delete this message?');
    if (!ok) return;

    try {
      await chatApiClient.deleteMessage(user.id, activeConversationId, messageId, true); // Show toast on error
      setMessages((prev) => prev.filter((m) => m.id !== messageId));
      toast({
        title: 'Success',
        description: 'Message deleted',
        variant: 'success'
      });
    } catch (err: any) {
      const msg = err?.message || 'Failed to delete message';
      toast({
        title: 'Error',
        description: msg,
        variant: 'destructive'
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!user) return;

    if (!activeConversationId) {
      await handleNewConversation();
      return;
    }

    if (!input.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter a message before sending',
        variant: 'destructive'
      });
      return;
    }

    if (input.trim().length > 500) {
      toast({
        title: 'Error',
        description: 'Message is too long. Please keep it under 500 characters.',
        variant: 'destructive',
      });
      return;
    }

    const outgoing = input;
    setInput('');
    setIsSending(true);
    setError(undefined);

    try {
      const result = await chatApiClient.sendMessage(user.id, outgoing, activeConversationId, true); // Show toast on error

      // Always refresh messages from server so we have real message IDs
      await loadMessages(result.conversation_id);

      // Refresh conversation ordering
      const list = await chatApiClient.listConversations(user.id, true); // Show toast on error
      setConversations(list);

      // Ensure active conversation matches response
      if (result.conversation_id !== activeConversationId) {
        setActiveConversationId(result.conversation_id);
      }

      if (!labels[result.conversation_id]) {
        persistLabels({
          ...labels,
          [result.conversation_id]: deriveConversationLabel(messages),
        });
      }

      // Handle tool calls if present
      if (result.tool_calls && result.tool_calls.length > 0) {
        setPendingToolCalls(prev => ({
          ...prev,
          [result.conversation_id]: result.tool_calls
        }));
      }
    } catch (err: any) {
      const msg = err?.message || 'Chat request failed';
      setError(msg);
      toast({
        title: 'Error',
        description: msg,
        variant: 'destructive'
      });
    } finally {
      setIsSending(false);
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-neutral-50 to-neutral-100 dark:from-neutral-900 dark:to-neutral-950">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex flex-col items-center"
        >
          <div className="w-16 h-16 rounded-full bg-gradient-to-r from-primary-500 to-primary-600 flex items-center justify-center mb-4">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <div className="text-xl font-semibold text-neutral-900 dark:text-white">Loading Chat</div>
        </motion.div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-neutral-50 to-neutral-100 dark:from-neutral-900 dark:to-neutral-950 p-4">
        <Card className="bg-white/80 dark:bg-neutral-800/80 backdrop-blur-xl border border-neutral-200/50 dark:border-neutral-700/50 shadow-xl max-w-md w-full">
          <CardHeader className="text-center space-y-2">
            <div className="mx-auto w-16 h-16 rounded-full bg-gradient-to-r from-primary-500 to-primary-600 flex items-center justify-center">
              <Bot className="w-8 h-8 text-white" />
            </div>
            <CardTitle className="text-2xl font-bold text-neutral-900 dark:text-white">
              Access Required
            </CardTitle>
          </CardHeader>
          <CardContent className="text-center">
            <p className="text-neutral-600 dark:text-neutral-300 mb-6">
              Please log in to access the AI Assistant chat.
            </p>
            <Button
              variant="gradient"
              onClick={() => window.location.href = '/login'}
              className="w-full"
            >
              Go to Login
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const Sidebar = (
    <motion.aside
      initial={false}
      animate={{
        width: sidebarOpen ? '100%' : '100%',
        height: '100%'
      }}
      className="flex h-full w-full flex-col bg-white dark:bg-neutral-900 border-r border-neutral-200 dark:border-neutral-700 md:w-80 md:min-w-80"
    >
      <div className="flex items-center justify-between border-b border-neutral-200 dark:border-neutral-700 px-4 py-4">
        <div>
          <div className="text-base font-semibold text-neutral-900 dark:text-white flex items-center gap-2">
            <Link href="/" className="hover:underline">
              <Sparkles className="w-5 h-5 text-primary-500" />
              Conversations
            </Link>
          </div>
          <div className="text-xs text-neutral-500 dark:text-neutral-400">Your AI chat history</div>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={handleNewConversation}
          className="flex items-center gap-2"
        >
          <MessageSquarePlus className="h-4 w-4" aria-hidden="true" />
          <span className="hidden sm:inline">New</span>
        </Button>
      </div>

      <div className="p-4">
        <label className="sr-only" htmlFor="conversation-search">
          Search conversations
        </label>
        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-400" />
          <Input
            id="conversation-search"
            value={conversationSearch}
            onChange={(e) => setConversationSearch(e.target.value)}
            placeholder="Search conversations..."
            className="w-full pl-9 pr-3 py-2"
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-2 pb-4">
        {isLoadingConversations ? (
          <div className="px-2 text-sm text-neutral-500 dark:text-neutral-400 flex items-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-500 mr-2" />
            Loading conversations...
          </div>
        ) : filteredConversations.length === 0 ? (
          <div className="px-2 text-sm text-neutral-500 dark:text-neutral-400 text-center py-8">
            No conversations found.
          </div>
        ) : (
          <ul className="space-y-1" role="list">
            {filteredConversations.map((c) => {
              const isActive = c.id === activeConversationId;
              const title = labels[c.id] || `Conversation ${c.id.slice(0, 8)}`;

              return (
                <motion.li
                  key={c.id}
                  whileHover={{ scale: 1.01 }}
                  whileTap={{ scale: 0.99 }}
                >
                  <button
                    type="button"
                    onClick={() => void selectConversation(c.id)}
                    className={`group flex w-full flex-col rounded-lg px-3 py-2 text-left transition-all focus:outline-none focus:ring-2 focus:ring-primary-500 ${
                      isActive
                        ? 'bg-primary-50 dark:bg-primary-900/30 border border-primary-200 dark:border-primary-800'
                        : 'hover:bg-neutral-50 dark:hover:bg-neutral-800/50'
                    }`}
                    aria-current={isActive ? 'page' : undefined}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <div className={`truncate text-sm font-medium ${isActive ? 'text-primary-800 dark:text-primary-200' : 'text-neutral-900 dark:text-neutral-100'}`}>
                        {title}
                      </div>
                      <div className="shrink-0 text-xs text-neutral-500 dark:text-neutral-400">{formatTime(c.updated_at)}</div>
                    </div>
                    <div className="mt-1 truncate text-xs text-neutral-500 dark:text-neutral-400">{c.id.slice(0, 12)}...</div>
                  </button>
                </motion.li>
              );
            })}
          </ul>
        )}
      </div>
    </motion.aside>
  );

  return (
    <div className="flex h-screen bg-gradient-to-br from-neutral-50 to-neutral-100 dark:from-neutral-900 dark:to-neutral-950">
      {/* Desktop sidebar */}
      <div className="hidden md:block">{Sidebar}</div>

      {/* Mobile sidebar overlay */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 flex md:hidden"
            role="dialog"
            aria-modal="true"
          >
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm"
              onClick={() => setSidebarOpen(false)}
            />
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="relative h-full w-[92%] max-w-sm bg-white dark:bg-neutral-900 shadow-xl"
            >
              <div className="absolute right-3 top-3 z-10">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setSidebarOpen(false)}
                  className="rounded-full bg-white/90 dark:bg-neutral-800/90 text-neutral-700 dark:text-neutral-200 hover:bg-neutral-100 dark:hover:bg-neutral-700/50"
                >
                  <X className="h-4 w-4" aria-hidden="true" />
                  <span className="sr-only">Close sidebar</span>
                </Button>
              </div>
              {Sidebar}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main chat */}
      <div className="flex min-w-0 flex-1 flex-col">
        <motion.header
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="sticky top-0 z-10 border-b border-neutral-200 dark:border-neutral-700 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-xl px-4 py-4"
        >
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <Button
                variant="outline"
                size="icon"
                onClick={() => setSidebarOpen(true)}
                className="md:hidden"
              >
                <Menu className="h-4 w-4" aria-hidden="true" />
                <span className="sr-only">Open conversations</span>
              </Button>

              <div className="flex items-center gap-2">
                <Link href="/" className="w-8 h-8 rounded-full bg-gradient-to-r from-primary-500 to-primary-600 flex items-center justify-center hover:scale-105 transition-transform">
                  <Bot className="w-4 h-4 text-white" />
                </Link>
                <div>
                  <div className="text-sm font-semibold text-neutral-900 dark:text-white">
                    <Link href="/" className="hover:underline">Todo AI Assistant</Link>
                  </div>
                  <div className="text-xs text-neutral-500 dark:text-neutral-400">
                    {user?.name || user?.email}
                  </div>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleClearConversation}
                disabled={!activeConversationId || messages.length === 0}
                className="hidden sm:flex"
              >
                Clear
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleDeleteConversation}
                disabled={!activeConversationId}
                className="text-red-600 dark:text-red-400 border-red-200 dark:border-red-800 hover:bg-red-50 dark:hover:bg-red-900/20"
              >
                <Trash2 className="h-4 w-4 sm:mr-2" />
                <span className="hidden sm:inline">Delete</span>
              </Button>
            </div>
          </div>
        </motion.header>

        <div className="flex min-h-0 flex-1 flex-col px-4 py-4">
          {/* Messages */}
          <PerformanceChatMessages
            messages={messages}
            isSending={isSending}
            error={error}
            formatTime={formatTime}
            handleDeleteMessage={handleDeleteMessage}
          />
          <div ref={messagesEndRef} />

          {/* Composer */}
          <motion.form
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            onSubmit={handleSubmit}
            className="mt-auto"
          >
            <div className="flex gap-2">
              <div className="flex-1 relative">
                <Input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask me to add, update, delete, or complete tasks..."
                  className="w-full rounded-xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 px-4 py-3 pr-12 text-sm text-neutral-900 dark:text-white placeholder:text-neutral-500 dark:placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  disabled={isSending || isLoadingMessages}
                  maxLength={500}
                />
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-xs text-neutral-500 dark:text-neutral-400">
                  {input.length}/500
                </div>
              </div>
              <Button
                type="submit"
                disabled={isSending || !input.trim()}
                className="h-12 flex items-center gap-2"
              >
                {isSending ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                    Sending...
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4" />
                    Send
                  </>
                )}
              </Button>
            </div>
            <div className="mt-2 flex items-center justify-between text-xs text-neutral-500 dark:text-neutral-400">
              <span>Tip: Use natural language to manage your tasks</span>
            </div>
          </motion.form>
        </div>
      </div>
    </div>
  );
}
