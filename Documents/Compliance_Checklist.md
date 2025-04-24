# Hybrid RAG Application

This project implements a **Hybrid Retrieval-Augmented Generation (RAG)** application using Streamlit for the user interface. It integrates OpenAI's GPT models with vector-based retrieval methods (using Chroma and BM25) to answer user queries based on a provided context. The application also evaluates the relevance of retrieved context using Athina's evaluation framework.

## Project Structure

```
hybrid_rag_app/
├── app.py                # Main Streamlit app file
├── context.csv           # Sample data file
├── requirements.txt      # Python package dependencies
```

### 1. `requirements.txt`
This file lists all the Python packages required for the app to function:

```txt
streamlit
langchain
langchain-openai
chromadb
datasets
pandas
athina
rank_bm25
google-generativeai
```

### 2. `context.csv`
This file contains the context data used to answer queries. The context is divided into chunks for efficient retrieval. Here's an example of how the file might look:

```csv
text
"MacConkey agar is a selective and differential culture medium for bacteria..."
"zoonotic disease since around 1910, but in the 1930s knowledge was gained..."
"medium was developed by Alfred Theodore MacConkey while working as a bacteriologist..."
...
```

### 3. `app.py`
This is the main Streamlit app file that implements the logic for RAG, context retrieval, and evaluation. The app allows users to input queries, retrieve relevant context, generate responses using GPT models, and evaluate the context relevance.

#### Key Features:
- **Retrieval**: Uses both vector retrieval (Chroma) and keyword-based retrieval (BM25).
- **Generation**: Generates answers using GPT models.
- **Evaluation**: Uses Athina's evaluation framework to assess context relevance.



## How to Run

1. **Save the Files**: Place `requirements.txt`, `app.py`, and `context.csv` in the same folder called `hybrid_rag_app`.

2. **Install Dependencies**:
   Open the terminal, navigate to the `hybrid_rag_app` folder, and run the following command:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App**:
   From the same directory, run:
   ```bash
   streamlit run app.py
   ```

   This will start the Streamlit app and open it in your browser.

## Key Notes

- **API Keys**: Ensure you set up the `OPENAI_API_KEY` and `ATHINA_API_KEY` in the `secrets.toml` file or through the Streamlit Cloud secrets management. Replace the placeholders with your actual API keys.
  
- **Context Data**: The `context.csv` file contains the context for answering user queries. Ensure that this file is in the correct directory.

- **Evaluation**: The app also evaluates the relevance of the retrieved context using the Athina framework and displays the evaluation results in a table.

## Important Considerations

- **Caching**: The `@st.cache_resource()` decorator is used to cache the results of the `initialize_rag` function to improve performance.

- **Secrets Management**: Store your API keys securely using Streamlit's secrets management to avoid hardcoding sensitive information.

## Future Enhancements

- Add more complex retrieval techniques like using FAISS or Elasticsearch for large-scale data.
- Implement additional evaluation metrics beyond context relevancy.
- Add a more dynamic UI with filters and advanced search options.

Let me know if you have any questions or need further modifications!
