# 后端API测试脚本

$baseUrl = "http://localhost:8000/api/v1"
$testResults = @()

function Test-Endpoint {
    param(
        [string]$name,
        [string]$method,
        [string]$endpoint,
        [object]$body = $null
    )
    
    try {
        $url = "$baseUrl$endpoint"
        $params = @{
            Uri = $url
            Method = $method
            ContentType = "application/json"
            ErrorAction = "Stop"
        }
        
        if ($body) {
            $params["Body"] = $body | ConvertTo-Json
        }
        
        $response = Invoke-WebRequest @params
        $result = @{
            Name = $name
            Status = "✅ PASS"
            StatusCode = $response.StatusCode
            Message = "成功"
        }
    }
    catch {
        $result = @{
            Name = $name
            Status = "❌ FAIL"
            StatusCode = $_.Exception.Response.StatusCode
            Message = $_.Exception.Message
        }
    }
    
    $testResults += $result
    return $result
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🧪 后端API测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 健康检查
Write-Host "1️⃣ 健康检查" -ForegroundColor Yellow
$result = Test-Endpoint -name "健康检查" -method "GET" -endpoint "/health"
Write-Host "   $($result.Status) - $($result.Message)" -ForegroundColor $(if ($result.Status -like "*PASS*") { "Green" } else { "Red" })

# 2. 用户注册
Write-Host ""
Write-Host "2️⃣ 用户认证" -ForegroundColor Yellow

$registerBody = @{
    email = "test@example.com"
    password = "Test@123456"
    username = "testuser"
} | ConvertTo-Json

$result = Test-Endpoint -name "用户注册" -method "POST" -endpoint "/auth/register" -body $registerBody
Write-Host "   $($result.Status) - $($result.Message)" -ForegroundColor $(if ($result.Status -like "*PASS*") { "Green" } else { "Red" })

# 3. 用户登录
$loginBody = @{
    email = "test@example.com"
    password = "Test@123456"
} | ConvertTo-Json

$result = Test-Endpoint -name "用户登录" -method "POST" -endpoint "/auth/login" -body $loginBody
Write-Host "   $($result.Status) - $($result.Message)" -ForegroundColor $(if ($result.Status -like "*PASS*") { "Green" } else { "Red" })

# 4. 获取模型列表
Write-Host ""
Write-Host "3️⃣ 生成功能" -ForegroundColor Yellow

$result = Test-Endpoint -name "获取模型列表" -method "GET" -endpoint "/models"
Write-Host "   $($result.Status) - $($result.Message)" -ForegroundColor $(if ($result.Status -like "*PASS*") { "Green" } else { "Red" })

# 5. 管理员登录
Write-Host ""
Write-Host "4️⃣ 管理功能" -ForegroundColor Yellow

$adminLoginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$result = Test-Endpoint -name "管理员登录" -method "POST" -endpoint "/admin/login" -body $adminLoginBody
Write-Host "   $($result.Status) - $($result.Message)" -ForegroundColor $(if ($result.Status -like "*PASS*") { "Green" } else { "Red" })

# 总结
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📊 测试总结" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$passCount = ($testResults | Where-Object { $_.Status -like "*PASS*" }).Count
$failCount = ($testResults | Where-Object { $_.Status -like "*FAIL*" }).Count
$totalCount = $testResults.Count

Write-Host ""
Write-Host "总测试数: $totalCount" -ForegroundColor Cyan
Write-Host "通过: $passCount ✅" -ForegroundColor Green
Write-Host "失败: $failCount ❌" -ForegroundColor Red
Write-Host ""

if ($failCount -eq 0) {
    Write-Host "🎉 所有测试通过！" -ForegroundColor Green
} else {
    Write-Host "⚠️ 有 $failCount 个测试失败" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "详细结果:" -ForegroundColor Cyan
$testResults | Format-Table -AutoSize

