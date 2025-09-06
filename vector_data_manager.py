def store_ragdata(datastore):
# Read all data to be kept in FAISS DataStore
    #datastore = ".//ApiData/"

    import json
    from langchain_text_splitters import RecursiveJsonSplitter
    from langchain_core.documents import Document

    #from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings

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
            if filename.endswith(".json"):
                    filepath = os.path.join(dirpath, filename)
                    print(filepath)

                    with open(filepath, 'r') as file:
                        json_data_1 = json.load(file)
                        json_data = [
                                    json_data_1,
                                    ]
                        documents = [
                            Document(page_content=item["type"], metadata={k: v for k, v in item.items() if k != "type"})
                            for item in json_data
                                    ]

                        # LoadExisting vector index
                    try:
                        existing_vector_store = FAISS.load_local('.//faiss_index_USGS', embeddings, allow_dangerous_deserialization=True)
                        
                        # Generate embeddings for new data chunks
                        existing_vector_store.add_documents(documents)
                        #new_vector_store = FAISS.from_documents(documents, embeddings)
                        #existing_vector_store.merge_from(new_vector_store)
                        existing_vector_store.save_local('.//faiss_index_USGS')

                        print("updated")

                    except:
                                                
                        # Create FAISS vector store
                        vectorstore = FAISS.from_documents(documents, embeddings)

                        # Save and reload the vector store
                        vectorstore.save_local("faiss_index_USGS")
                        
                        # Create a retriever
                        #existing_vector_store = FAISS.load_local("faiss_index_USGS", embeddings, allow_dangerous_deserialization=True)
                        #retriever = existing_vector_store.as_retriever()
                        print("new")

##full load Test
#datastore = ".//ApiData/"
#store_ragdata(datastore)
