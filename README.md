# LLM Chat Setup Guide

Welcome to the LLM Chat project! This application enables users to:
- Perform Retrieval-Augmented Generation (RAG).
- Chat with an LLM (Language Model).
- Conduct web searches.
- Generate images using Stable Diffusion.

Follow the steps below to set up the application on your local machine.

---

## Prerequisites

1. **Python**: Ensure you have Python 3.8 or later installed.
   - [Download Python](https://www.python.org/downloads/)

2. **Virtual Environment** (Recommended): Install `virtualenv` or `venv` for an isolated Python environment.

3. **Git**: Install Git to clone the repository.
   - [Download Git](https://git-scm.com/downloads)

4. **Pinecone**: Create an account on Pinecone and obtain your API key.
   - [Sign up for Pinecone](https://www.pinecone.io/)
---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/abhishekbiswas772/llm_chat.git
cd llm_chat
```

### 2. Set Up the Environment

#### Option 1: Using `venv`

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Option 2: Using `virtualenv`

```bash
virtualenv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
For installing torch and its dependency
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118      # for gpu enabled mechine
```

```bash
pip3 install torch torchvision torchaudio   # for cpu enabled mechine
```

### 4. Download Models and Resources

- **Stable Diffusion**: Ensure the Stable Diffusion model weights are downloaded and stored in the specified path.
- **LLM**: Download the pre-trained LLM model files using the `transformers` library.

### 5. Configure Environment Variables

Create a `.env` file in the root directory to store API keys and sensitive information:

```
OPENAI_API_KEY=
PINECONE_API_KEY=
INDEX_NAME=
```
---

## Running the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

Access the application at: `http://localhost:8501`

## Features Overview

1. **RAG (Retrieval-Augmented Generation)**:
   - Upload documents or provide URLs for retrieval-based Q&A.

2. **Chat with LLM**:
   - Chat with the integrated language model for general or task-specific queries.

3. **Web Search**:
   - Enter a query to fetch results from the web using scraping or an API.

4. **Image Generation**:
   - Generate images by providing prompts, leveraging Stable Diffusion.

---

## Troubleshooting

1. **Dependencies Not Installing**:
   - Ensure Python and pip versions are up to date.
   - Use `pip install --upgrade pip` if needed.

2. **Model Issues**:
   - Verify paths for model weights in `.env`.
   - Check internet connectivity for downloading models.

3. **Streamlit Errors**:
   - Ensure Streamlit is installed and activated in the current environment.

4. **Image Generation Errors**:
   - Verify the Stable Diffusion model path and ensure compatible GPU drivers are installed.

---

## Contributing

Feel free to fork the repository, make changes, and submit a pull request. Suggestions and feedback are always welcome!

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.