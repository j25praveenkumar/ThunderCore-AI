import React from 'react';
import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';

const NAV = [
  { path: '/chat',     icon: '⚡', label: 'Chat'     },
  { path: '/notes',    icon: '📝', label: 'Notes'    },
  { path: '/memory',   icon: '🧠', label: 'Memory'   },
  { path: '/history',  icon: '🕐', label: 'History'  },
  { path: '/settings', icon: '⚙️', label: 'Settings' },
];

export default function Sidebar() {
  return (
    <motion.aside
      initial={{ x: -80 }}
      animate={{ x: 0 }}
      className="w-20 flex flex-col items-center py-6 bg-thunder-surface border-r border-thunder-border"
    >
      {/* Logo */}
      <div className="mb-8 flex flex-col items-center">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-thunder-accent to-thunder-accent2
                        flex items-center justify-center text-lg font-bold glow-accent">
          ⚡
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-2 w-full px-2">
        {NAV.map(({ path, icon, label }) => (
          <NavLink
            key={path}
            to={path}
            className={({ isActive }) =>
              `flex flex-col items-center py-3 rounded-xl text-xs gap-1 transition-all duration-200
               ${isActive
                 ? 'bg-thunder-card text-thunder-accent border border-thunder-border glow-accent'
                 : 'text-thunder-muted hover:text-thunder-text hover:bg-thunder-card'
               }`
            }
          >
            <span className="text-lg">{icon}</span>
            <span className="font-medium">{label}</span>
          </NavLink>
        ))}
      </nav>
    </motion.aside>
  );
}
