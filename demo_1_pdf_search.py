"""
Demo 1: PDF Document Search Application
Uses OpenAI Responses API with File Search tool to search through PDF documents.
"""

import os
from openai import OpenAI
import time


class PDFSearchAssistant:
    """A simple assistant that searches through PDF documents using the Responses API."""

    def __init__(self, api_key: str = None):
        """Initialize the PDF Search Assistant.

        Args:
            api_key: OpenAI API key. If not provided, reads from OPENAI_API_KEY env var.
        """
        self.client = OpenAI(api_key=api_key)
        self.vector_store_id = None
        self.conversation_history = []

    def create_vector_store(self, name: str = "PDF Document Store") -> str:
        """Create a vector store for PDF documents.

        Args:
            name: Name for the vector store

        Returns:
            Vector store ID
        """
        print(f"Creating vector store: {name}")
        vector_store = self.client.vector_stores.create(
            name=name,
            expires_after={
                "anchor": "last_active_at",
                "days": 7  # Auto-expire after 7 days of inactivity
            }
        )
        self.vector_store_id = vector_store.id
        print(f"✓ Created vector store with ID: {self.vector_store_id}")
        return self.vector_store_id

    def upload_pdf(self, file_path: str) -> dict:
        """Upload a PDF file to the vector store.

        Args:
            file_path: Path to the PDF file

        Returns:
            Dictionary with upload status
        """
        if not self.vector_store_id:
            raise ValueError("Vector store not created. Call create_vector_store() first.")

        file_name = os.path.basename(file_path)
        print(f"Uploading {file_name}...")

        try:
            # Upload file to OpenAI
            with open(file_path, 'rb') as f:
                file_response = self.client.files.create(
                    file=f,
                    purpose="assistants"
                )

            # Add file to vector store
            self.client.vector_stores.files.create(
                vector_store_id=self.vector_store_id,
                file_id=file_response.id
            )

            # Wait for processing
            time.sleep(2)

            print(f"✓ Successfully uploaded: {file_name}")
            return {"file": file_name, "status": "success", "file_id": file_response.id}

        except Exception as e:
            print(f"✗ Failed to upload {file_name}: {str(e)}")
            return {"file": file_name, "status": "failed", "error": str(e)}

    def search(self, query: str, model: str = "gpt-4o-mini") -> str:
        """Search through uploaded PDFs using natural language query.

        Args:
            query: Natural language search query
            model: OpenAI model to use

        Returns:
            Response text
        """
        if not self.vector_store_id:
            raise ValueError("Vector store not created. Call create_vector_store() first.")

        instructions = """You are a helpful research assistant that searches through PDF documents.
        Answer questions accurately based on the documents provided.
        Always cite your sources when possible using the document names.
        If you're not sure about something, admit it and stick to the information in the documents."""

        # Get the previous response ID if we have conversation history
        previous_response_id = None
        if self.conversation_history:
            previous_response_id = self.conversation_history[-1]["response_id"]

        print(f"\nSearching: {query}")
        print("=" * 60)

        # Create response with file search
        response = self.client.responses.create(
            input=query,
            model=model,
            instructions=instructions,
            previous_response_id=previous_response_id,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [self.vector_store_id],
                "max_num_results": 5
            }]
        )

        # Extract response text
        response_text = response.output[-1].content[0].text

        # Save to conversation history
        self.conversation_history.append({
            "query": query,
            "response": response_text,
            "response_id": response.id
        })

        return response_text

    def search_streaming(self, query: str, model: str = "gpt-4o-mini"):
        """Search with streaming response for real-time output.

        Args:
            query: Natural language search query
            model: OpenAI model to use
        """
        if not self.vector_store_id:
            raise ValueError("Vector store not created. Call create_vector_store() first.")

        instructions = """You are a helpful research assistant that searches through PDF documents.
        Answer questions accurately based on the documents provided.
        Always cite your sources when possible using the document names.
        If you're not sure about something, admit it and stick to the information in the documents."""

        # Get the previous response ID if we have conversation history
        previous_response_id = None
        if self.conversation_history:
            previous_response_id = self.conversation_history[-1]["response_id"]

        print(f"\nSearching: {query}")
        print("=" * 60)
        print("Response: ", end="", flush=True)

        # Create streaming response
        stream = self.client.responses.create(
            input=query,
            model=model,
            instructions=instructions,
            previous_response_id=previous_response_id,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [self.vector_store_id],
                "max_num_results": 5
            }],
            stream=True
        )

        # Process stream
        full_text = []
        current_response_id = None

        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
                full_text.append(event.delta)
            elif event.type == "response.completed":
                current_response_id = event.response.id

        print("\n" + "=" * 60)

        # Save to conversation history
        response_text = ''.join(full_text)
        self.conversation_history.append({
            "query": query,
            "response": response_text,
            "response_id": current_response_id
        })

    def cleanup(self):
        """Delete the vector store and cleanup resources."""
        if self.vector_store_id:
            try:
                self.client.vector_stores.delete(self.vector_store_id)
                print(f"✓ Cleaned up vector store: {self.vector_store_id}")
            except Exception as e:
                print(f"✗ Error cleaning up: {e}")


def main():
    """Demo application for PDF document search."""
    print("=" * 60)
    print("PDF Document Search Demo")
    print("Using OpenAI Responses API with File Search")
    print("=" * 60)

    # Initialize assistant
    assistant = PDFSearchAssistant()

    # Create vector store
    assistant.create_vector_store("Research Papers Store")

    # Upload PDF documents
    # Update these paths to your actual PDF files
    pdf_files = [
        "./notebooks/assets-resources/pdfs/future_agents.pdf",
        "./notebooks/assets-resources/pdfs/attention_paper.pdf"
    ]

    print("\nUploading documents...")
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            assistant.upload_pdf(pdf_file)
        else:
            print(f"⚠ File not found: {pdf_file}")

    print("\n" + "=" * 60)
    print("Documents uploaded and ready for search!")
    print("=" * 60)

    # Example searches
    queries = [
        "What is the main topic of these papers?",
        "Explain the attention mechanism in simple terms",
        "What are the key findings about the future of agents?"
    ]

    print("\nRunning example searches...\n")

    for query in queries:
        assistant.search_streaming(query)
        print()

    # Interactive mode
    print("\n" + "=" * 60)
    print("Interactive Mode - Type 'quit' to exit")
    print("=" * 60)

    while True:
        user_query = input("\nYour question: ").strip()

        if user_query.lower() in ['quit', 'exit', 'q']:
            print("\nExiting...")
            break

        if not user_query:
            continue

        try:
            assistant.search_streaming(user_query)
        except Exception as e:
            print(f"Error: {e}")

    # Cleanup
    print("\nCleaning up resources...")
    assistant.cleanup()
    print("Done!")


if __name__ == "__main__":
    main()
