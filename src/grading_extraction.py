from ollama import generate
import os
import re
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def list_folders(directory):
    try:
        # Get all entries in directory
        entries = os.listdir(directory)
        # Filter to only folders
        folders = [entry for entry in entries
                   if os.path.isdir(os.path.join(directory, entry))]
        return folders
    except Exception as e:
        logging.error(f"Error listing folders: {str(e)}")
        return []

# Function to list all files with name of grading_{student name}.md in the directory


def list_grading_files(directory):
    try:
        # Get all entries in directory
        entries = os.listdir(directory)
        # Filter to any files starting with grading_ and ending in .md
        grading_files = [entry for entry in entries
                         if os.path.isfile(os.path.join(directory, entry))
                         and entry.lower().startswith('grading_')
                         and entry.lower().endswith('.md')]
        return grading_files
    except Exception as e:
        logging.error(f"Error listing grading files: {str(e)}")
        return []


def extract_student_name(file_name):
    # Remove the grading_ prefix and .md suffix
    student_name = file_name.replace("grading_", "").replace(".md", "")
    return student_name


# # Extract grading data from a markdown file by using ollama llm model

# def extract_grading_data_from_markdown_file(file_path, model):
#     try:
#         # Read the file
#         with open(file_path, "r") as file:
#             file_contents = file.read()
#         # Use the model to extract data
#         prompt = """extract grading data from markdown file for each category, then total marks. Put the data in a dictionary
#         Example:

#         #### Structure (2/2 marks) -> {'structure': {'marks': 2, 'total': 2}}

#         #### Emotions/Feelings (1/1 mark) -> {'emotions/feelings': {'marks': 1, 'total': 1}}


#         ### Choose a tone to match the theme of the writing (3 marks)
#         - 1 mark: The tone is inconsistent or only partially matches the theme. The tone is dark and somewhat sci-fi, which doesn't match the cozy, humorous tone of the image.
#         -> {'tone': {'marks': 1, 'total': 3}}

#         ### Use at least THREE figurative languages (2/3) -> {'At least 3 figurative languages': {'marks': 2, 'total': 3}}

#         ### TOTAL MARKS: 10.5/14 (75%) -> {'total marks': {'marks': 10.5, 'total': 14}}

#         GRADING CONTENT:
#         """

#         structured_outputs = {
#             "type": "object",
#             "properties": {
#                     "structure": {
#                         "type": "object",
#                         "properties": {
#                             "marks": {"type": "number"},
#                             "total": {"type": "number"}
#                         }
#                     },
#                 "tone": {
#                         "type": "object",
#                         "properties": {
#                             "marks": {"type": "number"},
#                             "total": {"type": "number"}
#                         }
#                 },
#                 "emotions/feelings": {
#                         "type": "object",
#                         "properties": {
#                             "marks": {"type": "number"},
#                             "total": {"type": "number"}
#                         }
#                 },
#                 "precise words or phrases": {
#                         "type": "object",
#                         "properties": {
#                             "marks": {"type": "number"},
#                             "total": {"type": "number"}
#                         }
#                 },
#                 "use at least THREE figurative languages": {
#                         "type": "object",
#                         "properties": {
#                             "marks": {"type": "number"},
#                             "total": {"type": "number"}
#                         }
#                 },
#                 "have a moral": {
#                         "type": "object",
#                         "properties": {
#                             "marks": {"type": "number"},
#                             "total": {"type": "number"}
#                         }
#                 },
#                 "write with an outstanding idea": {
#                         "type": "object",
#                         "properties": {
#                             "marks": {"type": "number"},
#                             "total": {"type": "number"}
#                         }
#                 },
#                 "total marks": {
#                         "type": "object",
#                         "properties": {
#                             "marks": {"type": "number"},
#                             "total": {"type": "number"}
#                         }
#                 }
#             },
#             "required": [
#                 "structure",
#                 "tone",
#                 "emotions/feelings",
#                 "precise words or phrases",
#                 "use at least THREE figurative languages",
#                 "have a moral",
#                 "write with an outstanding idea",
#                 "total marks"
#             ]}

#         response = generate(
#             model=model, prompt=f"{prompt}: \n{file_contents}", format=structured_outputs
#         )
#         return response['response']
#     except Exception as e:
#         logging.error(f"Error extracting grading data: {str(e)}")
#         return {}


