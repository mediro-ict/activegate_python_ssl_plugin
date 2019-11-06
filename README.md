"# activegate_python_ssl_plugin" 

This plugin checks the SSL certificates of host in the hosts.txt file and logs problems on Dyantrace if the certificate is aout to expire.

![SSLCert](/images/problem.png)

## Installation
ActiveGate Plugins need to get installed both, on you Tenant and on the Environment ActiveGate they are supposed to collect data for - mainly for security reasons. NO third party code is getting executed by your ActiveGate unless your Tenant and your Agent agree on the authenticity of your plugin.
This is why you need to install, in addition to your Tenant, on selected ActiveGates, that have the Remote Plugin module running and are supposed to execute your Plugin.

This plugin checks the SSL certificates of host in the hosts.txt file and logs problems on Dyantrace if the certificate is about to expire.
