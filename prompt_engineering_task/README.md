# Prompt Engineering Task - README

## Overview
This chatbot serves as a companion for discussing and analyzing philosophical ideas. It leverages LangChain and TOGHER-AI LLM to provide insightful responses.

## Technologies Used
- **Frontend**: Built with React.
- **Backend**: Built using FastAPI.

## Installation
### Frontend
1. Install dependencies:
   ```sh
   npm install
   ```
2. Run the app:
   ```sh
   npm run dev
   ```

### Backend
1. Install dependencies:
   ```sh
   pip install langchain langchain-community langchain_together python-decouple fastapi uvicorn
   ```
2. Run the server:
   - **Linux**:
     ```sh
     python3 main.py
     ```
   - **Windows**:
     ```sh
     python main.py
     ```

## Features
- Uses LangChain to manage LLM prompts.
- Supports memory management for chat history.
- Configurable parameters such as temperature and max tokens.

## Future Enhancements
- Improve response accuracy through fine-tuning.
- Expand philosophical knowledge base.
- Add multimodal capabilities.

This chatbot provides an engaging way to explore philosophical ideas through AI-driven discussions.

