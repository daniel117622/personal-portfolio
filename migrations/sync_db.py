import subprocess
import sys

# Configuration variables
# IMPORTANT: Run 'docker ps' in your terminal to find your exact container names and update these variables.
LOCAL_CONTAINER  = "mongo_db"
REMOTE_CONTAINER = "mongo_db"
DB_NAME          = "kuhaku_blog"
SERVER_USER      = "your_user"
SERVER_IP        = "your_server_ip"
LOCAL_DUMP_DIR   = "./db_volume/dump"
REMOTE_PATH      = "/tmp/db_dump"

def run_cmd(command: str) -> None:
    """Executes a shell command and logs clean errors on failure."""
    print(f"\n>>> {command}")
    try:
        # capture_output grabs stdout and stderr to prevent raw stack traces from bubbling up
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("\n[ERROR] Step failed.")
        print(f"Command: {e.cmd}")
        print(f"Details: {e.stderr.strip() if e.stderr else 'No additional error output provided by the system.'}")
        sys.exit(1)

def sync_database():
    print("--- 1. Extracting local database ---")
    run_cmd(f"docker exec {LOCAL_CONTAINER} mongodump --db {DB_NAME} --out /tmp/dump")
    run_cmd(f"docker cp {LOCAL_CONTAINER}:/tmp/dump {LOCAL_DUMP_DIR}")

    print("\n--- 2. Transferring to remote server ---")
    run_cmd(f"scp -r {LOCAL_DUMP_DIR} {SERVER_USER}@{SERVER_IP}:{REMOTE_PATH}")

    print("\n--- 3. Restoring on remote server ---")
    remote_commands = (
        f"docker cp {REMOTE_PATH} {REMOTE_CONTAINER}:/tmp/dump && "
        f"docker exec {REMOTE_CONTAINER} mongorestore --db {DB_NAME} --drop /tmp/dump/{DB_NAME} && "
        f"rm -rf {REMOTE_PATH} && "
        f"docker exec {REMOTE_CONTAINER} rm -rf /tmp/dump"
    )
    run_cmd(f"ssh {SERVER_USER}@{SERVER_IP} \"{remote_commands}\"")

    print("\n--- 4. Cleaning up local temp files ---")
    run_cmd(f"rm -rf {LOCAL_DUMP_DIR}")
    run_cmd(f"docker exec {LOCAL_CONTAINER} rm -rf /tmp/dump")
    
    print("\nSynchronization complete.")

if __name__ == "__main__":
    sync_database()