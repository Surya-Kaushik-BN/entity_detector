import re
import json
import os
import sys
from typing import List, Dict

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_path)


class ProfaneLLMDetector:
    """
    A class to detect profane language in conversations using a language model (LLM).

    Attributes:
    ----------
    llm_client : object
        The language model client used to process conversations.
    result_ids : dict
        A dictionary to store IDs of conversations where profane language was used by 'Agent' or 'Customer'.

    Methods:
    -------
    detect_entity(conversations_list: List) -> bool:
        Detects if profane language was used in the given conversations.
    
    find_profane_words(conversations_list: List, id: str) -> None:
        Finds and stores IDs of conversations where profane language was used.
    
    get_all_profane_ids(file_path: str) -> Dict:
        Processes all JSON files in the given directory and returns a dictionary of IDs with profane conversations.
    
    llm_call(conversations_list: List) -> List:
        Calls the language model to process the conversation history and returns the response.
    
    get_prompt(conversation_history: str) -> str:
        Generates a prompt for the language model based on the conversation history.
    
    run(file_path: str) -> Dict:
        Runs the detection process on all JSON files in the given directory and returns a dictionary of profane IDs.
    """
    def __init__(self, llm_client):
        """
        Initializes the ProfaneLLMDetector with the given language model client.

        Parameters:
        ----------
        llm_client : object
            The language model client used to process conversations.
        """
        self.llm_client = llm_client
        self.result_ids = {'Agent': [], 'Customer': []}
    
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
        llm_response = self.llm_call(conversations_list=conversations_list)
        if len(llm_response) != 0:
            return True
        return False
        
    
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
        llm_response = self.llm_call(conversations_list=conversations_list)
        for role in llm_response:
            self.result_ids[role].append(id)
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
    

    def llm_call(self, conversations_list: List) -> List:
        """
        Calls the language model to process the conversation history and returns the response.

        Parameters:
        ----------
        conversations_list : List
            A list of conversations to be analyzed.

        Returns:
        -------
        List
            The response from the language model.
        """
        history = ""
        for conversation in conversations_list:
            history += f"{conversation['speaker']}: {conversation['text']}\n"
        
        prompt = self.get_prompt(conversation_history=history)
        response = self.llm_client.run(message=prompt)
        output = json.loads(response.text)
        
        return output
        

    def get_prompt(self, conversation_history: str) -> str:
        """
        Generates a prompt for the language model based on the conversation history.

        Parameters:
        ----------
        conversation_history : str
            The conversation history to be included in the prompt.

        Returns:
        -------
        str
            The generated prompt.
        """
        prompt = f"""
        The conversation between an 'Agent' and 'Customer' is shared below, enclosed between ```. 
        The Agents sentences and Customers sentences are denoted by their role, a colon and the sentence spoken by them.
        You need to go through each sentence of the conversation carefully, and identify if the Agent, Customer or both
        have used profane/vulgar words and language. Do not miss out on any profane words.

        The output should be a list. The list should contain the roles (Agent, Customer) if they have used profane language
        If both have used profane language, have both of them in the list. If one of them have used profane language, just give 
        one role in the list. If neither has used profane language, send out an empty list.
        Make sure it has no other addition character such as quote, \n, etc. I just want a list. 
        

        The conversation is as follows:
        ```
        {conversation_history}
        ```
        """
        return prompt

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