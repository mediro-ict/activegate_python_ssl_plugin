# Active Gate SSL Checker Plugin

This plugin checks the SSL certificates of hosts in the hosts.txt file and logs problems on Dyantrace if the certificate is about to expire.

![SSLCert](/images/problem.png)

![SSLCert](/images/custom_event1.png)

## Requirements
This plugin requires at least Dynatrace Active Gate v1.185.137
Download the latest zip for your ActiveGate here: https://github.com/mediro-ict/activegate_python_ssl_plugin/releases

## Installation
ActiveGate Plugins need to get installed both, on you Tenant and on the Environment ActiveGate they are supposed to collect data for - mainly for security reasons. NO third party code is getting executed by your ActiveGate unless your Tenant and your Agent agree on the authenticity of your plugin.
This is why you need to install, in addition to your Tenant, on selected ActiveGates, that have the Remote Plugin module running and are supposed to execute your Plugin.

 ### Dynatrace Tenant
Upload the plugin to your Dynatrace tenant using the GUI: Settings --> Custom Extensions --> Uplood extensions
 Complete the property fields:

 ![SSLCert](/images/plugin_conf.png)
 
 Complete the following fields:
 * Endpoint name: The name of the active gate endpoint
 * Poll Interval: How often a certificate should be checked in minutes
 * Custom Event Period Threshold: Threshold to raise a custom event before expiration in Days
 * Problem Alert Period Threshold: Threshold to raise a Problem event before expiration in Days*Hosts: Comma seperated list of the Host certificates to monitor eg. www.google.com443,www.example.com:443
 * Choose ActiveGate: The Windows or Linux Active Gate that the plugin is running on.

 ### Windows AG
 Unzip the plugin's zip file in the C:\Program Files\Dynatrace\remotepluginmodule\plugin_deployment folder
 Move the hosts.txt file to the C:\Program Files\Dynatrace\remotepluginmodule\agent\lib64  folder.
 Restart the AG Service

 ### Linux AG 
 Unzip the plugin's zip file in the opt/dynatrace/remotepluginmodule/plugin_deployment directory.
 Move the hosts.txt file to the /opt/dynatrace/remotepluginmodule/agent/lib64/ directory.

 Restart The Remote plugin service : service remotepluginmodule restart


## Troubleshooting

### Windows AG
Check the Remote plugin module logs in C:\ProgramData\dynatrace\remotepluginmodule\log\remoteplugin

### Linux AG
Check the Remote plugin module logs in : /var/lib/dynatrace/remotepluginmodule/log/remoteplugin