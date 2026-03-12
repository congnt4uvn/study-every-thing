# Làm mới cấu hình Microservices một cách động

Hiện tại, bên trong mạng lưới microservices của chúng ta, chúng ta có ba microservices khác nhau và có một config server, và chúng ta có thể đọc các thuộc tính từ config server trong quá trình khởi động các ứng dụng microservices.

Vậy là mọi thứ đang hoạt động hoàn hảo và bạn có thể nghĩ rằng đây là kết thúc của spring cloud config server và chúng ta có thể không gặp phải bất kỳ thách thức nào khác về mặt quản lý cấu hình.

Nhưng trong bài giảng này, tôi muốn giới thiệu một vấn đề mới mà chúng ta có thể gặp phải bên trong môi trường microservices về mặt quản lý cấu hình.

Hãy nghĩ như bạn đã thiết lập config server và tất cả các microservices của bạn đã khởi động bằng cách kết nối với config server, chúng đã tải các thuộc tính một cách hoàn hảo.

Đột nhiên bạn muốn thay đổi một thuộc tính cụ thể bên trong config server của bạn và bạn muốn điều tương tự được phản ánh ngay lập tức mà không cần khởi động lại các microservices của bạn.

Ở đây bạn có thể có một câu hỏi, vấn đề gì xảy ra nếu tôi khởi động lại microservices của mình. Bên trong microservice, đó không phải là một microservice mà có hàng trăm microservices và sẽ có nhiều instance cho mỗi microservice.

Vì vậy, việc khởi động lại các instances của microservices của bạn lại là một tác vụ thủ công mà ai đó phải đảm nhiệm.

Bất cứ khi nào bạn đưa một số tác vụ thủ công vào bên trong microservice, thì nó sẽ làm cho thiết lập microservices của bạn trở nên rất phức tạp.

Đó là lý do tại sao chúng ta nên tìm kiếm một tùy chọn để làm mới các thuộc tính mà không cần khởi động lại các instances microservices.

Ví dụ, hãy nghĩ như bạn có một feature flag mà bạn đã cấu hình bên trong config server. Vì vậy, dựa trên một feature flag như một cờ boolean, bạn muốn kiểm soát hành vi của logic nghiệp vụ microservice của bạn.

Khi cờ bị vô hiệu hóa, bạn muốn thực thi một đoạn mã khác.

Những cờ này bạn muốn thay đổi bất cứ lúc nào bên trong config server và bạn muốn điều tương tự được phản ánh ngay lập tức bên trong các microservices riêng lẻ của bạn mà không cần khởi động lại.

Vì vậy, đây là kịch bản phổ biến nhất mà các dự án sẽ cố gắng đạt được bên trong mạng lưới microservices của họ.

Đó là lý do tại sao trong bài giảng này, hãy cùng tập trung vào cách làm mới các cấu hình hoặc thuộc tính bên trong microservices mà không cần khởi động lại các instances.

## Bước 1: Thêm Spring Boot Actuator Dependency

Đầu tiên, chúng ta cần đảm bảo tất cả các microservices riêng lẻ của chúng ta đều có dependency spring boot actuator được định nghĩa bên trong pom.xml.

Vì vậy, nếu bạn có thể vào pom.xml của cards microservice và tìm kiếm actuator, bạn có thể thấy có spring boot starter actuator đã được thêm vào, điều tương tự chúng ta đã thêm từ lâu bên trong loans và accounts microservice.

Vì vậy, chúng ta đã có dependency actuator bên trong các instances microservices của chúng ta.

## Bước 2: Chuyển đổi Record Classes thành Normal Classes

Bước tiếp theo, chúng ta cần đi đến các lớp Dto nơi chúng ta đang cố gắng giữ tất cả các chi tiết thuộc tính của chúng ta.

Vì vậy, ở đây chúng ta có bên trong accounts microservice, có một record class với tên AccountsContactInfo chứa tất cả các thuộc tính mà microservice của tôi sẽ đọc trong quá trình khởi động từ config server.

