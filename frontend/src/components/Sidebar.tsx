import React from 'react';
import { FrameworkStage } from '../types';
import { exampleQuestions } from '../utils';

interface SidebarProps {
  frameworkSteps: FrameworkStage[];
  frameworkProgress: Record<string, boolean>;
  frameworkLoading: boolean;
  progressPercentage: number;
  onReloadFramework: () => void;
  onExecuteCommand: (command: string) => void;
  onSendExampleMessage: (question: string) => void;
  onGenerateStructuredSummary: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  frameworkSteps,
  frameworkProgress,
  frameworkLoading,
  progressPercentage,
  onReloadFramework,
  onExecuteCommand,
  onSendExampleMessage,
  onGenerateStructuredSummary
}) => {
  return (
    <div className="lg:col-span-1 space-y-4 overflow-y-auto custom-scrollbar">
      
      {/* Framework Progress */}
      <div className="sidebar-glass rounded-xl p-4 backdrop-blur-sm">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
          <span className="mr-2">🎯</span>
          Framework Fortschritt
        </h3>
        
        {/* Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between text-sm text-white/70 mb-2">
            <span>Fortschritt</span>
            <span>{progressPercentage}%</span>
          </div>
          <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-purple-500 to-pink-500 h-full rounded-full transition-all duration-500 progress-transition"
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        </div>

        {/* Framework stages */}
        <div className="space-y-2">
          {/* Loading state */}
          {frameworkLoading && (
            <div className="flex items-center p-4 rounded-lg bg-white/5 border border-white/10">
              <div className="flex space-x-1 mr-3">
                <div className="w-2 h-2 bg-white/80 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-white/80 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-white/80 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
              <div className="text-white/70 text-sm">Lade Framework-Stufen...</div>
            </div>
          )}
          
          {/* Framework stages (loaded from master config) */}
          {frameworkSteps.map((stage) => (
            <div key={stage.key} className="flex items-center p-2 rounded-lg bg-white/5 border border-white/10">
              <div 
                className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                  frameworkProgress[stage.key] 
                    ? 'bg-green-500/20 text-green-400' 
                    : 'bg-white/10 text-white/50'
                }`}
              >
                <span className="text-sm">{stage.icon || '📌'}</span>
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium text-white">{stage.title}</div>
                <div className="text-xs text-white/60">{stage.description}</div>
              </div>
              <div className="ml-3">
                {frameworkProgress[stage.key] && (
                  <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                  </svg>
                )}
              </div>
            </div>
          ))}
          
          {/* Message when no framework stages loaded */}
          {!frameworkLoading && frameworkSteps.length === 0 && (
            <div className="text-center p-4 rounded-lg bg-red-500/10 border border-red-500/20">
              <div className="text-red-300 text-sm">⚠️ Konnte Framework-Stufen nicht laden</div>
              <div className="text-red-300/70 text-xs mt-1">Überprüfen Sie die Backend-Verbindung</div>
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="sidebar-glass rounded-xl p-4">
        <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
          <span className="mr-2">⚡</span>
          Schnellaktionen
        </h3>
        <div className="space-y-2">
          <button
            onClick={onReloadFramework}
            disabled={frameworkLoading}
            className="w-full bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 py-2 px-3 rounded-lg text-sm flex items-center space-x-2 transition-all duration-200 disabled:opacity-50"
          >
            <span>🔄</span>
            <span>{frameworkLoading ? 'Lädt...' : 'Framework neu laden'}</span>
          </button>
          <button
            onClick={() => onExecuteCommand('/reset')}
            className="w-full bg-red-500/20 hover:bg-red-500/30 text-red-300 py-2 px-3 rounded-lg text-sm flex items-center space-x-2 transition-all duration-200"
          >
            <span>🗑️</span>
            <span>Session zurücksetzen</span>
          </button>
          <button
            onClick={() => onExecuteCommand('/save')}
            className="w-full bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 py-2 px-3 rounded-lg text-sm flex items-center space-x-2 transition-all duration-200"
          >
            <span>💾</span>
            <span>Session speichern</span>
          </button>
          <button
            onClick={onGenerateStructuredSummary}
            disabled={progressPercentage < 100}
            className={`w-full py-2 px-3 rounded-lg text-sm flex items-center space-x-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed ${
              progressPercentage >= 100 
                ? 'bg-green-500/40 border border-green-400 animate-pulse text-green-300 hover:bg-green-500/30' 
                : 'bg-green-500/20 text-green-300'
            }`}
          >
            <span>📄</span>
            <span>
              {progressPercentage >= 100 
                ? 'Zusammenfassung erstellen' 
                : `Zusammenfassung (${progressPercentage}%)`
              }
            </span>
          </button>
        </div>
      </div>

      {/* Quick Start Examples */}
      <div className="sidebar-glass rounded-xl p-4">
        <h3 className="text-lg font-semibold text-white mb-3 flex items-center">
          <span className="mr-2">🚀</span>
          Schnellstart
        </h3>
        <div className="space-y-2">
          {exampleQuestions.map((question, index) => (
            <button
              key={index}
              onClick={() => onSendExampleMessage(question)}
              className="w-full text-left p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 text-white/90 text-xs transition-all duration-200"
            >
              {question}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Sidebar;