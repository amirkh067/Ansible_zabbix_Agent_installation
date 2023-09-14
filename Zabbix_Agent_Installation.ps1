# Specify the path to the Zabbix agent MSI package
$AgentPackage = Join-Path $PSScriptRoot "zabbix_agent2-6.0.18-windows-amd64-openssl.msi"

# Specify the executable file for executing MSI packages
$exe = "msiexec.exe"

# Specify the IP address and port of the Zabbix proxy server
#$proxyIP = "172.20.40.43"

# Get the proxyIP from the console
$proxyIP = Read-Host "Enter the IP address of the Zabbix proxy server"
$proxyPort = "10050"

Write-Host "Zabbix Proxy IP: $proxyIP"
Write-Host "Zabbix Proxy Port: $proxyPort"

# Get the hostname of the local computer
$hostname = $env:COMPUTERNAME

# Specify the arguments for the MSI package installation
$Arguments = "/i `"$AgentPackage`" HOSTNAME=$hostname SERVER=$proxyIP SERVERACTIVE=$proxyIP ListenPort=$proxyPort /quiet /qn /norestart /l*v `"$(Join-Path $PSScriptRoot 'zabbix_install.log')`""

# Start the installation process and wait for it to exit
$Process = Start-Process -FilePath $exe -ArgumentList $Arguments -PassThru
$Process.WaitForExit()

# Check the exit code of the installation process
if ($Process.ExitCode -eq 0) {
    # Installation succeeded
    Write-Host "Zabbix agent installation started."
    Write-Host "Zabbix agent installation completed successfully."
    $AgentVersion = "6.0.18"
    $InstallLocation = "C:\Program Files\Zabbix Agent 2"

    # Specify the Zabbix agent configuration file
    $ZabbixConfig = "zabbix_agent2.conf"

    # Add a configuration line to allow the "system.run" item key
    $allowDenyKey = "AllowKey=system.run[*]"
    Add-Content -Path "$InstallLocation\$ZabbixConfig" -Value $allowDenyKey 

    # Restart the Zabbix agent service
     $serviceName = "Zabbix Agent 2"
     $service = Get-Service -Name $serviceName
     
     if ($service -ne $null) {
         Write-Host "Restarting the Zabbix agent service..."
         Restart-Service -Name $serviceName -Force
         Write-Host "Zabbix agent service restarted."
     } else {
         Write-Host "Zabbix agent service not found. Restart manually if needed."
     }

} else {
    # Installation failed
    Write-Host "Zabbix agent installation failed with exit code: $($Process.ExitCode)"
}