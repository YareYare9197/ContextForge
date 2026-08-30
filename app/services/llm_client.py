from typing import Protocol


class LLMClient(Protocol):
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        ...


class MockLLMClient:
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        return "Mock answer generated from retrieved context."
    