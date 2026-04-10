$ErrorActionPreference = "Stop"

& .\env_setter.ps1
python .\build_blog.py
gitq
