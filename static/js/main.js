/**
 * 主要JavaScript文件
 * 包含通用功能和初始化
 */

// 检查用户登录状态
async function checkLoginStatus() {
    try {
        const response = await fetch('/auth/check');
        const data = await response.json();
        return data.logged_in;
    } catch (error) {
        console.error('检查登录状态失败:', error);
        return false;
    }
}

// 导航菜单初始化
function initializeNavigation() {
    // 登出按钮处理
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
}

// 登出函数
async function logout() {
    try {
        const response = await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (data.success) {
            alert('登出成功');
            window.location.href = '/';
        } else {
            alert('登出失败: ' + data.message);
        }
    } catch (error) {
        alert('登出出错: ' + error.message);
    }
}

// 标签页切换
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            
            // 隐藏所有标签内容
            const tabContents = document.querySelectorAll('.tab-content');
            tabContents.forEach(content => content.classList.remove('active'));
            
            // 移除所有标签按钮的活跃状态
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // 显示选中的标签
            const selectedTab = document.getElementById(tabName);
            if (selectedTab) {
                selectedTab.classList.add('active');
            }
            
            // 标记当前按钮为活跃
            this.classList.add('active');
        });
    });
}

// 表单验证
function validateForm(formData, rules) {
    const errors = [];

    for (const [field, rule] of Object.entries(rules)) {
        const value = formData[field];

        if (rule.required && !value) {
            errors.push(`${rule.label}不能为空`);
        }

        if (rule.minLength && value && value.length < rule.minLength) {
            errors.push(`${rule.label}长度不能少于${rule.minLength}个字符`);
        }

        if (rule.maxLength && value && value.length > rule.maxLength) {
            errors.push(`${rule.label}长度不能超过${rule.maxLength}个字符`);
        }

        if (rule.pattern && value && !rule.pattern.test(value)) {
            errors.push(`${rule.label}格式不正确`);
        }
    }

    return errors;
}

// 显示消息提示
function showMessage(message, type = 'info', duration = 3000) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    document.body.insertBefore(messageDiv, document.body.firstChild);
    
    if (duration > 0) {
        setTimeout(() => {
            messageDiv.remove();
        }, duration);
    }
    
    return messageDiv;
}

// 复制到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showMessage('已复制到剪贴板', 'success', 2000);
    }).catch(() => {
        alert('复制失败，请手动复制');
    });
}

// 下载文件
function downloadFile(content, filename, mimeType = 'text/plain') {
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

// 初始化页面
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeTabs();

    // 检查登录状态，如果需要登录则跳转
    const currentPath = window.location.pathname;
    const protectedRoutes = ['/classic', '/modern', '/image-share'];
    
    if (protectedRoutes.includes(currentPath)) {
        checkLoginStatus().then(isLoggedIn => {
            if (!isLoggedIn) {
                window.location.href = '/login';
            }
        });
    }
});

// 防抖函数
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// 节流函数
function throttle(func, delay) {
    let lastCallTime = 0;
    return function(...args) {
        const now = Date.now();
        if (now - lastCallTime >= delay) {
            func.apply(this, args);
            lastCallTime = now;
        }
    };
}

// 生成随机字符串
function generateRandomString(length = 32) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

// API请求包装器
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await fetch(url, { ...defaultOptions, ...options });
        
        if (!response.ok) {
            throw new Error(`API请求失败: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API请求出错:', error);
        throw error;
    }
}

// 确认框
function confirm(message) {
    return window.confirm(message);
}

// 提示输入框
function prompt(message, defaultValue = '') {
    return window.prompt(message, defaultValue);
}
