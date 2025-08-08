import { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Chat from './components/Chat';
import ExportModal from './components/ExportModal';
import Footer from './components/Footer';
import { Message, FrameworkStage } from './types';
import { 
  chatAPI, 
  sessionUtils, 
  updateFrameworkProgress,
  exportUtils
} from './utils';

function App() {
  // State management
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [isActive] = useState(true);
  const [startTime] = useState(Date.now());
  const [showExport, setShowExport] = useState(false);
  const [frameworkLoading, setFrameworkLoading] = useState(true);
  const [frameworkProgress, setFrameworkProgress] = useState<Record<string, boolean>>({});
  const [frameworkSteps, setFrameworkSteps] = useState<FrameworkStage[]>([]);

  // Computed values
  const progressPercentage = frameworkSteps.length > 0 
    ? Math.round((Object.values(frameworkProgress).filter(v => v === true).length / frameworkSteps.length) * 100)
    : 0;
  
  const messageCount = messages.filter(m => m.type === 'user').length;

  // Initialize app
  useEffect(() => {
    loadFrameworkStages();
  }, []);

  // Load framework stages from API
  const loadFrameworkStages = async () => {
    setFrameworkLoading(true);
    try {
      const stages = await chatAPI.loadFrameworkStages();
      setFrameworkSteps(stages);
      
      // Initialize progress tracking for all loaded stages
      const initialProgress: Record<string, boolean> = {};
      stages.forEach(step => {
        initialProgress[step.key] = false;
      });
      setFrameworkProgress(initialProgress);
      
      console.log('Framework stages loaded:', stages);
    } catch (error) {
      console.error('Failed to load framework stages:', error);
      setFrameworkSteps([]);
      setFrameworkProgress({});
    } finally {
      setFrameworkLoading(false);
    }
  };

  // Send message handler
  const handleSendMessage = async () => {
    if (!newMessage.trim() || loading) return;

    const userMessage = newMessage.trim();
    setNewMessage('');
    setLoading(true);

    // Add user message
    const userMsg: Message = {
      type: 'user',
      content: userMessage,
      timestamp: Date.now()
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      const sessionId = sessionUtils.getSessionId();
      const response = await chatAPI.sendMessage(userMessage, sessionId);

      // Add assistant response
      const assistantMsg: Message = {
        type: 'assistant',
        content: response.message || response.reply || 'Keine Antwort erhalten',
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, assistantMsg]);

      // Update framework progress
      const newProgress = updateFrameworkProgress(
        assistantMsg.content,
        frameworkSteps,
        frameworkProgress
      );
      setFrameworkProgress(newProgress);

    } catch (error) {
      console.error('Chat Error Details:', error);
      
      let errorMessage = 'Entschuldigung, es gab einen Fehler bei der Verbindung.';
      
      if (error instanceof Error) {
        if (error.message.includes('Failed to fetch')) {
          errorMessage += ' Bitte stellen Sie sicher, dass der Backend-Server läuft (http://localhost:8000).';
        } else if (error.message.includes('404')) {
          errorMessage += ' API-Endpoint nicht gefunden. Überprüfen Sie die Backend-Konfiguration.';
        }
      }
      
      const errorMsg: Message = {
        type: 'assistant',
        content: errorMessage,
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  // Generate structured summary
  const handleGenerateStructuredSummary = async () => {
    if (progressPercentage < 100) return;

    setLoading(true);

    try {
      // Create a structured prompt for the AI
      const completedSteps = frameworkSteps.filter(step => frameworkProgress[step.key]);
      const summaryPrompt = `Bitte erstellen Sie eine strukturierte Zusammenfassung basierend auf unserem Design Thinking Prozess. Berücksichtigen Sie dabei alle Framework-Stufen, die wir durchlaufen haben:

${completedSteps.map(step => 
`- ${step.icon} ${step.title}: ${step.description}`
).join('\n')}

Erstellen Sie eine detaillierte Analyse mit folgenden Abschnitten:
1. Problemübersicht
2. Ursachenanalyse
3. Lösungsansätze
4. Zielgruppen
5. Implementierungsplan
6. Erfolgsmessung

Nutzen Sie alle relevanten Informationen aus unserem Gespräch und strukturieren Sie diese in einem professionellen Format.`;

      const sessionId = sessionUtils.getSessionId();
      const response = await chatAPI.sendMessage(summaryPrompt, sessionId);

      // Add the structured summary as a special message
      const summaryMsg: Message = {
        type: 'assistant',
        content: `## 📋 Strukturierte Design Thinking Zusammenfassung\n\n${response.message || response.reply}`,
        timestamp: Date.now(),
        isStructuredSummary: true
      };
      setMessages(prev => [...prev, summaryMsg]);

    } catch (error) {
      console.error('Fehler bei der Zusammenfassung:', error);
      
      const errorMsg: Message = {
        type: 'assistant',
        content: '❌ Fehler bei der Erstellung der strukturierten Zusammenfassung. Bitte versuchen Sie es erneut.',
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  // Execute commands
  const handleExecuteCommand = (command: string) => {
    if (command === '/reset') {
      setMessages([]);
      // Reset framework progress using current framework steps
      const resetProgress: Record<string, boolean> = {};
      frameworkSteps.forEach(step => {
        resetProgress[step.key] = false;
      });
      setFrameworkProgress(resetProgress);
      
      const systemMsg: Message = {
        type: 'system',
        content: '🔄 Session wurde zurückgesetzt.',
        timestamp: Date.now()
      };
      setMessages([systemMsg]);
    } else if (command === '/save') {
      exportUtils.downloadSession(messages, frameworkProgress, progressPercentage);
      
      const systemMsg: Message = {
        type: 'system',
        content: '💾 Session wurde als JSON-Datei gespeichert.',
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, systemMsg]);
    } else if (command === '/export') {
      setShowExport(true);
    }
  };

  // Send example message
  const handleSendExampleMessage = (question: string) => {
    setNewMessage(question);
    // Will trigger send on next render when newMessage updates
    setTimeout(handleSendMessage, 0);
  };

  // Reload framework
  const handleReloadFramework = async () => {
    try {
      await loadFrameworkStages();
      const systemMsg: Message = {
        type: 'system',
        content: '✅ Framework-Stufen wurden neu geladen.',
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, systemMsg]);
    } catch (error) {
      const systemMsg: Message = {
        type: 'system',
        content: '❌ Fehler beim Neuladen der Framework-Stufen.',
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, systemMsg]);
    }
  };

  return (
    <div className="h-full bg-gradient-to-br from-blue-900 via-purple-900 to-pink-900">
      
      {/* Header with Status */}
      <Header
        isActive={isActive}
        startTime={startTime}
        messageCount={messageCount}
        progressPercentage={progressPercentage}
      />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto p-4 h-[calc(100vh-120px)]">
        <div className="grid lg:grid-cols-4 gap-6 h-full">
        
          {/* Sidebar - Framework Progress & Controls */}
          <Sidebar
            frameworkSteps={frameworkSteps}
            frameworkProgress={frameworkProgress}
            frameworkLoading={frameworkLoading}
            progressPercentage={progressPercentage}
            onReloadFramework={handleReloadFramework}
            onExecuteCommand={handleExecuteCommand}
            onSendExampleMessage={handleSendExampleMessage}
            onGenerateStructuredSummary={handleGenerateStructuredSummary}
          />

          {/* Main Chat Area */}
          <Chat
            messages={messages}
            newMessage={newMessage}
            loading={loading}
            onMessageChange={setNewMessage}
            onSendMessage={handleSendMessage}
          />
        </div>
      </div>

      {/* Export Modal */}
      <ExportModal
        show={showExport}
        messages={messages}
        frameworkSteps={frameworkSteps}
        frameworkProgress={frameworkProgress}
        progressPercentage={progressPercentage}
        onClose={() => setShowExport(false)}
      />

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;