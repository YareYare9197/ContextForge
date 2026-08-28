from pathlib import Path


class DocumentReader:
    def read(
        self,
        path: Path,
        content_type: str,
    ) -> str:
        if not path.exists():
            raise FileNotFoundError("stored file not found")

        is_text_file = (
            content_type.startswith("text/")
            or path.suffix.lower() in {".md", ".txt"}
        )

        if not is_text_file:
            raise ValueError(
                "only Markdown and text files are supported currently"
            )

        return path.read_text(encoding="utf-8")
        