Với thiết lập này, chúng ta có một vấn đề bất cứ khi nào chúng ta sử dụng một record class, điều đó có nghĩa là một khi đối tượng của AccountContactInfoDto này được tạo trong quá trình khởi động, chúng ta không thể thay đổi các giá trị thuộc tính tại runtime bằng cách gọi phương thức setter.

Bất cứ khi nào bạn sử dụng record class, tất cả các trường của bạn sẽ là final. Một khi đối tượng được tạo với sự trợ giúp của constructor, thì không có cách nào để thay đổi các giá trị bên trong các trường.

Đó là lý do tại sao chúng ta cần chuyển đổi AccountsContactInfo này thành một class bình thường thay vì record class.

Vì vậy, hãy để tôi loại bỏ record và đề cập đến class. Sau đó, chúng ta cần loại bỏ các cú pháp này như chúng ta không cần đề cập đến các trường bên trong các dấu ngoặc này.

Vì vậy, tôi đang loại bỏ điều đó, bây giờ bên trong class của tôi, tôi sẽ định nghĩa tất cả các trường.

Trường đầu tiên là `private String message`. Một khi tôi đã định nghĩa điều này, tôi sẽ đề cập đến dấu chấm phẩy, sau đó tôi sẽ đề cập `private Map contactDetails`, tôi sẽ đề cập đến dấu chấm phẩy ở cuối và tương tự tôi sẽ đề cập private trước trường List, đó là `onCallSupport`.

Vì vậy, bây giờ chúng ta có ba trường khác nhau bên trong class của chúng ta. Bước tiếp theo, chúng ta cần đề cập annotation `@Getter` và annotation `@Setter`.

Vì vậy, đây là các annotations từ Lombok sử dụng các annotations này. Chỉ framework spring boot của tôi mới có thể lấy các trường và đặt các trường tại runtime.

### Áp dụng cho LoansContactInfoDto

Hãy để tôi thực hiện các thay đổi tương tự bên trong LoansContactInfoDto.

Vì vậy, hãy để tôi tìm kiếm LoansContactInfoDto. Ở đây tôi sẽ loại bỏ record này và thay đổi thành class. Sau đó, tôi sẽ loại bỏ tất cả các trường này và loại bỏ các dấu ngoặc này.

Sau đó, tôi sẽ lấy các trường này từ AccountsInfoDto vì chúng ta sẽ duy trì cùng một bộ trường ở đây, điều này cũng sẽ hoạt động đúng mà không có bất kỳ vấn đề nào khi trao đổi như bạn biết, tôi cần đề cập annotation `@Getter` tiếp theo là annotation `@Setter`.

### Áp dụng cho CardsContactInfoDto

Vì vậy, hãy để tôi làm điều tương tự cho CardsContactInfoDto.

Vì vậy, trước tiên tôi sẽ đề cập đến các annotations Lombok, sau đó tôi sẽ thay đổi record này thành class, tiếp theo tôi sẽ loại bỏ tất cả các trường này cùng với các dấu ngoặc và tôi sẽ lấy tên trường từ các class khác mà chúng ta có.

Và tôi sẽ đề cập điều tương tự trong CardsContactInfoDto.

Vì vậy, chúng ta đã thực hiện những thay đổi liên quan đến Dto này trong tất cả các microservices. Vì vậy, điều này sẽ cho phép các microservices của chúng ta thay đổi các giá trị thuộc tính tại runtime.

## Bước 3: Cấu hình Actuator Endpoints

Sau khi thực hiện những thay đổi này, tôi cần vào application.yml của Accounts Microservice.

Bên trong application.yml này, chúng ta cần bật các đường dẫn API actuator. Theo mặc định, actuator sẽ không expose tất cả các đường dẫn API liên quan đến quản lý.

