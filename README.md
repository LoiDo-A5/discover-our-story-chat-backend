Hướng dẫn cài đặt và chạy project Django ở môi trường local sử dụng Docker Compose
🚀 Hướng dẫn cài đặt và chạy project ở môi trường local
⚙️ Yêu cầu
Trước khi bắt đầu, bạn cần đảm bảo máy đã cài đặt:

Docker
Docker Compose
🔧 Các bước cài đặt và chạy project
Clone project từ GitHub (nếu cần)

git clone https://github.com/your-username/your-repo.git
cd your-repo
Build Docker containers

docker-compose build
Lệnh này sẽ build toàn bộ các container định nghĩa trong file docker-compose.yml.

Khởi chạy Docker containers

docker-compose up
Kiểm tra các container đã chạy

docker-compose ps
Apply migrations cho database

docker compose exec app poetry run python manage.py migrate
Tạo superuser để đăng nhập vào Django admin

docker compose exec app poetry run python manage.py createsuperuser
Truy cập ứng dụng Mở trình duyệt và vào địa chỉ:

http://localhost:8000/admin
Đăng nhập bằng tài khoản user admin đã tạo.

(Tuỳ chọn) Truy cập vào Django shell để test

docker compose exec app poetry run python manage.py shell
📁 Cấu trúc volume & network
Volumes:
postgres_data: Dữ liệu PostgreSQL sẽ được lưu tại đây để không mất khi container bị xoá.
Networks:
backend: Các service app, db, và redis nằm chung network này để có thể giao tiếp với nhau.
