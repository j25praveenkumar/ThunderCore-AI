import React from 'react';
import { motion } from 'framer-motion';

export default function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex items-start mb-3"
    >
      <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-thunder-accent to-thunder-accent2
                      flex items-center justify-center text-sm mr-2 flex-shrink-0">
        ⚡
      </div>
      <div className="bg-thunder-card border border-thunder-border px-4 py-3 rounded-2xl rounded-tl-sm">
        <span className="typing-dot" />
        <span className="typing-dot" />
        <span className="typing-dot" />
      </div>
    </motion.div>
  );
}
