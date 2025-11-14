export interface SearchFormData {
  FIRST_NAME: string;
  LAST_NAME: string;
  STREET1: string;
  STREET2: string;
  CITY: string;
  STATE: string;
  ZIP: string;
}

export interface ExperianRequestPayload {
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