# Define input and output folders
$inputFolder = "."
$outputFile = "scenarios.json"
$outputLines = @()

$outputLines += "["
$needsScenarioSep = 0

# Get all .txt files in the input folder
Get-ChildItem -Path $inputFolder -Filter *.md | ForEach-Object {
    $inputFile = $_.FullName

    # Read input file
    $lines = Get-Content $inputFile
    if ($needsScenarioSep) {
        $outputLines += ","
    }
    $needsScenarioSep = 1
    $outputLines += "{"

    $needsAttrSep = 0
    # Process each line with your regex
    foreach ($line in $lines) {
        if ($needsAttrSep) {
            $outputLines += ","
        }
        $needsAttrSep = 1

        if ($line -match '# (.+)') {
            $name = $matches[1].Trim()
            $outputLines += """name"": ""$name"""
        } elseif ($line -match '\*\*(\w+)\*\*:\s*(.+)\s*') {
            $attr = $matches[1].Trim()
            $content = $matches[2].Trim()
            $outputLines += """$attr"": ""$content"""
        }
    }
    $outputLines += "}"


    Write-Host "Processed $($_.Name)"
}

$outputLines += "]"

# Write output file
$outputLines | Set-Content $outputFile