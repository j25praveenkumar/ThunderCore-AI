import React from 'react';
import { motion } from 'framer-motion';

export default function MessageBubble({ role, content, timestamp }) {
  const isUser = role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}
    >
      {/* Avatar */}
      {!isUser && (
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-thunder-accent to-thunder-accent2
                        flex items-center justify-center text-sm mr-2 flex-shrink-0 mt-1">
          ⚡
        </div>
      )}

      <div className={`max-w-[70%] flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap
            ${isUser
              ? 'bg-thunder-accent text-white rounded-tr-sm'
              : 'bg-thunder-card text-thunder-text border border-thunder-border rounded-tl-sm'
            }`}
        >
          {content}
        </div>
        {timestamp && (
          <span className="text-xs text-thunder-muted mt-1 px-1">
            {new Date(timestamp).toLocaleTimeString()}
          </span>
        )}
      </div>

      {/* User avatar */}
      {isUser && (
        <div className="w-8 h-8 rounded-lg bg-thunder-border flex items-center justify-center
                        text-sm ml-2 flex-shrink-0 mt-1">
          👤
        </div>
      )}
    </motion.div>
  );
}
