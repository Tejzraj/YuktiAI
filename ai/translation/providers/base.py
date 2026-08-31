from abc import ABC, abstractmethod


class TranslationProvider(ABC):
    @abstractmethod
    def translate(self, text: str, source_language: str, target_language: str) -> str:
        """
        Translates text from source_language to target_language.
        Raises Exception if provider fails.
        """
        pass
