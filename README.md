<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">Recipe Creator Agent</h1>
<h3 align="center">AI-Powered Culinary Assistant</h3>

<p align="center">
  <strong>Generate personalized recipes, plan meals, and master cooking with AI guidance</strong><br/>
  Transform ingredients into delicious meals with dietary-aware recipe creation
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/recipe-creator/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/Paraschamoli/recipe-creator/build-and-push.yml?branch=main" alt="Build Status">
  </a>
  <img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python Version">
  <a href="https://github.com/Paraschamoli/recipe-creator/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Paraschamoli/recipe-creator" alt="License">
  </a>
</p>

---

## 🎯 What is Recipe Creator Agent?

An AI-powered culinary assistant that generates personalized recipes based on available ingredients, dietary preferences, cuisine choices, and skill level. It suggests creative meal ideas, provides step-by-step cooking instructions, offers substitutions, and adjusts recipes for health goals—helping users cook smarter, faster, and more creatively.

### Key Features
*   **🍳 Personalized Recipe Generation** - Create recipes from available ingredients
*   **🥗 Dietary Adaptation** - Adjust for vegetarian, vegan, gluten-free, keto, and more
*   **⏱️ Time-Optimized Meals** - Recipes tailored to your time constraints
*   **📋 Meal Planning** - Weekly meal plans and shopping lists
*   **🧠 Cooking Guidance** - Step-by-step instructions and techniques
*   **⚡ Lazy Initialization** - Fast boot times, initializes on first request
*   **🔐 Secure API Handling** - No API keys required at startup

---

## 🛠️ Tools & Capabilities

### Core Technologies
*   **ExaTools** - Recipe search and ingredient lookup
*   **Mem0 AI Memory** - Remember user preferences and dietary restrictions
*   **OpenRouter LLM** - Culinary knowledge and recipe generation
*   **Dietary Awareness** - Adapt recipes for specific dietary needs

### Recipe Creation Process
1.  **Ingredient Analysis** - Understand available ingredients and constraints
2.  **Recipe Search** - Find matching recipes from culinary databases
3.  **Personalization** - Adapt recipes to dietary preferences and skill level
4.  **Detailed Instructions** - Provide clear, step-by-step cooking guidance
5.  **Nutritional Information** - Include estimated nutritional values
6.  **Meal Planning** - Create comprehensive meal plans and shopping lists

---

> **🌐 Join the Internet of Agents**
> Register your agent at [bindus.directory](https://bindus.directory) to make it discoverable worldwide and enable agent-to-agent collaboration. It takes 2 minutes and unlocks the full potential of your agent.

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Paraschamoli/recipe-creator.git
cd recipe-creator

# Set up virtual environment with uv
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys:
OPENROUTER_API_KEY=your_openrouter_api_key_here
EXA_API_KEY=your_exa_api_key_here
MEM0_API_KEY=your_mem0_api_key_here
```

### 3. Run Locally

```bash
# Start the recipe creator agent
python -m recipe_creator

# Or using uv
uv run python -m recipe_creator
```

### 4. Test with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at: http://localhost:3773
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file:

```env
# Required API Keys
OPENROUTER_API_KEY=your_openrouter_api_key_here  # Get from: https://openrouter.ai/keys
EXA_API_KEY=your_exa_api_key_here                # Get from: https://exa.ai
MEM0_API_KEY=your_mem0_api_key_here              # Get from: https://app.mem0.ai/dashboard/api-keys

# Optional
MODEL_NAME=openai/gpt-4o                         # OpenRouter model ID
DEBUG=true                                       # Enable debug logging
```

### Port Configuration
Default port: `3773` (can be changed in `agent_config.json`)

---

## 💡 Usage Examples

### Via HTTP API

```bash
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "I have chicken breast, broccoli, garlic, and rice. Need a healthy dinner recipe that takes less than 45 minutes and is gluten-free."
      }
    ]
  }'
