import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getNotes, createNote, deleteNote } from '../api/thunder';

export default function NotesPage() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);

  const load = () => getNotes().then(setNotes).catch(() => {});

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    if (!title.trim() || !content.trim()) return;
    setLoading(true);
    try {
      await createNote(title, content);
      setTitle('');
      setContent('');
      load();
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    await deleteNote(id);
    load();
  };

  return (
    <div className="h-full overflow-y-auto p-6">
      <h1 className="text-xl font-semibold text-thunder-text mb-6">📝 Notes</h1>

      {/* Create note */}
      <div className="bg-thunder-card border border-thunder-border rounded-2xl p-4 mb-6">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Note title..."
          className="w-full bg-transparent text-thunder-text placeholder-thunder-muted
                     outline-none text-sm mb-3 border-b border-thunder-border pb-2"
        />
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Note content..."
          rows={3}
          className="w-full bg-transparent text-thunder-text placeholder-thunder-muted
                     outline-none text-sm resize-none"
        />
        <div className="flex justify-end mt-3">
          <button
            onClick={handleCreate}
            disabled={loading || !title.trim() || !content.trim()}
            className="px-4 py-2 bg-thunder-accent text-white rounded-xl text-sm
                       hover:bg-red-500 disabled:opacity-40 transition-colors duration-200"
          >
            Save Note
          </button>
        </div>
      </div>

      {/* Notes list */}
      <div className="grid grid-cols-1 gap-3">
        <AnimatePresence>
          {notes.length === 0 && (
            <p className="text-thunder-muted text-sm text-center py-8">No notes yet. Create one above.</p>
          )}
          {notes.map((note) => (
            <motion.div
              key={note.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="bg-thunder-card border border-thunder-border rounded-xl p-4
                         hover:border-thunder-accent transition-colors duration-200"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1 min-w-0">
                  <h3 className="text-thunder-text font-medium text-sm truncate">{note.title}</h3>
                  <p className="text-thunder-muted text-xs mt-1 leading-relaxed line-clamp-3">
                    {note.content}
                  </p>
                  <span className="text-xs text-thunder-muted mt-2 block">
                    {new Date(note.created_at).toLocaleDateString()}
                  </span>
                </div>
                <button
                  onClick={() => handleDelete(note.id)}
                  className="ml-3 text-thunder-muted hover:text-thunder-accent transition-colors
                             text-lg flex-shrink-0"
                  title="Delete note"
                >
                  ×
                </button>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
