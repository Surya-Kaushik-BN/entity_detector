import re
import json
import os
import sys
from typing import List, Dict


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProfaneRegexDetector:
    """
    A class to detect profane language in conversations using regular expressions.

    Attributes:
    ----------
    profanity_pattern : re.Pattern
        A compiled regular expression to match profane words.
    result_ids : dict
        A dictionary to store IDs of conversations where profane language was used by 'Agent' or 'Customer'.

    Methods:
    -------
    detect_entity(conversations_list: List) -> bool:
        Detects if profane language was used in the given conversations.
    
    detect_profanity(text: str) -> bool:
        Checks if the given text contains profane words.
    
    find_profane_words(conversations_list: List, id: str) -> None:
        Finds and stores IDs of conversations where profane language was used.
    
    get_all_profane_ids(file_path: str) -> Dict:
        Processes all JSON files in the given directory and returns a dictionary of IDs with profane conversations.
    
    run(file_path: str) -> Dict:
        Runs the detection process on all JSON files in the given directory and returns a dictionary of profane IDs.
    """
    def __init__(self):
        """
        Initializes the ProfaneRegexDetector with predefined patterns for profane words.

        Loads the profane words from a JSON file and compiles them into a regular expression pattern.
        """
        with open(os.path.join(base_path, "profanity_detector", "profane_words.json"), "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                profane_words = data
        self.profanity_pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, profane_words)) + r')\b', re.IGNORECASE)
        self.result_ids = {"Agent": [], "Customer": []}

    
    def detect_entity(self, conversations_list: List) -> bool:
        """
        Detects if profane language was used in the given conversations.

        Parameters:
        ----------
        conversations_list : List
            A list of conversations to be analyzed.

        Returns:
        -------
        bool
            True if profane language was used, False otherwise.
        """
        for conversation in conversations_list: 
            if self.detect_profanity(conversation["text"]): 
                return True
        return False

    def detect_profanity(self, text: str) -> bool:
        """
        Checks if the given text contains profane words.

        Parameters:
        ----------
        text : str
            The text to be analyzed.

        Returns:
        -------
        bool
            True if the text contains profane words, False otherwise.
        """
        return bool(self.profanity_pattern.search(text))
    
    def find_profane_words(self, conversations_list: List, id: str) -> None:
        """
        Finds and stores IDs of conversations where profane language was used.

        Parameters:
        ----------
        conversations_list : List
            A list of conversations to be analyzed.
        id : str
            The ID of the conversation being analyzed.
        """
        detection_count = {"Agent": 0, "Customer": 0}
        for conversation in conversations_list: 
            if self.detect_profanity(conversation["text"]): 
                detection_count[conversation["speaker"]] += 1
        
        if detection_count["Agent"] != 0:
            self.result_ids["Agent"].append(id)
        if detection_count["Customer"] != 0:
            self.result_ids["Customer"].append(id)
        return

    def get_all_profane_ids(self, file_path: str) -> Dict:
        """
        Processes all JSON files in the given directory and returns a dictionary of IDs with profane conversations.

        Parameters:
        ----------
        file_path : str
            The path to the directory containing JSON files.

        Returns:
        -------
        Dict
            A dictionary of IDs with profane conversations.
        """
        files = os.listdir(file_path)
        json_files = [file for file in files if file.endswith('.json')]
        for file in json_files:
            with open(os.path.join(file_path, file), "r") as f:
                data = json.load(f)
            self.find_profane_words(conversations_list=data, id=file.split(".")[0])
        
        return self.result_ids

    def run(self, file_path: str) -> Dict:
        """
        Runs the detection process on all JSON files in the given directory and returns a dictionary of profane IDs.

        Parameters:
        ----------
        file_path : str
            The path to the directory containing JSON files.

        Returns:
        -------
        Dict
            A dictionary of IDs with profane conversations.
        """
        return self.get_all_profane_ids(file_path=file_path)