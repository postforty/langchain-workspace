from langchain_community.document_loaders import PyPDFLoader

# https:/www.riss.kr
file_path = r"data\KCI_FI003153549.pdf" # raw-string
loader = PyPDFLoader(file_path)

# print(loader)

pages = loader.load()

# print(type(pages))
# print(len(pages))
# print(pages[5])

full_txt = ""

for page in pages:
    full_txt += page.page_content

print(full_txt)
