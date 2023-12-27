import os
import yaml

def new_chatid(chatid):
    yaml_file_path = os.path.expanduser("~/.config/cappriciosec-tools/cappriciosec.yaml")
    folder_path = os.path.dirname(yaml_file_path)
    os.makedirs(folder_path, exist_ok=True)

    if not os.path.exists(yaml_file_path):
        initial_content = {"config": {"chatid": chatid}}

        with open(yaml_file_path, "w") as file:
            yaml.dump(initial_content, file, default_flow_style=False)

        print(f"Config file created at: {yaml_file_path}")

    else:
        with open(yaml_file_path, "r") as file:
            data = yaml.safe_load(file)

        if "config" in data and "chatid" in data["config"]:
            print(f"chatid is already present: {data['config']['chatid']}")

        else:
            data.setdefault("config", {})
            data["config"]["chatid"] = chatid

            with open(yaml_file_path, "w") as file:
                yaml.dump(data, file, default_flow_style=False)

            print(f"chatid appended to YAML file: {yaml_file_path}")
