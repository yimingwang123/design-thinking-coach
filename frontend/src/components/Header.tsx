import React from 'react';
import { formatDuration } from '../utils';

interface HeaderProps {
  isActive: boolean;
  startTime: number;
  messageCount: number;
  progressPercentage: number;
}

const Header: React.FC<HeaderProps> = ({
  isActive,
  startTime,
  messageCount,
  progressPercentage
}) => {
  return (
    <div className="glass border-0 border-b border-white/20 p-4 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">🧠</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Design Thinking Coach</h1>
          </div>
          <div 
            className={`px-3 py-1 rounded-full text-sm font-medium border border-current ${
              isActive 
                ? 'bg-green-500/20 text-green-300 animate-pulse-glow' 
                : 'bg-red-500/20 text-red-300'
            }`}
          >
            <span>{isActive ? '🟢 Aktiv' : '🔴 Inaktiv'}</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-6 text-white/80 text-sm">
          <div className="flex items-center space-x-2">
            <span>⏱️</span>
            <span>{formatDuration(startTime)}</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>💬</span>
            <span>{messageCount} Nachrichten</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>✅</span>
            <span>{Math.round(progressPercentage)}% Fortschritt</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;