import subprocess
import json

output = subprocess.check_output(['nix-instantiate', '--verbose', '--eval', '--json', '--strict', 'recover-builtin-names.nix']).decode()
json_data = json.loads(output)
builtins = json_data['custom_builtins']

for builtin in builtins:
    print('custom_builtins.' + builtin)
    print('builtins.' + builtins[builtin])