```

### Sample Recipe Queries

```text
"Create a vegetarian pasta recipe with mushrooms and spinach for 2 people, ready in 30 minutes"

"Suggest healthy breakfast options with oats and fruits that are vegan and high in protein"

"What can I make with leftover turkey and potatoes? Looking for something creative for 4 servings"

"Need a quick dessert recipe using chocolate and bananas, suitable for kids and ready in 20 minutes"

"Give me a gluten-free dinner recipe using salmon and asparagus, with nutritional information"

"Plan a weekly meal prep for keto diet with shopping list and calorie counts"
```

### Expected Output Format

```markdown
# {Recipe Title} 🍽️

## Basic Information
- **Cuisine Type:** {Cuisine}
- **Preparation Time:** {Prep time} minutes
- **Cooking Time:** {Cook time} minutes
- **Total Time:** {Total time} minutes
- **Difficulty:** {Beginner/Intermediate/Advanced}
- **Servings:** {Number of servings}
- **Dietary Tags:** 🌱 Vegetarian / 🌿 Vegan / 🌾 Gluten-free / 🥜 Contains nuts / ⏱️ Quick

## Ingredients
### Main Ingredients
- {Ingredient 1} - {Quantity}
- {Ingredient 2} - {Quantity}
- {Ingredient 3} - {Quantity}

### Seasonings & Sauces
- {Seasoning 1} - {Quantity}
- {Seasoning 2} - {Quantity}

## Instructions
1. {Step 1 - detailed instruction}
2. {Step 2 - detailed instruction}
3. {Step 3 - detailed instruction}
4. {Step 4 - detailed instruction}

## Nutritional Information (per serving)
- **Calories:** {Number}
- **Protein:** {Number}g
- **Carbohydrates:** {Number}g
- **Fat:** {Number}g
- **Fiber:** {Number}g

## Tips & Variations
- **Substitutions:** {Ingredient substitution options}
- **Time-saving tips:** {Make-ahead suggestions}
- **Common mistakes:** {What to avoid}
- **Variations:** {Different ways to prepare}

## Pairing Suggestions
- **Side dishes:** {Recommended sides}
- **Wine pairing:** {Wine suggestions if appropriate}
- **Presentation:** {Plating tips}

## Storage & Leftovers
- **Refrigerator:** {Storage duration}
- **Freezer:** {Freezing instructions}
- **Reheating:** {Best reheating methods}

---
Recipe created by ChefGenius AI
Bon Appétit! 🍴
Date: {current_date}
```

---

## 🐳 Docker Deployment

### Quick Docker Setup

```bash
# Build the image
docker build -t recipe-creator -f Dockerfile.agent .

# Run container
docker run -d \
  -p 3773:3773 \
  -e OPENROUTER_API_KEY=your_key_here \
  -e EXA_API_KEY=your_exa_key_here \
  -e MEM0_API_KEY=your_mem0_key_here \
  --name recipe-creator \
  recipe-creator

# Check logs
docker logs -f recipe-creator
```

### Docker Compose (Recommended)

`docker-compose.yml`:

```yaml
version: '3.8'
services:
  recipe-creator:
    build:
      context: .
      dockerfile: Dockerfile.agent
    ports:
      - "3773:3773"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - EXA_API_KEY=${EXA_API_KEY}
      - MEM0_API_KEY=${MEM0_API_KEY}
    restart: unless-stopped
```

Run with Compose:

```bash
# Start with compose
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 📁 Project Structure

```text
recipe-creator/
├── recipe_creator/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Main agent implementation
│   ├── agent_config.json        # Agent configuration
│   └── skills/
│       └── recipe-creator/
│           └── skill.yaml       # Skill definition
├── pyproject.toml               # Python dependencies
├── Dockerfile.agent             # Docker build file
├── docker-compose.yml           # Docker Compose setup
├── README.md                    # This documentation
├── .env.example                 # Environment template
└── tests/                       # Test files
    └── test_main.py
```

