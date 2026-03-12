# Hướng Dẫn Thực Hành IAM Policies

## Tổng Quan

Hướng dẫn thực hành này sẽ minh họa cách hoạt động của IAM policies bằng cách quản lý quyền hạn cho người dùng tên Stephane. Chúng ta sẽ khám phá cách thêm và xóa quyền, hiểu về kế thừa policy, và tạo các policy tùy chỉnh.

## Thiết Lập Người Dùng Ban Đầu

### Kiểm Tra Quyền Của Người Dùng

Hãy bắt đầu bằng cách xem xét IAM policies chi tiết. Trước tiên, điều hướng đến phần IAM users.

**Trạng thái hiện tại:**
- Người dùng "Stephane" thuộc nhóm admin
- Có quyền administrator access đối với AWS
- Có thể thực hiện bất kỳ hành động nào trong AWS console

**Xác minh:**
1. Đăng nhập bằng user Stephane
2. Truy cập IAM console
3. Nhấp vào "Users" ở menu bên trái
4. Bạn có thể thấy user Stephane hiển thị

Vì Stephane có quyền administrator thông qua nhóm admin, nó có thể xem và quản lý tất cả người dùng.

## Xóa Quyền Của Người Dùng

### Xóa Khỏi Nhóm Admin

Để minh họa cách hoạt động của quyền, hãy xóa Stephane khỏi nhóm admin:

**Các bước:**
1. Điều hướng đến nhóm admin
2. Xóa user Stephane khỏi nhóm này
3. Hành động này sẽ thu hồi ngay lập tức tất cả các quyền liên quan

### Xác Minh Mất Quyền

Sau khi xóa user, làm mới trang IAM users:

**Kết quả:**
- Hiển thị zero users (không có user nào)
- Xuất hiện lỗi "Access Denied" (Truy cập bị từ chối)
- Thông báo lỗi: "You don't have permission to do iamListUsers"

**Điều gì đã xảy ra:**
Bằng cách xóa Stephane khỏi nhóm admin, chúng ta đã mất quyền xem users. Điều này chứng minh rằng việc tham gia nhóm trực tiếp kiểm soát quyền truy cập.

## Khôi Phục Quyền Hạn Chế

### Thêm Quyền Read-Only

Hãy khắc phục điều này bằng cách thêm quyền hạn chế:

**Các bước:**
1. Điều hướng đến IAM
2. Vào "Users" và tìm Stephane
3. Lưu ý: Hiện tại có zero permission policies (không có policy nào)
4. Nhấp "Add permissions"
5. Chọn "Attach policies directly" (không thêm vào nhóm)
6. Chọn policy `IAMReadOnlyAccess`
7. Thêm permission này

### Kiểm Tra Quyền Read-Only

Sau khi thêm IAMReadOnlyAccess policy:

**Những gì bạn có thể làm:**
- Làm mới trang users - bây giờ nó hoạt động!
- Xem user Stephane
- Xem các user groups (như "admin")

**Những gì bạn không thể làm:**
- Thử tạo một nhóm mới có tên "developers"
- Bạn sẽ nhận được lỗi: không thể tạo groups
- Lý do: IAMReadOnlyAccess chỉ cung cấp quyền đọc

**Nguyên tắc quan trọng:**
Người dùng chỉ nên có quyền cho những gì họ cần làm (nguyên tắc đặc quyền tối thiểu - principle of least privilege).

## Tạo Nhiều Nguồn Quyền

### Tạo Nhóm Developer

Hãy tạo một nhóm mới để minh họa nhiều nguồn permission:

**Các bước:**
1. Vào "User Groups" ở menu bên trái
2. Tạo nhóm có tên "developers"
3. Thêm user Stephane vào nhóm này
4. Đính kèm bất kỳ policy nào (ví dụ: "AlexaForBusiness" - policy cụ thể không quan trọng cho demo này)
5. Tạo nhóm