Đó là lý do tại sao chúng ta cần bật chúng một cách cụ thể bằng cách giới thiệu một thuộc tính ở đây.

Vì vậy, thuộc tính mà tôi muốn đề cập ở đây là `management` vì chúng ta muốn bật các API liên quan đến quản lý.

Vì vậy, chúng ta cần đề cập `management` này ở vị trí gốc. Và tại management này, tôi cần đề cập `endpoints`, trong endpoints này chúng ta cần đề cập `web`, sau web này chúng ta cần đề cập `exposure`.

Sau exposure, chúng ta cần đề cập `include`. Một khi chúng ta định nghĩa phần tử include này bên trong thuộc tính của bạn, chúng ta cần bật actuator endpoint sẽ cho phép làm mới các thuộc tính tại runtime.

Ở đây thay vì chỉ đề cập refresh API, thay vào đó chúng ta có thể đề cập giá trị asterisk (*). Với giá trị asterisk này, tôi đang nói với spring boot actuator của mình để bật và expose tất cả các management endpoint được hỗ trợ bởi spring boot actuator.

Và bên trong các endpoints này, chúng ta cũng sẽ có endpoint liên quan đến refresh.

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

### Áp dụng cho Cards và Loans Microservices

Bây giờ chúng ta cần thực hiện bộ thay đổi tương tự bên trong loans và cards microservice.

Vì vậy, hãy để tôi vào application.yml của cards microservice. Trong cards microservice này, chúng ta cần mở application.yml. Bên trong application.yml, tôi sẽ giới thiệu cùng một thuộc tính.

Hãy để tôi làm điều tương tự cho loans microservice. Bên trong application.yml, tôi sẽ đề cập cùng một thuộc tính.

## Demo: Thay đổi thuộc tính tại Runtime

Với điều này, chúng ta đã thực hiện tất cả các thay đổi liên quan bên trong microservices của chúng ta. Bước tiếp theo, hãy cùng thử khởi động tất cả các microservices của chúng ta, sau đó chúng ta có thể thử thay đổi một thuộc tính runtime bên trong GitHub repo và xem liệu theo mặc định nó có phản ánh bên trong các microservices riêng lẻ của chúng ta không.

Vì vậy, đầu tiên hãy để tôi thực hiện build. Một khi build hoàn thành, tôi sẽ dừng tất cả các ứng dụng của mình. Sau khi tất cả các ứng dụng của tôi dừng lại, đầu tiên tôi sẽ khởi động ứng dụng config server của mình.

Một khi config server của tôi khởi động thành công, tôi sẽ khởi động AccountsApplication, tiếp theo là CardsApplication. Sau CardsApplication, tôi cũng sẽ khởi động LoansApplication.

Bây giờ tất cả các instances microservices và config servers của tôi đã khởi động thành công.

### Thay đổi Properties trong GitHub Repo

Bước tiếp theo, tôi sẽ thử thay đổi các giá trị thuộc tính bên trong GitHub repo.

Hiện tại bạn có thể thấy đối với accounts-prod.yml, chúng ta có message nói rằng: "hello, welcome to EazyBank accounts related prod APIs". Ở đây trong message này, tôi sẽ thay thế "prod" này bằng "production", nhưng trước khi tôi thử thay thế, trước tiên hãy để tôi chỉ cho bạn ngay bây giờ accounts microservice hoặc microservice khác của chúng ta sẽ có message với giá trị prod.

Vì vậy, ở đây tôi đang thử gọi API contact-info cho accounts microservice. Bạn có thể thấy có prod APIs ở đây.

Tương tự, nếu tôi vào cards và gọi contact-info này, ở đây chúng ta cũng đang nhận được prod APIs và điều tương tự tôi có thể xác nhận cho loans.

Vì vậy, đối với loans, tôi cũng chỉ đang thử gọi contact-info này sẽ có prod APIs này bên trong message.

