# 测试生成API脚本

Write-Host "========== 测试生成API ==========" -ForegroundColor Green

# 1. 注册用户
Write-Host "`n1. 注册用户..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$username = "testgen_$timestamp"
$email = "testgen_$timestamp@example.com"
$body = @{username=$username; email=$email; password='password123'} | ConvertTo-Json
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/auth/register -Method POST -ContentType 'application/json' -Body $body
    Write-Host "✓ 注册成功 (状态码: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "✗ 注册失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 2. 登录
Write-Host "`n2. 登录用户..." -ForegroundColor Yellow
$body = @{email=$email; password='password123'} | ConvertTo-Json
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/auth/login -Method POST -ContentType 'application/json' -Body $body
    $token = ($response.Content | ConvertFrom-Json).access_token
    Write-Host "✓ 登录成功 (状态码: $($response.StatusCode))" -ForegroundColor Green
    Write-Host "  令牌: $($token.Substring(0, 20))..." -ForegroundColor Gray
} catch {
    Write-Host "✗ 登录失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 3. 创建生成任务
Write-Host "`n3. 创建生成任务..." -ForegroundColor Yellow
$body = @{prompt='a beautiful landscape'; model_name='sd15'} | ConvertTo-Json
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/generation/create -Method POST -ContentType 'application/json' -Body $body -Headers @{Authorization="Bearer $token"}
    $taskData = $response.Content | ConvertFrom-Json
    $taskId = $taskData.id
    Write-Host "✓ 创建成功 (状态码: $($response.StatusCode))" -ForegroundColor Green
    Write-Host "  任务ID: $taskId" -ForegroundColor Gray
    Write-Host "  状态: $($taskData.status)" -ForegroundColor Gray
} catch {
    Write-Host "✗ 创建失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 4. 查询任务状态
Write-Host "`n4. 查询任务状态..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/generation/status/$taskId" -Method GET -Headers @{Authorization="Bearer $token"}
    $taskData = $response.Content | ConvertFrom-Json
    Write-Host "✓ 查询成功 (状态码: $($response.StatusCode))" -ForegroundColor Green
    Write-Host "  任务ID: $($taskData.id)" -ForegroundColor Gray
    Write-Host "  状态: $($taskData.status)" -ForegroundColor Gray
    Write-Host "  提示词: $($taskData.prompt)" -ForegroundColor Gray
} catch {
    Write-Host "✗ 查询失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 5. 获取生成历史
Write-Host "`n5. 获取生成历史..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/generation/history" -Method GET -Headers @{Authorization="Bearer $token"}
    $history = $response.Content | ConvertFrom-Json
    Write-Host "✓ 获取成功 (状态码: $($response.StatusCode))" -ForegroundColor Green
    Write-Host "  历史记录数: $($history.Count)" -ForegroundColor Gray
    if ($history.Count -gt 0) {
        Write-Host "  最新任务: ID=$($history[0].id), 状态=$($history[0].status)" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ 获取失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 6. 删除任务
Write-Host "`n6. 删除任务..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/generation/$taskId" -Method DELETE -Headers @{Authorization="Bearer $token"}
    Write-Host "✓ 删除成功 (状态码: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "✗ 删除失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n========== 所有测试通过！==========" -ForegroundColor Green

