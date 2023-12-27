import os
import subprocess
import platform
import requests
import re

class S5CmdRunner:
    """
    A class that provides methods for interacting with s5cmd, a command-line tool for efficient S3 data transfer.

    Attributes:
        s5cmd_path (str): The path to the s5cmd executable.

    Methods:
        __init__(): Initializes the S5CmdRunner object.
        has_s5cmd() -> bool: Checks if s5cmd is available.
        get_s5cmd() -> None: Downloads and installs s5cmd if it is not available.
        call_function(command: str, *args): Calls a function with the specified command and arguments.
        download_file(file_uri) -> str: Downloads a file from a URI to a temporary local path.
        generate_s5cmd_file(s3_uris, dest_dir) -> str: Generates a command file for s5cmd with the specified S3 URIs and destination directory.
        download_from_s3_list(s3_uris, dest_dir): Downloads multiple files from S3 using s5cmd.
        is_local_file(path) -> bool: Checks if a file path is a local file.
        download_from_url(url) -> str: Downloads a file from a URL to a temporary local path.
        cp(from_str, to_str): Copies a file from a local path or URL to an S3 URI or vice versa using s5cmd.
        mv(from_str, to_str): Moves a file from a local path to an S3 URI or vice versa using s5cmd.
        run(txt_uri): Runs s5cmd with a command file specified by a local path, URL, or S3 URI.
    """
    def __init__(self):
        self.s5cmd_path = os.path.expanduser('~/s5cmd')
        if not self.has_s5cmd():
            self.get_s5cmd()

    def has_s5cmd(self) -> bool:
        return os.path.exists(self.s5cmd_path) and os.access(self.s5cmd_path, os.X_OK)

    def get_s5cmd(self) -> None:
        arch = platform.machine()
        s5cmd_url = ""

        if arch == 'x86_64':
            s5cmd_url = "https://huggingface.co/kiriyamaX/s5cmd-backup/resolve/main/s5cmd_2.2.2_Linux-64bit/s5cmd"
        elif arch == 'aarch64':
            s5cmd_url = "https://huggingface.co/kiriyamaX/s5cmd-backup/resolve/main/s5cmd_2.2.2_Linux-arm64/s5cmd"
        else:
            raise ValueError("Unsupported architecture")

        subprocess.run(["wget", "-O", self.s5cmd_path, s5cmd_url])
        subprocess.run(["chmod", "+x", self.s5cmd_path])

    def call_function(self, command: str, *args):
        subprocess.run([command, *args])

    def download_file(self, file_uri):
        local_path = '/tmp/downloaded_file.txt'
        if file_uri.startswith('s3://'):
            self.call_function(self.s5cmd_path, "cp", file_uri, local_path)
        elif re.match(r'https?://', file_uri):
            response = requests.get(file_uri)
            response.raise_for_status()
            with open(local_path, 'w') as file:
                file.write(response.text)
        else:
            raise ValueError("Unsupported URI scheme")
        return local_path

    def generate_s5cmd_file(self, s3_uris, dest_dir):
        command_file_path = '/tmp/s5cmd_commands.txt'
        with open(command_file_path, 'w') as file:
            for s3_uri in s3_uris:
                command = f"cp {s3_uri} {dest_dir}/{os.path.basename(s3_uri)}\n"
                file.write(command)
        return command_file_path

    def download_from_s3_list(self, s3_uris, dest_dir):
        if not self.has_s5cmd():
            raise RuntimeError("s5cmd is not available")

        command_file_path = self.generate_s5cmd_file(s3_uris, dest_dir)
        self.run(command_file_path)

    
    def is_local_file(self, path):
        return os.path.isfile(path)
    

    def download_from_url(self, url):
        """
        Download a file from a URL to a temporary local path.

        Args:
            url (str): The URL of the file to download.

        Returns:
            str: The local path of the downloaded file.
        """
        local_path = '/tmp/temp_file'
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, 'wb') as file:
            file.write(response.content)
        return local_path

    def cp(self, from_str, to_str):
        """
        Copy a file from a local path or URL to an S3 URI or from an S3 URI to a local path.

        Args:
            from_str (str): The source file path or URL.
            to_str (str): The destination file path or S3 URI.
        """
        if not self.has_s5cmd():
            raise RuntimeError("s5cmd is not available")

        if re.match(r'https?://', from_str):
            from_str = self.download_from_url(from_str)

        self.call_function(self.s5cmd_path, "cp", from_str, to_str)

    
    def mv(self, from_str, to_str):
        """
        Move a file from a local path to an S3 URI or from an S3 URI to a local path.

        Args:
            from_str (str): The source file path or S3 URI.
            to_str (str): The destination file path or S3 URI.
        """
        if not self.has_s5cmd():
            raise RuntimeError("s5cmd is not available")

        self.call_function(self.s5cmd_path, "mv", from_str, to_str)
    
    def run(self, txt_uri):
        """
        Run s5cmd with a command file specified by a local path, URL, or S3 URI.

        Args:
            txt_uri (str): The path, URL, or S3 URI of the command file.
        """
        if not self.has_s5cmd():
            raise RuntimeError("s5cmd is not available")

        if self.is_local_file(txt_uri):
            local_txt_path = txt_uri
        elif re.match(r'https?://', txt_uri):
            local_txt_path = self.download_from_url(txt_uri)
        else:
            local_txt_path = self.download_file(txt_uri)

        self.call_function(self.s5cmd_path, "run", local_txt_path)


if __name__ == '__main__':
    # Example usage:
    runner = S5CmdRunner()
    runner.run('s3://your-bucket/path-to-your-file.txt')
    # Or
    runner.run('http://example.com/path-to-your-file.txt')
