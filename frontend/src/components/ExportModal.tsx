import React from 'react';
import { Message, FrameworkStage } from '../types';
import { exportUtils } from '../utils';

interface ExportModalProps {
  show: boolean;
  messages: Message[];
  frameworkSteps: FrameworkStage[];
  frameworkProgress: Record<string, boolean>;
  progressPercentage: number;
  onClose: () => void;
}

const ExportModal: React.FC<ExportModalProps> = ({
  show,
  messages,
  frameworkSteps,
  frameworkProgress,
  progressPercentage,
  onClose
}) => {
  if (!show) return null;

  const structuredOutput = exportUtils.generateStructuredOutput(
    messages,
    frameworkSteps,
    frameworkProgress,
    progressPercentage
  );

  const handleCopyToClipboard = async () => {
    try {
      await exportUtils.copyToClipboard(structuredOutput);
      alert('✅ Strukturierte Ausgabe wurde in die Zwischenablage kopiert!');
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
      alert('❌ Fehler beim Kopieren in die Zwischenablage');
    }
  };

  const handleDownloadMarkdown = () => {
    exportUtils.downloadMarkdown(structuredOutput);
  };

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      onClick={handleBackdropClick}
    >
      <div className="glass-card rounded-xl p-6 max-w-4xl max-h-[80vh] overflow-y-auto m-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold text-white">📄 Strukturierte Ausgabe</h3>
          <button 
            onClick={onClose}
            className="text-white/60 hover:text-white text-2xl transition-colors"
          >
            &times;
          </button>
        </div>
        
        <div className="space-y-4 text-white">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button 
              onClick={handleCopyToClipboard}
              className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg transition-colors"
            >
              📋 In Zwischenablage kopieren
            </button>
            <button 
              onClick={handleDownloadMarkdown}
              className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition-colors"
            >
              📥 Als Markdown herunterladen
            </button>
          </div>
          
          <div className="bg-black/20 rounded-lg p-4 text-sm">
            <pre className="whitespace-pre-wrap font-mono text-white/90">
              {structuredOutput}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExportModal;