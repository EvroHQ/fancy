#!/usr/bin/env python3
import os
import random
import subprocess
from datetime import datetime

project_dir = r"C:\Users\EvroHQ\Desktop\fancy\fancy"
number_file_path = os.path.join(project_dir, "number.txt")

os.chdir(project_dir)

def read_number():
    try:
        with open(number_file_path, 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        with open(number_file_path, 'w') as f:
            f.write('0')
        return 0
    except ValueError:
        return 0

def write_number(num):
    with open(number_file_path, 'w') as f:
        f.write(str(num))

def git_commit():
    try:
        print("Staging changes...")
        subprocess.run(['git', 'add', 'number.txt'], check=True, cwd=project_dir)

        date = datetime.now().strftime('%Y-%m-%d')
        commit_message = f"Update number: {date}"
        print("Committing changes...")
        subprocess.run(['git', 'commit', '-m', commit_message], check=True, cwd=project_dir)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du commit Git : {e}")

def git_push():
    try:
        print("Pushing changes...")
        result = subprocess.run(['git', 'push'], capture_output=True, text=True, check=True, cwd=project_dir)
        print("Push Git réussi.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du push Git : {e}")
        print(e.stderr)

def update_cron_with_random_time():
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)

    task_name = "UpdateNumberTask"
    script_path = os.path.join(project_dir, "update_number.py")
    time_str = f"{random_hour:02}:{random_minute:02}"

    subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True)

    command = f'schtasks /create /tn "{task_name}" /tr "python {script_path}" /sc daily /st {time_str}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Tâche planifiée pour {time_str} demain.")
    else:
        print("Erreur lors de la planification de la tâche :")
        print(result.stderr)
    print(f"Chemin du script : {script_path}")

def create_startup_task():
    task_name = "UpdateNumberTask"
    script_path = os.path.join(project_dir, "update_number.py")

    command = f'schtasks /create /tn "{task_name}" /tr "python {script_path}" /sc onstart /ru System /f'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Tâche planifiée pour le démarrage de l'ordinateur.")
    else:
        print(f"Erreur lors de la création de la tâche planifiée : {result.stderr}")

def main():
    print("Début du script...")
    try:
        current_number = read_number()
        print(f"Numéro actuel : {current_number}")

        new_number = current_number + 1
        write_number(new_number)
        print(f"Numéro mis à jour : {new_number}")

        git_commit()
        print("Commit Git effectué.")

        git_push()
        print("Push Git effectué.")

        update_cron_with_random_time()
        print("Tâche planifiée avec succès.")

        create_startup_task()
        
    except Exception as e:
        print(f"Erreur : {str(e)}")
        exit(1)

    print("Fin du script.")

if __name__ == "__main__":
    main()
