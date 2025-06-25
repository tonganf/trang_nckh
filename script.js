// Danh sách các trường cần thiết theo đúng thứ tự
const REQUIRED_FIELDS = [
    'TBLANG', 'TBMATH', 'TBCT', 'TMKNM', 'TBLT',
    'M17', 'M19', 'M22', 'M30', 'M32', 'M33',
    'M34', 'M35', 'M36', 'M38', 'M41', 'M43',
    'M44', 'M45', 'M47'
];

// DOM Elements
const form = document.getElementById('predictForm');
const clearBtn = document.getElementById('clearBtn');
const predictBtn = document.getElementById('predictBtn');
const loading = document.getElementById('loading');
const result = document.getElementById('result');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    addInputValidation();
});

// Event Listeners
function initializeEventListeners() {
    form.addEventListener('submit', handleFormSubmit);
    clearBtn.addEventListener('click', clearAllInputs);
    
    // Add input event listeners for real-time validation and restriction
    REQUIRED_FIELDS.forEach(field => {
        const input = document.getElementById(field);
        if (input) {
            input.addEventListener('input', validateInput);
            input.addEventListener('blur', validateInput);
            restrictInput(input); // Add input restriction
        }
    });
}

// Form submission handler
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!validateForm()) {
        showResult('Vui lòng điền đầy đủ và chính xác tất cả các trường!', 'error');
        return;
    }
    
    const formData = collectFormData();
    
    try {
        showLoading(true);
        const prediction = await sendPredictionRequest(formData);
        showResult(`${prediction}`, 'success');
    } catch (error) {
        console.error('Prediction error:', error);
        showResult(`❌ Lỗi: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// Collect form data
function collectFormData() {
    const data = {};
    REQUIRED_FIELDS.forEach(field => {
        const input = document.getElementById(field);
        if (input) {
            // Chuyển đổi dấu phẩy thành dấu chấm trước khi parse float
            const value = input.value.replace(',', '.');
            data[field] = parseFloat(value) || 0;
        }
    });
    return data;
}

// Send prediction request to backend
async function sendPredictionRequest(data) {
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    return result.prediction;
}

// Form validation
function validateForm() {
    let isValid = true;
    
    REQUIRED_FIELDS.forEach(field => {
        const input = document.getElementById(field);
        if (input && !validateSingleInput(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// Validate single input
function validateSingleInput(input) {
    const value = input.value;
    
    // Cho phép trường hợp rỗng hoặc đang nhập dấu thập phân
    if (value === '' || value === '0.' || /^\d{1,2}\.$/.test(value)) {
        input.classList.remove('invalid');
        return true;
    }
    
    // Chuyển dấu phẩy thành dấu chấm để kiểm tra
    const valueToCheck = value.replace(',', '.');
    
    // Kiểm tra định dạng số thập phân hợp lệ
    if (!/^\d{1,2}(\.\d{0,2})?$/.test(valueToCheck)) {
        input.classList.add('invalid');
        return false;
    }
    
    // Kiểm tra giá trị số
    const numValue = parseFloat(valueToCheck);
    if (isNaN(numValue) || numValue < 0 || numValue > 10) {
        input.classList.add('invalid');
        return false;
    }
    
    input.classList.remove('invalid');
    return true;
}

// Restrict input to only allow numbers between 0-10, cho phép số lẻ/thập phân
function restrictInput(input) {
    let previousValue = '';

    input.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Nếu giá trị rỗng, cho phép
        if (value === '') {
            previousValue = value;
            return;
        }

        // Chuyển dấu phẩy thành dấu chấm
        value = value.replace(/,/g, '.');

        // Kiểm tra nếu giá trị chỉ là "0." hoặc số hợp lệ với dấu thập phân
        const isValidDecimal = /^(\d{1,2}\.?\d{0,2}|\d{0,2}\.?\d{0,2})$/.test(value);
        
        if (isValidDecimal) {
            // Nếu là số hợp lệ, kiểm tra giá trị
            if (value.endsWith('.')) {
                // Cho phép nếu đang nhập dấu thập phân
                previousValue = value;
                e.target.value = value;
            } else {
                const numValue = parseFloat(value);
                if (!isNaN(numValue) && numValue <= 10) {
                    previousValue = value;
                    e.target.value = value;
                } else {
                    // Nếu giá trị > 10, quay lại giá trị trước
                    e.target.value = previousValue;
                }
            }
        } else {
            // Nếu không hợp lệ, quay lại giá trị trước
            e.target.value = previousValue;
        }
        
        validateSingleInput(e.target);
    });

    // Xử lý sự kiện keydown
    input.addEventListener('keydown', function(e) {
        // Cho phép các phím điều hướng và control
        if (e.key === 'Backspace' || 
            e.key === 'Delete' || 
            e.key === 'ArrowLeft' || 
            e.key === 'ArrowRight' || 
            e.key === 'Tab' || 
            e.key === 'Enter' ||
            ((e.ctrlKey || e.metaKey) && ['a', 'c', 'v', 'x'].includes(e.key.toLowerCase()))) {
            return;
        }
        
        // Cho phép nhập số
        if (e.key >= '0' && e.key <= '9') {
            return;
        }
        
        // Cho phép nhập dấu chấm và dấu phẩy
        if (e.key === '.' || e.key === ',') {
            const currentValue = e.target.value;
            // Chỉ cho phép một dấu thập phân
            if (!currentValue.includes('.') && !currentValue.includes(',')) {
                return;
            }
        }
        
        // Chặn tất cả các phím khác
        e.preventDefault();
    });
}

// Input validation event handler
function validateInput(e) {
    validateSingleInput(e.target);
}

// Add input validation styles
function addInputValidation() {
    const style = document.createElement('style');
    style.textContent = `
        .input-field input.invalid {
            border-color: #f56565 !important;
            box-shadow: 0 0 0 3px rgba(245, 101, 101, 0.1) !important;
        }
        
        .input-field input.invalid:focus {
            border-color: #f56565 !important;
            box-shadow: 0 0 0 3px rgba(245, 101, 101, 0.2) !important;
        }
    `;
    document.head.appendChild(style);
}

// Clear all inputs
function clearAllInputs() {
    REQUIRED_FIELDS.forEach(field => {
        const input = document.getElementById(field);
        if (input) {
            input.value = '';
            input.classList.remove('invalid');
        }
    });
    
    hideResult();
    showResult('✅ Đã xóa tất cả dữ liệu!', 'success');
    setTimeout(hideResult, 2000);
}

// Show loading state
function showLoading(show) {
    if (show) {
        loading.classList.remove('hidden');
        predictBtn.disabled = true;
        predictBtn.textContent = '⏳ Đang xử lý...';
    } else {
        loading.classList.add('hidden');
        predictBtn.disabled = false;
        predictBtn.innerHTML = '🔮 Dự đoán Tình trạng';
    }
}

// Show result
function showResult(message, type) {
    result.textContent = message;
    result.className = `result ${type}`;
    result.classList.remove('hidden');
    
    // Auto hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            hideResult();
        }, 5000);
    }
}

// Hide result
function hideResult() {
    result.classList.add('hidden');
}

// Utility functions
function formatNumber(num) {
    return parseFloat(num).toFixed(2);
}

// Add some sample data for testing (optional)
function fillSampleData() {
    const sampleData = {
        'TBLANG': 7.5,
        'TBMATH': 8.0,
        'TBCT': 7.8,
        'TMKNM': 8.2,
        'TBLT': 7.9,
        'M17': 8.1,
        'M19': 7.7,
        'M22': 8.3,
        'M30': 7.6,
        'M32': 8.0,
        'M33': 7.9,
        'M36': 8.2,
        'M41': 7.8,
        'M44': 8.1,
        'M45': 7.7,
        'M47': 8.0
    };
    
    Object.entries(sampleData).forEach(([field, value]) => {
        const input = document.getElementById(field);
        if (input) {
            input.value = value;
        }
    });
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl + Enter to submit
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        form.dispatchEvent(new Event('submit'));
    }
    
    // Ctrl + R to clear (prevent page refresh)
    if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        clearAllInputs();
    }
});

// Add development helper (remove in production)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('🚀 Development mode detected');
    console.log('💡 Keyboard shortcuts:');
    console.log('   Ctrl + Enter: Submit form');
    console.log('   Ctrl + R: Clear all inputs');
    
    // Add sample data button in development
    const devButton = document.createElement('button');
    devButton.textContent = '🧪 Fill Sample Data';
    devButton.className = 'btn btn-secondary';
    devButton.type = 'button';
    devButton.style.marginTop = '10px';
    devButton.onclick = fillSampleData;
    
    const formActions = document.querySelector('.form-actions');
    formActions.appendChild(devButton);
} 