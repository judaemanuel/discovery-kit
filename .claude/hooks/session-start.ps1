<#
  Injeta o conteudo integral dos guias operacionais do vault no inicio de cada
  sessao (SessionStart), para nao depender de o agente lembrar de ir le-los.
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

$files = @(
    (Join-Path $root "_WIP\README.md"),
    (Join-Path $root "_WIP\GUIA-FRONTMATTER.md"),
    (Join-Path $root "_WIP\GUIA-FLUXO-DISCOVERY.md")
)

$parts = foreach ($f in $files) {
    if (Test-Path -LiteralPath $f) {
        $titulo = Split-Path -Leaf $f
        $conteudo = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
        "## $titulo`n`n" + $conteudo
    }
}

if ($parts.Count -eq 0) {
    exit 0
}

$context = "# Guias operacionais do vault (injetados automaticamente)`n`n" + ($parts -join "`n`n---`n`n")

$result = @{
    hookSpecificOutput = @{
        hookEventName     = "SessionStart"
        additionalContext = $context
    }
}

$result | ConvertTo-Json -Depth 5
