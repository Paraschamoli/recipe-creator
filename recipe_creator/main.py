"""recipe-creator - A Bindu Agent for intelligent recipe creation and meal planning."""

import argparse
import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from textwrap import dedent
from typing import Any

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.exa import ExaTools
from agno.tools.mem0 import Mem0Tools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global agent instance
agent: Agent | None = None
_initialized = False
_init_lock = asyncio.Lock()


def load_config() -> dict:
    """Load agent configuration from project root."""
    # Try multiple possible locations for agent_config.json
    possible_paths = [
        Path(__file__).parent.parent / "agent_config.json",  # Project root
        Path(__file__).parent / "agent_config.json",  # Same directory as main.py
        Path.cwd() / "agent_config.json",  # Current working directory
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except (PermissionError, json.JSONDecodeError) as e:
                print(f"⚠️  Error reading {config_path}: {type(e).__name__}")
                continue
            except Exception as e:
                print(f"⚠️  Unexpected error reading {config_path}: {type(e).__name__}")
                continue

    # If no config found or readable, create a minimal default
    print("⚠️  No agent_config.json found, using default configuration")
    return {
        "name": "recipe-creator",
        "description": "AI recipe creator and meal planning assistant",
        "version": "1.0.0",
        "deployment": {
            "url": "http://127.0.0.1:3773",
            "expose": True,
            "protocol_version": "1.0.0",
            "proxy_urls": ["127.0.0.1"],
            "cors_origins": ["*"],
        },
        "environment_variables": [
            {"key": "OPENROUTER_API_KEY", "description": "OpenRouter API key for LLM calls", "required": True},
            {"key": "EXA_API_KEY", "description": "Exa API key for recipe search and lookup", "required": True},
            {"key": "MEM0_API_KEY", "description": "Mem0 API key for memory operations", "required": True},
        ],
    }


async def initialize_agent() -> None:
    """Initialize the recipe creator agent with proper model and tools."""
    global agent

    # Get API keys from environment
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    exa_api_key = os.getenv("EXA_API_KEY")
    mem0_api_key = os.getenv("MEM0_API_KEY")
    model_name = os.getenv("MODEL_NAME", "openai/gpt-4o")

    # Validate required API keys
    if not openrouter_api_key:
        error_msg = (
            "No OpenRouter API key provided. Set OPENROUTER_API_KEY environment variable.\n"
            "Get your key from: https://openrouter.ai/keys"
        )
        raise ValueError(error_msg)

    if not exa_api_key:
        error_msg = "No Exa API key provided. Set EXA_API_KEY environment variable.\nGet your key from: https://exa.ai"
        raise ValueError(error_msg)

    if not mem0_api_key:
        error_msg = (
            "No Mem0 API key provided. Set MEM0_API_KEY environment variable.\n"
            "Get your key from: https://app.mem0.ai/dashboard/api-keys"
        )
        raise ValueError(error_msg)

    # Initialize model
    model = OpenRouter(
        id=model_name,
        api_key=openrouter_api_key,
        cache_response=True,
        supports_native_structured_outputs=True,
    )
    print(f"✅ Using OpenRouter model: {model_name}")

    # Initialize tools
    exa_tools = ExaTools(api_key=exa_api_key)
    mem0_tools = Mem0Tools(api_key=mem0_api_key)

    # Create the recipe creator agent
    agent = Agent(
        name="ChefGenius",
        model=model,
        tools=[exa_tools, mem0_tools],
        description=dedent("""\
            You are ChefGenius, a passionate and knowledgeable culinary expert with expertise in global cuisine! 🍳

            Your mission is to help users create delicious meals by providing detailed,
            personalized recipes based on their available ingredients, dietary restrictions,
            and time constraints. You combine deep culinary knowledge with nutritional wisdom
            to suggest recipes that are both practical and enjoyable."""),
        instructions=dedent("""\
            Approach each recipe recommendation with these steps:

            1. Analysis Phase 📋
               - Understand available ingredients
               - Consider dietary restrictions
               - Note time constraints
               - Factor in cooking skill level
               - Check for kitchen equipment needs

            2. Recipe Selection 🔍
               - Use Exa to search for relevant recipes
               - Ensure ingredients match availability
               - Verify cooking times are appropriate
               - Consider seasonal ingredients
               - Check recipe ratings and reviews

            3. Detailed Information 📝
               - Recipe title and cuisine type
               - Preparation time and cooking time
               - Complete ingredient list with measurements
               - Step-by-step cooking instructions
               - Nutritional information per serving
               - Difficulty level
               - Serving size
               - Storage instructions

            4. Extra Features ✨
               - Ingredient substitution options
               - Common pitfalls to avoid
               - Plating suggestions
               - Wine pairing recommendations
               - Leftover usage tips
               - Meal prep possibilities

            Presentation Style:
            - Use clear markdown formatting
            - Present ingredients in a structured list
            - Number cooking steps clearly
            - Add emoji indicators for:
              🌱 Vegetarian
              🌿 Vegan
              🌾 Gluten-free
              🥜 Contains nuts
              ⏱️ Quick recipes
            - Include tips for scaling portions
            - Note allergen warnings
            - Highlight make-ahead steps
            - Suggest side dish pairings"""),
        expected_output=dedent("""\
            # {Recipe Title} 🍽️

            ## Basic Information
            - **Cuisine Type:** {Cuisine}
            - **Preparation Time:** {Prep time}
            - **Cooking Time:** {Cook time}
            - **Total Time:** {Total time}
            - **Difficulty:** {Beginner/Intermediate/Advanced}
            - **Servings:** {Number of servings}
            - **Dietary Tags:** {Emoji indicators}

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
            Date: {current_date}"""),
        add_datetime_to_context=True,
        markdown=True,
    )
    print("✅ Recipe Creator Agent initialized")


async def run_agent(messages: list[dict[str, str]]) -> Any:
    """Run the agent with the given messages."""
    global agent
    if not agent:
        error_msg = "Agent not initialized"
        raise RuntimeError(error_msg)

    # Run the agent and get response
    response = await agent.arun(messages)
    return response


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages with lazy initialization."""
    global _initialized

    # Lazy initialization on first call
    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing Recipe Creator Agent...")
            await initialize_agent()
            _initialized = True

    # Run the async agent
    result = await run_agent(messages)
    return result


async def cleanup() -> None:
    """Clean up any resources."""
    print("🧹 Cleaning up Recipe Creator Agent resources...")
    # Clean up any resources if needed


def main():
    """Run the main entry point for the Recipe Creator Agent."""
    parser = argparse.ArgumentParser(description="Bindu Recipe Creator Agent")
    parser.add_argument(
        "--openrouter-api-key",
        type=str,
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (env: OPENROUTER_API_KEY)",
    )
    parser.add_argument(
        "--exa-api-key",
        type=str,
        default=os.getenv("EXA_API_KEY"),
        help="Exa API key (env: EXA_API_KEY)",
    )
    parser.add_argument(
        "--mem0-api-key",
        type=str,
        default=os.getenv("MEM0_API_KEY"),
        help="Mem0 API key (env: MEM0_API_KEY)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "openai/gpt-4o"),
        help="Model ID for OpenRouter (env: MODEL_NAME)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to agent_config.json (optional)",
    )
    args = parser.parse_args()

    # Set environment variables if provided via CLI
    if args.openrouter_api_key:
        os.environ["OPENROUTER_API_KEY"] = args.openrouter_api_key
    if args.exa_api_key:
        os.environ["EXA_API_KEY"] = args.exa_api_key
    if args.mem0_api_key:
        os.environ["MEM0_API_KEY"] = args.mem0_api_key
    if args.model:
        os.environ["MODEL_NAME"] = args.model

    print("🤖 Recipe Creator Agent - Intelligent Culinary Assistant")
    print("🍳 Capabilities: Recipe search, meal planning, ingredient analysis, nutritional guidance")

    # Load configuration
    config = load_config()

    try:
        # Bindufy and start the agent server
        print("🚀 Starting Bindu Recipe Creator Agent server...")
        print(f"🌐 Server will run on: {config.get('deployment', {}).get('url', 'http://127.0.0.1:3773')}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 Recipe Creator Agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup on exit
        asyncio.run(cleanup())


if __name__ == "__main__":
    main()
