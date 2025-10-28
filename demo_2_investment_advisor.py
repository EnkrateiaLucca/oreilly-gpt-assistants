"""
Demo 2: Investment Suggestion Generator
Uses OpenAI Responses API with Code Interpreter to analyze data and generate investment suggestions.
"""

import os
from openai import OpenAI
from typing import Optional


class InvestmentAdvisor:
    """An AI investment advisor that uses the Responses API with Code Interpreter."""

    def __init__(self, api_key: str = None):
        """Initialize the Investment Advisor.

        Args:
            api_key: OpenAI API key. If not provided, reads from OPENAI_API_KEY env var.
        """
        self.client = OpenAI(api_key=api_key)
        self.conversation_id = None

    def get_investment_suggestion(
        self,
        query: str,
        model: str = "gpt-4o",
        use_code_interpreter: bool = True,
        stream: bool = True
    ) -> str:
        """Get investment suggestions based on user query.

        Args:
            query: Investment-related question or scenario
            model: OpenAI model to use
            use_code_interpreter: Whether to enable code interpreter for analysis
            stream: Whether to stream the response

        Returns:
            Investment suggestion text
        """
        instructions = """You are a professional investment advisor with expertise in:
        - Portfolio diversification and risk management
        - Market analysis and trends
        - Asset allocation strategies
        - Financial planning and retirement savings
        - Stock, bond, ETF, and mutual fund analysis

        Guidelines:
        - Provide data-driven insights when possible
        - Use code interpreter to perform calculations and create visualizations
        - Always include risk disclaimers
        - Explain your reasoning clearly
        - Consider the user's risk tolerance and investment timeline
        - Suggest diversified portfolios when appropriate

        IMPORTANT DISCLAIMER: Always remind users that this is educational information,
        not professional financial advice. Users should consult with licensed financial
        advisors before making investment decisions."""

        # Setup tools
        tools = []
        if use_code_interpreter:
            tools.append({
                "type": "code_interpreter",
                "container": {"type": "auto"}
            })

        # Create response
        if stream:
            return self._stream_response(query, instructions, tools, model)
        else:
            return self._sync_response(query, instructions, tools, model)

    def _stream_response(self, query: str, instructions: str, tools: list, model: str):
        """Stream the response with real-time output."""
        print("\n" + "=" * 60)
        print(f"Query: {query}")
        print("=" * 60)
        print("Investment Advisor: ", end="", flush=True)

        stream = self.client.responses.create(
            input=query,
            model=model,
            instructions=instructions,
            previous_response_id=self.conversation_id,
            tools=tools,
            stream=True
        )

        full_text = []
        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
                full_text.append(event.delta)
            elif event.type == "response.output_item.added":
                if hasattr(event, 'item') and event.item.type == "code_interpreter_call":
                    print("\n\n[Running analysis...]", flush=True)
            elif event.type == "response.completed":
                self.conversation_id = event.response.id

        print("\n" + "=" * 60)
        return ''.join(full_text)

    def _sync_response(self, query: str, instructions: str, tools: list, model: str) -> str:
        """Get synchronous response."""
        response = self.client.responses.create(
            input=query,
            model=model,
            instructions=instructions,
            previous_response_id=self.conversation_id,
            tools=tools
        )

        self.conversation_id = response.id
        return response.output[-1].content[0].text

    def analyze_portfolio(
        self,
        portfolio_data: dict,
        model: str = "gpt-4o"
    ) -> str:
        """Analyze a portfolio and provide suggestions.

        Args:
            portfolio_data: Dictionary with portfolio information
            model: OpenAI model to use

        Returns:
            Analysis and suggestions
        """
        # Format portfolio data into a query
        query = f"""Please analyze this investment portfolio and provide suggestions:

Portfolio Details:
- Age: {portfolio_data.get('age', 'Not specified')}
- Risk Tolerance: {portfolio_data.get('risk_tolerance', 'Moderate')}
- Investment Timeline: {portfolio_data.get('timeline', 'Not specified')}
- Current Holdings: {portfolio_data.get('holdings', 'Not specified')}
- Investment Goals: {portfolio_data.get('goals', 'Not specified')}

Please provide:
1. Analysis of current allocation
2. Risk assessment
3. Diversification recommendations
4. Suggested adjustments (if any)
5. Expected return projections (with visualizations if helpful)"""

        return self.get_investment_suggestion(query, model=model, stream=True)

    def compare_investments(
        self,
        investment_options: list,
        criteria: str = "risk-adjusted returns",
        model: str = "gpt-4o"
    ) -> str:
        """Compare different investment options.

        Args:
            investment_options: List of investment options to compare
            criteria: Criteria for comparison
            model: OpenAI model to use

        Returns:
            Comparison analysis
        """
        options_str = "\n".join([f"- {option}" for option in investment_options])

        query = f"""Please compare these investment options based on {criteria}:

{options_str}

Provide:
1. Side-by-side comparison
2. Pros and cons of each option
3. Risk analysis
4. Historical performance (if applicable)
5. Recommendation based on different investor profiles
6. Use visualizations to illustrate key differences"""

        return self.get_investment_suggestion(query, model=model, stream=True)

    def market_outlook(
        self,
        sector: str = "general market",
        model: str = "gpt-4o"
    ) -> str:
        """Get market outlook and investment implications.

        Args:
            sector: Market sector to analyze
            model: OpenAI model to use

        Returns:
            Market analysis and outlook
        """
        query = f"""Provide a market outlook analysis for {sector}:

Please include:
1. Current market conditions
2. Key trends and drivers
3. Potential risks and opportunities
4. Investment strategies for current conditions
5. Sector-specific recommendations (if applicable)

Note: Focus on general principles and educational insights rather than specific stock picks."""

        return self.get_investment_suggestion(query, model=model, stream=True)

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_id = None
        print("Conversation reset.")


