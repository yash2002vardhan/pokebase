# Pokebase 🎮

A modern, interactive Pokémon information and strategy platform that combines real-time Pokémon data with AI-powered insights. Built with FastAPI backend and Next.js frontend, featuring a beautiful glassmorphism UI with animated Pokémon bubbles.

## 🌟 Features

### Core Functionality
- **Pokémon Data Retrieval**: Get comprehensive information about any Pokémon including stats, abilities, moves, and types
- **Pokémon Comparison**: Side-by-side comparison of two Pokémon with detailed analysis
- **AI-Powered Strategy**: Generate battle strategies using Google's Gemini AI
- **Team Building**: Get AI recommendations for building competitive Pokémon teams
- **Interactive UI**: Beautiful glassmorphism design with floating, physics-based Pokémon bubbles

### Technical Features
- **RESTful API**: Well-structured FastAPI backend with comprehensive endpoints
- **Real-time Monitoring**: Prometheus metrics integration for API monitoring
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Modern Frontend**: Next.js 15 with TypeScript, Material-UI, and Framer Motion
- **Responsive Design**: Mobile-friendly interface with smooth animations
- **Error Handling**: Robust error handling and logging throughout the application

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/                 # API endpoints and routing
│   │   ├── endpoints.py     # Main API endpoints
│   │   └── router.py        # API router configuration
│   ├── config/              # Configuration modules
│   │   ├── env.py          # Environment settings
│   │   ├── llm.py          # Gemini AI configuration
│   │   ├── logging.py      # Logging setup
│   │   └── metrics.py      # Prometheus metrics
│   ├── service/             # Business logic layer
│   │   └── pokemon.py      # Pokémon data service
│   ├── utils/               # Utility functions
│   │   ├── parse_pokemon_data.py  # Data parsing and role assignment
│   │   ├── prompts.py             # AI prompt templates
│   │   └── generate_descriptions.py  # Description generation
│   └── main.py             # FastAPI application entry point
├── tests/                  # Test suite
└── pyproject.toml         # Python dependencies and configuration
```

### Frontend (Next.js)
```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx        # Main application page
│   │   ├── layout.tsx      # App layout and theme
│   │   └── globals.css     # Global styles
│   ├── utils/
│   │   └── api.ts          # API communication utilities
│   ├── mui-provider.tsx    # Material-UI theme provider
│   └── mui-theme.ts        # Custom theme configuration
├── public/                 # Static assets
└── package.json           # Node.js dependencies
```

## 🚀 Getting Started

### Prerequisites
- **Python 3.12** (for backend)
- **Node.js 18+** (for Next.js frontend)
- **PDM** (Python Dependency Manager)
- **Google Gemini API Key**

### Clone the Repository

1. **Clone the repository**
   ```bash
   git clone https://github.com/yash2002vardhan/pokebase.git
   cd pokebase
   ```

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies using PDM**
   ```bash
   pdm install
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   ```

4. **Run the development server**
   ```bash
   pdm run dev
   ```
   The API will be available at `http://localhost:8000`

5. **View API documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`
   - Metrics: `http://localhost:8000/metrics`

### Frontend Setup

1. **Navigate back to project root and then to frontend directory**
   ```bash
   # If you're in the backend directory, go back to project root first
   cd ..
   
   # Then navigate to frontend directory  
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   # Create .env.local file
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
   ```

4. **Run the Next.js development server**
   ```bash
   npm run dev
   ```
   The Next.js application will be available at `http://localhost:3000`

## 📖 API Documentation

### Endpoints

#### Pokémon Information
- **GET** `/api/v1/pokemon/{pokemon_name}`
  - Get detailed information about a specific Pokémon
  - Returns: Comprehensive Pokémon data with AI-generated description

#### Pokémon Comparison
- **GET** `/api/v1/pokemon/compare/{pokemon1}/{pokemon2}`
  - Compare two Pokémon side by side
  - Returns: Detailed comparison with strengths and weaknesses

#### Strategy Generation
- **POST** `/api/v1/pokemon/strategy`
  - Generate AI-powered battle strategies
  - Body: `"your strategy query"`
  - Returns: Detailed strategy recommendations

