#!/usr/bin/env python3
"""
Script cài đặt dependencies an toàn cho hệ thống dự đoán tình trạng sinh viên
"""

import subprocess
import sys
import os

def run_command(command):
    """Chạy command và in output"""
    print(f"🔄 Đang chạy: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ Thành công!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi: {e}")
        if e.stderr:
            print(f"Chi tiết lỗi: {e.stderr}")
        return False

def main():
    print("🚀 Bắt đầu cài đặt dependencies...")
    
    # Upgrade pip trước
    print("\n📦 Cập nhật pip...")
    if not run_command(f"{sys.executable} -m pip install --upgrade pip"):
        print("⚠️ Không thể cập nhật pip, tiếp tục...")
    
    # Cài đặt setuptools mới nhất
    print("\n🔧 Cài đặt setuptools...")
    if not run_command(f"{sys.executable} -m pip install --upgrade setuptools"):
        print("⚠️ Không thể cài setuptools, tiếp tục...")
    
    # Cài đặt wheel
    print("\n⚙️ Cài đặt wheel...")
    if not run_command(f"{sys.executable} -m pip install wheel"):
        print("⚠️ Không thể cài wheel, tiếp tục...")
    
    # Cài đặt từng package riêng lẻ để tránh conflict
    packages = [
        "Flask==2.3.3",
        "Flask-CORS==4.0.0", 
        "joblib>=1.3.0",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0"
    ]
    
    print("\n📚 Cài đặt các thư viện cần thiết...")
    failed_packages = []
    
    for package in packages:
        print(f"\n📦 Cài đặt {package}...")
        if not run_command(f"{sys.executable} -m pip install {package}"):
            failed_packages.append(package)
    
    # Báo cáo kết quả
    print("\n" + "="*50)
    if not failed_packages:
        print("🎉 Cài đặt hoàn tất thành công!")
        print("✅ Tất cả dependencies đã được cài đặt.")
        print("\n🚀 Bạn có thể chạy ứng dụng bằng: python app.py")
    else:
        print("⚠️ Một số packages không cài được:")
        for pkg in failed_packages:
            print(f"   ❌ {pkg}")
        print("\n💡 Thử cài đặt thủ công:")
        for pkg in failed_packages:
            print(f"   pip install {pkg}")
    
    print("\n📋 Kiểm tra phiên bản Python:")
    print(f"   Python: {sys.version}")
    print(f"   Pip: ", end="")
    run_command(f"{sys.executable} -m pip --version")

if __name__ == "__main__":
    main() 