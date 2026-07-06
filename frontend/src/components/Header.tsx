import React from 'react';
import { NavLink } from 'react-router-dom';

export const Header: React.FC = () => {
  return (
    <header className="flex justify-between items-center w-full px-8 py-4 sticky top-0 z-30 bg-[#F8FAF3]/70 backdrop-blur-lg border-b border-outline-variant/10">
      <div className="flex items-center gap-8">
        <div className="flex gap-6">
          <NavLink
            to="/pipeline"
            className={({ isActive }) =>
              `font-body text-sm font-semibold transition-all pb-1 border-b-2 ${
                isActive ? 'text-primary border-primary' : 'text-on-surface-variant border-transparent hover:text-primary'
              }`
            }
          >
            Pipeline
          </NavLink>
          <NavLink
            to="/history"
            className={({ isActive }) =>
              `font-body text-sm font-semibold transition-all pb-1 border-b-2 ${
                isActive ? 'text-primary border-primary' : 'text-on-surface-variant border-transparent hover:text-primary'
              }`
            }
          >
            Archived
          </NavLink>
          <NavLink
            to="/reports"
            className={({ isActive }) =>
              `font-body text-sm font-semibold transition-all pb-1 border-b-2 ${
                isActive ? 'text-primary border-primary' : 'text-on-surface-variant border-transparent hover:text-primary'
              }`
            }
          >
            Reports
          </NavLink>
        </div>
      </div>
      
      <div className="flex items-center gap-6">
        {/* Search Input */}
        <div className="relative w-64 hidden sm:block">
          <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline">search</span>
          <input
            className="w-full pl-10 pr-4 py-2 bg-surface-container-low border-none rounded-full text-xs font-body focus:ring-2 focus:ring-primary focus:bg-white transition-all outline-none"
            placeholder="Search applications..."
            type="text"
          />
        </div>

        {/* Notifications and Help */}
        <button className="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors text-[20px] outline-none">
          notifications
        </button>
        <button className="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors text-[20px] outline-none">
          help_outline
        </button>
      </div>
    </header>
  );
};
