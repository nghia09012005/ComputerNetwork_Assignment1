#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course.
#
# WeApRous release
#
# The authors hereby grant to Licensee personal permission to use
# and modify the Licensed Source Code for the sole purpose of studying
# while attending the course
#

from urllib.parse import urlparse, unquote

def get_auth_from_url(url):
    """Given a url with authentication components, extract them into a tuple of
    username,password.

    :rtype: (str,str)
    """
    parsed = urlparse(url)

    try:
        auth = (unquote(parsed.username), unquote(parsed.password))
    except (AttributeError, TypeError):
        auth = ("", "")

    return auth

# 
# Đầu vào: Một URL có thể chứa thông tin xác thực, ví dụ: http://username:password@example.com
# 
# Cách hoạt động:
# - Sử dụng urlparse để phân tích URL
# - Lấy username và password từ phần thông tin xác thực của URL
# - Sử dụng unquote để giải mã các ký tự đặc biệt trong username và password (nếu có)
# 
# Giá trị trả về: Một tuple chứa (username, password)
# 
# Xử lý ngoại lệ:
# - Nếu URL không chứa thông tin xác thực, hàm trả về ("", "")
# - Xử lý các trường hợp lỗi như thiếu thuộc tính hoặc kiểu dữ liệu không đúng
#