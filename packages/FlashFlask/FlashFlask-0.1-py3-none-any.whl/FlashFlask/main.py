import os
import zipfile
from datetime import datetime

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
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        extract_dir = os.path.join(extract_path, project_name)
        zip_ref.extractall(extract_dir)
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
    with open(metadata_file, "w") as f:
        f.write(f"Project: {project_name}\n")
        f.write(f"License: {lis}\n")
        f.write(f"Author: {author}\n")


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
