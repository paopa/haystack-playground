"""
I'd like to validate a case that one document store component in two or
more pipelines.

Conclusion:
after running the code, we can see that the document store component
works well in two or more pipelines. so the same object can be used in
two or more pipelines.
"""

from haystack.dataclasses.document import Document
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from haystack.document_stores.types import DuplicatePolicy
from haystack.components.writers import DocumentWriter
from haystack import Pipeline

document_store = QdrantDocumentStore(
    ":memory:",
    embedding_dim=5,
    recreate_index=True,
    return_embedding=True,
    wait_result_from_api=True,
)
document_store.write_documents(
    [
        Document(content="This is first", embedding=[0.0] * 5),
        Document(content="This is second", embedding=[0.1, 0.2, 0.3, 0.4, 0.5]),
    ]
)

print(document_store.count_documents())


async def case(id: int):
    documents = [
        Document(content=f"id: {id}, This is third", embedding=[0.0] * 5),
        Document(
            content=f"id: {id}, This is fourth", embedding=[0.1, 0.2, 0.3, 0.4, 0.5]
        ),
    ]

    document_writer = DocumentWriter(
        document_store=document_store, policy=DuplicatePolicy.NONE
    )

    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component(instance=document_writer, name="writer")

    indexing_pipeline.run({"writer": {"documents": documents}})

    print(f"id: {id}, count: {document_store.count_documents()}")


tasks = [case(i) for i in range(5)]

import asyncio

asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
