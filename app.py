import os
import shutil
import keyboard

def get_disk_space(path="."):
    total, used, free = shutil.disk_usage(path)
    return total, free

def format_size(size_in_bytes):
    if size_in_bytes >= 1024**3:
        return f"{size_in_bytes / 1024**3:.2f} GB"
    elif size_in_bytes >= 1024**2:
        return f"{size_in_bytes / 1024**2:.2f} MB"
    elif size_in_bytes >= 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    else:
        return f"{size_in_bytes} Bytes"

def delete_all_pict_files():
    print("\nSearching and deleting all .PICTERS files in the system...")
    deleted_count = 0
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file == ".PICTERS":
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
    print(f"\nDeleted .PICTERS files: {deleted_count}")

def delete_created_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"\nFile {file_path} successfully deleted.")
        else:
            print(f"\nFile {file_path} not found for deletion.")
    except Exception as e:
        print(f"\nError deleting file: {e}")

def fill_disk_with_file(file_path):
    try:
        with open(file_path, "wb") as f:
            chunk_size = 1024 * 1024 * 500  # 500 MB per write operation
            data = os.urandom(chunk_size)
            total_written = 0

            while True:
                disk_root = os.path.splitdrive(file_path)[0]
                total, free = get_disk_space(disk_root)
                if free <= chunk_size:
                    last_chunk = free if free > 0 else 0
                    f.write(os.urandom(last_chunk))
                    total_written += last_chunk
                    print(f"\nDisk full. Free space: {format_size(free)}.")
                    break

                f.write(data)
                total_written += chunk_size
                print(
                    f"\rFile size: {format_size(total_written)} | "
                    f"Free space: {format_size(free)}",
                    end="",
                )

                if keyboard.is_pressed("ctrl+d"):
                    print("\nCtrl+D pressed. Deleting file...")
                    delete_created_file(file_path)
                    return

    except Exception as e:
        print(f"\nError: {e}")

    input("\nFilling completed. Press any key to exit.")

def choose_disk():
    print("Choose a disk to use:")
    drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
    for i, drive in enumerate(drives):
        print(f"{i + 1}. {drive}")

    while True:
        try:
            choice = int(input("Enter the disk number: ")) - 1
            if 0 <= choice < len(drives):
                selected_drive = drives[choice]
                if selected_drive.upper() == "C:\\":
                    safe_folder = os.path.join(selected_drive, "SafeFolderForPICTERS")
                    os.makedirs(safe_folder, exist_ok=True)
                    print(f"Disk C selected. The file will be created in: {safe_folder}")
                    return safe_folder
                else:
                    print(f"Disk selected: {selected_drive}")
                    return selected_drive
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Enter a valid number.")

def main_menu():
    while True:
        print("\n1. Fill disk with .PICTERS file")
        print("2. Delete all .PICTERS files from the system")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            disk_root = choose_disk()
            file_name = ".PICTERS"
            file_path = os.path.join(disk_root, file_name)
            fill_disk_with_file(file_path)
        elif choice == "2":
            delete_all_pict_files()
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
