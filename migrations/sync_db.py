import os
import platform
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()

# Configuration variables
# IMPORTANT: Run 'docker ps' in your terminal to find your exact
# container names and update these variables.
LOCAL_CONTAINER = "8b78317b40aa_mongo_db"
REMOTE_CONTAINER = "mongo_db"
DB_NAME = "blog_db"
LOCAL_DUMP_DIR = "./db_volume/dump"
REMOTE_PATH = "/tmp/db_dump"

SERVER_USER = os.environ["SERVER_USER"]
SERVER_IP = os.environ["SERVER_IP"]
MONGO_URI = os.environ["MONGO_URI"]

# Ping count/flag differs between Linux/macOS and Windows
PING_FLAG = "-n" if platform.system().lower() == "windows" else "-c"


def ping_server(host: str, count: int = 3) -> bool:
    """Returns True if the host responds to ping, False otherwise."""
    command = f"ping {PING_FLAG} {count} {host}"
    print(f"\n>>> {command}")
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[ERROR] Host {host} is unreachable.")
        print(result.stderr.strip() or result.stdout.strip())
        return False
    print(result.stdout.strip())
    return True


def run_cmd(command: str) -> None:
    """Executes a shell command and logs clean errors on failure."""
    print(f"\n>>> {command}")
    try:
        # capture_output grabs stdout and stderr to prevent raw stack
        # traces from bubbling up
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("\n[ERROR] Step failed.")
        print(f"Command: {e.cmd}")
        details = e.stderr.strip() if e.stderr else "No additional error output provided."
        print(f"Details: {details}")
        sys.exit(1)


print("--- 0. Checking server reachability ---")
if not ping_server(SERVER_IP):
    sys.exit(1)

print("\n--- 1. Extracting local database ---")
run_cmd(f"docker exec {LOCAL_CONTAINER} mongodump --db {DB_NAME} --out /tmp/dump")
run_cmd(f"mkdir -p {LOCAL_DUMP_DIR}")
run_cmd(f"docker cp {LOCAL_CONTAINER}:/tmp/dump/. {LOCAL_DUMP_DIR}")
print("\n--- 2. Transferring to remote server ---")
run_cmd(f"scp -r {LOCAL_DUMP_DIR} {SERVER_USER}@{SERVER_IP}:{REMOTE_PATH}")

print("\n--- 3. Restoring on remote server ---")
remote_commands = (
    f"docker cp {REMOTE_PATH} {REMOTE_CONTAINER}:/tmp/dump && "
    f"docker exec {REMOTE_CONTAINER} mongorestore --db {DB_NAME} --drop "
    f"/tmp/dump/{DB_NAME} && "
    f"rm -rf {REMOTE_PATH} && "
    f"docker exec {REMOTE_CONTAINER} rm -rf /tmp/dump"
)
run_cmd(f'ssh {SERVER_USER}@{SERVER_IP} "{remote_commands}"')

print("\n--- 4. Cleaning up local temp files ---")
run_cmd(f"rm -rf {LOCAL_DUMP_DIR}")
run_cmd(f"docker exec {LOCAL_CONTAINER} rm -rf /tmp/dump")

print("\nSynchronization complete.")