### Thêm Lại Vào Nhóm Admin

Bây giờ hãy thêm Stephane trở lại nhóm admin:

**Các bước:**
1. Điều hướng đến nhóm admin
2. Nhấp "Add users"
3. Thêm lại Stephane vào nhóm này

### Kiểm Tra Nhiều Quyền

Điều hướng trở lại user Stephane để xem tất cả quyền:

**Các Permission Policies hiện tại (tổng cộng 3):**

1. **AdministratorAccess**
   - Nguồn: Kế thừa từ nhóm "admin"
   - Mức độ truy cập: Quyền administrator đầy đủ

2. **AlexaForBusiness** (managed policy)
   - Nguồn: Kế thừa từ nhóm "developers"
   - Mức độ truy cập: Đặc thù cho Alexa for Business

3. **IAMReadOnlyAccess**
   - Nguồn: Đính kèm trực tiếp vào user
   - Mức độ truy cập: Quyền read-only đối với IAM

**Bài học quan trọng:**
Người dùng kế thừa các quyền khác nhau dựa trên cách chúng được đính kèm:
- Thông qua tư cách thành viên nhóm
- Thông qua đính kèm policy trực tiếp

## Hiểu Cấu Trúc Policy

### Kiểm Tra AdministratorAccess Policy

Điều hướng đến "Policies" ở menu bên trái và chọn `AdministratorAccess`:

**Xem tóm tắt:**
- Cho phép tất cả các dịch vụ trong AWS (số lượng có thể thay đổi theo thời gian)
- Các dịch vụ bao gồm: App Mesh, Alexa for Business, Amplify, v.v.
- Tất cả các dịch vụ đều có "Full access"

**Cấu trúc JSON:**

Nhấp vào tab "JSON" để xem policy thô:

```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```

**Giải thích:**
- `*` (dấu sao) trong AWS có nghĩa là "bất cứ thứ gì"
- `Action: "*"` = Cho phép mọi hành động
- `Resource: "*"` = Trên mọi tài nguyên
- Kết quả: Quyền truy cập administrator đầy đủ

### Kiểm Tra IAMReadOnlyAccess Policy

Hãy xem một ví dụ policy khác:

**Xem tóm tắt:**
- IAM được ủy quyền với "Full: List" và "Limited: Read"
- Bạn có thể mở rộng để xem tất cả các API calls được cho phép

**Cấu trúc JSON:**

```json
{
  "Effect": "Allow",
  "Action": [
    "iam:GenerateCredentialReport",
    "iam:GenerateServiceLastAccessedDetails",
    "iam:Get*",
    "iam:List*"
  ],
  "Resource": "*"
}
```

**Hiểu về Wildcards:**
- `Get*` có nghĩa là bất cứ thứ gì bắt đầu với "Get" theo sau bởi bất kỳ ký tự nào
  - Ví dụ: GetUsers, GetGroups
- `List*` có nghĩa là bất cứ thứ gì bắt đầu với "List" theo sau bởi bất kỳ ký tự nào
  - Ví dụ: ListUsers, ListGroups
- Sử dụng wildcards (`*`) nhóm nhiều API calls liên quan lại với nhau

Policy được cho phép trên `Resource: "*"`, có nghĩa là tất cả các tài nguyên.

## Tạo Policy Tùy Chỉnh

### Sử Dụng Visual Editor

AWS cung cấp hai phương pháp để tạo policies:

1. **Visual Editor** - Giao diện thân thiện với người dùng
2. **JSON Editor** - Chỉnh sửa JSON trực tiếp

**Tạo Policy với Visual Editor:**

**Các bước:**
1. Nhấp "Create policy"
2. Chọn giữa Visual Editor hoặc JSON
3. Chọn Visual Editor
4. Chọn service: IAM
5. Chọn actions:
   - Chọn "ListUsers" (1 trong 38 list actions)
   - Chọn "GetUser" (1 trong 32 read actions)
