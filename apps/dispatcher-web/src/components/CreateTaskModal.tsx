import React, { useState } from 'react';

interface CreateTaskModalProps {
  onClose: () => void;
  onSubmit: (title: string, description: string) => Promise<void>;
}

const CreateTaskModal: React.FC<CreateTaskModalProps> = ({ onClose, onSubmit }) => {
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await onSubmit(title, desc);
    setLoading(false);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-zinc-900 border border-zinc-800 p-6 rounded-xl shadow-2xl w-full max-w-md">
        <h2 className="text-xl font-bold text-white mb-4">✨ Create New Agent Task</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm text-zinc-400 mb-1">Task Title</label>
            <input 
              required
              className="w-full bg-zinc-950 border border-zinc-800 rounded-lg p-2 text-white focus:border-blue-500 outline-none"
              placeholder="e.g. Implement login screen"
              value={title}
              onChange={e => setTitle(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm text-zinc-400 mb-1">Description & Agent Context</label>
            <textarea 
              required
              className="w-full bg-zinc-950 border border-zinc-800 rounded-lg p-2 text-white focus:border-blue-500 outline-none min-h-[100px]"
              placeholder="Provide exact details for the Developer Agent..."
              value={desc}
              onChange={e => setDesc(e.target.value)}
            />
          </div>
          <div className="flex justify-end gap-3 mt-4">
            <button type="button" onClick={onClose} className="px-4 py-2 text-zinc-400 hover:text-white transition-colors">Cancel</button>
            <button disabled={loading} type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors">
              {loading ? 'Dispatching...' : 'Dispatch Task 🚀'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
export default CreateTaskModal;
