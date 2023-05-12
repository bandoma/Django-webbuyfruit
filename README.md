# Django-webbuyfruit
Web của tôi có những chức năng cơ bản của một web bình thường:
3.1	Đăng nhập.
•	Giao diện đăng nhập:
Người dùng nhập thông tin tài khoản và mật khẩu. Sau đó, kiểm tra thông tin đăng nhập với dữ liệu trong cơ sở dữ liệu và cho phép họ truy cập vào trang đã được bảo mật.
 
Hình 3: Chức năng login

3.2	Đăng ký.
•	Giao diện đăng ký tài khoản mới:
Là chức năng cho phép người dùng đăng ký tài khoản mới trên website. Người dùng nhập thông tin tài khoản và mật khẩu. Sau đó, kiểm tra thông tin đăng ký của người dùng và lưu thông tin tài khoản vào cơ sở dữ liệu.
 
Hình 4: Chức năng đăng ký của user
3.3	Quên mật khẩu 
•	Giao diện quên mật khẩu
-	Đây là chức cho cho phép người dùng có thể lấy lại mật khẩu khi không nhớ mật khẩu của mình thông qua gmail.
 
Hình 5: Chức năng quên mật khẩu
3.4	Đổi mật khẩu	
 
-	Ở đây bạn có thể thay đổi mật khẩu cho an toàn, nếu bạn nhập sai sẽ bị cảnh báo
3.5	Trang chủ
•	Giao diện trang chủ:
Đây là chức năng mặc định được hiển thị khi người dùng truy cập vào website.

 
Hình 6: Trang chủ web

3.6	Shop
•	Giao diện Sidebar Shop:
Khi chưa Login
-	Sẽ xem được các giá tiền hay chi tiết sản phẩm  sản phẩm, sắp xếp theo giá từ cao đến thấp hoặc từ thấp đến cao
-	Có thể xem ở hình “Con mắt” sẽ hiện ra thế này:
 
Hình 7: Xem tóm tắt sản phẩm
 
Hình 8: Giao diện SidebarShop
Khi chưa login, sẽ có yêu cầu bạn đăng nhập nếu bạn muốn Add to Cart hoặc Add to Wishlist
Khi đã Login 
-	Sẽ có Mycart ở góc bên phải màn hình
 
Hình 9: My cart khi đã Login

3.7	Gallery
•	Giao diện của Gallery
Ở đây, chúng tôi hiện các hình ảnh của các sản phẩm. Khách hàng có thể xem chi tiết theo tất cả hoặc theo từng loại, có thể thêm vào giỏ hàng hoặc thêm vào danh sách yêu thích.
 
Hình 10: Giao diện Gallery
3.8	Chức năng quản lý
3.8.1	Quản lý giỏ hàng 
•	Chỉ khi đăng nhập vào mới có thể thêm vào giỏ hàng và xem giỏ hàng.
•	Giao diện của giỏ hàng đơn giản:
 
Hình 11: Giao diện cart và sidebar shop
-	Ở đây có thể thấy số lượng sản phẩm ở trên mycart
3.8.2	Quản lý shop-detail
 
Hình 12: Quản lý shop-detail
-	Ở đây chúng ta có thể xem chi tiết sản phẩm


3.8.3	Quản lý Cart
 
Hình 13: Quản lý Cart
-	Ở đây user có thể xoá nếu không muốn ở trong cart có thể đổi được số lượng (quantity) của hàng, có thể thấy được tổng giá trị đơn hàng trong cart
-	Nếu bạn muốn checkout, bạn phải tích vào những sản phẩm bạn muốn mua rồi sau đó checkout
3.8.4	Quản lý checkout
 
Hình 14: Quản lý Checkout
Ở đây, bạn phải điền đầy đủ thông tin về tên,địa chỉ, số điện thoại, kiểm tra có đúng sản phẩm và giá tiền và tổng tiền hay chưa, số điện thoại bắt buộc phải có 10 số, khi nhập đầy đủ hãy ấn place Order
3.8.5	Receipt
 
Hình 15: Hoá đơn (Receipt)
3.9	Báo cáo cho admin
 
Hình 16: Báo cáo cho admin
Ở Đây nếu thấy thiếu hang, hay ship trễ bạn có thể báo cáo cho admin, admin sẽ phản hồi lại cho bạn
3.10	Admin phản hồi
Admin nhận và phản hồi cho bạn các vấn đề mà bạn hỏi
 
Hình 17: Admin trả lời cho user
4.	Chức năng của admin 
4.1	Chức năng thêm,sửa, xoá sản phẩm
 
Hình 18: Thêm,sửa,xoá sản phẩm của admin
-	Chúng ta có thể xem tất cả các sản phẩm, xoá hay chỉnh sửa nếu có sai hay bị lỗi gì đó
4.2	Chức năng thêm,sửa, xoá thể loại
 
Hình 19: Thêm, sửa, xoá thể loại của admin
-	Chúng ta có thể xem tất cả các thể loại, xoá hay chỉnh sửa nếu có sai hay bị lỗi gì đó
4.3	Chức năng xem,xoá người dùng
 
Hình 20: Chức năng xem,xoá người dùng
4.4	Chức năng biểu đồ
4.4.1	Biểu đồ cột 
-	Ở đây, nhóm chúng em tạo biểu đồ cột để xem sản phẩm nào được mua nhiều nhất, nhằm tạo ra được việc nên nhập sản phẩm nào về
 
Hình 21: Biểu đồ cột
4.4.2	Biểu đồ đường
-	Ở đây, nhóm chúng em tạo ra biểu đồ đường để xem ngày hôm đó ,có bao nhiêu đơn hang được mua, để xem mức độ tang trưởng theo tháng hoặc theo quý
 
Hình 22: Biểu đồ đường
Chúng ta có thể xem được ngày đó họ mua cái gì
 
Hình 23: Xem hoá đơn từng ngày
5.	Một vài điểm cần lưu ý
5.1	Mã hoá
Ở đây, nhóm chúng em đã mã hoá password của user thành mã hoá md5 để an toàn cho người dùng
 
Hình 24: Mã hoá md5 cho người dùng
5.2	Tạo các pattern
Ở đây, nhằm tạo được tài khoản đầy đủ và hợp lệ, nhóm chúng em đã thêm các pattern 
 
Hình 25: Pattern email
Email phải có @ mới hợp lệ
 
Hình 26: Pattern Phone
Số phải có đủ 10 số mới là hợp lệ và chỉ được nhập số
5.3	Áp dụng AI vào web
 
Hình 27: Áp dụng AI bằng cách đề xuất sản phẩm
