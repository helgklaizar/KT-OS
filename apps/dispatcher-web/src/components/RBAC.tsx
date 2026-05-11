import React, { createContext, useContext, useState } from 'react';

type Role = 'Admin' | 'Junior';

interface RBACContextType {
  role: Role;
  setRole: (role: Role) => void;
  canManageAgents: boolean;
}

const RBACContext = createContext<RBACContextType | undefined>(undefined);

export function RBACProvider({ children }: { children: React.ReactNode }) {
  const [role, setRole] = useState<Role>('Admin');
  
  return (
    <RBACContext.Provider value={{ role, setRole, canManageAgents: role === 'Admin' }}>
      <div className="fixed top-4 right-4 z-50 bg-zinc-800 p-2 rounded-lg flex items-center gap-2 border border-zinc-700 shadow-xl">
        <span className="text-xs font-semibold text-zinc-400">🛡️ SOC2 RBAC:</span>
        <select 
          value={role} 
          onChange={e => setRole(e.target.value as Role)} 
          className="bg-zinc-900 text-white text-sm rounded px-2 py-1 outline-none border border-zinc-700 focus:border-blue-500"
        >
          <option value="Admin">Admin (Full Access)</option>
          <option value="Junior">Junior (Read-Only)</option>
        </select>
      </div>
      {children}
    </RBACContext.Provider>
  );
}

export const useRBAC = () => {
  const context = useContext(RBACContext);
  if (!context) throw new Error("useRBAC must be used within RBACProvider");
  return context;
};
