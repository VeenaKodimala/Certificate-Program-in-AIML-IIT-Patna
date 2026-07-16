# RAG - Retrieval-Augmented Generation
- Usually, when we ask an LLM a question regarding my company's policy,it confidently generates data, which is hallucinated and not accurate. This is because the LLM does not have access to my company's policy documents. To solve this problem, we can use RAG (Retrieval-Augmented Generation) to retrieve relevant information from my company's policy documents and provide it to the LLM for generating accurate responses.
- My company's policy documents are highly confidential and cannot be shared with the LLM. That is when RAG comes into play. RAG allows us to retrieve relevant information from my company's policy documents without exposing the entire document to the LLM. This way, we can ensure that the LLM generates accurate responses based on the retrieved information while keeping the policy documents confidential.
- One more issue w/o RAG is, my policy document or any other confidential doc of that matter, will be very large. So,, on uploading thease large documents to LLM, the entire context window of the LLM will be filled with the document, leaving no space for the actual question. And also, so costly.
- This will result in the LLM not being able to generate accurate responses.
- RAG is actually a helper hand for LLM, by proviing the info, so that LLM can build an answer around it.

-------------------------------------------------------------

### Example scenario:

- Let's say we have a 1000 policy document that contains information about my company's all the policies. Now a chat bot has to be built so that, I f I ask any ques related to the above docs, the chatbot shld be able to answer.
- We cannot use any Inference providers(Groq,OpenAI etc), bcoz as seen earlier, it is costly and also data breach is inevitable. 
-------------------------------------------------------------
- For the above scenario, there are two phases:
  1. **Indexing Phase**: In this phase, we will index the 1000 policy documents using a vector database. The vector database will store the embeddings of the documents, which will allow us to retrieve relevant information quickly and efficiently.
  2. **Query/Retrieval Phase**: In this phase, when a user asks a question, we will retrieve relevant information from the vector database using the embeddings of the question. The retrieved information will then be provided to the LLM for generating accurate responses. 