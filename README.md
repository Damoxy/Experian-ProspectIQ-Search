# KC Experian Integration

### Frontend (React + Material UI)
- Clean, professional form interface for data input
- Fields: First Name, Last Name, Street Address 1 & 2, City, State, ZIP
- Loading indicators during API calls
- Error handling with user-friendly messages
- Dynamic table display showing only non-empty response data
- Responsive Material UI design

### Backend (FastAPI)
- RESTful API with automatic documentation
- Input validation using Pydantic models
- Experian API integration
- Data transformation and cleaning
- CORS configuration for frontend integration
- Comprehensive error handling

## 📋 Prerequisites

- **Node.js** (v16 or higher) and **npm**
- **Python** (v3.8 or higher)
- **Git** (for version control)

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd KC_Experian
```

### 2. Backend Setup

#### Create and Activate Virtual Environment
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Install Dependencies
```powershell
pip install -r requirements.txt
```

#### Environment Configuration
Copy the example environment file:
```powershell
cp .env.example .env
```

Edit `.env` if needed to update configuration:
```env
# Experian API Configuration
EXPERIAN_API_URL=<EXPERIAN_API_URL>
EXPERIAN_AUTH_TOKEN=<EXPERIAN_AUTH_TOKEN>

# Server Configuration
HOST=localhost
PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Frontend Setup

#### Navigate to Frontend Directory
```powershell
cd ../frontend
```

#### Install Dependencies
```powershell
npm install
```

## 🚀 Running the Application

### Option 1: Using VS Code Tasks (Recommended)
1. Open the project in VS Code
2. Use `Ctrl+Shift+P` and run "Tasks: Run Task"
3. Select "Start Full Application" to start both servers simultaneously
   - Or run "Start Backend Server" and "Start Frontend Server" individually

### Option 2: Manual Startup

#### Start Backend Server
```powershell
cd backend
.\venv\Scripts\Activate.ps1
cd app
python main.py
```
Backend will be available at: http://localhost:8000

#### Start Frontend Server (in a new terminal)
```powershell
cd frontend
npm start
```
Frontend will be available at: http://localhost:3000

## 🔍 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Main Endpoint: POST /search

**Request Body:**
```json
{
  "FIRST_NAME": "John",
  "LAST_NAME": "Doe", 
  "STREET1": "123 Main St",
  "STREET2": "Apt 4B",
  "CITY": "Dallas",
  "STATE": "TX",
  "ZIP": "75201"
}
```

**Response:**
- Cleaned JSON object with only non-empty fields from Experian API
- Error messages for invalid requests or API failures

## 📁 Project Structure

```
KC_Experian/
├── backend/
│   ├── .env                       # Environment variables (create from .env.example)
│   ├── .env.example               # Environment template
│   ├── requirements.txt           # Python dependencies
│   ├── venv/                      # Python virtual environment
│   └── app/
│       └── main.py                # FastAPI application
├── frontend/
│   ├── package.json               # Node.js dependencies and scripts
│   ├── tsconfig.json              # TypeScript configuration
│   ├── public/
│   │   └── index.html             # HTML template
│   └── src/
│       ├── App.tsx                # Main React component
│       ├── index.tsx              # React entry point
│       ├── types.ts               # TypeScript type definitions
│       ├── components/
│       │   ├── SearchForm.tsx     # Form component
│       │   └── ResultsTable.tsx   # Results display component
│       └── services/
│           └── api.ts             # API service functions
└── README.md                      # This file
```

## 🧪 Testing the Application

1. **Start both servers** (backend on :8000, frontend on :3000)
2. **Open http://localhost:3000** in your browser
3. **Fill out the search form** with contact information:
   - Last Name is required
   - Other fields are optional but recommended for better results
4. **Click "Search"** to query the Experian API
5. **View results** in the table below (only populated fields will be displayed)

## 🛡️ Error Handling

The application includes comprehensive error handling:
- **Frontend**: User-friendly error messages for network issues
- **Backend**: Detailed logging and proper HTTP status codes
- **Validation**: Input validation with clear error messages
- **Timeouts**: 30-second timeout for Experian API requests

## 🔧 Development

### Backend Development
- The FastAPI server runs with auto-reload enabled in development mode
- API documentation is automatically generated at `/docs`
- Environment variables control configuration

### Frontend Development  
- React development server includes hot-reload
- Material UI provides consistent theming
- TypeScript ensures type safety

### VS Code Integration
- Tasks are configured for easy development workflow
- Use Command Palette (`Ctrl+Shift+P`) → "Tasks: Run Task" for quick access

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change ports in `.env` (backend) or update proxy in `package.json` (frontend)

2. **Virtual Environment Issues**
   - Recreate venv: `rm -rf venv` then `python -m venv venv`

3. **Dependencies Not Installing**
   - Ensure Python/Node.js versions meet requirements
   - Clear npm cache: `npm cache clean --force`

4. **CORS Errors**
   - Verify `ALLOWED_ORIGINS` in `.env` matches frontend URL

5. **Experian API Errors**
   - Check `EXPERIAN_AUTH_TOKEN` in `.env`
   - Verify network connectivity to Experian endpoints

### Getting Help
- Check browser developer console for frontend issues
- Check terminal output for backend issues  
- Review API documentation at http://localhost:8000/docs

## 📝 Notes

- The Experian API token used is for demonstration purposes
- All response data is cleaned to remove empty/null values
- The application is configured for development - additional security measures needed for production
- Material UI provides consistent, professional styling throughout the interface