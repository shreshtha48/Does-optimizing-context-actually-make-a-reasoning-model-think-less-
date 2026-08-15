<system_instructions>
You are an expert systems administrator and root-cause analyst. Your task is to diagnose system anomalies by analyzing the provided log file.

BACKGROUND: 
The provided text is a logcat output from an Android device. It contains interleaved messages from various system services (like ActivityManager, PowerManagerService) and background applications.

RULES & CONSTRAINTS:
1. EXTRACTION: You must identify errors, trace variables, and extract timestamps STRICTLY using only the provided <context>. Do not hallucinate log entries that do not exist.
2. SYNTHESIS: Once the anomaly is identified from the text, you MAY use your external knowledge of system architecture (e.g. Android internals) to propose a logical root cause and a solution.
3. If the specific error cannot be found in the context, explicitly state: "Information not available in the provided context."
</system_instructions>

<context>
03-17 16:13:45.317  1702 14640 D WindowManager: interceptKeyBeforeQueueing: key 4 , result : 1
03-17 16:13:45.317  1702  2105 D PowerManagerService: userActivityNoUpdateLocked: eventTime=261849949, event=1, flags=0x0, uid=1000
03-17 16:13:45.318  1702  2105 D PowerManagerService: ready=true,policy=3,wakefulness=1,wksummary=0x0,uasummary=0x1,bootcompleted=true,boostinprogress=false,waitmodeenable=false,mode=false,manual=38,auto=-1,adj=0.0userId=0
03-17 16:13:45.358  2227  2227 I PhoneStatusBar: resumeSuspendedAutohide
03-17 16:13:45.361  1702  3137 D WindowManager: interceptKeyTq keycode=4 interactive=true keyguardActive=false policyFlags=2b000002 down false canceled false
03-17 16:13:45.362  1702  3137 D WindowManager: interceptKeyBeforeQueueing: key 4 , result : 1
03-17 16:13:45.362  2227  2318 V AudioManager: querySoundEffectsEnabled...
03-17 16:13:45.382  1702  3697 D PowerManagerService: acquire lock=189667585, flags=0x1, tag="*launch*", name=android, ws=WorkSource{10113}, uid=1000, pid=1702
03-17 16:13:45.382  1702  3697 D PowerManagerService: ready=true,policy=3,wakefulness=1,wksummary=0x1,uasummary=0x1,bootcompleted=true,boostinprogress=false,waitmodeenable=false,mode=false,manual=38,auto=-1,adj=0.0userId=0
03-17 16:13:45.382  1702  3697 D PowerManagerService: Acquiring suspend blocker "PowerManagerService.WakeLocks".
03-17 16:13:45.402  1702  3694 V WindowManager: Skipping AppWindowToken{9f4ef63 token=Token{a64f992 ActivityRecord{de9231d u0 com.tencent.qt.qtl/.activity.info.NewsDetailXmlActivity t761}}} -- going to hide
03-17 16:13:45.405  2227  2227 I PhoneStatusBar: setSystemUiVisibility vis=508 mask=ffffffff oldVal=40000500 newVal=508 diff=40000008 fullscreenStackVis=0 dockedStackVis=0, fullscreenStackBounds=Rect(0, 0 - 720, 1280), dockedStackBounds=Rect(0, 0 - 0, 0)
03-17 16:13:45.408  2227  2227 I PhoneStatusBar: cancelAutohide
03-17 16:13:45.408  2227  2227 I PhoneStatusBar: notifyUiVisibilityChanged:vis=0x508, SystemUiVisibility=0x508
03-17 16:13:45.466  1702 17632 W ActivityManager: Bad activity token: android.os.BinderProxy@2bd79ce
03-17 16:13:45.466  1702 17632 W ActivityManager: java.lang.ClassCastException: android.os.BinderProxy cannot be cast to com.android.server.am.ActivityRecord$Token
03-17 16:13:45.512  1702  2639 V WindowManager: Skipping AppWindowToken{9f4ef63 token=Token{a64f992 ActivityRecord{de9231d u0 com.tencent.qt.qtl/.activity.info.NewsDetailXmlActivity t761}}} -- going to hide
03-17 16:13:45.598  1702  2556 D PowerManagerService: release:lock=189667585, flg=0x0, tag="*launch*", name=android", ws=WorkSource{10113}, uid=1000, pid=1702
03-17 16:13:45.599  1702  2556 D PowerManagerService: ready=true,policy=3,wakefulness=1,wksummary=0x0,uasummary=0x1,bootcompleted=true,boostinprogress=false,waitmodeenable=false,mode=false,manual=38,auto=-1,adj=0.0userId=0
03-17 16:13:45.599  1702  2556 D PowerManagerService: Releasing suspend blocker "PowerManagerService.WakeLocks".
03-17 16:13:45.626  2227  2227 I PhoneStatusBar: setSystemUiVisibility vis=40000500 mask=ffffffff oldVal=508 newVal=40000500 diff=40000008 fullscreenStackVis=0 dockedStackVis=0, fullscreenStackBounds=Rect(0, 0 - 720, 1280), dockedStackBounds=Rect(0, 0 - 0, 0)
03-17 16:13:45.627  2227  2227 I PhoneStatusBar: cancelAutohide
03-17 16:13:45.627  2227  2227 I PhoneStatusBar: notifyUiVisibilityChanged:vis=0x40000500, SystemUiVisibility=0x40000500
03-17 16:13:46.143  1702  2105 D PowerManagerService: userActivityNoUpdateLocked: eventTime=261850777, event=2, flags=0x0, uid=1000
03-17 16:13:46.144  1702  2105 D PowerManagerService: ready=true,policy=3,wakefulness=1,wksummary=0x0,uasummary=0x1,bootcompleted=true,boostinprogress=false,waitmodeenable=false,mode=false,manual=38,auto=-1,adj=0.0userId=0
03-17 16:13:46.145  2227  2227 I PhoneStatusBar: suspendAutohide
03-17 16:13:46.146  2227  2227 I PhoneStatusBar: suspendAutohide
03-17 16:13:46.146  2227  2227 I PanelView: onTouchEvent::0, x=271.0, y=14.0
03-17 16:13:46.148  2227  2227 I PanelView: schedulePeek
03-17 16:13:46.153  1702  2113 V AudioManager: getRingtonePlayer...
</context>

<user_question>
The `ActivityManager` (PID 1702) threw a `ClassCastException` at 16:13:45.466. What specific class was the system attempting to cast `android.os.BinderProxy` into, and what was the `wksummary` value logged by the `PowerManagerService` immediately before the bad activity token was reported?
</user_question>
