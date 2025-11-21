// Authentication Types
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  created_at: string;
  is_active: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Search Types
export interface SearchFormData {
  FIRST_NAME: string;
  LAST_NAME: string;
  STREET1: string;
  STREET2: string;
  CITY: string;
  STATE: string;
  ZIP: string;
}

export interface KnowledgeCoreRequestPayload {
  LEAD_TRANS_DETAILS: {
    FIRST_NAME: string;
    LAST_NAME: string;
  };
  LEAD_ADDRESS: {
    STREET1: string;
    STREET2: string;
    CITY: string;
    STATE: string;
    ZIP: string;
  };
}

export interface SearchResult {
  [key: string]: any;
}

export interface ApiError {
  message: string;
  status?: number;
}