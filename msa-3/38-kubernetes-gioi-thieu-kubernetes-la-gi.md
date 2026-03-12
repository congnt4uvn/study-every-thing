# Kubernetes là gì? - Giới thiệu nhanh

Trong bài giảng trước, tôi đã nói với các bạn rằng chúng ta sẽ sử dụng Kubernetes như một sản phẩm điều phối container (container orchestration).

Bây giờ, trong bài giảng này, hãy để tôi cố gắng giới thiệu nhanh về Kubernetes là gì.

## Tổng quan

Như chúng ta đã biết, Kubernetes là một hệ thống mã nguồn mở để tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng được đóng gói trong container.

Đây là nền tảng điều phối (orchestration platform) nổi tiếng nhất hiện có trên thị trường.

Và một lợi thế nữa của Kubernetes là nó **trung lập với nền tảng đám mây** (cloud neutral).

Nếu bạn thiết lập cụm Kubernetes trong hệ thống local của mình hoặc trong AWS, GCP, Azure, bất kể bạn thiết lập ở đâu, các khái niệm của Kubernetes đều sẽ tương tự.

Đó là lý do tại sao chúng ta có thể gọi Kubernetes là một nền tảng trung lập với đám mây.

## Lịch sử và Nguồn gốc

Kubernetes này, như tôi đã nói, được phát triển và mã nguồn mở hóa bởi Google.

Vào khoảng năm 2015, Google đã quyết định mã nguồn mở hóa một trong những dự án nội bộ mà họ đã phát triển trong hơn 15 năm. Chỉ với các khái niệm Kubernetes này, đằng sau hậu trường, Google đã cố gắng chạy phần lớn các sản phẩm của họ như YouTube, Google Photos, Gmail.

Rất nhiều sản phẩm của Google tận dụng loại công nghệ Kubernetes này đằng sau hậu trường trong Google.

Và vì Kubernetes có rất nhiều tiềm năng, vào khoảng năm 2015, Google đã quyết định mã nguồn mở hóa nó để các tổ chức khác cũng có thể hưởng lợi từ framework này.

Tất nhiên, cái tên không phải là Kubernetes khi họ sử dụng nó trong Google. Khi họ cố gắng mã nguồn mở hóa sản phẩm nội bộ ra thế giới bên ngoài, thì họ đã đặt tên này, đó là Kubernetes.

Vì vậy, vì Kubernetes này đã giúp Google chạy các ứng dụng nội bộ của họ trong hơn 15 năm, chúng ta có thể tự tin nói rằng những sản phẩm này có thể giúp bất kỳ tổ chức nào và bất kỳ lượng traffic nào. Bởi vì không có ứng dụng nào trên thế giới nhận được nhiều traffic hơn các sản phẩm của Google.

Đó là lý do tại sao ngay lập tức, ngay khi điều này được phát hành cho mã nguồn mở, nhiều tổ chức đã áp dụng nó vào việc triển khai microservices của họ.

## Các khả năng chính

Vậy Kubernetes sẽ giúp bạn như thế nào:

- **Hệ thống phân tán**: Nó sẽ giúp bạn chạy các hệ thống phân tán một cách linh hoạt - các hệ thống phân tán như ứng dụng cloud native hoặc microservices.

- **Mở rộng tự động**: Nó có khả năng tự động mở rộng và xử lý failover cho ứng dụng của bạn.

- **Các mẫu triển khai**: Cung cấp các mẫu triển khai sẽ đảm bảo không có downtime cho ứng dụng của bạn.

### Service Discovery và Load Balancing

Ngoài những lợi thế này, Kubernetes cũng có khả năng hoạt động như một service discovery agent và cung cấp load balancing.

Khi chúng ta thảo luận về Eureka Server, tôi đã nói rằng với sự trợ giúp của Eureka Server, chúng ta đang thực hiện client side load balancing, trong khi với sự trợ giúp của Kubernetes, chúng ta có thể loại bỏ Eureka Server và chúng ta có thể giao việc load balancing cho Kubernetes.

Và với điều đó, chúng ta sẽ sử dụng **server side load balancing**.

Tôi sẽ chỉ cho bạn cách loại bỏ Eureka bất cứ khi nào chúng ta cố gắng sử dụng Kubernetes trong mạng lưới microservices trong các phần sắp tới.

### Điều phối Container và Storage

Và ngoài service discovery agent và load balancing, Kubernetes cũng có khả năng thực hiện điều phối container và storage.

Vì vậy, với sự trợ giúp của Kubernetes, chúng ta có thể kiểm soát bất kỳ số lượng container nào cùng với các yêu cầu storage của chúng.

### Các tính năng bổ sung

Và Kubernetes này cũng có khả năng:

- **Rollout và rollback tự động** - Như chúng ta đã thảo luận, nó cũng cung cấp khả năng tự phục hồi (self-healing).

- **Quản lý cấu hình** - Hơn nữa, với sự trợ giúp của Kubernetes, chúng ta cũng có thể cấu hình các properties và secrets cần thiết cho microservices của chúng ta.

## Tên gọi "Kubernetes"

Và cuối cùng, tôi muốn chia sẻ với bạn thông tin về cách tên Kubernetes được đặt cho framework này.

Từ **Kubernetes** có nguồn gốc từ tiếng Hy Lạp.

Trong tiếng Hy Lạp, ý nghĩa của Kubernetes là **người lái tàu hoặc phi công** (helmsman or pilot) người sẽ điều khiển con tàu.

Đó là lý do tại sao chúng ta có logo này cho Kubernetes.

Vì vậy, bất cứ khi nào bạn nhìn thấy logo này, xin lưu ý rằng nó liên quan đến Kubernetes, giống như cách người lái tàu kiểm soát toàn bộ con tàu về cách điều hướng. Rất giống nhau, với sự trợ giúp của Kubernetes, chúng ta có thể kiểm soát tất cả các container mà chúng ta có trong mạng lưới microservice của mình.

### So sánh với thế giới thực

Trong thế giới thực, các container sẽ được chuyên chở trong một con tàu như thế nào - trong một con tàu, tất cả các container của chúng ta sẽ được di chuyển từ nơi này sang nơi khác.

Và con tàu sẽ được kiểm soát như thế nào với sự trợ giúp của người lái tàu hoặc thuyền trưởng.

Vì vậy, với ví dụ thế giới thực đó, vì chúng ta sẽ kiểm soát các container được phát triển với sự trợ giúp của Docker hoặc bất kỳ công nghệ containerization nào khác, tên Kubernetes này đã được đặt cho dự án hoặc sản phẩm này.

### K8s - Dạng viết tắt

Đôi khi mọi người có thể gọi Kubernetes ở dạng viết tắt là **K8s**, vì vậy đây là cách viết tắt của Kubernetes.

Vậy tên viết tắt này xuất hiện như thế nào?

Nếu chúng ta cố gắng đếm số chữ cái giữa chữ cái đầu tiên **K** và chữ cái cuối cùng **S** trong từ Kubernetes, sẽ có **tám ký tự**.

Đó là lý do tại sao cái tên này xuất hiện, đó là K8s.

Vì vậy, bất cứ khi nào bạn thấy tên viết tắt trong bất kỳ blog hoặc trang web nào, xin lưu ý rằng họ đang đề cập đến sản phẩm Kubernetes.

## Tóm tắt

Tôi hy vọng bạn đã rõ ràng với phần giới thiệu nhanh về Kubernetes này.

Cảm ơn bạn và tôi sẽ gặp bạn trong bài giảng tiếp theo. Tạm biệt.