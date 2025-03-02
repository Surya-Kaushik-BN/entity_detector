# entity_detector

## Overview
The `entity_detector` repository provides a Streamlit-based web application for detecting entities such as profanity and privacy compliance issues in text data. The application supports both pattern matching and machine learning (LLM) methods for entity detection.

## Features
- **Profanity Detection**: Detects profane content using regex patterns or LLM.
- **Privacy and Compliance Detection**: Identifies privacy compliance issues using regex patterns or LLM.
- **Streamlit UI**: User-friendly interface for uploading JSON files and selecting detection methods.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/entity_detector.git
    cd entity_detector
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Open your web browser and navigate to 'https://entitydetector-fdyapffkbgp6m8raipgkpt.streamlit.app/'

2. Upload the JSON file containing the dataset.

3. Select the entity type and detection method, then click the "Detect Entity" button to start the analysis.

## Running the application locally
1. Run the Streamlit application:
    ```sh
    streamlit run UI/streamlit_app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Upload a JSON file containing the text data you want to analyze.

4. Select the entity type and detection method, then click the "Detect Entity" button to start the analysis.

## Finding entities using a batch of documents.
1. Go to any detector class and initiate it, and use the run method, providing the directory path which contains all the files.

## Project Structure
- `container/di_container_template.py`: Dependency injection container setup.
- `UI/streamlit_app.py`: Streamlit application for the user interface.
- `privacy_compliance_detector/`: Contains detectors for privacy compliance.
- `profanity_detector/`: Contains detectors for profanity.
- `clients/llm_client.py`: Client for interacting with the LLM.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License.