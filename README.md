#cách chạy chương trình
1. chạy file start.py, chọn số nút cần khởi tạo trên giao diện và start.
Có thể thấy console log các trạng thái hiện tại của mạng

2. chạy file showlog.py để xem các log được commit
3. chạy file client.py để có thể thêm vào 1 log mesage. Nhập một số nguyên

#các testcase hiện tại
1. khi mạng mất đi leader sẽ tự động tìm leader mới. Các shutdown một node hoặc resume một node
là click vào node đó trên giao diện
2. khi 1 node start lại, nó sẽ thêm được các log trước đó bị bỏ lỡ
3. khi một node mất kết nối, nó không thể thêm mới một entry
4.  khi node mất kết nối quay lại và qua trình bầu cử diễn ra do hết thời gian time out(khi leader bị ngắt) => node quay lại
này ko thể trở thành leader vì các entry của nó quá cũ