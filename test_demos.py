"""
Quick test script for both demo applications.
"""

import os
from demo_1_pdf_search import PDFSearchAssistant
from demo_2_investment_advisor import InvestmentAdvisor


def test_pdf_search():
    """Test the PDF search demo."""
    print("=" * 60)
    print("Testing Demo 1: PDF Document Search")
    print("=" * 60)

    try:
        # Initialize
        assistant = PDFSearchAssistant()

        # Create vector store
        assistant.create_vector_store("Test PDF Store")

        # Upload one PDF
        test_pdf = "./notebooks/assets-resources/pdfs/attention_paper.pdf"
        if os.path.exists(test_pdf):
            assistant.upload_pdf(test_pdf)

            # Run a test query
            print("\nRunning test query...")
            response = assistant.search(
                "What is this paper about in one sentence?",
                model="gpt-4o-mini"
            )
            print(f"\nResponse: {response}\n")

            # Cleanup
            assistant.cleanup()

            print("✓ Demo 1 test passed!")
            return True
        else:
            print(f"✗ Test PDF not found: {test_pdf}")
            return False

    except Exception as e:
        print(f"✗ Demo 1 test failed: {e}")
        return False


def test_investment_advisor():
    """Test the investment advisor demo."""
    print("\n" + "=" * 60)
    print("Testing Demo 2: Investment Advisor")
    print("=" * 60)

    try:
        # Initialize
        advisor = InvestmentAdvisor()

        # Run a simple test query without streaming
        print("\nRunning test query...")
        response = advisor.get_investment_suggestion(
            "What are the key principles of portfolio diversification? Keep it brief.",
            model="gpt-4o-mini",
            use_code_interpreter=False,
            stream=False
        )
        print(f"\nResponse preview: {response[:200]}...\n")

        print("✓ Demo 2 test passed!")
        return True

    except Exception as e:
        print(f"✗ Demo 2 test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("DEMO APPLICATION TESTS")
    print("=" * 60)
    print("\nNote: These tests require OPENAI_API_KEY to be set")
    print("=" * 60 + "\n")

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  WARNING: OPENAI_API_KEY not set!")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        return

    results = []

    # Test Demo 1
    results.append(("PDF Search Demo", test_pdf_search()))

    # Test Demo 2
    results.append(("Investment Advisor Demo", test_investment_advisor()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")

    all_passed = all(result[1] for result in results)
    print("=" * 60)

    if all_passed:
        print("\n🎉 All tests passed! Demos are ready to use.")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")

    print("\nTo run the full demos:")
    print("  python demo_1_pdf_search.py")
    print("  python demo_2_investment_advisor.py")


if __name__ == "__main__":
    main()
