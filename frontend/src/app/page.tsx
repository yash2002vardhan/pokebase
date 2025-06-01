'use client';

import { useState, useRef } from 'react';
import { api } from '@/utils/api';

const COMMANDS = [
  '/get-pokemon-data',
  '/compare',
  '/strategy',
  '/team',
];

export default function Home() {
  const [command, setCommand] = useState('');
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState<number | null>(null);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Filtered command suggestions
  const isTypingCommand = command.startsWith('/') && !command.includes(' ');
  const filteredSuggestions =
    isTypingCommand && command.length > 1
      ? COMMANDS.filter((c) => c.startsWith(command))
      : [];

  const handleCommand = async (e: React.FormEvent) => {
    e.preventDefault();
    setResult(null);
    setError(null);
    setLoading(true);
    setShowSuggestions(false);

    // Save to history
    setHistory((prev) => (command.trim() ? [command, ...prev.slice(0, 19)] : prev));
    setHistoryIndex(null);

    const [cmd, ...args] = command.trim().split(/\s+/);
    try {
      if (cmd === '/get-pokemon-data' && args.length === 1) {
        const res = await api.get<string>(`/pokemon/${args[0]}`);
        setResult(res);
      } else if (cmd === '/compare' && args.length === 2) {
        const res = await api.get<string>(`/pokemon/compare/${args[0]}/${args[1]}`);
        setResult(res);
      } else if (cmd === '/strategy' && args.length >= 1) {
        const query = args.join(' ');
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/pokemon/strategy`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(query),
        });
        if (!res.ok) throw new Error('API call failed');
        const data = await res.json();
        setResult(data);
      } else if (cmd === '/team' && args.length >= 1) {
        const query = args.join(' ');
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/pokemon/team-building`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(query),
        });
        if (!res.ok) throw new Error('API call failed');
        const data = await res.json();
        setResult(data);
      } else {
        setError('Invalid command or arguments.');
      }
    } catch (err) {
      setError('Error processing command.');
    } finally {
      setLoading(false);
    }
  };

  // Handle input changes and show suggestions
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCommand(e.target.value);
    setError(null);
    setShowSuggestions(e.target.value.startsWith('/') && !e.target.value.includes(' '));
    setHistoryIndex(null);
  };

  // Handle suggestion click
  const handleSuggestionClick = (suggestion: string) => {
    setCommand(suggestion + ' ');
    setShowSuggestions(false);
    inputRef.current?.focus();
  };

  // Handle keyboard navigation for history and suggestions
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (showSuggestions && filteredSuggestions.length > 0) {
      if (e.key === 'ArrowDown' || e.key === 'Tab') {
        e.preventDefault();
        setCommand(filteredSuggestions[0] + ' ');
        setShowSuggestions(false);
        return;
      }
    }
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (history.length > 0) {
        const newIndex = historyIndex === null ? 0 : Math.min(historyIndex + 1, history.length - 1);
        setHistoryIndex(newIndex);
        setCommand(history[newIndex]);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (history.length > 0) {
        if (historyIndex === null) return;
        if (historyIndex === 0) {
          setHistoryIndex(null);
          setCommand('');
        } else {
          setHistoryIndex(historyIndex - 1);
          setCommand(history[historyIndex - 1]);
        }
      }
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-slate-900 py-8">
      <div className="bg-slate-800 p-8 rounded-lg shadow-lg w-full max-w-xl text-center mb-8 border border-slate-700">
        <h1 className="text-3xl font-bold mb-4 text-white">Pokebase Frontend</h1>
        <p className="text-slate-300 mb-2">Use slash commands to interact with the backend:</p>
        <ul className="text-slate-400 text-left mb-4 text-sm">
          <li><span className="text-blue-400">/get-pokemon-data &lt;name&gt;</span> — Get Pokémon description</li>
          <li><span className="text-blue-400">/compare &lt;name1&gt; &lt;name2&gt;</span> — Compare two Pokémon</li>
          <li><span className="text-blue-400">/strategy &lt;query&gt;</span> — Get strategy suggestion</li>
          <li><span className="text-blue-400">/team &lt;query&gt;</span> — Get team suggestion</li>
        </ul>
        <form onSubmit={handleCommand} className="flex flex-col items-center gap-4 relative">
          <div className="w-full relative">
            <input
              ref={inputRef}
              type="text"
              placeholder="Type a command, e.g. /get-pokemon-data pikachu"
              value={command}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              className={`border ${error ? 'border-red-500' : 'border-slate-600'} bg-slate-900 text-white p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500`}
              autoFocus
              autoComplete="off"
            />
            {showSuggestions && filteredSuggestions.length > 0 && (
              <ul className="absolute left-0 right-0 bg-slate-700 border border-slate-600 rounded mt-1 z-10 text-left">
                {filteredSuggestions.map((s) => (
                  <li
                    key={s}
                    className="px-4 py-2 cursor-pointer hover:bg-blue-600 text-white"
                    onClick={() => handleSuggestionClick(s)}
                  >
                    {s}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <button
            type="submit"
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-semibold disabled:opacity-50"
            disabled={loading}
          >
            {loading ? 'Processing...' : 'Run Command'}
          </button>
        </form>
        {error && <p className="text-red-400 mt-4">{error}</p>}
        {result && <pre className="mt-4 text-left whitespace-pre-wrap text-slate-200 bg-slate-900 p-4 rounded-lg border border-slate-700">{result}</pre>}
      </div>
    </main>
  );
}
