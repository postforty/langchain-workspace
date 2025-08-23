from langchain_community.document_loaders import PyPDFLoader

# https:/www.riss.kr
file_path = r"data\KCI_FI003153549.pdf"
loader = PyPDFLoader(file_path)

print(loader)