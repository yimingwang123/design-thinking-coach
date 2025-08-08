import React, { useRef, useEffect } from 'react';
import { Message } from '../types';
import { formatTime, formatMarkdown } from '../utils';

interface ChatProps {
  messages: Message[];
  newMessage: string;
  loading: boolean;
  onMessageChange: (message: string) => void;
  onSendMessage: () => void;
}

const Chat: React.FC<ChatProps> = ({
  messages,
  newMessage,
  loading,
  onMessageChange,
  onSendMessage
}) => {
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (messagesContainerRef.current) {
      const container = messagesContainerRef.current;
      container.scrollTop = container.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!loading) {
        onSendMessage();
      }
    }
  };

  return (
    <div className="lg:col-span-3 chat-container flex flex-col">
      
      {/* Messages */}
      <div className="chat-glass rounded-xl p-4 mb-4 flex flex-col flex-1 overflow-hidden">
        <div 
          ref={messagesContainerRef}
          className="messages-container custom-scrollbar space-y-4 pr-2 will-change-scroll overflow-y-auto flex-1"
        >
          
          {messages.map((message, index) => (
            <div key={index} className="animate-fade-in-up">
              {/* User Message */}
              {message.type === 'user' && (
                <div className="flex justify-end">
                  <div className="bg-blue-600/90 text-white rounded-lg px-4 py-2 max-w-2xl lg:max-w-4xl shadow-lg">
                    <div className="flex items-start space-x-2">
                      <div className="flex-1">
                        <div className="whitespace-pre-wrap">{message.content}</div>
                        <span className="text-xs text-white/80 block mt-1">
                          {formatTime(message.timestamp)}
                        </span>
                      </div>
                      <span className="text-lg">👤</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Assistant Message */}
              {message.type === 'assistant' && (
                <div className="flex justify-start">
                  <div className="bg-gray-800/90 text-white rounded-lg px-4 py-2 max-w-2xl lg:max-w-4xl shadow-lg">
                    <div className="flex items-start space-x-2">
                      <span className="text-lg">🤖</span>
                      <div className="flex-1">
                        <div 
                          className="whitespace-pre-wrap prose prose-sm max-w-none text-white prose-headings:text-white prose-p:text-white prose-strong:text-white prose-ul:text-white prose-ol:text-white prose-table:text-white prose-th:text-white prose-td:text-white prose-th:border-white/20 prose-td:border-white/20"
                          dangerouslySetInnerHTML={{ __html: formatMarkdown(message.content) }}
                        />
                        <span className="text-xs text-white/80 block mt-1">
                          {formatTime(message.timestamp)}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* System Message */}
              {message.type === 'system' && (
                <div className="flex justify-center">
                  <div className="bg-gray-600/50 text-white/80 rounded-lg px-3 py-1 text-sm">
                    {message.content}
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* Loading Indicator */}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-800/90 text-white rounded-lg px-4 py-2">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">🤖</span>
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-white/80 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-white/80 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-white/80 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Welcome Message */}
          {messages.length === 0 && (
            <div className="text-center py-8">
              <div className="text-6xl mb-4">🧠</div>
              <h2 className="text-2xl font-bold text-white mb-2">Willkommen beim Design Thinking Coach!</h2>
              <p className="text-white/70 mb-4">Ich helfe Ihnen dabei, Ihre Ideen strukturiert zu entwickeln.</p>
              <p className="text-sm text-white/50">Beschreiben Sie Ihr Problem oder Ihre Idee, und wir arbeiten gemeinsam daran!</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Input Area */}
      <div className="chat-glass rounded-xl p-4">
        <div className="flex space-x-4">
          <div className="flex-1">
            <textarea
              value={newMessage}
              onChange={(e) => onMessageChange(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Beschreiben Sie Ihr Problem oder stellen Sie eine Frage..."
              className="w-full px-4 py-2 rounded-lg bg-white border border-gray-300 text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={2}
              disabled={loading}
            />
            <div className="text-xs text-white/80 mt-1">
              Enter zum Senden, Shift+Enter für neue Zeile
            </div>
          </div>
          <button 
            onClick={onSendMessage}
            disabled={loading || !newMessage.trim()}
            className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold py-2 px-6 rounded-lg shadow-lg transform hover:scale-105 disabled:hover:scale-100 transition-all duration-200 disabled:cursor-not-allowed"
          >
            {loading ? '...' : 'Senden'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;