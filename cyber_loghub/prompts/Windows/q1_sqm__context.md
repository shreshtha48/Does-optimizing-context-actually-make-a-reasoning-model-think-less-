<system_instructions>
You are an expert systems administrator and root-cause analyst. Your task is to diagnose system anomalies by analyzing the provided log file.

BACKGROUND: 
The provided text is a Component-Based Servicing (CBS) and Client Side Rendering (CSI) log from a Windows operating system. It details system updates, manifest parsing, and TrustedInstaller operations.

RULES & CONSTRAINTS:
1. EXTRACTION: You must identify errors, trace variables, and extract timestamps STRICTLY using only the provided <context>. Do not hallucinate log entries that do not exist.
2. SYNTHESIS: Once the anomaly is identified from the text, you MAY use your external knowledge of system architecture (e.g. Windows internals) to propose a logical root cause and a solution.
3. If the specific error cannot be found in the context, explicitly state: "Information not available in the provided context."
</system_instructions>

<context>
2016-09-28 04:30:31, Info                  CBS    Starting the TrustedInstaller main loop.
2016-09-28 04:30:31, Info                  CBS    TrustedInstaller service starts successfully.
2016-09-28 04:30:31, Info                  CBS    SQM: Initializing online with Windows opt-in: False
2016-09-28 04:30:31, Info                  CBS    SQM: Cleaning up report files older than 10 days.
2016-09-28 04:30:31, Info                  CBS    SQM: Requesting upload of all unsent reports.
2016-09-28 04:30:31, Info                  CBS    SQM: Failed to start upload with file pattern: C:\Windows\servicing\sqm\*_std.sqm, flags: 0x2 [HRESULT = 0x80004005 - E_FAIL]
2016-09-28 04:30:31, Info                  CBS    SQM: Failed to start standard sample upload. [HRESULT = 0x80004005 - E_FAIL]
2016-09-28 04:30:31, Info                  CBS    SQM: Queued 0 file(s) for upload with pattern: C:\Windows\servicing\sqm\*_all.sqm, flags: 0x6
2016-09-28 04:30:31, Info                  CBS    SQM: Warning: Failed to upload all unsent reports. [HRESULT = 0x80004005 - E_FAIL]
2016-09-28 04:30:31, Info                  CBS    No startup processing required, TrustedInstaller service was not set as autostart, or else a reboot is still pending.
2016-09-28 04:30:31, Info                  CBS    NonStart: Checking to ensure startup processing was not required.
2016-09-28 04:30:31, Info                  CSI    00000004 IAdvancedInstallerAwareStore_ResolvePendingTransactions (call 1) (flags = 00000004, progress = NULL, phase = 0, pdwDisposition = @0xb6fd90
2016-09-28 04:30:31, Info                  CSI    00000005 Creating NT transaction (seq 1), objectname [6]"(null)"
2016-09-28 04:30:31, Info                  CSI    00000006 Created NT transaction (seq 1) result 0x00000000, handle @0x214
2016-09-28 04:30:31, Info                  CSI    00000007@2016/9/27:20:30:31.462 CSI perf trace:
</context>

<user_question>
The CBS service repeatedly reports an `E_FAIL` error (HRESULT 0x80004005) during the `SQM` upload phase. Extract the exact file pattern that triggered the first failure. Based on your knowledge of Windows Servicing, what is the purpose of SQM files?
</user_question>
