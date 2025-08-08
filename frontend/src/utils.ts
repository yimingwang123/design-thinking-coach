import { Message, FrameworkStage, ChatResponse, ConfigResponse } from './types';

// API utilities
const getBackendURL = (): string => {
  return (window as any).backendURL || '';
};

export const chatAPI = {
  sendMessage: async (message: string, sessionId: string): Promise<ChatResponse> => {
    const backendURL = getBackendURL();
    const response = await fetch(`${backendURL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: sessionId,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  loadFrameworkStages: async (): Promise<FrameworkStage[]> => {
    const backendURL = getBackendURL();
    const response = await fetch(`${backendURL}/api/config`);
    
    if (!response.ok) {
      throw new Error(`API config endpoint failed: ${response.status}`);
    }
    
    const data: ConfigResponse = await response.json();
    
    if (data.config?.framework?.stages) {
      return data.config.framework.stages.map(stage => ({
        key: stage.key,
        title: stage.title,
        description: stage.description,
        icon: stage.icon || '📌',
        keywords: stage.keywords || []
      }));
    } else {
      throw new Error('Framework stages not found in config');
    }
  },
};

// Session management
export const sessionUtils = {
  getSessionId: (): string => {
    let sessionId = localStorage.getItem('dt-session-id');
    if (!sessionId) {
      sessionId = 'session-' + Date.now();
      localStorage.setItem('dt-session-id', sessionId);
    }
    return sessionId;
  },
};

// Time formatting
export const formatTime = (timestamp: number): string => {
  return new Date(timestamp).toLocaleTimeString('de-DE', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

export const formatDuration = (startTime: number): string => {
  const duration = Date.now() - startTime;
  const minutes = Math.floor(duration / 60000);
  const seconds = Math.floor((duration % 60000) / 1000);
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
};

// Markdown formatting
export const formatMarkdown = (text: string): string => {
  // Simple markdown parsing - in a real app, consider using a proper markdown library
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
    .replace(/## (.*?)(?=\n|$)/g, '<h2 class="text-lg font-bold text-white mt-4 mb-2">$1</h2>')
    .replace(/# (.*?)(?=\n|$)/g, '<h1 class="text-xl font-bold text-white mt-4 mb-2">$1</h1>');
};

// Framework progress tracking
export const updateFrameworkProgress = (
  content: string,
  frameworkSteps: FrameworkStage[],
  currentProgress: Record<string, boolean>
): Record<string, boolean> => {
  const lower = content.toLowerCase();
  const newProgress = { ...currentProgress };
  
  frameworkSteps.forEach(stage => {
    const keywords = stage.keywords || [];
    const found = keywords.some(keyword => lower.includes(keyword.toLowerCase()));
    
    if (found) {
      newProgress[stage.key] = true;
    }
  });
  
  return newProgress;
};

// Export utilities
export const exportUtils = {
  generateStructuredOutput: (
    messages: Message[],
    frameworkSteps: FrameworkStage[],
    frameworkProgress: Record<string, boolean>,
    progressPercentage: number
  ): string => {
    const completedSteps = frameworkSteps.filter(step => 
      frameworkProgress[step.key]
    );

    let output = `# Design Thinking Analyse\n\n`;
    output += `**Datum:** ${new Date().toLocaleDateString('de-DE')}\n`;
    output += `**Fortschritt:** ${progressPercentage}%\n\n`;

    completedSteps.forEach(step => {
      output += `## ${step.icon} ${step.title}\n`;
      output += `${step.description}\n\n`;
      
      // Extract relevant messages for this step
      const relevantMessages = messages.filter(msg => 
        msg.type === 'assistant' && 
        msg.content.toLowerCase().includes(step.key.toLowerCase())
      );
      
      if (relevantMessages.length > 0) {
        output += relevantMessages[0].content + '\n\n';
      }
    });

    output += `---\n\n`;
    output += `**Generiert durch Design Thinking Coach v1.0**\n`;
    output += `**Session-Nachrichten:** ${messages.filter(m => m.type === 'user').length}\n`;

    return output;
  },

  downloadMarkdown: (content: string): void => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `design-thinking-analyse-${new Date().toISOString().split('T')[0]}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },

  downloadSession: (
    messages: Message[],
    frameworkProgress: Record<string, boolean>,
    progressPercentage: number
  ): void => {
    const sessionData = {
      timestamp: new Date().toISOString(),
      messages,
      frameworkProgress,
      progressPercentage
    };

    const blob = new Blob([JSON.stringify(sessionData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `design-thinking-session-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  },

  copyToClipboard: async (content: string): Promise<void> => {
    await navigator.clipboard.writeText(content);
  },
};

// Example questions
export const exampleQuestions = [
  "Unser Team hat Kommunikationsprobleme in Remote-Meetings",
  "Kunden finden unsere Website zu kompliziert", 
  "Mitarbeiter sind unzufrieden mit dem Onboarding-Prozess",
  "Wir brauchen ein besseres System für Projektmanagement",
  "Unsere App hat eine hohe Absprungrate"
];