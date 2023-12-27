import sys
import toml
import argparse
import requests
from tqdm import tqdm
from git import Repo, RemoteProgress, cmd
from colorama import Fore, Style, Back
from ginz.lockfile import LockFile
from ginz.tree import TreeNode

class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm(colour="GREEN", dynamic_ncols=True)

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()

    def write_lock_file(self, config):
        lock_data = {}
        for section_name, section in config.items():
            branch = section.get("branch")
            if branch is None:
                branch = "main"
            lock_data[section_name] = {
                "source": section.get("source"),
                "branch": branch
            }

        with open("ginz-lock.toml", "w") as lock_file:
            toml.dump(lock_data, lock_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--version", "-v", action="store_true", help="Print Out Version")

    parser.add_argument("--config-url", help="Fetch Config From Server And Run")

    parser.add_argument("--refetch", action="store_true", help="ReFetch Repositories")

    parser.add_argument("--dir", default=".", help="Custom directory for cloning repositories")

    args = parser.parse_args()

    if args.refetch:
        print(f"{Back.YELLOW} THIS IS A EXPERIMENTAL FEATURE {Back.RESET}")
        print(f"{Back.YELLOW} USE AT YOUR OWN RISK           {Back.RESET}")

        print(f"{Fore.YELLOW}fetching metadatas....{Fore.RESET}")

        try:
            with open("Ginz.toml") as file:
                config = toml.loads(file.read())
                for section_name, section in config.items():
                    try:
                        dir = cmd.Git(section_name)
                        dir.pull()

                        print(f"{Fore.GREEN}Updated {Back.GREEN}{section_name}{Back.RESET}{Fore.RESET}")
                    except OSError:
                        print(f"{Fore.RED}{section_name} doesn't exist, skipping. {Fore.RESET}")
        except FileNotFoundError:
            print(f"{Fore.RED}FileNotFound: Ginz.toml file not found {Fore.RESET}")
            sys.exit(1)

        print(f"{Fore.GREEN}Updated All Repos{Fore.RESET}")
        sys.exit()

    if args.version:
        print(f"{Fore.YELLOW}v1.0.0{Fore.RESET}")
        sys.exit()

    root_tree = TreeNode("Cloned Directory")

    if args.config_url:
        with open("GInz.toml") as config_file:
            config = toml.load(config_file)

            try:
                response = requests.get(args.config_url)
                response.raise_for_status()

                config_content = response.text

                # Parse the downloaded TOML configuration
                config = toml.loads(config_content)
                for section_name, section in config.items():
                    branch = section.get("branch")
                    if branch is None:
                        branch = "main"
                    repo = Repo.clone_from(url=section.get("source"), to_path=f"{args.dir}/{section_name}", progress=CloneProgress(), branch=branch)

                    child_node = TreeNode(f"{section_name} (branch: \x1b[3m {Fore.YELLOW}*{branch}*) {Fore.RESET} {Style.RESET_ALL}")
                    root_tree.add_child(child_node)

                root_tree.print_tree()

                # Write lock file
                CloneProgress().write_lock_file(config)

                sys.exit()
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}requests.exceptions.RequestException: Error While Downloading Config{Fore.RESET}")
                sys.exit(1)

    else:
        try:
            with open("GInz.toml") as config_file:
                config = toml.load(config_file)
        except FileNotFoundError:
            print(f"{Back.RED}Error:{Back.RESET} GInz.toml not found")
            sys.exit(1)

    for section_name, section in config.items():
        branch = section.get("branch")
        if branch is None:
            branch = "main"
        repo = Repo.clone_from(url=section.get("source"), to_path=f"{args.dir}/{section_name}", progress=CloneProgress(), branch=branch)

        child_node = TreeNode(f"{section_name} (branch: \x1b[3m {Fore.YELLOW}*{branch}*) {Fore.RESET} {Style.NORMAL}")
        root_tree.add_child(child_node)

    root_tree.print_tree()

    # Write lock file
    CloneProgress().write_lock_file(config)
