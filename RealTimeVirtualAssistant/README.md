# RAG Framework with FastAPI Integration

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** framework with FastAPI to handle user queries, process images/screenshots, retrieve relevant documents, and generate responses using a Large Language Model (LLM). The framework is modular, scalable, and integrates image processing, retrieval systems, and natural language generation to answer user queries based on product documentation.

## Table of Contents

- [Features](#features)
- [Framework Architecture](#framework-architecture)
  - [Input Layer](#input-layer)
  - [Retrieval Layer](#retrieval-layer)
  - [Reader Layer](#reader-layer)
  - [Storage Layer](#storage-layer)
  - [Orchestration Layer](#orchestration-layer)
  - [User Interface Layer](#user-interface-layer)
- [FastAPI Integration](#fastapi-integration)
  - [API Endpoints](#api-endpoints)
- [Directory Structure](#directory-structure)
- [Technology Stack](#technology-stack)
- [Deployment](#deployment)
- [Testing](#testing)

## Features

- **OCR Integration**: Extracts text from images/screenshots using OCR tools.
- **Query Processing**: Handles user queries and formats them for retrieval.
- **Hybrid Retrieval**: Combines dense and sparse retrieval techniques to fetch relevant documents.
- **LLM Response Generation**: Uses an LLM (e.g., OpenAI GPT, Hugging Face) to generate human-like responses based on retrieved documents.
- **FastAPI Integration**: Exposes RESTful API endpoints for easy interaction with the framework.
  
## Framework Architecture

### **1. Input Layer**

The input layer is responsible for processing user queries and images/screenshots. It includes the following components:

1. **Image Processor**: Extracts text from images/screenshots using OCR tools like Tesseract or AWS Textract.
2. **Query Processor**: Normalizes and tokenizes user queries to make them suitable for embedding generation.
3. **Embedding Generator**: Converts queries into vector embeddings using pre-trained models (e.g., Sentence-BERT, OpenAI embeddings).

### **2. Retrieval Layer**

The retrieval layer performs document retrieval using both dense and sparse retrieval techniques:

1. **Dense Retriever**: Uses embedding-based search (e.g., FAISS, Pinecone).
2. **Sparse Retriever**: Implements traditional search methods (e.g., BM25) using Elasticsearch or Solr.
3. **Hybrid Retriever**: Combines results from dense and sparse retrieval to improve relevance.

### **3. Reader Layer**

The reader layer is responsible for generating the response using the retrieved documents:

1. **Context Preparer**: Formats the query and retrieved documents into a structured prompt for the LLM.
2. **LLM Interface**: Interfaces with the LLM to generate a contextual response.
3. **Response Post-Processor**: Cleans and structures the response for display.

### **4. Storage Layer**

The storage layer manages the documents and embeddings:

1. **Document Database**: Stores raw documents and metadata.
2. **Vector Store**: Manages document embeddings for dense retrieval.
3. **Indexing Service**: Handles document chunking, embedding generation, and indexing.

### **5. Orchestration Layer**

The orchestration layer manages the flow between components, ensuring proper sequencing and handling of errors:

1. **Pipeline Orchestrator**: Coordinates the execution of various components.
2. **API Gateway**: Exposes FastAPI endpoints for communication with external systems.

### **6. Parser Layer**

The layer provides a parser to convert LLM response to HTML.

## FastAPI Integration

The FastAPI app exposes several endpoints for interacting with the RAG framework:

### **API Endpoints**

1. **`POST /upload-image`**:
   - Accepts an image file and extracts text using OCR.
   - **Request**: `multipart/form-data` with an image file.
   - **Response**: JSON with extracted text.
   
   ```json
   {
     "extracted_text": "Sample extracted text from the image."
   }
   ```

2. **`POST /submit-query`**:
   - Accepts a user query and returns embeddings for retrieval.
   - **Request**: JSON with a query string.
   - **Response**: JSON with query embeddings.
   
   ```json
   {
     "query_embedding": [0.23, 0.57, 0.89, ...]
   }
   ```

3. **`POST /retrieve-documents`**:
   - Accepts query embeddings and retrieves the most relevant documents from the storage.
   - **Request**: JSON with query embeddings.
   - **Response**: JSON with the top-N documents.
   
   ```json
   {
     "documents": [
       {"id": 1, "text": "Relevant document content..."},
       {"id": 2, "text": "Another relevant document..."}
     ]
   }
   ```

4. **`POST /generate-response`**:
   - Accepts a user query and retrieved documents, and generates a response using an LLM.
   - **Request**: JSON with query and documents.
   - **Response**: JSON with the generated response.
   
   ```json
   {
     "response": "Here's a detailed response based on the documents and query."
   }
   ```

## Directory Structure

```
rag_framework/
│
├── app/                         # FastAPI application
│   ├── main.py                  # FastAPI app entry point
│   ├── routers/                 # FastAPI routes
│   ├── services/                # Business logic for APIs
│   ├── models/                  # Data models for APIs
│   ├── config/                  # Configuration files
│
├── input_layer/                 # OCR and query processing
├── retrieval_layer/             # Retrieval logic (dense, sparse)
├── reader_layer/                # LLM response generation
├── storage_layer/               # Document and vector storage
├── orchestration_layer/         # Pipeline orchestration
├── ui_layer/                    # Frontend and dashboard
├── tests/                       # Unit and integration tests
└── config/                      # Configuration files
```

## Technology Stack

- **Backend**: Python (FastAPI, Celery for task orchestration).
- **OCR**: Tesseract, AWS Textract, or Google Vision API.
- **Embeddings**: OpenAI embeddings, Hugging Face Transformers, Sentence-BERT.
- **Retrieval**: FAISS, Pinecone (dense), Elasticsearch, Solr (sparse).
- **LLM**: OpenAI GPT, Hugging Face models, BMC HelixGPT.
- **Frontend**: React.js, Angular (for user interface).
- **Database**: PostgreSQL, Elasticsearch, or MongoDB for document storage.
- **Containerization**: Docker.
- **Orchestration**: Kubernetes, Docker Compose for deployment.

## Deployment

1. **Run FastAPI App Locally**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Containerize**:
   - Dockerfile to containerize the FastAPI application.
   - Build Docker image:
     ```bash
     docker build -t rag-framework .
     ```
   - Run Docker container:
     ```bash
     docker run -p 8000:8000 rag-framework
     ```

3. **Deploy on Cloud**:
   - Use AWS/GCP/Azure for cloud deployment.
   - Use Kubernetes for container orchestration.

## Testing

This project includes unit and integration tests for each module:

1. **Test Retrieval**:
   - Ensures retrieval systems (dense, sparse, hybrid) return relevant documents.
   
2. **Test LLM**:
   - Verifies the response generated by the LLM based on context.

3. **Test API Endpoints**:
   - Validates the FastAPI endpoints for image upload, query submission, and response generation.

To run tests:
```bash
pytest tests/
```

---

## Conclusion

This RAG-based framework provides an end-to-end solution for processing queries, retrieving documents, and generating responses using LLMs. The integration of FastAPI ensures that the system is scalable and can be easily accessed via RESTful APIs.
