 # Specify the path to the Zabbix agent MSI package
$AgentPackage = "C:\zabbix_agent2-6.0.18-windows-amd64-openssl.msi"

# Specify the executable file for executing MSI packages
$exe = "msiexec.exe"

# Specify the IP address and port of the Zabbix proxy server
$proxyIP = "172.20.40.44"
$proxyPort = "10050"

# Get the hostname of the local computer
$hostname = $env:COMPUTERNAME

# Specify the arguments for the MSI package installation
#$Arguments = "/i `"$AgentPackage`" HOSTNAME=$hostname SERVER=$proxyIP SERVERACTIVE=$proxyIP /quiet /qn /norestart"
$Arguments = "/i `"$AgentPackage`" HOSTNAME=$hostname SERVER=$proxyIP SERVERACTIVE=$proxyIP ListenPort=$proxyPort /quiet /qn /norestart /l*v C:\zabbix_install.log"


# Start the installation process and wait for it to exit
$Process = Start-Process -FilePath msiexec -ArgumentList $Arguments -PassThru
$Process.WaitForExit()

# Check the exit code of the installation process
if ($Process.ExitCode -eq 0) {
    # Installation succeeded
    Write-Host "Zabbix agent installation completed successfully."
    $AgentVersion = "6.0.18"
    $InstallLocation = "C:\Program Files\Zabbix Agent 2"

    # Specify the Zabbix agent configuration file
    $ZabbixConfig = "zabbix_agent2.conf"

    
    # Add a configuration line to allow the "system.run" item key
    # $allowDenyKey = "AllowKey=system.run[*]"
    # Add-Content -Path "$InstallLocation\$ZabbixConfig" -Value $allowDenyKey
    
    # Change timeout settings
    $timeout = "Timeout=30"
    Add-Content -Path "$InstallLocation\$ZabbixConfig" -Value $timeout
    
} else {
    # Installation failed
    Write-Host "Zabbix agent installation failed with exit code: $($Process.ExitCode)"
}