def extract_grading_data_from_markdown_file(file_path, model):
    try:
        # Read the file
        with open(file_path, "r") as file:
            file_contents = file.read()
        # Use the model to extract data
        prompt = """extract grading data from markdown file for each category, then total marks. Put the data in a dictionary
        Example:
        
        #### Structure (2/2 marks) -> {'structure': {'marks': 2, 'total': 2}}
        
        #### Emotions/Feelings (1/1 mark) -> {'emotions/feelings': {'marks': 1, 'total': 1}}
        
        
        ### Choose a tone to match the theme of the writing (3 marks)
        - 1 mark: The tone is inconsistent or only partially matches the theme. The tone is dark and somewhat sci-fi, which doesn't match the cozy, humorous tone of the image.
        -> {'tone': {'marks': 1, 'total': 3}}
        
        ### Use at least THREE figurative languages (2/3) -> {'At least 3 figurative languages': {'marks': 2, 'total': 3}}
        
        ### TOTAL MARKS: 10.5/14 (75%) -> {'total marks': {'marks': 10.5, 'total': 14}}
        
        GRADING CONTENT:
        """

        structured_outputs = {
            "type": "object",
            "properties": {
                    "structure": {
                        "type": "object",
                        "properties": {
                            "marks": {"type": "number"},
                            "total": {"type": "number"}
                        }
                    },
                "tone": {
                        "type": "object",
                        "properties": {
                            "marks": {"type": "number"},
                            "total": {"type": "number"}
                        }
                },
                "emotions/feelings": {
                        "type": "object",
                        "properties": {
                            "marks": {"type": "number"},
                            "total": {"type": "number"}
                        }
                },
                "precise words or phrases": {
                        "type": "object",
                        "properties": {
                            "marks": {"type": "number"},
                            "total": {"type": "number"}
                        }
                },
                "use at least THREE figurative languages": {
                        "type": "object",
                        "properties": {
                            "marks": {"type": "number"},
                            "total": {"type": "number"}
                        }
                },
                "have a moral": {
                        "type": "object",
                        "properties": {
                            "marks": {"type": "number"},
                            "total": {"type": "number"}
                        }
                },
                "write with an outstanding idea": {
                        "type": "object",
                        "properties": {
                            "marks": {"type": "number"},
                            "total": {"type": "number"}
                        }
                },
                "total marks": {
                        "type": "object",
                        "properties": {
                            "marks": {"type": "number"},
                            "total": {"type": "number"}
                        }
                }
            },
            "required": [
                "structure",
                "tone",
                "emotions/feelings",
                "precise words or phrases",
                "use at least THREE figurative languages",
                "have a moral",
                "write with an outstanding idea",
                "total marks"
            ]}
        response = generate(
            model=model, prompt=f"{prompt}: \n{file_contents}", format=structured_outputs
        )

        try:
            if isinstance(response['response'], str):
                response['response'] = json.loads(
                    response['response'].replace("'", '"'))
        except json.JSONDecodeError as e:
            logging.error(
                f"Failed to parse response string to dictionary: {e}")
            response['response'] = {}  # Fallback to empty dict

        return response['response']
    except Exception as e:
        logging.error(f"Error extracting grading data: {str(e)}")
        return {}


if __name__ == "__main__":
    folder = "./writings"
    logging.info(f"Folders found: {list_folders(folder)}")
    folder = "./writings/001_TabbyCat"
    files = list_grading_files(folder)
    logging.info(f"Grading files found: {files}")
    student_names = [extract_student_name(file) for file in files]
    logging.info(f"Student names extracted: {student_names}")
    # md_file = "./writings/001_TabbyCat/grading_mang.md"
    # md_file = "./writings/001_TabbyCat/grading_skylar.md"
    # md_file = "./writings/001_TabbyCat/grading_mang_1.md"
    md_file = "./writings/001_TabbyCat/grading_sue.md"

    models = [
        "phi3.5",
        "granite3.1-moe:1b",
        "granite3.1-dense:2b",
        "granite3.1-dense:latest",
        "llama3.2:latest",
        "minicpm-v:8b-2.6-q4_K_M",
        "vanilj/Phi-4:latest",
        "mistral",
        "phi3:3.8b-mini-4k-instruct-q8_0",
        "granite3.1-moe:3b-instruct-q8_0",
        "granite3.1-dense:8b-instruct-q5_K_M",
        "mistral-nemo:12b-instruct-2407-q4_K_M"
    ]

    model = models[4]

    grading_data = extract_grading_data_from_markdown_file(
        md_file, model)
    logging.info(
        f"Grading data extracted: {grading_data}")
