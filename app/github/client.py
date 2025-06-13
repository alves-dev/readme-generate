import shutil
from pathlib import Path

import git
from git import Repo

from app.config.setting import setting


class GitRepository:

    def __init__(self, repo_name: str):
        self.repo_url = f'{setting.GITHUB_BASE_CLONE_URL}/{repo_name}.git'
        self.repo_name = repo_name.split("/")[-1]
        self.repo_path = Path("../repository/" + self.repo_name)
        self.repo_url_with_token = self.repo_url.replace("https://", f"https://{setting.GITHUB_TOKEN}@")
        self.repo: Repo = self.__clone_repo()

    def write_file(self, file_name: str, text_to_write: str):
        full_file_path = self.repo_path.joinpath(file_name)

        with open(full_file_path, "w") as f:
            f.write(text_to_write)

    def commit_and_push(self, commit_message: str) -> bool:
        try:
            self.repo.git.add(A=True)
            self.repo.git.config("user.name", "readme-generate")
            self.repo.git.config("user.email", "comit@readmegenerate.com")
            self.repo.git.commit("-m", commit_message)
            self.repo.git.push("--set-upstream", self.repo_url_with_token, 'main')
            return True
        except Exception as e:
            print(f"Erro ao fazer commit/push: {e}")
            return False

    def __clone_repo(self) -> Repo:
        if self.repo_path.exists():
            self.__remove_repo_folder()

        return git.Repo.clone_from(self.repo_url_with_token, self.repo_path)

    def __remove_repo_folder(self):
        path = self.repo_path
        shutil.rmtree(path)
