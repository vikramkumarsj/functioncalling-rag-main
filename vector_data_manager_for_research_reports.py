def store_ragdata(datastore):
# Read all data to be kept in FAISS DataStore
    #datastore = ".//ApiData/"

    import json
    from langchain_text_splitters import RecursiveJsonSplitter
    from langchain_core.documents import Document

    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings

    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter


    # Define the embeddings model name
    embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
    # Specify model arguments, including the device
    model_kwargs = {"device": "cpu"}
    # Load the embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model_name,
        model_kwargs=model_kwargs
    )

    import os

    for dirpath, dirnames, filenames in os.walk(datastore):
        for filename in filenames:
            if filename.endswith(".pdf"):
                    filepath = os.path.join(dirpath, filename)
                    print(filepath)

                    # 1. Load and Extract Text
                    loader = PyPDFLoader(filepath)
                    pages = loader.load_and_split()
                    text = " ".join([page.page_content for page in pages])

                    # 2. Chunk the Text
                    text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                    )
                    chunks = text_splitter.split_text(text)

   
                    try:
                        existing_vector_store = FAISS.load_local('.//faiss_index_USGS', embeddings, allow_dangerous_deserialization=True)
                        
                        # Generate embeddings for new data chunks
                        existing_vector_store.add_texts(chunks)
                        #new_vector_store = FAISS.from_documents(documents, embeddings)
                        #existing_vector_store.merge_from(new_vector_store)
                        existing_vector_store.save_local('.//faiss_index_USGS')

                        print("updated")

                    except:
                                                
                        # Create FAISS vector store
                        vector_store = FAISS.from_texts(chunks, embeddings)

                        # Save and reload the vector store
                        vectorstore.save_local("faiss_index_USGS")
                        
                        # Create a retriever
                        #existing_vector_store = FAISS.load_local("faiss_index_USGS", embeddings, allow_dangerous_deserialization=True)
                        #retriever = existing_vector_store.as_retriever()
                        print("new")

#full load Test
#datastore = ".//research_reports/"
#store_ragdata(datastore)