def main():
    """Demo application for investment suggestions."""
    print("=" * 60)
    print("Investment Suggestion Generator Demo")
    print("Using OpenAI Responses API with Code Interpreter")
    print("=" * 60)
    print("\n⚠️  DISCLAIMER: This is for educational purposes only.")
    print("Not professional financial advice. Consult licensed advisors.")
    print("=" * 60)

    # Initialize advisor
    advisor = InvestmentAdvisor()

    # Example 1: General investment question
    print("\n\n### Example 1: General Investment Advice")
    advisor.get_investment_suggestion(
        "I'm 30 years old with moderate risk tolerance. How should I allocate $10,000 for retirement?"
    )

    # Example 2: Portfolio analysis
    print("\n\n### Example 2: Portfolio Analysis")
    portfolio = {
        "age": 35,
        "risk_tolerance": "Moderate to Aggressive",
        "timeline": "25-30 years until retirement",
        "holdings": "60% stocks (S&P 500 index), 30% bonds, 10% cash",
        "goals": "Retirement savings, aiming for $2M by age 65"
    }
    advisor.analyze_portfolio(portfolio)

    # Example 3: Compare investment options
    print("\n\n### Example 3: Investment Comparison")
    advisor.compare_investments(
        investment_options=[
            "S&P 500 Index Fund (VOO)",
            "Total Bond Market Fund (BND)",
            "Real Estate Investment Trust (VNQ)",
            "Technology Sector ETF (XLK)"
        ],
        criteria="risk-adjusted returns for a 10-year investment horizon"
    )

    # Example 4: Market outlook
    print("\n\n### Example 4: Market Outlook")
    advisor.market_outlook(sector="technology sector")

    # Interactive mode
    print("\n\n" + "=" * 60)
    print("Interactive Mode - Ask your investment questions!")
    print("Commands: 'quit' to exit, 'reset' to start new conversation")
    print("=" * 60)

    while True:
        user_input = input("\nYour question: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using Investment Advisor!")
            break

        if user_input.lower() == 'reset':
            advisor.reset_conversation()
            continue

        if not user_input:
            continue

        try:
            advisor.get_investment_suggestion(user_input)
        except Exception as e:
            print(f"\nError: {e}")

    print("\n" + "=" * 60)
    print("Remember: Always consult with licensed financial advisors")
    print("before making investment decisions!")
    print("=" * 60)


if __name__ == "__main__":
    main()
