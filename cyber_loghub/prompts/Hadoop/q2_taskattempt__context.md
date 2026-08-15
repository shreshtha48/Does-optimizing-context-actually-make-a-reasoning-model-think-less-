<system_instructions>
You are an expert systems administrator and root-cause analyst. Your task is to diagnose system anomalies by analyzing the provided log file.

BACKGROUND: 
The provided text is a system log from an Apache Hadoop distributed cluster, specifically detailing MapReduce operations, resource management (YARN), and HDFS client interactions.

RULES & CONSTRAINTS:
1. EXTRACTION: You must identify errors, trace variables, and extract timestamps STRICTLY using only the provided <context>. Do not hallucinate log entries that do not exist.
2. SYNTHESIS: Once the anomaly is identified from the text, you MAY use your external knowledge of system architecture (e.g. Hadoop internals) to propose a logical root cause and a solution.
3. If the specific error cannot be found in the context, explicitly state: "Information not available in the provided context."
</system_instructions>

<context>
2015-10-18 18:04:54,708 INFO [IPC Server handler 14 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000004_0 is : 0.44968578
2015-10-18 18:04:55,630 INFO [IPC Server handler 8 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000006_0 is : 0.44980705
2015-10-18 18:04:56,318 INFO [IPC Server handler 16 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000001_0 is : 0.37322965
2015-10-18 18:04:56,396 INFO [IPC Server handler 19 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000002_0 is : 0.38007197
2015-10-18 18:04:56,568 INFO [IPC Server handler 8 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000000_0 is : 0.3624012
2015-10-18 18:04:57,396 INFO [IPC Server handler 19 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000009_0 is : 0.76133776
2015-10-18 18:04:57,427 INFO [IPC Server handler 8 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000008_0 is : 0.34610128
2015-10-18 18:04:57,443 INFO [IPC Server handler 14 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000007_0 is : 0.3707891
2015-10-18 18:04:59,771 INFO [IPC Server handler 0 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000001_0 is : 0.37551183
2015-10-18 18:04:59,787 INFO [IPC Server handler 10 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000002_0 is : 0.38137424
2015-10-18 18:05:02,802 INFO [IPC Server handler 10 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000001_0 is : 0.37551183
2015-10-18 18:05:02,818 INFO [IPC Server handler 4 on 62270] org.apache.hadoop.mapred.TaskAttemptListenerImpl: Progress of TaskAttempt attempt_1445144423722_0020_m_000002_0 is : 0.38137424
2015-10-18 18:05:27,570 WARN [LeaseRenewer:msrabi@msra-sa-41:9000] org.apache.hadoop.ipc.Client: Address change detected. Old: msra-sa-41/10.190.173.170:9000 New: msra-sa-41:9000
2015-10-18 18:05:27,570 WARN [LeaseRenewer:msrabi@msra-sa-41:9000] org.apache.hadoop.hdfs.LeaseRenewer: Failed to renew lease for [DFSClient_NONMAPREDUCE_1537864556_1] for 30 seconds.  Will retry shortly ...
2015-10-18 18:05:28,570 WARN [LeaseRenewer:msrabi@msra-sa-41:9000] org.apache.hadoop.ipc.Client: Address change detected. Old: msra-sa-41/10.190.173.170:9000 New: msra-sa-41:9000
</context>

<user_question>
Locate the first recorded progress update for TaskAttempt `attempt_1445144423722_0020_m_000001_0`. What was the progress value, which IPC Server handler processed it, and at what timestamp did it remain stalled at that exact value?
</user_question>
