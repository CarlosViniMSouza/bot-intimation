$exclude = @("venv", "bot_alvara_citation.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "bot_alvara_citation.zip" -Force