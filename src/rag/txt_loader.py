import os

def load_txt_documents(folder_path):

    documents = []

    for root, dirs, files in os.walk(folder_path):

        for file in files:

            if file.endswith(".txt"):

                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:

                    text = f.read()

                documents.append({
                    "source": file,
                    "folder": os.path.basename(root),
                    "content": text
                })

    return documents