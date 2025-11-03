# Test async generation

# Login
$body = @{email='asynctest@example.com'; password='password123'} | ConvertTo-Json
$response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/auth/login -Method POST -ContentType 'application/json' -Body $body
$token = ($response.Content | ConvertFrom-Json).access_token
Write-Host "Login successful"

# Create async task
$body = @{prompt='a beautiful sunset'; model_name='stable-diffusion-1.5'} | ConvertTo-Json
$response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/generation/create-async -Method POST -ContentType 'application/json' -Body $body -Headers @{Authorization="Bearer $token"}
$taskData = $response.Content | ConvertFrom-Json
$taskId = $taskData.id
Write-Host "Async task created: $taskId"
Write-Host "Status: $($taskData.status)"

# Poll status
Write-Host "Polling status..."
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/generation/status/$taskId -Method GET -Headers @{Authorization="Bearer $token"}
    $status = ($response.Content | ConvertFrom-Json).status
    Write-Host "[$i] Status: $status"
    
    if ($status -eq 'completed' -or $status -eq 'failed') {
        break
    }
}

# Get result
Write-Host "Getting result..."
$response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/generation/result/$taskId -Method GET -Headers @{Authorization="Bearer $token"}
$result = $response.Content | ConvertFrom-Json
Write-Host "Result: $($result.image_url)"

