import json
import os
import sys
from typing import List


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_path)

from dotenv import load_dotenv
load_dotenv()

class PrivacyComplianceLLMDetector:
    """
    A class to detect privacy compliance issues in conversations using a language model (LLM).

    Attributes:
    ----------
    llm_client : object
        The language model client used to process conversations.
    unverified_call_ids : list
        A list to store IDs of conversations where sensitive information was shared before verification.

    Methods:
    -------
    detect_entity(conversations_list: List) -> bool:
        Detects if sensitive information was shared before verification in the given conversations.
    
    find_unverified_conversations(conversations_list: List, id: str) -> None:
        Finds and stores IDs of conversations where sensitive information was shared before verification.
    
    get_all_unverified_ids(file_path: str) -> List:
        Processes all JSON files in the given directory and returns a list of IDs with unverified conversations.
    
    llm_call(conversations_list: List) -> str:
        Calls the language model to process the conversation history and returns the response.
    
    get_prompt(conversation_history: str) -> str:
        Generates a prompt for the language model based on the conversation history.
    
    run(file_path: str) -> List:
        Runs the detection process on all JSON files in the given directory and returns a list of unverified IDs.
    """
    def __init__(self, llm_client):
        """
        Initializes the PrivacyComplianceLLMDetector with the given language model client.

        Parameters:
        ----------
        llm_client : object
            The language model client used to process conversations.
        """
        self.llm_client = llm_client
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
        llm_response = self.llm_call(conversations_list=conversations_list)
        if llm_response == 'Y':
            return True
        return False

    def find_unverified_conversations(self, conversations_list: List, id: str) -> None:
        """
        Finds and stores IDs of conversations where sensitive information was shared before verification.

        Parameters:
        ----------
        conversations_list : List
            A list of conversations to be analyzed.
        id : str
            The ID of the conversation being analyzed.
        """
        llm_response = self.llm_call(conversations_list=conversations_list)
        if llm_response == 'Y':
            self.unverified_call_ids.append(id)
        return

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
            self.find_unverified_conversations(conversations_list=data, id=file.split(".")[0])
        
        return self.unverified_call_ids

    def llm_call(self, conversations_list: List) -> str:
        """
        Calls the language model to process the conversation history and returns the response.

        Parameters:
        ----------
        conversations_list : List
            A list of conversations to be analyzed.

        Returns:
        -------
        str
            The response from the language model.
        """
        history = ""
        for conversation in conversations_list:
            history += f"{conversation['speaker']}: {conversation['text']}\n"
        
        prompt = self.get_prompt(conversation_history=history)
        
        response = self.llm_client.run(message=prompt)
        output = response.text.strip()
        
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
        You need to go through each sentence of the conversation carefully, and see if the Agent has shared sensitive information
        before partial or full identity verification of the customer.

        Senstive information includes Balance or account details
        Identify verification is done using date of birth(dob) or address or social security number (ssn). 
        Please note that social security number or address can be partially identified. If partially identified, then it is 
        considered as verified. 

        The output should be just a 'Y' or 'N'.
        - If the Agent has shared senstive information before identity verification respond with 'Y'.
        - If the Agent has shared sensitive information after complete identity verification  respond with 'N'.
        - If the Agent asks for partial identity information and the Customer provides the corresponding
          partial verification data,  respond with 'N'.
          For example, if the Agent asks for last 4 characters of SSN, and the user gives the last 4 characters
          that is considered as verified. The output should be strictly 'N'. Do not take your own decision and wrongly respond with
          'Y' justifying that the complete information was not give. 
        - If the Agent has not shared sensitive information at all  respond with 'N'.


        Strictly understand the context of the conversation. Identify if identity verification is done before agent shares sensitive
        information. 
        

        The conversation is as follows:
        ```
        {conversation_history}
        ```
        """
        return prompt

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