# Nen tang ma hoa AWS

## Tong quan
Tai lieu nay tom tat 3 mo hinh ma hoa pho bien trong he thong cloud va dich vu AWS:
- Ma hoa khi truyen du lieu (in transit)
- Ma hoa phia may chu khi luu tru (server-side at rest)
- Ma hoa phia may khach (client-side)

---

## 1) Ma hoa khi truyen du lieu (TLS/SSL)

### Khai niem
Du lieu duoc ma hoa truoc khi gui qua mang va giai ma sau khi den noi nhan.

### Y chinh
- TLS la phien ban moi hon cua SSL.
- HTTPS cho biet ket noi duoc bao ve bang chung chi TLS.
- Bao ve du lieu tren duong truyen giua client va server.

### Tai sao quan trong
- Giam rui ro tan cong man-in-the-middle tren mang cong cong hoac mang chia se.
- Cac nut trung gian co the chuyen goi tin nhung khong doc duoc noi dung da ma hoa.

### Vi du
1. Nguoi dung nhap username va password tren client.
2. Client ma hoa du lieu bang TLS.
3. Du lieu da ma hoa di qua mang.
4. Chi server dich moi giai ma duoc.

---

## 2) Ma hoa phia may chu khi luu tru (Server-Side Encryption At Rest)

### Khai niem
Dich vu ma hoa du lieu sau khi nhan, luu duoi dang da ma hoa, va giai ma truoc khi tra ve client.

### Y chinh
- Du lieu luu tru o trang thai da ma hoa.
- Quy trinh ma hoa/giai ma do dich vu xu ly.
- Dich vu can quan ly va truy cap khoa ma hoa (thuong la data key).

### Vi du tren AWS (Amazon S3)
1. Client tai object len (thuong qua HTTPS).
2. S3 nhan du lieu va ma hoa de luu tru.
3. Object trong kho o dang da ma hoa.
4. Khi tai xuong, S3 giai ma va tra lai du lieu ro cho client (thuong qua HTTPS).

---

## 3) Ma hoa phia may khach (Client-Side Encryption)

### Khai niem
Client tu ma hoa truoc khi upload va tu giai ma sau khi download. Server khong thay duoc plaintext.

### Y chinh
- Client tu quan ly khoa.
- Dich vu luu tru chi giu ciphertext.
- Phu hop khi khong muon server co kha nang giai ma noi dung.

### Luong xu ly
1. Client co du lieu goc va khoa ma hoa.
2. Client ma hoa du lieu tai cho.
3. Ban ma duoc upload len dich vu luu tru (S3, FTP server, he thong dung EBS, ...).
4. Client tai ban ma ve.
5. Client dung khoa cua minh de giai ma.

---

## So sanh nhanh

| Mo hinh | Ma hoa o dau | Ben nao giai ma duoc plaintext | Loi ich chinh |
|---|---|---|---|
| In transit (TLS) | Trong luc truyen qua mang | Endpoint dich | Bao ve du lieu tren duong truyen |
| Server-side at rest | Tren dich vu/may chu luu tru | Dich vu (co khoa) | Bao ve du lieu khi luu tru |
| Client-side | Tren client | Chi client | Bao mat toi da khoi server |

---

## Meo hoc nhanh
- Phan biet ro in transit va at rest.
- HTTPS nghia la su dung TLS cho duong truyen.
- Server-side encryption: khoa do dich vu quan ly.
- Client-side encryption: server khong giai ma duoc neu khong co khoa client.

## Tom tat 1 cau
Dung TLS de bao ve du lieu khi truyen, dung server-side encryption de bao ve du lieu khi luu tru, va dung client-side encryption khi chi client duoc phep doc plaintext.
