import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getMemory, addMemory, deleteMemory } from '../api/thunder';

export default function MemoryPage() {
  const [items, setItems] = useState([]);
  const [key, setKey] = useState('');
  const [value, setValue] = useState('');

  const load = () => getMemory().then(setItems).catch(() => {});

  useEffect(() => { load(); }, []);

  const handleAdd = async () => {
    if (!key.trim() || !value.trim()) return;
    await addMemory(key, value);
    setKey(''); setValue('');
    load();
  };

  const handleDelete = async (id) => {
    await deleteMemory(id);
    load();
  };

  return (
    <div className="h-full overflow-y-auto p-6">
      <h1 className="text-xl font-semibold text-thunder-text mb-6">🧠 Memory</h1>
      <p className="text-thunder-muted text-sm mb-6">
        Facts Thunder remembers about you. You can also say "remember my X is Y" in chat.
      </p>

      {/* Add memory */}
      <div className="bg-thunder-card border border-thunder-border rounded-2xl p-4 mb-6 flex gap-3">
        <input
          value={key}
          onChange={(e) => setKey(e.target.value)}
          placeholder="Key (e.g. favorite editor)"
          className="flex-1 bg-transparent text-thunder-text placeholder-thunder-muted
                     outline-none text-sm border-b border-thunder-border pb-1"
        />
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Value (e.g. VS Code)"
          className="flex-1 bg-transparent text-thunder-text placeholder-thunder-muted
                     outline-none text-sm border-b border-thunder-border pb-1"
        />
        <button
          onClick={handleAdd}
          disabled={!key.trim() || !value.trim()}
          className="px-4 py-2 bg-thunder-accent text-white rounded-xl text-sm
                     hover:bg-red-500 disabled:opacity-40 transition-colors duration-200"
        >
          Save
        </button>
      </div>

      {/* Memory list */}
      <div className="flex flex-col gap-2">
        <AnimatePresence>
          {items.length === 0 && (
            <p className="text-thunder-muted text-sm text-center py-8">No memories saved yet.</p>
          )}
          {items.map((item) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0, x: -20 }}
              className="flex items-center justify-between bg-thunder-card border border-thunder-border
                         rounded-xl px-4 py-3 hover:border-thunder-accent2 transition-colors duration-200"
            >
              <div>
                <span className="text-thunder-accent2 text-sm font-medium">{item.key}</span>
                <span className="text-thunder-muted text-sm mx-2">→</span>
                <span className="text-thunder-text text-sm">{item.value}</span>
              </div>
              <button
                onClick={() => handleDelete(item.id)}
                className="text-thunder-muted hover:text-thunder-accent transition-colors text-lg"
              >
                ×
              </button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
