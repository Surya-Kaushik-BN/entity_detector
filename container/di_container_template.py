from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

import os
import sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_path)
from privacy_compliance_detector.llm_detector import PrivacyComplianceLLMDetector
from privacy_compliance_detector.regex_detector import PrivacyComplianceRegexDetector
from profanity_detector.llm_detector import ProfaneLLMDetector
from profanity_detector.regex_detector import ProfaneRegexDetector
from clients.llm_client import LLMClient



class DIContainer(containers.DeclarativeContainer):

    @classmethod
    def create_container(cls, ):
        container = cls()
        container.llm_client = providers.Singleton(LLMClient)
        container.verification_regex_detector = providers.Singleton(PrivacyComplianceRegexDetector)
        container.verification_llm_detector = providers.Singleton(PrivacyComplianceLLMDetector, container.llm_client)
        container.profane_regex_detector = providers.Singleton(ProfaneRegexDetector)
        container.profane_llm_detector = providers.Singleton(ProfaneLLMDetector, container.llm_client)
        return container        
