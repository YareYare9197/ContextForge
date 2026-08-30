class PromptBuilder:
    def build(
        self,
        question: str,
        chunks: list[dict],
    ) -> dict[str, str]:
        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty")

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

        system_prompt = (
            "You answer questions using only the provided context. "
            "If the context does not contain the answer, say that the "
            "answer was not found in the uploaded documents. "
            "Do not invent facts. Mention the source numbers you used."
        )

        user_prompt = (
            f"Context:\n{context}\n\n"
            f"Question:\n{question}"
        )

        return {
            "system": system_prompt,
            "user": user_prompt,
        }