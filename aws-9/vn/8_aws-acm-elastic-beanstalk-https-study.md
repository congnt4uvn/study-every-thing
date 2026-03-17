# Ghi Chu Hoc AWS: ACM + Elastic Beanstalk + HTTPS

## Muc tieu bai hoc
Trien khai ung dung web co HTTPS bang cach:
- Tao chung chi SSL/TLS trong AWS Certificate Manager (ACM)
- Xac thuc quyen so huu domain bang Route 53 (DNS validation)
- Gan chung chi vao Application Load Balancer trong Elastic Beanstalk
- Truy cap ung dung an toan qua custom domain

## Kien truc su dung
- **ACM**: Cap va quan ly chung chi public
- **Route 53**: Quan ly DNS zone va record xac thuc/CNAME
- **Elastic Beanstalk**: Trien khai moi truong ung dung
- **Application Load Balancer (ALB)**: Xu ly HTTPS tren cong 443
- **EC2 + Auto Scaling Group**: Duoc Beanstalk tao ra

## Quy trinh tung buoc

### 1. Tao chung chi public trong ACM
1. Mo **AWS Certificate Manager**.
2. Chon **Request a public certificate**.
3. Nhap domain (vi du: `acmdemo.example.com`).
4. Chon **DNS validation**.
5. Giu key algorithm mac dinh va gui yeu cau.

### 2. Xac thuc domain trong Route 53
1. Trong ACM, tim record dang cho xac thuc.
2. Bam **Create records in Route 53**.
3. Cho den khi trang thai chung chi la **Issued**.

## 3. Tao moi truong Elastic Beanstalk co listener HTTPS
1. Tao moi **Web server environment**.
2. Dung managed platform (trong bai hoc la Node.js sample app).
3. Chon **Application Load Balancer**.
4. Them listener:
   - Port: **443**
   - Protocol: **HTTPS**
5. Chon chung chi ACM vua tao.
6. Chon TLS security policy.
7. Khoi tao moi truong.

## 4. Tro custom domain ve URL cua Beanstalk
1. Trong hosted zone cua Route 53, tao DNS record:
   - Name: `acmdemo`
   - Type: **CNAME**
   - Value: Domain cua Beanstalk (khong kem protocol)
2. Cho DNS propagate.

## 5. Kiem tra HTTPS
- Mo `https://acmdemo.example.com`.
- Kiem tra bieu tuong khoa tren trinh duyet va thong tin chung chi.
- Trong **EC2 > Load Balancers > Listeners**, xac nhan co listener HTTPS 443 va dung chung chi ACM.

## Diem can nho
- DNS validation nhanh va de khi ACM va Route 53 cung tai khoan AWS.
- TLS duoc terminate tai ALB, khong phai tren EC2.
- Co the thay doi chung chi mac dinh hoac them chung chi moi tren listener cua ALB.
- DNS propagation cham co the gay truy cap tam thoi khong on dinh.

## Loi thuong gap
- Chung chi bi **Pending validation**: thieu/sai DNS validation record.
- Domain khong phan giai: CNAME sai hoac DNS chua propagate xong.
- HTTPS chua hoat dong: chua tao listener 443 hoac chon sai chung chi.

## Don dep tai nguyen (tranh phat sinh chi phi)
Sau khi test xong:
1. Xoa Elastic Beanstalk environment/application.
2. Xoa Route 53 test records (tuy chon nhung nen lam).
3. Xoa ACM certificate khong con su dung.

## Cau hoi on tap nhanh
1. Vi sao DNS validation thuong duoc uu tien khi dung Route 53?
2. HTTPS duoc terminate o dau trong mo hinh nay?
3. Loai DNS record nao dung de tro subdomain ve URL cua Beanstalk?
4. Can xoa nhung tai nguyen nao de tranh ton chi phi?
