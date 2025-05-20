Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName System.Windows.Forms

function Show-PasswordWindow {
    $xaml = @"
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        Title="Password Visualizer" Height="300" Width="600" Topmost="True"
        WindowStartupLocation="CenterScreen" ResizeMode="NoResize">
    <Grid Margin="10">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
        </Grid.RowDefinitions>
        <TextBlock Text="Enter password (displayed in color below):"
                   FontSize="18" Margin="0,0,0,10" Grid.Row="0"/>
        <TextBox Name="InputBox" FontSize="24" FontFamily="Consolas"
                 Grid.Row="1" Margin="0,0,0,10" AcceptsReturn="False" AcceptsTab="False"/>
        <TextBlock Name="PasswordText"
                   FontSize="36" FontFamily="Consolas"
                   TextAlignment="Center" TextWrapping="Wrap"
                   Grid.Row="2" Margin="0,10,0,10"/>
        <StackPanel Grid.Row="3" Orientation="Horizontal" HorizontalAlignment="Left" Margin="0,10,0,0">
            <TextBlock Text="Capital: " Foreground="Green" FontSize="14" Margin="0,0,10,0"/>
            <TextBlock Text="Lower: " Foreground="Blue" FontSize="14" Margin="0,0,10,0"/>
            <TextBlock Text="Number: " Foreground="Red" FontSize="14" Margin="0,0,10,0"/>
            <TextBlock Text="Symbol: " Foreground="Black" FontSize="14"/>
        </StackPanel>
        <Button Name="OKButton" Content="OK" Width="100" Height="40"
                FontSize="16" Grid.Row="4" HorizontalAlignment="Center" Margin="0,10,0,0"/>
    </Grid>
</Window>
"@

    $reader = New-Object System.Xml.XmlNodeReader ([xml]$xaml)
    $window = [Windows.Markup.XamlReader]::Load($reader)

    $inputBox = $window.FindName("InputBox")
    $passwordText = $window.FindName("PasswordText")
    $okButton = $window.FindName("OKButton")

    $script:result = $null

    # Update color-coded display as user types
    $inputBox.Add_TextChanged({
        $passwordText.Inlines.Clear()
        $password = $inputBox.Text
        foreach ($char in $password.ToCharArray()) {
            $run = New-Object System.Windows.Documents.Run
            $run.Text = $char
            switch -Regex -CaseSensitive ($char) {
                '[A-Z]' { $run.Foreground = 'Green' }
                '[a-z]' { $run.Foreground = 'Blue' }
                '\d'    { $run.Foreground = 'Red' }
                default { $run.Foreground = 'Black' }
            }
            $passwordText.Inlines.Add($run)
        }
    })

    # Handle OK button click
    $okButton.Add_Click({
        $script:result = $inputBox.Text
        $window.DialogResult = $true
        $window.Close()
    })

    # Handle Enter key press
    $inputBox.Add_KeyDown({
        if ($_.Key -eq 'Return') {
            $script:result = $inputBox.Text
            $window.DialogResult = $true
            $window.Close()
        }
    })

    # Ensure UI operations are on the correct thread
    $window.Dispatcher.Invoke([Action]{ $window.ShowDialog() }) | Out-Null
    return $script:result
}

# Main Execution
# Ensure STA thread mode for compiled executable
[Threading.Thread]::CurrentThread.SetApartmentState([Threading.ApartmentState]::STA)

# Create application context only if it doesn't exist
if (-not [Windows.Application]::Current) {
    $app = New-Object Windows.Application
    $appCreated = $true
} else {
    $app = [Windows.Application]::Current
    $appCreated = $false
}

try {
    $password = Show-PasswordWindow
}
finally {
    # Clean up application context only if we created it
    if ($appCreated) {
        $app.Dispatcher.Invoke([Action]{ $app.Shutdown() })
    }
}