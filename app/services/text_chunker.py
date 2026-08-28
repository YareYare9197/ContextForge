class TextChunker:
    def __init__(
        self,
        max_characters: int = 1200,
        overlap_characters: int = 150,
    ):
        self.max_characters = max_characters
        self.overlap_characters = overlap_characters

    def split(self, text: str) -> list[str]:
        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

        chunks: list[str] = []
        current = ""

        for paragraph in paragraphs:
            candidate = (
                paragraph
                if not current
                else current + "\n\n" + paragraph
            )

            if current and len(candidate) > self.max_characters:
                chunks.append(current)

                overlap = current[-self.overlap_characters:]
                current = overlap + "\n\n" + paragraph
            else:
                current = candidate

        if current:
            chunks.append(current)

        return chunks
    