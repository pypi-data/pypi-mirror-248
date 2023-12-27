import requests
import os
import argparse
from tqdm import tqdm

TITLE = """\
  ____  _____    _    ____  __  __ _____    __               ____ _ _   _   _       _ 
 |  _ \| ____|  / \  |  _ \|  \/  | ____|  / _| ___  _ __   / ___(_) |_| | | |_   _| |__  
 | |_) |  _|   / _ \ | | | | |\/| |  _|   | |_ / _ \| '__| | |  _| | __| |_| | | | | '_ \ 
 |  _ <| |___ / ___ \| |_| | |  | | |___  |  _| (_) | |    | |_| | | |_|  _  | |_| | |_) |
 |_| \_\_____/_/   \_\____/|_|  |_|_____| |_|  \___/|_|     \____|_|\__|_| |_|\__,_|_.__/ 
                                                                                          
"""  # nopep8


def download_file_with_progress(url, title):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(
        desc=title,
        total=total_size,
        unit='iB',
        unit_scale=True)
    content = b""

    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        content += data

    progress_bar.close()
    return content.decode('utf-8')


def replace(file_content, old_string, new_string):
    modified_content = file_content.replace(old_string, new_string)
    return modified_content


def write_to_file(filepath, content, force):
    if not os.path.exists(filepath) or force:
        with open(filepath, "w") as file:
            file.write(content)
        print(f"Created/Updated {filepath}")
    else:
        print(
            f"Skipping creating {filepath}: File already exists (run with --force flag to overwrite files)")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="README Generator")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode - files created have .test extension. This does not update filename references inside the templates.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing files.")

    args = parser.parse_args()

    _extension = ""
    if args.test:
        print("Test mode enabled..")
        _extension = ".test"

    print(TITLE)

    # URLs of the files to be downloaded
    readme_url = "https://raw.githubusercontent.com/Cutwell/readme-template/main/README.md"
    contributing_url = "https://raw.githubusercontent.com/Cutwell/readme-template/main/.github/CONTRIBUTING.md"
    pull_request_template_url = "https://raw.githubusercontent.com/Cutwell/readme-template/main/.github/PULL_REQUEST_TEMPLATE.md"
    logo_svg_url = "https://github.com/Cutwell/readme-template/blob/main/logo-64x64.svg"

    # Download files
    readme_content = download_file_with_progress(
        readme_url, "Cutwell/readme-template/README.md")
    contributing_content = download_file_with_progress(
        contributing_url, "Cutwell/readme-template/CONTRIBUTING.md")
    pull_request_template_content = download_file_with_progress(
        pull_request_template_url,
        "Cutwell/readme-template/.github/PULL_REQUEST_TEMPLATE.md")
    logo_svg_content = download_file_with_progress(
        logo_svg_url, "Cutwell/readme-template/logo.svg")

    # Prompt user for GitHub username and repository name
    github_username = input("\nEnter your GitHub username: ")
    repository_name = input("Enter your repository name: ")
    print()

    # Define old and new strings for find and replace
    old_string = "Cutwell/readme-template"
    new_string = f"{github_username}/{repository_name}"

    # Perform find and replace
    modified_readme = readme_content.replace(old_string, new_string)
    modified_contributing = contributing_content.replace(
        old_string, new_string)
    modified_pull_request_template = pull_request_template_content.replace(
        old_string, new_string)

    # Create .github folder if it doesn't exist
    folder_path = os.path.join(os.getcwd(), ".github")

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        os.makedirs(".github")

    # Save modified content back to files
    write_to_file(f"README{_extension}.md", modified_readme, args.force)
    write_to_file(
        f".github/CONTRIBUTING{_extension}.md",
        modified_contributing,
        args.force)
    write_to_file(
        f".github/PULL_REQUEST_TEMPLATE{_extension}.md",
        modified_pull_request_template,
        args.force)
    write_to_file(f"logo-64x64{_extension}.svg", logo_svg_content, args.force)


def cli():
    main()


if __name__ == "__main__":
    main()
