# 完整的异步生成测试脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "异步生成功能完整测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. 注册用户
Write-Host "`n[1/5] 注册用户..." -ForegroundColor Yellow
$body = @{
    username = 'asynctest'
    email = 'asynctest@example.com'
    password = 'password123'
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/auth/register -Method POST -ContentType 'application/json' -Body $body
    Write-Host "✅ 注册成功" -ForegroundColor Green
} catch {
    Write-Host "⚠️  用户可能已存在，继续..." -ForegroundColor Yellow
}

# 2. 登录
Write-Host "`n[2/5] 登录..." -ForegroundColor Yellow
$body = @{
    email = 'asynctest@example.com'
    password = 'password123'
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/auth/login -Method POST -ContentType 'application/json' -Body $body
$token = ($response.Content | ConvertFrom-Json).access_token
Write-Host "✅ 登录成功，Token: $($token.Substring(0, 20))..." -ForegroundColor Green

# 3. 创建异步生成任务
Write-Host "`n[3/5] 创建异步生成任务..." -ForegroundColor Yellow
$body = @{
    prompt = 'a beautiful sunset over mountains'
    model_name = 'stable-diffusion-1.5'
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/generation/create-async -Method POST -ContentType 'application/json' -Body $body -Headers @{Authorization="Bearer $token"}
$taskData = $response.Content | ConvertFrom-Json
$taskId = $taskData.id
Write-Host "✅ 异步任务创建成功，Task ID: $taskId" -ForegroundColor Green
Write-Host "   状态: $($taskData.status)" -ForegroundColor Cyan

# 4. 轮询任务状态
Write-Host "`n[4/5] 轮询任务状态..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$completed = $false

while ($attempt -lt $maxAttempts -and -not $completed) {
    Start-Sleep -Seconds 1
    $attempt++
    
    try {
        $response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/generation/status/$taskId -Method GET -Headers @{Authorization="Bearer $token"}
        $status = ($response.Content | ConvertFrom-Json).status
        
        Write-Host "   [$attempt/$maxAttempts] 状态: $status" -ForegroundColor Cyan
        
        if ($status -eq 'completed') {
            Write-Host "✅ 任务完成！" -ForegroundColor Green
            $completed = $true
        } elseif ($status -eq 'failed') {
            Write-Host "❌ 任务失败！" -ForegroundColor Red
            $completed = $true
        }
    } catch {
        Write-Host "   [$attempt/$maxAttempts] 查询中..." -ForegroundColor Gray
    }
}

# 5. 获取任务结果
Write-Host "`n[5/5] 获取任务结果..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/generation/result/$taskId -Method GET -Headers @{Authorization="Bearer $token"}
    $result = $response.Content | ConvertFrom-Json
    Write-Host "✅ 获取结果成功" -ForegroundColor Green
    Write-Host "   图片URL: $($result.image_url)" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️  获取结果失败: $_" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "测试完成！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