Bây giờ hãy để tôi vào GitHub repo, ở đây tôi sẽ nhấp vào nút edit này và thay thế prod này bằng production.

Vì vậy, tôi sẽ làm điều tương tự cho các microservices khác. Trước đó, hãy để tôi commit file này trực tiếp vào GitHub repo.

Một khi tôi hoàn thành với file accounts này, tôi sẽ mở file liên quan đến cards. Vì vậy, cards-prod là file mà chúng ta cần thay đổi ở đây.

Vì vậy, hãy để tôi nhấp vào nút edit này và thay thế prod này bằng production. Commit các thay đổi vào GitHub repo, sau đó tôi sẽ mở loans-prod.yml.

Và ở đây tôi cũng sẽ nhấp vào nút edit này, thay thế prod này bằng production và commit các thay đổi vào GitHub repo.

### Kiểm tra Config Server

Bây giờ trước tiên tôi sẽ cho thấy hành vi của config server. Ở đây tôi đang thử gọi API account/prod có sẵn bên trong config server.

Bạn có thể thấy config server của tôi có giá trị thuộc tính mới nhất là production. Điều này xác nhận bất cứ khi nào một microservice instance đang cố gắng gọi đường dẫn API này trong quá trình khởi động, config server của tôi sẽ không dựa vào cache cục bộ.

Nó luôn luôn sẽ kiểm tra với bản sao chính có sẵn bên trong GitHub repo và nó sẽ trả về cùng các giá trị mới nhất cho accounts microservice.

Điều tương tự tôi có thể xác nhận cho loans. Đối với loans, chúng ta cũng có production này, tương tự cho cards chúng ta có thể xác nhận. Vì vậy, đối với cards, nó cũng hoạt động tốt.

Điều này có nghĩa là không có vấn đề gì trong việc làm mới các thuộc tính trên config server.

### Vấn đề với Microservices

Bây giờ vấn đề duy nhất là các microservices của chúng ta phải có khả năng đọc các giá trị mới nhất này và chúng ta đã biết rằng microservices sẽ chỉ kết nối với config server trong quá trình khởi động của ứng dụng.

Bây giờ, để phản ánh các thuộc tính mới nhất này, chúng ta cần khởi động lại các instances microservices và chúng ta đang cố gắng tránh quy trình đó vì chúng ta cần tránh khởi động lại các ứng dụng microservices của chúng ta vì nó sẽ ảnh hưởng đến lưu lượng truy cập và vì nó liên quan đến quy trình thủ công.

### Giải pháp: Actuator Refresh API

Vậy làm thế nào để vượt qua thách thức này?

Như tôi đã nói, actuator sẽ expose một API với tên refresh. Nếu bạn vào accounts actuator như `localhost:8080/actuator` đối với actuator này, bạn sẽ có rất nhiều API được expose.

Và ở đây chỉ cần tìm kiếm refresh. Vì vậy, đây là đường dẫn. Nếu tôi thử gọi điều này, nó nói rằng method not allowed vì từ trình duyệt, luôn luôn phương thức http get sẽ được gọi.

Nhưng refresh API này chỉ hỗ trợ phương thức post. Đó là lý do tại sao chúng ta cần vào postman để gọi refresh API này.

Trước đó, hãy để tôi gọi tất cả contact info một lần nữa bên trong microservices của tôi để đảm bảo các thuộc tính chưa được phản ánh hiện tại bên trong microservices.

Vì vậy, đối với loans, bạn có thể thấy cùng một prod cũ vẫn ở đó. Tương tự đối với accounts, cùng một cái cũ vẫn ở đó. Và bây giờ đối với cards, tôi đang thử gọi cho điều này, cũng có cùng một giá trị prod cũ ở đây.

### Gọi Refresh Endpoint

Bước tiếp theo, chúng ta cần gọi URL actuator refresh. Đối với điều tương tự bên trong thư mục accounts, bạn có thể thấy có một request với tên refresh config.

