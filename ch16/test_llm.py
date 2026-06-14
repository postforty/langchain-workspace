import asyncio
from interface_adapters.llm_services.langchain_client import LangChainGeminiClient

client = LangChainGeminiClient()
# Before running we need to make sure we get the response from the chain directly.
chain = client._qa_chain
res = chain.invoke({"query": "독백이 뭐야?", "context": "독백은 혼자 하는 말이다."})
print("TYPE:", type(res))
print("VALUE:", repr(res))
