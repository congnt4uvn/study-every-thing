# Ghi Chu Hoc AWS: AWS Certificate Manager (ACM)

## ACM la gi?
AWS Certificate Manager (ACM) la dich vu giup ban de dang cap phat, quan ly va trien khai chung chi SSL/TLS.

## Vi sao chung chi quan trong?
Chung chi SSL/TLS duoc dung de ma hoa du lieu khi truyen (in-flight encryption) cho website va API thong qua endpoint HTTPS.

## Vi du kien truc
- Nguoi dung ket noi toi Application Load Balancer (ALB) bang HTTPS.
- ALB chuyen tiep luu luong ve EC2 o backend (vi du qua HTTP trong mang noi bo).
- ACM cap phat va quan ly chung chi TLS cho domain cua ban.
- Chung chi duoc gan vao ALB de client co the truy cap HTTPS an toan.

## Tinh nang chinh cua ACM
- Ho tro ca chung chi TLS public va private.
- Chung chi TLS public mien phi.
- Tu dong gia han chung chi.
- Tich hop voi nhieu dich vu AWS, bao gom:
  - Elastic Load Balancing (ELB/ALB)
  - CloudFront
  - API Gateway

## Ghi nho nhanh
Neu ban can ma hoa du lieu khi truyen va chung chi duoc quan ly tren AWS, hay nghi den ACM.
