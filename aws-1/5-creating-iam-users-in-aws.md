# Tạo IAM Users trong AWS

## Giới thiệu

Trong hướng dẫn này, chúng ta sẽ thực hành sử dụng dịch vụ IAM (Identity and Access Management) để tạo người dùng trong AWS. Đây là kỹ năng cơ bản để quản lý tài khoản AWS một cách an toàn.

## Truy cập IAM Console

Để bắt đầu:
1. Gõ "IAM" vào thanh tìm kiếm của AWS
2. Điều hướng đến IAM console

Khi đến IAM Dashboard, bạn sẽ thấy một số khuyến nghị về bảo mật mà chúng ta có thể bỏ qua tạm thời.

## Hiểu về IAM như một Global Service

Một điều quan trọng cần chú ý: nếu bạn nhìn vào góc trên bên phải và nhấp vào "Global", bạn sẽ thấy rằng tùy chọn chọn region không hoạt động. Điều này có nghĩa là **IAM là một dịch vụ toàn cầu (global service)** - không có region nào được chọn.

Khi bạn tạo một user trong IAM, nó sẽ có sẵn ở mọi nơi. Tuy nhiên, một số console AWS khác được đề cập trong khóa học này sẽ dành riêng cho từng region cụ thể.

## Tại sao phải tạo IAM Users?

Hiện tại, khi bạn lần đầu đăng nhập vào AWS, bạn đang sử dụng cái gọi là **root user**. Bạn có thể xác định điều này bằng cách nhấp vào góc trên bên phải - bạn sẽ chỉ thấy account ID.

**Quan trọng:** Việc sử dụng root account cho các hoạt động hàng ngày không phải là best practice. Do đó, chúng ta muốn tạo các user như admin users để có thể sử dụng tài khoản của mình một cách an toàn hơn.

## Tạo IAM User đầu tiên

### Bước 1: Bắt đầu tạo User

1. Điều hướng đến "Users" ở thanh bên trái
2. Nhấp "Create user"
3. Cung cấp username (ví dụ: "Stephane")

### Bước 2: Cấu hình truy cập Console

Khi thiết lập quyền truy cập console, bạn có hai tùy chọn:
- **Identity Center** (được AWS khuyến nghị)
- **Create an IAM user** (đơn giản hơn và là điều bạn cần biết cho kỳ thi)

Trong hướng dẫn này, chúng ta sẽ chọn tùy chọn thứ hai: tạo IAM user.

### Bước 3: Cấu hình Password

Bạn có hai tùy chọn về mật khẩu:

**Đối với người dùng khác:**
- Để là auto-generated password
- Yêu cầu thay đổi mật khẩu khi đăng nhập lần đầu

**Đối với chính bạn:**
- Nhập custom password
- Có thể bỏ chọn "User must create a new password at next sign-in"

### Bước 4: Thêm Permissions

Thay vì thêm permissions trực tiếp, hãy sử dụng groups (best practice):

1. Nhấp "Create a group"
2. Đặt tên group là "admin"
3. Gắn policy "AdministratorAccess"
4. Thêm user vào admin group

### Bước 5: Thêm Tags (Tùy chọn)

Tags là metadata tùy chọn có thể được thêm vào các tài nguyên AWS. Ví dụ:
- Key: `department`
- Value: `engineering`

Mặc dù chúng ta sẽ không thêm tags ở mọi nơi trong khóa học này, nhưng biết cách chúng hoạt động là điều tốt.

### Bước 6: Review và Create

Xem lại tất cả các cài đặt:
- Username
- Permissions (thông qua group membership)
- Tags

Sau đó nhấp "Create user" để hoàn tất quá trình.

## Hiểu về IAM Groups và Permissions

Sau khi tạo user, hãy xem cách permissions hoạt động:

### User Groups
1. Điều hướng đến "User groups" ở thanh bên trái
2. Bạn sẽ thấy group "admin" mà chúng ta đã tạo
3. Group hiển thị:
   - Một user (Stephane)
   - Policy AdministratorAccess được gắn vào group

### User Permissions
Khi bạn xem permission policies của user, bạn sẽ thấy:
- AdministratorAccess có mặt
- Nhưng nó **không được gắn trực tiếp**
- Nó được gắn **thông qua group "admin"**

Điều này có nghĩa là user kế thừa permissions từ admin group mà họ thuộc về. **Đây là lý do tại sao chúng ta đặt users vào groups** - việc quản lý permissions theo cách này đơn giản hơn nhiều.

## Tùy chỉnh Sign-in URL

Để việc đăng nhập dễ dàng hơn:

1. Quay lại IAM Dashboard
2. Nhìn vào phần AWS account của bạn
3. Bạn sẽ thấy Account ID và Sign-in URL
4. Nhấp "Create alias" để tùy chỉnh URL
5. Nhập một alias (ví dụ: "aws-stephane-v5") - nó phải là duy nhất
6. Điều này đơn giản hóa sign-in URL của bạn

## Đăng nhập với IAM User

### Sử dụng hai cửa sổ trình duyệt (Khuyến nghị)

Để quản lý đồng thời cả root và IAM user accounts:

1. Giữ cửa sổ trình duyệt hiện tại với root user
2. Mở một **cửa sổ private/incognito** trong trình duyệt của bạn
   - Chrome, Firefox và Safari đều có tính năng này
3. Dán sign-in URL vào cửa sổ private

**Lợi ích của cách tiếp cận này:**
- Bạn có thể có hai cửa sổ đặt cạnh nhau
- Root account ở bên trái (cửa sổ thông thường)
- IAM user ở bên phải (cửa sổ private)
- Cả hai đều duy trì trạng thái đăng nhập đồng thời

### Quy trình đăng nhập

1. Đến trang đăng nhập AWS
2. Chọn "IAM user" (không phải root user)
3. Nhập một trong hai:
   - Account ID, hoặc
   - Account alias (cái bạn đã tạo)
4. Nhập IAM username của bạn (ví dụ: "Stephane")
5. Nhập password của bạn
6. Nhấp "Sign in"

### Xác minh đăng nhập

Sau khi đăng nhập, nhìn vào góc trên bên phải:
- **Cửa sổ IAM user:** Hiển thị account ID và IAM username
- **Cửa sổ Root user:** Chỉ hiển thị account ID

## Lời nhắc quan trọng về bảo mật

⚠️ **Quan trọng:** Hãy chắc chắn không làm mất thông tin đăng nhập root account và admin login của bạn. Nếu không, bạn sẽ gặp rắc rối lớn với tài khoản của mình và sẽ phải liên hệ với bộ phận hỗ trợ của AWS.

### Best Practices cho khóa học này

- **Khuyến nghị:** Sử dụng IAM user cho các hoạt động hàng ngày (không phải root user)
- Đôi khi trong khóa học, bạn có thể thấy cả root và IAM user đều được sử dụng
- Khi bạn cần sử dụng cụ thể root hoặc IAM user, nó sẽ được chỉ ra rõ ràng
- Đừng lo lắng - bạn sẽ được hướng dẫn trong suốt khóa học

## Các bước tiếp theo

Trong phần còn lại của section này, vui lòng giữ hai cửa sổ này mở (root và IAM user) vì chúng ta sẽ sử dụng chúng trong các bài giảng sắp tới.

---

**Tóm tắt:** Bây giờ bạn đã học được cách:
- Truy cập IAM console
- Hiểu IAM như một global service
- Tạo IAM users với permissions phù hợp
- Sử dụng groups để quản lý permissions hiệu quả
- Tùy chỉnh sign-in URL của bạn
- Đăng nhập với IAM user trong khi vẫn duy trì quyền truy cập root