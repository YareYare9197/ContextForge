class PromptBuilder:
    def build(
        self,
        question: str,
        chunks: list[dict],
    ) -> dict[str, str]:
        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty")

        if not chunks:
            return {
                "system": (
                    "No relevant uploaded document was found. "
                    "Answer the question using general knowledge. "
                    "Clearly state that the answer is general and not "
                    "based on an uploaded document. "
                    "Do not invent sources."
                ),
                "user": question,
            }

        context_parts = []

        for index, chunk in enumerate(chunks, start=1):
            source = (
                f"document={chunk['document_id']}, "
                f"chunk={chunk['chunk_index']}"
            )

            context_parts.append(
                f"[Source {index}: {source}]\n"
                f"{chunk['content']}"
            )

        context = "\n\n".join(context_parts)

        return {
            "system": (
                "Answer using only the provided document context. "
                "Do not invent facts. "
                "Mention the source numbers used."
            ),
            "user": (
                f"Context:\n{context}\n\n"
                f"Question:\n{question}"
            ),
        }