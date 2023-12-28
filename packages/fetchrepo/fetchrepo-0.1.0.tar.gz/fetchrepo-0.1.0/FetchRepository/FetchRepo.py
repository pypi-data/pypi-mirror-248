import os
import requests
import tarfile
import tempfile
from io import BytesIO
import json

class FetchRepo:
    def __init__(self):
        self.headers = None

    def _download_and_extract_repo(self, https_link, branch=None, headers=None):
        response = requests.get(https_link, headers=headers)
        if response.status_code == 200:
            return response.content if response.content else None
        print('Failed to download the repository')
        return None

    def _is_binary(self, data):
        binary_threshold = 0.2
        if data:
            non_ascii_ratio = sum(1 for char in data if char < 32 or char > 127) / len(data)
            return non_ascii_ratio > binary_threshold
        return False

    def _read_ignore_files(self, file_path):
        ignore_files = []
        with open(file_path, 'r') as f:
            ignore_files = [line.strip() for line in f.readlines()]
        return ignore_files

    def _exclude_files(self, file_path, ignore_files):
        for excluded_file in ignore_files:
            if excluded_file.lower() in file_path.lower():
                return True
        return False

    def _convert_to_json(self, repo_content, root_dir, ignore_files):
        result = []
        if not repo_content:
            return result

        with tempfile.TemporaryDirectory() as temp_dir, \
             tarfile.open(fileobj=BytesIO(repo_content), mode="r:gz") as tar:
            tar.extractall(temp_dir)
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.relpath(os.path.join(root, file), temp_dir)

                    if self._exclude_files(file_path, ignore_files):
                        continue

                    with open(os.path.join(root, file), 'rb') as f:
                        file_content = f.read()
                        if self._is_binary(file_content):
                            continue
                        file_content = file_content.decode('utf-8', errors='replace')

                    formatted_path = os.path.join(root_dir, file_path).replace(os.path.sep, '/')
                    formatted_content = self._indent_code(file_content)
                    file_info = {"file_path": formatted_path, "content": formatted_content}
                    result.append(file_info)

        return result

    def _indent_code(self, code):
        indented_code = '\n'.join(['    ' + line for line in code.splitlines()])
        return indented_code

    def _print_repo_content_json(self, repo_content, root_dir, ignore_files):
        json_structure = self._convert_to_json(repo_content, root_dir, ignore_files)
        formatted_json = json.dumps(json_structure, indent=2, separators=(',', ': '), sort_keys=True)
        return formatted_json

    def _get_github_repo_branches(self, repo_link, headers=None):
        owner, repo = repo_link.split("/")[-2:]
        api_url = f"https://api.github.com/repos/{owner}/{repo}/branches"
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            branches = response.json()
            branch_names = [branch["name"] for branch in branches]
            print("Branches:", branch_names)
            return branch_names
        else:
            print(f"Failed to list branches. Status code: {response.status_code}")
            return None

    def harvest_github_repo(self, repo_link, branch=None, access_token=None):
        self.headers = None
        if access_token:
            self.headers = {"Authorization": f"Bearer {access_token}"}

        ignore_file_path = os.path.join(os.getcwd(), 'FetchRepository', 'ignore_files.txt')
        ignore_files = self._read_ignore_files(ignore_file_path)

        if not branch:
            branches = self._get_github_repo_branches(repo_link, headers=self.headers)
            if not branches:
                print("Unable to fetch branches. Exiting.")
                return None

            branch = input("Select a branch from the list above: ")
            if branch not in branches:
                print("Invalid branch. Exiting.")
                return None

        repo_content = self._download_and_extract_repo(f"{repo_link}/archive/{branch}.tar.gz", headers=self.headers)
        if not repo_content:
            print("Failed to download and extract repository content.")
            return None

        root_directory = os.getcwd()
        repo_content = self._print_repo_content_json(repo_content, root_directory, ignore_files)

        return repo_content