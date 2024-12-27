from langchain_community.document_loaders import (
    DirectoryLoader,
    UnstructuredMarkdownLoader,
)
from langchain_community.vectorstores.utils import filter_complex_metadata


def load_documents(path: str):
    loader = DirectoryLoader(
        path,
        glob="**/*.md",
        loader_cls=UnstructuredMarkdownLoader,
        loader_kwargs={"mode": "elements"},
    )
    docs = loader.load()
    return filter_complex_metadata(docs)
