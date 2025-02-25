import os

# 定義 .gitignore 的內容
gitignore_content = """# Ignore environment variable files
.env

# Ignore Python cache files
__pycache__/

# Ignore virtual environment folder
venv/

# Ignore IDE and editor configurations
*.vscode/
.idea/
*.swp

# Ignore system files
Thumbs.db
.DS_Store
"""

# 指定檔案儲存路徑
file_path = ".gitignore"

# 創建並寫入 .gitignore 檔案
with open(file_path, "w") as file:
    file.write(gitignore_content)

# 用 Notepad 打開 .gitignore 檔案
os.system(f'notepad.exe {file_path}')