#### Team Building
- **POST** `/api/v1/pokemon/team-building`
  - Get AI recommendations for team composition
  - Body: `"your team building requirements"`
  - Returns: Suggested team with explanations

#### Health Check
- **GET** `/api/v1/health`
  - Check API health status
  - Returns: `{"status": "healthy"}`

### Example Usage

```bash
# Get Pokémon data
curl http://localhost:8000/api/v1/pokemon/pikachu

# Compare Pokémon
curl http://localhost:8000/api/v1/pokemon/compare/pikachu/charizard

# Generate strategy
curl -X POST http://localhost:8000/api/v1/pokemon/strategy \
  -H "Content-Type: application/json" \
  -d '"How to counter Dragon-type Pokémon?"'

# Team building
curl -X POST http://localhost:8000/api/v1/pokemon/team-building \
  -H "Content-Type: application/json" \
  -d '"Build a balanced team for competitive play"'
```

## 🎮 Frontend Usage

### Command Interface
The frontend features a terminal-like command interface with the following commands:

- `/get-pokemon-data <pokemon_name>` - Get detailed Pokémon information
- `/compare <pokemon1> <pokemon2>` - Compare two Pokémon
- `/strategy <query>` - Generate battle strategies
- `/team <requirements>` - Get team building recommendations

### Interactive Features
- **Auto-completion**: Type `/` to see available commands
- **Command History**: Use arrow keys to navigate through previous commands
- **Animated Bubbles**: Floating Pokémon bubbles
- **Glassmorphism UI**: Modern, translucent design with blur effects
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🧪 Testing

### Backend Tests
```bash
cd backend
PYTHONPATH=. pdm run test
```

The test suite includes:
- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Service Tests**: External API integration testing
- **Mock Testing**: Isolated testing with mocked dependencies

### Test Coverage
- API endpoints with various scenarios
- Error handling and edge cases
- Service layer functionality
- Data parsing and validation

## 🔧 Configuration

### Backend Configuration
- **Environment Variables**: Configured via `.env` file
- **Logging**: Structured logging with different levels
- **Metrics**: Prometheus integration for monitoring
- **CORS**: Configurable cross-origin resource sharing

### Frontend Configuration
- **API URL**: Configurable backend endpoint
- **Theme**: Material-UI dark theme with custom Pokémon colors
- **Animations**: Framer Motion and custom CSS animations
- **Performance**: Next.js optimization with Turbopack

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **aiohttp**: Asynchronous HTTP client for external API calls
- **Google Gemini AI**: Advanced language model for strategy generation
- **Prometheus**: Metrics collection and monitoring
- **pytest**: Comprehensive testing framework

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe JavaScript development
- **Material-UI**: React component library with theming
- **Framer Motion**: Animation library for smooth interactions
- **Tailwind CSS**: Utility-first CSS framework

### External APIs
- **PokéAPI**: Comprehensive Pokémon data source
- **Google Gemini**: AI-powered content generation

## 📊 Monitoring and Metrics

The application includes comprehensive monitoring:
- **Request Metrics**: Track API usage and performance
- **Error Tracking**: Monitor and log application errors
- **Health Checks**: Ensure service availability
- **Performance Monitoring**: Track response times and throughput

Access metrics at: `http://localhost:8000/metrics`

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **PokéAPI** for providing comprehensive Pokémon data
- **Google Gemini** for AI-powered content generation
- **Pokémon Company** for the amazing Pokémon universe
- **Open Source Community** for the fantastic tools and libraries

## 🐛 Known Issues

- Gemini API key required for strategy and team building features
- Rate limiting may apply for external API calls
- Some Pokémon sprites may not load due to external dependencies

## 🔮 Future Enhancements

- [ ] User authentication and profiles
- [ ] Pokémon team save/load functionality
- [ ] Battle simulation features
- [ ] Real-time multiplayer capabilities
- [ ] Advanced filtering and search options
- [ ] Mobile app development
- [ ] Pokédex completion tracking

---

**Built with ❤️ by Yashvardhan Goel**

For questions or support, please open an issue on GitHub.

