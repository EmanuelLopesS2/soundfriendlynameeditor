# List audio devices and return selection
function Get-AudioDevices {
    Clear-Host
    Write-Host "`nListing Audio Devices:" -ForegroundColor Green
    Write-Host "--------------------" -ForegroundColor Green
    
    # Get and store devices in array
    $devices = Get-PnpDevice -Class "MEDIA" -Status OK | ForEach-Object {
        [PSCustomObject]@{
            Name = $_.FriendlyName
            ID = $_.InstanceId
        }
    }
    
    # List devices with index
    for ($i = 0; $i -lt $devices.Count; $i++) {
        Write-Host ("[{0}] {1}" -f ($i + 1), $devices[$i].Name) -ForegroundColor Yellow
    }
    
    return $devices
}

# Get valid user input
function Get-UserSelection {
    param (
        [array]$devices
    )
    
    while ($true) {
        Write-Host "`nEnter device number (1-$($devices.Count)): " -ForegroundColor Cyan -NoNewline
        $selection = Read-Host
        
        # Check if number is valid
        if ($selection -match '^\d+$') {
            $index = [int]$selection - 1
            if ($index -ge 0 -and $index -lt $devices.Count) {
                return $index
            }
        }
        
        Write-Host "Invalid selection. Please try again." -ForegroundColor Red
    }
}

# Handle system restart
function Request-Restart {
    while ($true) {
        Write-Host "`nDo you want to restart now? (Y/N): " -ForegroundColor Cyan -NoNewline
        $response = Read-Host
        
        switch ($response.ToUpper()) {
            'Y' {
                Write-Host "`nRestarting computer..." -ForegroundColor Yellow
                Start-Sleep -Seconds 2
                Restart-Computer -Force
                return
            }
            'N' {
                Write-Host "`nPlease remember to restart your computer to apply changes." -ForegroundColor Yellow
                return
            }
            default {
                Write-Host "Invalid input. Please enter Y or N." -ForegroundColor Red
            }
        }
    }
}

# Main function
function Main {
    # Check admin privileges
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        Write-Host "Please run this script as Administrator!" -ForegroundColor Red
        return
    }
    
    # Get device selection
    $devices = Get-AudioDevices
    $selectedIndex = Get-UserSelection $devices
    $selectedDevice = $devices[$selectedIndex]
    
    # Get new name
    Write-Host "`nSelected device: " -ForegroundColor Green -NoNewline
    Write-Host $selectedDevice.Name -ForegroundColor Yellow
    Write-Host "Enter new name (or press Enter to keep current): " -ForegroundColor Cyan -NoNewline
    $newName = Read-Host
    
    # Update device name
        # Update device name
    # Update device name
    # Update device name
    if ($newName) {
        try {
            $registryPath = "HKLM:\SYSTEM\CurrentControlSet\Enum\$($selectedDevice.ID)"
            
            # First check if Device Parameters exists
            if (Test-Path "$registryPath\Device Parameters") {
                Set-ItemProperty -Path "$registryPath\Device Parameters" -Name "FriendlyName" -Value $newName -ErrorAction Stop
            } else {
                Set-ItemProperty -Path $registryPath -Name "FriendlyName" -Value $newName -ErrorAction Stop
            }
            
            Write-Host "`nDevice name updated successfully!" -ForegroundColor Green
            Write-Host "Note: Physical devices require a system restart to display the new name." -ForegroundColor Yellow
            
            Request-Restart
        }
        catch {
            Write-Host "`nError updating device name: $_" -ForegroundColor Red
        }
    }
    else {
        Write-Host "`nNo changes made." -ForegroundColor Yellow
    }
}

# Run main script
Main