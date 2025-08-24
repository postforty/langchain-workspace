import pymupdf

file_path = r"data\KCI_FI003153549.pdf" # raw-string
doc = pymupdf.open(file_path)

# print(doc)
# print(doc.metadata)
# print(len(doc))
# print(doc[5].get_text())

full_text = ""
for page in doc:
    # pdf 문서 전처리
    clip_rect = pymupdf.Rect(
        0, # 왼쪽 x 좌표
        90, # 상단 y 좌표 (머리글 높이만큼 제외)
        page.rect.width, # 오른쪽 x 좌표 (페이지 전체 너비)
        page.rect.height - 0, # 하단 y 좌표
    )

    text = page.get_text(clip=clip_rect)
    full_text += text

# print(full_text)

# 텍스트 파일 생성
with open("output/result_pymupdf.txt", 'w', encoding="utf-8") as f:
    f.write(full_text)