Vì vậy, hãy để tôi nhấp vào điều này. Bạn có thể thấy đây là URL mà chúng ta cần gọi vì chúng ta đang cố gắng làm mới config của accounts microservice, chúng ta cần sử dụng URL endpoint của accounts microservice instance như `localhost:8080/actuator/refresh`.

Theo mặc định, URL này không bao giờ được expose bên trong microservices của bạn. Vì chúng ta đã đề cập đến cấu hình này bên trong tất cả các microservices, tất cả các management endpoints đang được expose.

Nếu bạn chỉ muốn expose refresh, bạn cần đề cập refresh ở đây, nhưng tôi muốn sử dụng Asterisk vì trong các phần sắp tới, chúng ta cần bật nhiều management endpoints khác.

Tôi hy vọng bạn hiểu rõ. Bây giờ tôi đang thử gọi API này. Không cần gửi bất kỳ dữ liệu request nào bên trong body. Nó có thể để trống, nhưng vui lòng đảm bảo phương thức Http là post.

Tôi đang thử nhấp vào nút send. Bạn sẽ nhận được phản hồi từ refresh API của bạn nói rằng thuộc tính accounts.message đã được thay đổi và điều tương tự hiện tại đang được làm mới đằng sau hậu trường.

Ngoài accounts.message, chúng ta cũng nhận được thêm một thuộc tính nữa là config.client.version. Vì vậy, bạn sẽ luôn nhận được thuộc tính này bất cứ khi nào bạn thay đổi điều gì đó trên GitHub repo vì bất cứ khi nào có thay đổi xảy ra, config server của bạn sẽ thay đổi số version đằng sau hậu trường và điều tương tự nó đang cố gắng gửi đến các ứng dụng config client như accounts microservice.

Chúng ta chỉ cần lo lắng về message này vì đây là message sẽ ảnh hưởng đến logic nghiệp vụ của chúng ta.

### Xác nhận Thay đổi

Vì vậy, bây giờ chúng ta đã làm mới nó. Tôi sẽ vào contact-info của accounts microservice. Vì vậy, đây là contact info của accounts microservice. Tôi đã không khởi động lại accounts microservice của mình.

Bạn đã sẵn sàng để xem điều kỳ diệu chưa? Hiện tại bạn có thể thấy giá trị ở đây là prod. Ngay khi tôi nhấp vào nút send, nó được thay đổi thành production API.

Điều đó có nghĩa là chúng ta có thể thay đổi giá trị thuộc tính runtime mà không cần khởi động lại accounts microservice của chúng ta.

### Áp dụng cho Loans và Cards

Bây giờ hoạt động tương tự tôi phải làm cho loans và cards.

Bây giờ nếu bạn vào và kiểm tra loans microservice, bạn có thể thấy nó vẫn đang tham chiếu đến prod vì chúng ta chưa gọi refresh API có sẵn đối với loans microservice.

Vì vậy, đối với điều tương tự, hãy vào thư mục loans và nhấp vào refresh config này, sau đó bạn có thể nhấp vào nút send. Bạn sẽ nhận được message nói rằng loans.message đã được thay đổi đằng sau hậu trường.

Bây giờ nếu bạn vào contact-info và thử gọi lần này, bạn sẽ nhận được production APIs.

Hãy để tôi làm điều tương tự cho cards. Đối với điều tương tự, trước tiên, tôi cần gọi refresh config này có mặt trong cards.

Một khi tôi nhận được phản hồi này, tôi có thể vào contact-info của cards và ở đây tôi đang thử nhấp vào nút send này. Bạn có thể thấy tôi đang nhận được production làm output.

## Tóm tắt các bước

Tôi hy vọng bạn đã hiểu rõ cách chúng ta có thể làm mới các giá trị thuộc tính runtime của chúng ta với sự trợ giúp của actuator refresh endpoint.

