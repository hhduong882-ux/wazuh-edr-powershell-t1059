# Kịch bản kiểm thử T1059.001 (PowerShell)

Chạy trên Windows Endpoint đã cài Sysmon và Wazuh Agent, trong môi trường lab.
Các lệnh dưới đây vô hại, chỉ để kích hoạt rule.

| Rule | Lệnh kiểm thử | Kết quả mong đợi |
|---|---|---|
| 100010 | `powershell -enc VwByAGkAdABlAC0ATwB1AHQAcAB1AHQAIAB3AGEAegB1AGgALQB0ADEAMAA1ADkALQB0AGUAcwB0AA==` | Cảnh báo level 10, Telegram nhận tin |
| 100011 | `powershell -w hidden -c "Start-Sleep 3"` | Cảnh báo level 10, Telegram nhận tin |
| 100012 | `powershell -c "(New-Object Net.WebClient).DownloadString('http://127.0.0.1/test')"` | Cảnh báo level 12, Active Response kill PowerShell |
| 100013 | `powershell -ep bypass -nop -c "Get-Date"` | Cảnh báo level 8 |
| 100014 | Mở PowerShell từ `mshta.exe` hoặc `wscript.exe` | Cảnh báo level 13, Active Response kill PowerShell |

Chuỗi Base64 ở rule 100010 là `Write-Output wazuh-t1059-test` mã hóa UTF-16LE.
Có thể dùng thêm [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) với kỹ thuật T1059.001.

## Các bước kiểm tra

1. Wazuh Dashboard, mục Threat Hunting / Events: lọc `rule.id: 100010..100014` và xem `data.win.eventdata.commandLine`.
2. Agent Windows: xem `C:\Program Files (x86)\ossec-agent\active-response\active-responses.log`, phải có dòng `taskkill` khi rule 100012 hoặc 100014 kích hoạt.
3. Manager: xem `/var/ossec/logs/active-responses.log` và `/var/ossec/logs/integrations.log` (Telegram).
4. Kiểm tra rule trước khi triển khai: `/var/ossec/bin/wazuh-logtest`, dán một log Sysmon Event 1 mẫu.

## Lưu ý

Rule 100012 và 100014 gắn nhóm `powershell_kill_trigger`, nên chính cửa sổ PowerShell bạn đang gõ lệnh thử cũng bị kill. Đó là hành vi đúng.
