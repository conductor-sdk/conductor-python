from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .Skill import SkillDocument

# RAG Service Interface
class SkillRegistryService(ABC):
    @abstractmethod
    def add_document(self, document: SkillDocument):
        """Add a single document to the registry"""
        pass
    
    @abstractmethod
    def find_relevant_skills(self, description: str, k: int = 5) -> List[SkillDocument]:
        """Find relevant skills for a given description"""
        pass
    
    @abstractmethod
    def get_document(self, doc_id: str) -> Optional[SkillDocument]:
        """Retrieve a specific document"""
        pass

# Stub implementation for now
class InMemorySkillRegistry(SkillRegistryService):
    def __init__(self):
        self.documents: Dict[str, SkillDocument] = {}
        
    def add_document(self, document: SkillDocument):
        self.documents[document.id] = document
    
    def find_relevant_skills(self, description: str, k: int = 5) -> List[SkillDocument]:
        # Stub implementation - return all documents for now
        return list(self.documents.values())[:k]
    
    def get_document(self, doc_id: str) -> Optional[SkillDocument]:
        return self.documents.get(doc_id)