Hãy cùng thử xem lại các bước mà chúng ta đã làm theo một cách rất nhanh chóng ở đây. Tôi đã đề cập đến tất cả các bước mà chúng ta đã làm theo bên trong slide này để nó sẽ đóng vai trò là tài liệu tham khảo cho bạn.

### Các bước cần tuân theo:

1. **Thêm Spring Boot Actuator Dependency** vào pom.xml
2. **Cấu hình Actuator** để expose refresh endpoint bằng cách thêm thuộc tính:
   ```yaml
   management.endpoints.web.exposure.include=refresh
   ```
   Hoặc bạn cũng có thể đề cập giá trị asterisk (*)
3. **Gọi Actuator Refresh Endpoint** bất cứ khi nào bạn muốn làm mới các thuộc tính của bạn bên trong accounts microservices hoặc bất kỳ microservices nào khác mà không cần khởi động lại, bạn chỉ cần gọi đường dẫn actuator, đó là `actuator/refresh` đối với microservices instance của bạn

### Quy trình làm mới cấu hình:

Vì vậy, hãy cùng thử hình dung điều này. Bạn có thể thấy ở đây trong bước đầu tiên, chúng ta sẽ push dữ liệu cấu hình mới vào config repo, sau đó chúng ta sẽ gọi `actuator/refresh` bằng phương thức Http post.

Vì vậy, tôi đang cố gắng đưa ra demo bằng cách sử dụng account microservice ở đây. Vì vậy, bây giờ account microservice của tôi đằng sau hậu trường sẽ yêu cầu configuration server cung cấp các giá trị thuộc tính đã được thay đổi so với phiên bản trước.

Vì vậy, config server của tôi sẽ đi và cố gắng pull tất cả các thay đổi mới nhất từ GitHub repo trong bước bốn và điều tương tự nó sẽ cố gắng gửi lại cho accounts microservice bằng cách tuân theo bước năm và bước sáu.

Và cuối cùng, vì account microservice của tôi sẽ nhận được các chi tiết thuộc tính đã được thay đổi, nó sẽ đọc chúng từ config server bên trong bước bảy bằng cách reload tất cả các cấu hình mới vào microservices mà không cần khởi động lại ứng dụng.

## Hạn chế của phương pháp này

Vì vậy, điều này là siêu, siêu hoàn hảo. Nhưng có một nhược điểm nghiêm trọng mà chúng ta có bên trong phương pháp này.

Nhược điểm là hãy nghĩ như bạn có 100 microservices và mỗi trong số chúng có năm instances khác nhau, điều đó có nghĩa là sẽ có tổng cộng 500 instances microservices đang chạy bên trong production của bạn.

Và vì lý do nào đó, bạn đang cố gắng thay đổi thuộc tính trong tất cả các microservices. Sau đó, bạn cần gọi refresh endpoint đối với tất cả 500 instances đang chạy bên trong production của bạn.

Và việc thực hiện điều này thủ công sẽ là một quy trình cực kỳ, cực kỳ cồng kềnh.

Một số operations team hoặc một số platform team sẽ cố gắng tự động hóa quy trình này bằng cách viết một số scripts bên trong CI/CD pipelines hoặc họ sẽ cố gắng viết Jenkins jobs hoặc CI/CD jobs, sẽ gọi tất cả các microservices instances refresh endpoints.

Nhưng vẫn vậy, nó có thể không phải là một giải pháp thuận tiện cho nhiều dự án.

## Kết luận

Đó là lý do tại sao hãy cùng khám phá điều này thêm nữa và cố gắng xác định liệu có bất kỳ tùy chọn tốt hơn nào mà chúng ta có để làm mới các thuộc tính một cách động mà không cần gọi refresh endpoint này cho từng instance microservice hay không.

Tôi hy vọng bạn đã hiểu rõ. Cảm ơn bạn và tôi sẽ gặp bạn trong bài giảng tiếp theo. Tạm biệt.