# AI Travel Master

A sophisticated multi-agent AI travel system built with **LangGraph** that coordinates between specialized assistants to provide comprehensive travel planning and booking services.

## Overview

The AI Travel Master is a **supervisor-based multi-agent system** that manages three specialized travel assistants:

- **Flight Assistant** - Searches, books, cancels, and modifies flight reservations
- **Accommodation Assistant** - Handles hotel and lodging searches, bookings, and changes  
- **Car Rental Assistant** - Manages car rental searches, bookings, and modifications

Each assistant provides **four core capabilities**:
- **Search** - Real-time search using Tavily API for current availability and pricing
- **Book** - Complete booking process with confirmation numbers
- **Cancel** - Cancellation handling with refund processing
- **Change** - Modification of existing reservations

## Architecture

![AI Travel Master System Architecture](static/travel_master_graph.png)

*The diagram above shows the LangGraph flow visualization of the AI Travel Master system, illustrating how the supervisor coordinates with the three specialized assistants (Flight, Accommodation, and Car Rental) in a multi-agent workflow.*

### Supervisor Pattern
The system uses LangGraph's supervisor pattern with:
- **Travel Master (Supervisor)** - Coordinates and routes requests to appropriate assistants
- **Specialized Assistants** - Handle domain-specific travel operations
- **Shared State Management** - Maintains conversation context across all assistants

### Real vs. Dummy Operations
- **Search Operations**: Use real web search via Tavily API for current information
- **Booking Operations**: Currently use dummy implementations with realistic confirmations
- **Global Coverage**: Worldwide search and booking capabilities

## Technology Stack

- **Framework**: [LangGraph](https://langchain-ai.github.io/langgraph/) for multi-agent orchestration
- **LLM Integration**: Azure OpenAI GPT-4 models
- **Search**: Tavily API for real-time travel information
- **Language**: Python 3.11+
- **Package Management**: Poetry

## Prerequisites

- Python 3.11 or higher
- Poetry for dependency management
- Azure OpenAI API access
- Tavily API key for search functionality

## Quick Start

### 1. Environment Setup

Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd "AI travel master"
pip install -e .
```

### 2. Configuration

Create a `.env` file in the project root:

```env
# Required: Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
AZURE_OPENAI_API_VERSION=2025-01-01-preview

# Required: Search API
TAVILY_API_KEY=your_tavily_api_key_here

# Optional: LangSmith Tracing (Recommended for debugging)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=travel-master
```

### 3. Launch the System

Start the LangGraph development server:

```bash
langgraph dev
```

The system will be available at `http://localhost:2024` with LangGraph Studio UI.

## Usage Examples

### Flight Search & Booking
```
User: "Find flights from New York to London departing December 15th, returning December 22nd for 2 passengers"

Travel Master → Flight Assistant:
- Searches real flight options using Tavily
- Presents available flights with pricing
- Handles booking with passenger details
- Provides confirmation numbers
```

### Complete Travel Planning
```
User: "Plan a trip to Paris from March 10-17: flights from Chicago, hotel near Eiffel Tower, and car rental"

Travel Master coordinates:
- Flight Assistant: Chicago to Paris flights
- Accommodation Assistant: Hotels near Eiffel Tower  
- Car Rental Assistant: Paris car rentals
- Provides comprehensive travel package
```

### Booking Management
```
User: "Cancel my hotel booking HT123456 and change my flight FL789012 to March 15th"

Travel Master handles:
- Accommodation Assistant: Processes hotel cancellation
- Flight Assistant: Modifies flight dates
- Provides updated confirmations
```

## Configuration

The system supports extensive configuration through the `Configuration` class:

- **Model Selection**: Choose between different GPT models for supervisor and assistants
- **Timezone Settings**: Configurable timezone for all operations
- **Search Limits**: Adjustable maximum search results
- **Assistant Prompts**: Customizable system prompts for each assistant

## Project Structure

```
src/travel_master/
├── travel_master.py              # Main supervisor
├── configuration.py              # System configuration
├── prompts.py                   # System prompts
├── state.py                     # Shared state management
├── utils.py                     # Utility functions
├── flight_assistant/            # Flight operations
│   ├── flight_assistant.py
│   └── flight_assistant_tools.py
├── accommodation_assistant/     # Hotel operations
│   ├── accommodation_assistant.py
│   └── accommodation_assistant_tools.py
└── car_rental_assistant/       # Car rental operations
    ├── car_rental_assistant.py
    └── car_rental_assistant_tools.py
```

## Testing

Run the test suite:

```bash
# Unit tests
python -m pytest tests/unit_tests/

# Integration tests  
python -m pytest tests/integration_tests/

# All tests
python -m pytest
```

## API Integration

### Current Integrations
- **Tavily Search API** - Real-time travel information search
- **Azure OpenAI** - Language model services

### Future Integrations
- **Flight APIs** - Direct airline booking integration
- **Hotel APIs** - Direct hotel booking systems
- **Car Rental APIs** - Direct rental company integration
- **Payment Processing** - Secure payment handling

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

**Transform your travel planning experience with AI Travel Master - your intelligent travel companion!**