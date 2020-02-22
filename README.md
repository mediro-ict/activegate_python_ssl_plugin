# Active Gate SSL Checker Plugin

This plugin checks the SSL certificates of hosts in the hosts.txt file and logs problems on Dyantrace if the certificate is about to expire.

![SSLCert](/images/problem.png)

## Installation
ActiveGate Plugins need to get installed both, on you Tenant and on the Environment ActiveGate they are supposed to collect data for - mainly for security reasons. NO third party code is getting executed by your ActiveGate unless your Tenant and your Agent agree on the authenticity of your plugin.
This is why you need to install, in addition to your Tenant, on selected ActiveGates, that have the Remote Plugin module running and are supposed to execute your Plugin.

 
 Windows AG
 Unzip the plugin's zip file in the C:\Program Files\Dynatrace\remotepluginmodule\plugin_deployment folder
 Move the hosts.txt file to the C:\Program Files\Dynatrace\remotepluginmodule\agent\lib64  folder.
 Restart the AG Service

 Linux AG 
 Unzip the plugin's zip file in the opt/dynatrace/remotepluginmodule/plugin_deployment directory.
 Move the hosts.txt file to the /opt/dynatrace/remotepluginmodule/agent/lib64/ directory.

 Restart The Remote plugin service : service remotepluginmodule restart

## Troubleshooting
Windows AG
Check the Remote plugin module logs in C:\ProgramData\dynatrace\remotepluginmodule\log\remoteplugin

Linux AG
Check the Remote plugin module logs in : /var/lib/dynatrace/remotepluginmodule/log/remoteplugin