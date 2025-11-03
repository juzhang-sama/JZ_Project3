# 测试异步生成API

Write-Host "========================================" -ForegroundColor Green
Write-Host "测试异步生成API" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 1. 注册用户
Write-Host "1. 注册用户..." -ForegroundColor Cyan
$body = @{username='asynctest'; email='asynctest@example.com'; password='password123'} | ConvertTo-Json
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/auth/register -Method POST -ContentType 'application/json' -Body $body
    Write-Host "✅ 注册成功" -ForegroundColor Green
} catch {
    Write-Host "⚠️ 用户可能已存在" -ForegroundColor Yellow
}

# 2. 登录
Write-Host ""
Write-Host "2. 登录用户..." -ForegroundColor Cyan
$body = @{email='asynctest@example.com'; password='password123'} | ConvertTo-Json
$response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/auth/login -Method POST -ContentType 'application/json' -Body $body
$token = ($response.Content | ConvertFrom-Json).access_token
Write-Host "✅ 登录成功" -ForegroundColor Green
Write-Host "令牌: $($token.Substring(0, 20))..." -ForegroundColor Gray

# 3. 创建异步生成任务
Write-Host ""
Write-Host "3. 创建异步生成任务..." -ForegroundColor Cyan
$body = @{prompt='a beautiful landscape with mountains'; model_name='stable-diffusion-1.5'} | ConvertTo-Json
$response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/generation/create-async -Method POST -ContentType 'application/json' -Body $body -Headers @{Authorization="Bearer $token"}
$taskData = $response.Content | ConvertFrom-Json
$taskId = $taskData.id
Write-Host "✅ 任务创建成功" -ForegroundColor Green
Write-Host "任务ID: $taskId" -ForegroundColor Gray
Write-Host "状态: $($taskData.status)" -ForegroundColor Gray

# 4. 查询任务状态
Write-Host ""
Write-Host "4. 查询任务状态..." -ForegroundColor Cyan
$response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/generation/status/$taskId -Method GET -Headers @{Authorization="Bearer $token"}
$statusData = $response.Content | ConvertFrom-Json
Write-Host "✅ 查询成功" -ForegroundColor Green
Write-Host "状态: $($statusData.status)" -ForegroundColor Gray
Write-Host "提示词: $($statusData.prompt)" -ForegroundColor Gray

# 5. 获取生成历史
Write-Host ""
Write-Host "5. 获取生成历史..." -ForegroundColor Cyan
$response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/generation/history -Method GET -Headers @{Authorization="Bearer $token"}
$historyData = $response.Content | ConvertFrom-Json
Write-Host "✅ 获取成功" -ForegroundColor Green
Write-Host "历史记录数: $($historyData.Count)" -ForegroundColor Gray

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ 所有测试完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

