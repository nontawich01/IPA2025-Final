import subprocess
import re
import os
import tempfile

def motd(ip,motd):
    playbook_file = 'playbook_motd.yaml'
    inventory_file = None

    try:
        with tempfile.NamedTemporaryFile("w", delete=False) as temp_inv:
            temp_inv.write("[routers]\n")
            temp_inv.write(f"{ip} ansible_user=admin ansible_password=cisco ansible_network_os=ios ansible_connection=network_cli\n")
            inventory_file = temp_inv.name

        command = ["ansible-playbook", "-i", inventory_file, playbook_file, "-e", f"motd_text='{motd}'"]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=120
        )

        stdout_result = result.stdout
        print("Playbook Output:\n", stdout_result)

        return "Ok: success"

    except subprocess.CalledProcessError as e:
        print("Error running playbook:")
        print(e.stderr)
        return False

    except subprocess.TimeoutExpired:
        print("Playbook execution timed out.")
        return False

    except Exception as e:
        print("Unexpected error:", str(e))
        return False

    finally:

        if inventory_file and os.path.exists(inventory_file):
            os.remove(inventory_file)