6. Xác định resources:
   - Tất cả resources, hoặc
   - Resources cụ thể
7. Nhấp "Next"
8. Đặt tên policy: "MyIAMPermissions"
9. Tạo policy

**Xem JSON Được Tạo:**

Sau khi tạo, xem policy để thấy JSON được tạo ra:

```json
{
  "Effect": "Allow",
  "Action": [
    "iam:ListUsers",
    "iam:GetUser"
  ],
  "Resource": "*"
}
```

Visual editor tự động tạo JSON dựa trên các lựa chọn của bạn.

**Sử dụng Policy:**
Policy này bây giờ có thể được đính kèm vào các groups hoặc users khi cần.

## Quản Lý Permissions trong AWS

Quy trình được minh họa cho thấy cách quản lý permissions trong AWS:

1. Tạo policies (có sẵn hoặc tùy chỉnh)
2. Đính kèm policies vào groups
3. Thêm users vào groups
4. Đính kèm policies trực tiếp vào users
5. Users kế thừa permissions từ tất cả các nguồn

## Dọn Dẹp và Xác Minh Cuối Cùng

### Xóa Các Tài Nguyên Không Cần Thiết

Để dọn dẹp môi trường demo:

**Các bước:**
1. Điều hướng đến "User Groups"
2. Xóa nhóm "developers" (không còn cần thiết)
3. Vào user Stephane
4. Xóa policy `IAMReadOnlyAccess` được đính kèm trực tiếp

**Trạng thái cuối cùng:**
- Stephane chỉ thuộc nhóm "admin"
- Có quyền administrator thông qua tư cách thành viên nhóm

### Xác Minh Chức Năng

Quay lại IAM console:

1. Điều hướng đến "Users"
2. Xác nhận tất cả users đều hiển thị
3. Mọi thứ hiển thị chính xác

**Kết luận:**
Hệ thống đang hoạt động chính xác với permissions được đơn giản hóa.

## Những Điểm Chính Cần Nhớ

### Các Khái Niệm Quan Trọng

1. **Permissions Dựa Trên Nhóm**: Đính kèm policies vào groups ảnh hưởng đến tất cả thành viên nhóm
2. **Đính Kèm Policy Trực Tiếp**: Policies có thể được đính kèm trực tiếp vào users
3. **Kế Thừa Permission**: Users có thể có permissions từ nhiều nguồn
4. **Read-Only vs. Full Access**: Các policies khác nhau cung cấp các mức độ truy cập khác nhau
5. **Cấu Trúc Policy**: Định dạng JSON với Effect, Action, và Resource
6. **Wildcards**: Sử dụng `*` để đại diện cho "bất kỳ" trong AWS policies
7. **Visual vs. JSON Editing**: Nhiều cách để tạo policies
8. **Least Privilege**: Chỉ cấp quyền cần thiết

### Thực Hành Tốt Nhất

- Sử dụng groups để quản lý permissions của nhiều users
- Áp dụng nguyên tắc đặc quyền tối thiểu
- Hiểu về kế thừa policy từ nhiều nguồn
- Sử dụng read-only policies khi không cần quyền ghi
- Tận dụng visual editor để tạo policy dễ dàng hơn
- Xem xét và dọn dẹp các policies và groups không cần thiết thường xuyên

## Kết Luận

Bản minh họa thực hành này đã cho thấy cách IAM policies hoạt động trong thực tế. Bạn đã học cách:
- Thêm và xóa quyền của người dùng
- Hiểu về kế thừa policy
- Kiểm tra các policies có sẵn
- Tạo policies tùy chỉnh
- Quản lý permissions thông qua groups và đính kèm trực tiếp

Hiểu các khái niệm này là điều cần thiết để quản lý đúng cách quyền truy cập và bảo mật trong AWS.

---

**Vậy là xong cho bài giảng này. Tôi hy vọng bạn thích nó, và tôi sẽ gặp bạn trong bài giảng tiếp theo!**