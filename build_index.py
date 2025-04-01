from rags_utils import load_texts_from_folder, build_vector_index
import sys

folder = sys.argv[1] if len(sys.argv) > 1 else "data_topic"
docs = load_texts_from_folder(folder)
build_vector_index(docs)
print(f"✅ RAG index built from folder: {folder}")