---

## 🔌 API Reference

### Health Check

```bash
GET http://localhost:3773/health
```

Response:
```json
{"status": "healthy", "agent": "Recipe Creator Agent"}
```

### Chat Endpoint

```bash
POST http://localhost:3773/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Your recipe request here"}
  ]
}
```

For complete API documentation, visit: [Bindu API Reference](https://docs.getbindu.com)

---

## 🧪 Testing

### Local Testing

```bash
# Install test dependencies
uv sync --group dev

# Run tests
pytest tests/

# Test with specific API keys
OPENROUTER_API_KEY=test_key EXA_API_KEY=test_key MEM0_API_KEY=test_key python -m pytest
```

### Integration Test

```bash
# Start agent
python -m recipe_creator &

# Test API endpoint
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "I have eggs, bread, and cheese. Breakfast ideas?"}]}'
```

---

## 🚨 Troubleshooting

### Common Issues & Solutions

**"ModuleNotFoundError"**
```bash
uv sync --force
```

**"Port 3773 already in use"**
Change port in `agent_config.json` or kill the process:
```bash
lsof -ti:3773 | xargs kill -9
```

**"No API key provided"**
Check if `.env` exists and variable names match. Or set directly:
```bash
export OPENROUTER_API_KEY=your_key
export EXA_API_KEY=your_exa_key
export MEM0_API_KEY=your_mem0_key
```

**Docker build fails**
```bash
docker system prune -a
docker-compose build --no-cache
```

**"Exa API key required"**
Get a key from Exa.ai for recipe search functionality

**"No recipes found for ingredients"**
Try broader ingredient categories or remove some constraints

---

## 📊 Dependencies

### Core Packages
*   **bindu** - Agent deployment framework
*   **agno** - AI agent framework
*   **exa-py** - Recipe search and ingredient lookup
*   **mem0ai** - Memory operations
*   **openai** - OpenAI client for embeddings
*   **python-dotenv** - Environment management

### Development Packages
*   **pytest** - Testing framework
*   **ruff** - Code formatting/linting
*   **pre-commit** - Git hooks

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1.  Fork the repository
2.  Create a feature branch: `git checkout -b feature/improvement`
3.  Make your changes following the code style
4.  Add tests for new functionality
5.  Commit with descriptive messages
6.  Push to your fork
7.  Open a Pull Request

**Code Style:**
*   Follow PEP 8 conventions
*   Use type hints where possible
*   Add docstrings for public functions
*   Keep functions focused and small

---

## 📄 License
MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Credits & Acknowledgments
*   **Developer:** Paras Chamoli
*   **Framework:** Bindu - Agent deployment platform
*   **Agent Framework:** Agno - AI agent toolkit
*   **Recipe Search:** Exa.ai for culinary database access
*   **Memory System:** Mem0 AI

## 🔗 Useful Links
*   🌐 **Bindu Directory:** [bindus.directory](https://bindus.directory)
*   📚 **Bindu Docs:** [docs.getbindu.com](https://docs.getbindu.com)
*   🐙 **GitHub:** [github.com/Paraschamoli/recipe-creator](https://github.com/Paraschamoli/recipe-creator)
*   💬 **Discord:** Bindu Community

<br>

<p align="center">
  <strong>Built with ❤️ by Paras Chamoli</strong><br/>
  <em>Making cooking accessible and enjoyable through AI</em>
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/recipe-creator/stargazers">⭐ Star on GitHub</a> •
  <a href="https://bindus.directory">🌐 Register on Bindu</a> •
  <a href="https://github.com/Paraschamoli/recipe-creator/issues">🐛 Report Issues</a>
</p>

> **Note:** This agent follows the Bindu pattern with lazy initialization and secure API key handling. It boots without API keys and only fails at runtime if keys are needed but not provided.
