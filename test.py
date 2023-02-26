from src.modules.customers.handlers.add_customers import AddCustomerHandler
from src.modules.customers.services import CustomerService
customer_service = CustomerService()
AddCustomerHandler(customer_service).post(data={"name": "Thai123", "phone": "  988501897  "})

# tư duy từ trên xuống
# 1.viết api gì làm gì, ví dụ viết api để tạo employee
# 2. từ đó viết Handler gì, Handler sau này sẽ có tác dụng route với endpoint api đó, khi request gọi tới api đó, flask
# sẽ gọi hàm của class handler đó
# 3. Viết DTO để validate gì
# 4. viết service xử lý các nghiệp vụ với data được truyền xuống, chú ý viết để reuse được -> tách nhỏ từng bước thành
# từng hàm (practice nhiều sẽ quen hơn)
# 5. có thể viết đồng thời cả hàm repositories mới nếu cần thiết các query cụ thể
# 6. k cần phải nghĩ hết ở trên rồi mới xuống dưới, vừa viết vừa thêm đồng thời các layer được nhg điểm bắt đầu thì là
# từ trên cùng.