from dataclasses import dataclass

@dataclass
class ChatResponse:
    question : str
    answer : str 
    document_path : str