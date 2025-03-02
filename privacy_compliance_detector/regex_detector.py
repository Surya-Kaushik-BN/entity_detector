import re
import json
import os
import sys
from typing import List

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PrivacyComplianceRegexDetector:
    """
    A class to detect privacy compliance issues in conversations using regular expressions.

    Attributes:
    ----------
    verification_patterns : list
        A list of patterns to identify verification phrases.
    verification_regex : re.Pattern
        A compiled regular expression to match verification phrases.
    sensitive_patterns : list
        A list of patterns to identify sensitive information.
    sensitive_regex : re.Pattern
        A compiled regular expression to match sensitive information.
    unverified_call_ids : list
        A list to store IDs of conversations where sensitive information was shared before verification.

    Methods:
    -------
    detect_entity(conversations_list: List) -> bool:
        Detects if sensitive information was shared before verification in the given conversations.
    
    is_verification_present(conversation: List) -> bool:
        Checks if verification is present in the given conversation.
    
    contains_sensitive_info(text: str) -> bool:
        Checks if the given text contains sensitive information.
    
    find_error_calls(conversation: List, id: str) -> None:
        Finds and stores IDs of conversations where sensitive information was shared before verification.
    
    get_all_unverified_ids(file_path: str) -> List:
        Processes all JSON files in the given directory and returns a list of IDs with unverified conversations.
    
    run(file_path: str) -> List:
        Runs the detection process on all JSON files in the given directory and returns a list of unverified IDs.
    """
    def __init__(self):
        """
        Initializes the PrivacyComplianceRegexDetector with predefined patterns for verification and sensitive information.
        """
        self.verification_patterns = [
            r"date of birth", r"dob", r"birth date", r"address", r"social security number", r"ssn"
        ]
        self.verification_regex = re.compile('|'.join(self.verification_patterns), re.IGNORECASE)

        self.sensitive_patterns = [
            r"account number", r"balance", r"amount due", \
            r"outstanding balance", r"card details", r"available credit", \
            r"funds", r"statement", r"your account"
        ]
        self.sensitive_regex = re.compile('|'.join(self.sensitive_patterns), re.IGNORECASE)

        self.unverified_call_ids = []
    
    def detect_entity(self, conversations_list: List) -> bool:
        """
        Detects if sensitive information was shared before verification in the given conversations.

        Parameters:
        ----------
        conversations_list : List
            A list of conversations to be analyzed.

        Returns:
        -------
        bool
            True if sensitive information was shared before verification, False otherwise.
        """
        if not self.is_verification_present(conversations_list):
            for entry in conversations_list:
                if entry["speaker"].lower() == "agent" and self.contains_sensitive_info(entry["text"]):
                    return True # Unverified
        return False

    def is_verification_present(self, conversation: List) -> bool:
        """
        Checks if verification is present in the given conversation.

        Parameters:
        ----------
        conversation : List
            A list of conversation entries to be analyzed.

        Returns:
        -------
        bool
            True if verification is present, False otherwise.
        """
        for entry in conversation:
            if entry["speaker"].lower() == "agent" and self.verification_regex.search(entry["text"]):
                return True
        return False
    
    def contains_sensitive_info(self, text: str) -> bool:
        """
        Checks if the given text contains sensitive information.

        Parameters:
        ----------
        text : str
            The text to be analyzed.

        Returns:
        -------
        bool
            True if the text contains sensitive information, False otherwise.
        """
        return bool(self.sensitive_regex.search(text))
    
    def find_error_calls(self, conversation: List, id: str) -> None:
        """
        Finds and stores IDs of conversations where sensitive information was shared before verification.

        Parameters:
        ----------
        conversation : List
            A list of conversation entries to be analyzed.
        id : str
            The ID of the conversation being analyzed.
        """
        if not self.is_verification_present(conversation):
            for entry in conversation:
                if entry["speaker"].lower() == "agent" and self.contains_sensitive_info(entry["text"]):
                    self.unverified_call_ids.append(id)
                    break

    def get_all_unverified_ids(self, file_path: str) -> List:
        """
        Processes all JSON files in the given directory and returns a list of IDs with unverified conversations.

        Parameters:
        ----------
        file_path : str
            The path to the directory containing JSON files.

        Returns:
        -------
        List
            A list of IDs with unverified conversations.
        """
        files = os.listdir(file_path)
        json_files = [file for file in files if file.endswith('.json')]
        for file in json_files:    
            with open(os.path.join(file_path, file), "r") as f:
                data = json.load(f)
            self.find_error_calls(conversation=data, id=file.split(".")[0])
        
        return self.unverified_call_ids
    
    def run(self, file_path: str) -> List:
        """
        Runs the detection process on all JSON files in the given directory and returns a list of unverified IDs.

        Parameters:
        ----------
        file_path : str
            The path to the directory containing JSON files.

        Returns:
        -------
        List
            A list of IDs with unverified conversations.
        """
        return self.get_all_unverified_ids(file_path=file_path)