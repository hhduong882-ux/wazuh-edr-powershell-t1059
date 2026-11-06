# Cấu hình Sysmon

Repo này không kèm file cấu hình Sysmon. Hãy tải một bộ cấu hình có sẵn, ví dụ:

- [SwiftOnSecurity/sysmon-config](https://github.com/SwiftOnSecurity/sysmon-config)
- [olafhartong/sysmon-modular](https://github.com/olafhartong/sysmon-modular)

Cài đặt (PowerShell, quyền Administrator):

```powershell
sysmon64.exe -accepteula -i sysmonconfig.xml
```

Cập nhật cấu hình đã cài: `sysmon64.exe -c sysmonconfig.xml`

Yêu cầu tối thiểu cho kịch bản T1059: bật **Event ID 1 (Process Create)**, vì rule cần các trường
`image`, `parentImage` và `commandLine`.

Nếu bạn dùng file cấu hình đã chỉnh sửa, hãy đặt vào thư mục này và ghi rõ nguồn gốc, giấy phép của tác giả gốc.
