const API_BASE_URL = 'http://127.0.0.1:8000/api/users';

// Login Form
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleLogin();
    });
}

// Register Form
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleRegister();
    });
}

// Login funksiyasi
async function handleLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    
    setLoading('login', true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Token saqlash
            if (rememberMe) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
            } else {
                sessionStorage.setItem('token', data.token);
                sessionStorage.setItem('user', JSON.stringify(data.user));
            }
            
            showAlert('success', data.message || 'Muvaffaqiyatli kirdingiz!');
            
            // Bosh sahifaga o'tish
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1500);
        } else {
            showAlert('danger', data.error || 'Login yoki parol noto\'g\'ri!');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('danger', 'Serverda xatolik yuz berdi!');
    } finally {
        setLoading('login', false);
    }
}

// Register funksiyasi
async function handleRegister() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const password2 = document.getElementById('password2').value;
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const phone = document.getElementById('phone').value;
    
    // Parollarni tekshirish
    if (password !== password2) {
        showAlert('danger', 'Parollar mos kelmadi!');
        return;
    }
    
    // Parol uzunligi
    if (password.length < 8) {
        showAlert('danger', 'Parol kamida 8 ta belgidan iborat bo\'lishi kerak!');
        return;
    }
    
    setLoading('register', true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                email,
                password,
                password2,
                first_name: firstName,
                last_name: lastName,
                phone: phone || null
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Token saqlash
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            showAlert('success', data.message || 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz!');
            
            // Login sahifaga o'tish
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1500);
        } else {
            // Xatoliklarni ko'rsatish
            let errorMessage = 'Ro\'yxatdan o\'tishda xatolik!';
            if (data.username) {
                errorMessage = data.username[0];
            } else if (data.email) {
                errorMessage = data.email[0];
            } else if (data.password) {
                errorMessage = data.password[0];
            }
            showAlert('danger', errorMessage);
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('danger', 'Serverda xatolik yuz berdi!');
    } finally {
        setLoading('register', false);
    }
}

// Loading holatini o'zgartirish
function setLoading(type, isLoading) {
    const btn = document.getElementById(`${type}Btn`);
    const btnText = document.getElementById(`${type}BtnText`);
    const spinner = document.getElementById(`${type}Spinner`);
    
    if (isLoading) {
        btn.disabled = true;
        btnText.style.display = 'none';
        spinner.style.display = 'inline-block';
    } else {
        btn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

// Alert ko'rsatish
function showAlert(type, message) {
    const alertBox = document.getElementById('alertBox');
    const alertMessage = document.getElementById('alertMessage');
    
    alertBox.className = `alert alert-${type} alert-dismissible fade show`;
    alertMessage.textContent = message;
    alertBox.style.display = 'block';
    
    // 5 soniyadan keyin yashirish
    setTimeout(() => {
        hideAlert();
    }, 5000);
}

// Alert yashirish
function hideAlert() {
    const alertBox = document.getElementById('alertBox');
    alertBox.style.display = 'none';
}

// Token borligini tekshirish
function isAuthenticated() {
    return localStorage.getItem('token') || sessionStorage.getItem('token');
}

// User ma'lumotlarini olish
function getCurrentUser() {
    const userStr = localStorage.getItem('user') || sessionStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// Logout funksiyasi
async function logout() {
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    
    try {
        await fetch(`${API_BASE_URL}/logout/`, {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json',
            }
        });
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    // Token o'chirish
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('user');
    
    // Login sahifaga o'tish
    window.location.href = 'login.html';
}