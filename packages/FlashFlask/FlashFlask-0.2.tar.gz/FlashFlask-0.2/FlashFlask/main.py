import os
import zipfile
import requests
import shutil
from datetime import datetime

COMMIT_ID = "a722c20508896a00004d1181d6b95ba19fead1c9"
LICENSES_FOLDER = "licenses/"
LICENSE_KEYWORDS = {
    "AFL-3.0": "Academic Free License v3.0",
    "Apache-2.0": "Apache license 2.0",
    "Artistic-2.0": "Artistic license 2.0",
    "BSL-1.0": "Boost Software License 1.0",
    "BSD-2-Clause": 'BSD 2-clause "Simplified" license',
    "BSD-3-Clause": 'BSD 3-clause "New" or "Revised" license',
    "BSD-3-Clause-Clear": "BSD 3-clause Clear license",
    "BSD-4-Clause": 'BSD 4-clause "Original" or "Old" license',
    "0BSD": "BSD Zero-Clause license",
    "CC0-1.0": "Creative Commons Zero v1.0 Universal",
    "CC-BY-4.0": "Creative Commons Attribution 4.0",
    "CC-BY-SA-4.0": "Creative Commons Attribution ShareAlike 4.0",
    "WTFPL": "Do What The F*ck You Want To Public License",
    "ECL-2.0": "Educational Community License v2.0",
    "EPL-1.0": "Eclipse Public License 1.0",
    "EPL-2.0": "Eclipse Public License 2.0",
    "EUPL-1.1": "European Union Public License 1.1",
    "AGPL-3.0": "GNU Affero General Public License v3.0",
    "GPL-2.0": "GNU General Public License v2.0",
    "GPL-3.0": "GNU General Public License v3.0",
    "LGPL-2.1": "GNU Lesser General Public License v2.1",
    "LGPL-3.0": "GNU Lesser General Public License v3.0",
    "ISC": "ISC",
    "LPPL-1.3c": "LaTeX Project Public License v1.3c",
    "MS-PL": "Microsoft Public License",
    "MIT": "MIT",
    "MPL-2.0": "Mozilla Public License 2.0",
    "OSL-3.0": "Open Software License 3.0",
    "PostgreSQL": "PostgreSQL License",
    "OFL-1.1": "SIL Open Font License 1.1",
    "NCSA": "University of Illinois/NCSA Open Source License",
    "Unlicense": "The Unlicense",
    "Zlib": "zLib License",
}


def get_latest_commit_id():
    url = f"https://api.github.com/repos/anxkhn/Flask-Starter-Template/commits"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        commits = response.json()

        if commits:
            latest_commit_id = commits[0]["sha"]
            return latest_commit_id
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None


def get_license_text(license_key):
    license_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        LICENSES_FOLDER,
        f"{license_key}.txt",
    )
    if os.path.exists(license_file_path):
        with open(license_file_path, "r") as license_file:
            return license_file.read()
    else:
        return None


def download_license(license_key, project_path, project_name, author):
    license_text = get_license_text(license_key)
    if license_text:
        # Replace placeholders with actual values
        license_text = license_text.replace("[year]", str(datetime.now().year))
        license_text = license_text.replace("<year>", str(datetime.now().year))
        license_text = license_text.replace("[yyyy]", str(datetime.now().year))
        license_text = license_text.replace("<fullname>", author)
        license_text = license_text.replace("<name of author>", author)
        license_text = license_text.replace("[fullname]", author)
        license_text = license_text.replace("[name of copyright owner]", author)
        license_file_path = os.path.join(project_path, "LICENSE.txt")
        with open(license_file_path, "w") as license_file:
            license_file.write(license_text)
    else:
        print(f"Failed to download license text for '{license_key}'.")


def extract_zip(zip_path, extract_path, project_name, lis, author):
    current_commit = get_latest_commit_id()
    if current_commit != COMMIT_ID:
        response = requests.get(
            "https://codeload.github.com/anxkhn/Flask-Starter-Template/zip/refs/heads/main",
            stream=True,
        )
        if response.status_code == 200:
            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)
        else:
            pass
    extract_dir = os.path.join(extract_path, project_name)
    while os.path.exists(extract_dir):
        user_input = input(
            f"The directory '{extract_dir}' already exists. Do you want to overwrite it? (yes/no): "
        )
        if user_input.lower() == "yes":
            shutil.rmtree(extract_dir)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            print(f"Successfully overwritten.")
            break
        else:
            project_name = input("Enter new project name: ").strip()
            extract_dir = os.path.join(extract_path, project_name)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    extracted_folder_path = os.path.join(extract_dir, "Flask-Starter-Template-main")
    # Move all contents from the extracted folder to the extract_dir
    for item in os.listdir(extracted_folder_path):
        item_path = os.path.join(extracted_folder_path, item)
        new_path = os.path.join(extract_dir, item)
        os.rename(item_path, new_path)
    # Remove the now-empty extracted folder
    os.rmdir(extracted_folder_path)
    # Optionally, you can update files or perform other actions based on user input
    update_project_metadata(extract_dir, project_name, lis, author)
    if not lis:
        # Default to MIT if no license is provided
        print("Defaulting to MIT license.")
        download_license("MIT", extract_dir, project_name, author)
    else:
        download_license(lis, extract_dir, project_name, author)


def update_project_metadata(extract_dir, project_name, lis, author):
    metadata_file = os.path.join(extract_dir, "metadata.txt")
    layout_file_path = os.path.join(extract_dir, "templates", "layout.html")
    # Update metadata.txt
    with open(metadata_file, "w") as f:
        f.write(f"Project: {project_name}\n")
        f.write(f"License: {lis}\n")
        f.write(f"Author: {author}\n")
    # Update layout.html
    with open(layout_file_path, "r") as layout_file:
        layout_content = layout_file.read()
    updated_layout_content = layout_content.replace("Your Project", project_name)
    with open(layout_file_path, "w") as layout_file:
        layout_file.write(updated_layout_content)


def list_available_licenses():
    print("Available licenses:")
    for i, (keyword, name) in enumerate(LICENSE_KEYWORDS.items(), start=1):
        print(f"{i}. {name} ({keyword})")


def main():
    zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.zip")
    extract_path = (
        input("Enter extraction path (default is current): ").strip() or os.getcwd()
    )
    project_name = input("Enter project name: ").strip()
    license_choice = input(
        "Enter the number of the license or 'help' to see available licenses: "
    ).strip()
    if license_choice.lower() == "help":
        list_available_licenses()
        license_choice = input("Enter the number of the license: ").strip()
    # Check if the user entered a number or the license name directly
    if license_choice.isdigit():
        try:
            license_choice = int(license_choice)
            if 1 <= license_choice <= len(LICENSE_KEYWORDS):
                lis = list(LICENSE_KEYWORDS.keys())[license_choice - 1]
            else:
                raise ValueError()
        except (ValueError, IndexError):
            print("Invalid license choice. Defaulting to MIT license.")
            lis = "MIT"
    else:
        # User entered the license name directly
        lis = license_choice
    author = input("Enter author: ").strip()
    extract_zip(zip_path, extract_path, project_name, lis, author)


if __name__ == "__main__":
    main()
