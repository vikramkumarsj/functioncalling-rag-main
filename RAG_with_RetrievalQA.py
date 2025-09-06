
def get_ragdata(query):

    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain.chains import RetrievalQA
    from langchain_ollama.chat_models import ChatOllama
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain.prompts import PromptTemplate

    from langchain.chains import create_retrieval_chain
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    # Define the embeddings model name
    embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
    # Specify model arguments, including the device
    model_kwargs = {"device": "cpu"}
    # Load the embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model_name,
        model_kwargs=model_kwargs
    )


    # LoadExisting vector inex
    existing_vector_store = FAISS.load_local('.//faiss_index_USGS', embeddings, allow_dangerous_deserialization=True)

    # Initialize the LLaMA model
    llm = ChatOllama(model="llama3.2")

    # set the context of the query against the RAG Store
    retriever=existing_vector_store.as_retriever(search_kwargs = {"k":2})

    template = """Use the following pieces of context containing USGS research report data as well as daily water statistics for different montoring locations to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    context = {context}
    question = {question}

    Helpful Answer:"""

    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

    # Create the RetrievalQA chain with return_source_documents=True

    qa_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | QA_CHAIN_PROMPT
            | llm
            | StrOutputParser()
            )

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-mpnet-base-v2')

    result = qa_chain.invoke(query)
    print("EOP")
    return(result)


# Interactive query loop for testing the RAG ouput
#while True:
#    query = input("Type your query (or type 'Exit' to quit): \n")
   
#    if query.lower() == "exit":
#        break

#    result = get_ragdata(query)
#    print(result)



# sample query: what is the approval status for monitoring location USGS-01482100