import os
import re
import logging

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

def extract_grading_data_from_markdown(base_dir):
    data = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Regular expression to capture lines with marks
                    matches = re.findall(r'### (.+) \(([\d\.]+)/[\d\.]+\s?marks?)\)', content)

                    # Extract file folder name
                    folder = root.split(os.sep)[-1]

                    for category, points in matches:
                      data.append({
                          "folder": folder,
                          "file": file,
                          "category": category.strip(),
                          "points": float(points.strip())
                      })
    return data

def extract_student_name(file_name):
    # Remove the grading_ prefix and .md suffix
    student_name = file_name.replace("grading_", "").replace(".md", "")
    return student_name

def extract_grading_data_from_markdown_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Regular expression to capture lines with marks
            matches = re.findall(r'### (.+) \(([\d\.]+)/[\d\.]+\s?marks?)\)', content)
            return matches
    except Exception as e:
        logging.error(f"Error extracting grading data from markdown file: {str(e)}")
        return []

if __name__ == "__main__":
    logging.info(f"Folders found: {list_folders('../writings')}")
    files = list_grading_files("../writings/001_TabbyCat")
    logging.info(f"Grading files found: {files}")
    student_names = [extract_student_name(file) for file in files]
    logging.info(f"Student names extracted: {student_names}")
    grading_data = extract_grading_data_from_markdown("../writings/001_TabbyCat/grading_mang.md")
    logging.info(f"Grading data extracted: {grading_data}")
