$ErrorActionPreference = "SilentlyContinue"
$LogFile = "C:\edr-test.log"
function Log {
    param([string]$Msg)
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $LogFile -Value "[$time] [kill-process.ps1] $Msg" -Encoding UTF8
}
Log "Active Response processing..."
# Đọc JSON từ Wazuh STDIN (Có kiểm tra dữ liệu)
$JsonLine = $null
try {
    if ([Console]::In.Peek() -ge 0 -or [Console]::IsInputRedirected) {
        $JsonLine = [Console]::In.ReadLine()
    }
} catch {}
$TargetPID = $null
if (-not [string]::IsNullOrWhiteSpace($JsonLine)) {
    try {
        $Alert = $JsonLine | ConvertFrom-Json
        $TargetPID = $Alert.parameters.alert.data.win.eventdata.processId
        if (-not $TargetPID) { $TargetPID = $Alert.data.win.eventdata.processId }
    } catch {}
}
# Tiêu diệt tiến trình
if ($TargetPID -and ($TargetPID -ne $PID)) {
    Log "Targeting specific PID: $TargetPID"
    taskkill /F /PID $TargetPID /T | Out-Null
    Log "SUCCESS: Terminated process PID $TargetPID"
} else {
    # Fallback: Quét diệt các tiến trình powershell độc hại
    Log "Fallback: Terminating powershell.exe"
    taskkill /F /IM powershell.exe | Out-Null
    Log "SUCCESS: Executed powershell taskkill fallback"
}
Log "Active Response finished."
Log "=============================================="
exit 0
