import datetime
import os
import uuid

def ensure_notes_dir_exists(notes_dir):
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)
        print(f"Created 'notes' directory: {notes_dir}")

def note_time(start_time, notes_dir, title, description=''):
    ensure_notes_dir_exists(notes_dir)  # Ensure the notes directory exists
    if start_time is None:
        print("Timer is not running. Start the timer first.")
        return

    current_time = datetime.datetime.now()
    elapsed_time = current_time - start_time
    uid = uuid.uuid4().hex[:8]  # Generate a short UID for this note
    note = f"UID: {uid} - Time Mark: {elapsed_time} - {description}\n"  # Embed the UID in the note

    formatted_title = title.replace(" ", "_")
    filename = f"{formatted_title}_{start_time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    filepath = os.path.join(notes_dir, filename)

    with open(filepath, 'a') as file:
        file.write(note)

    print(f"Noted: {note}")
    return filepath

def read_notes(notes_dir):
    ensure_notes_dir_exists(notes_dir)  # Ensure the notes directory exists
    notes = []
    for filename in os.listdir(notes_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(notes_dir, filename)
            with open(filepath, 'r') as file:
                content = file.read()
                for line in content.split('\n'):
                    if line.strip():
                        notes.append((filepath, line.strip()))
    return notes

def update_note_description(filepath, uid, new_description):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    updated = False
    for i, line in enumerate(lines):
        if f"UID: {uid}" in line:
            parts = line.split(' - ', 2)  # Split into three parts: UID, Time Mark, and Description
            if len(parts) == 3:
                parts[2] = new_description + '\n'  # Update the description part
                lines[i] = ' - '.join(parts)
                updated = True
                break

    if updated:
        with open(filepath, 'w') as file:
            file.writelines(lines)
    else:
        print("Note with the given UID was not found.")