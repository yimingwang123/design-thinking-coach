// Message types
export interface Message {
  type: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: number;
  isStructuredSummary?: boolean;
}

// Framework stage types
export interface FrameworkStage {
  key: string;
  title: string;
  description: string;
  icon: string;
  keywords: string[];
}

// API response types
export interface ChatResponse {
  message?: string;
  reply?: string;
}

export interface ConfigResponse {
  config: {
    framework: {
      stages: FrameworkStage[];
    };
  };
}

// App state types
export interface AppState {
  messages: Message[];
  newMessage: string;
  loading: boolean;
  isActive: boolean;
  startTime: number;
  showExport: boolean;
  frameworkLoading: boolean;
  frameworkProgress: Record<string, boolean>;
  frameworkSteps: FrameworkStage[];
}