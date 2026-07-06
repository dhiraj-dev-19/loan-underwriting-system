import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

export const Sidebar: React.FC = () => {
  const navigate = useNavigate();

  return (
    <aside className="fixed left-0 top-0 h-full z-40 flex flex-col p-4 w-64">
      <div className="bg-white/70 dark:bg-inverse-surface/70 backdrop-blur-xl h-[calc(100vh-32px)] w-full rounded-xl shadow-soft flex flex-col p-6 overflow-y-auto custom-scrollbar">
        {/* Title branding */}
        <div className="mb-10 pt-4">
          <h1 className="font-headline text-[24px] font-bold text-primary tracking-tight leading-tight">AI Underwriter</h1>
          <p className="font-label text-[11px] font-semibold text-outline-variant opacity-70 uppercase tracking-widest mt-1">Enterprise Intelligence</p>
        </div>

        {/* Navigation list */}
        <nav className="flex-1 space-y-2">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg font-label text-sm font-semibold tracking-wide transition-all duration-200 ${
                isActive
                  ? 'text-primary bg-surface-container-low/80 border-r-4 border-primary shadow-sm'
                  : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-low/40'
              }`
            }
          >
            <span className="material-symbols-outlined text-[20px]">dashboard</span>
            <span>Dashboard</span>
          </NavLink>

          <NavLink
            to="/assessment"
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg font-label text-sm font-semibold tracking-wide transition-all duration-200 ${
                isActive
                  ? 'text-primary bg-surface-container-low/80 border-r-4 border-primary shadow-sm'
                  : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-low/40'
              }`
            }
          >
            <span className="material-symbols-outlined text-[20px]">security_update_good</span>
            <span>Underwriting</span>
          </NavLink>

          <NavLink
            to="/history"
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg font-label text-sm font-semibold tracking-wide transition-all duration-200 ${
                isActive
                  ? 'text-primary bg-surface-container-low/80 border-r-4 border-primary shadow-sm'
                  : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-low/40'
              }`
            }
          >
            <span className="material-symbols-outlined text-[20px]">account_balance_wallet</span>
            <span>Portfolio</span>
          </NavLink>

          <NavLink
            to="/settings"
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg font-label text-sm font-semibold tracking-wide transition-all duration-200 ${
                isActive
                  ? 'text-primary bg-surface-container-low/80 border-r-4 border-primary shadow-sm'
                  : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-low/40'
              }`
            }
          >
            <span className="material-symbols-outlined text-[20px]">settings</span>
            <span>Settings</span>
          </NavLink>
        </nav>

        {/* CTA & Profile */}
        <div className="mt-auto pt-6">
          <button 
            onClick={() => navigate('/assessment')}
            className="w-full bg-primary hover:bg-primary-container text-white py-3 rounded-xl font-label text-xs uppercase tracking-wider font-bold flex items-center justify-center gap-2 transition-all hover:scale-[1.02] active:scale-95 shadow-md"
          >
            <span className="material-symbols-outlined text-[18px]">add</span>
            <span>New Analysis</span>
          </button>

          <div className="mt-6 flex items-center gap-3 pt-6 border-t border-outline-variant/30">
            <div className="w-10 h-10 rounded-full border-2 border-primary-fixed overflow-hidden flex-shrink-0">
              <img
                className="w-full h-full object-cover"
                alt="Alex Rivera Portrait"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuCczZUUwQvC0ij2TdOyK9cle-9AoTwg-2HmYLxLCmYj3zeiflJ43K4i6ynmsPGj-r1zeXuwa3Uo3y1lwgQPK9oKvwKC5vNaz2Zw6sl8N-bs25RA9tK-DENIL0MEMcT3ihqNQ49cqxx1Boi7dC5nyWehb1Jqdi4gpAiUSfaTX8LsWIakZj7vSvV4PY0RSjaqShVO5j0T00RMvOgCQ0PbUOQKTj-bNiqNcQcnBPgRkuivWOkO6NX380GpjZj-zFvsGu_tQOuDz0SKUzny"
              />
            </div>
            <div>
              <p className="font-label text-sm font-bold text-on-surface leading-tight">Alex Rivera</p>
              <p className="font-label text-[10px] text-outline uppercase tracking-wider font-medium">Senior Lead</p>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};
