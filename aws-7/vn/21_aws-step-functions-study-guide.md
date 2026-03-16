# Tai lieu hoc AWS Step Functions

## Tong quan

AWS Step Functions la dich vu workflow cua AWS dung de dieu phoi nhieu dich vu AWS thanh mot quy trinh co cau truc. Dich vu nay huu ich khi ban can:

- Dieu phoi Lambda va cac dich vu AWS khac
- Xay dung nhanh xu ly re nhanh theo dieu kien
- Chay nhieu tac vu song song
- Theo doi tung buoc thuc thi cua workflow
- Quan ly ro rang trang thai thanh cong va that bai

Vi du trong file nguon su dung workflow **Hello World** trong **Workflow Studio** de giai thich cach mot state machine hoat dong.

## Khai niem chinh

### 1. Workflow Studio

Workflow Studio la giao dien thiet ke truc quan, cho phep keo tha cac thanh phan vao workflow.

Nhung thanh phan duoc nhac den trong vi du:

- Task state nhu Lambda va service integration
- Choice state de tao logic re nhanh
- Parallel state de chay dong thoi
- Map state de lap qua danh sach phan tu
- Mau workflow co san cho cac truong hop pho bien

Do thi truc quan nay se duoc chuyen thanh code tu dong.

### 2. Amazon States Language (ASL)

Workflow do Step Functions tao ra duoc dinh nghia bang **Amazon States Language (ASL)**.

Diem can nho:

- Workflow tren giao dien truc quan tuong duong voi mot tai lieu JSON o ben phai man hinh console

JSON nay mo ta:

- Cac state
- Cach chuyen giua cac state
- Xu ly input va output
- Hanh vi thanh cong hoac loi

### 3. Loai state machine

Vi du nhac toi hai loai workflow:

- **Standard workflow**
- **Express workflow**

Khi cau hinh state machine, AWS con hien thi:

- Ten state machine
- Thong tin ve thoi gian chay va chi phi
- Quyen IAM role
- Logging va cau hinh bo sung

## Phan tich workflow trong vi du

Workflow Hello World la mot vi du nho nhung de thay cach Step Functions van hanh.

### Buoc 1. Khoi tao output va bien

Workflow bat dau bang viec tao gia tri output ban dau va mot so bien.

Gia tri duoc tao trong vi du:

- `IsHelloWorldExample = true`
- `ExecutionWaitTimeInSeconds = 3`
- `CheckpointCount = 0`

Muc dich:

- Chuan bi du lieu cho cac state phia sau
- Khoi tao bien duoc dung trong toan bo workflow

### Buoc 2. Choice state

Workflow di vao mot **Choice** state.

Dieu kien duoc dung:

- Neu `IsHelloWorldExample == true` thi di tiep toi wait state
- Neu khong thi di toi failure state

Day la cach Step Functions thuc hien logic `if`.

### Buoc 3. Wait state

Neu dieu kien dung, workflow se cho mot vai giay.

Thoi gian cho:

- Lay tu bien `ExecutionWaitTimeInSeconds`
- Trong vi du, workflow cho `3` giay

### Buoc 4. Tang checkpoint va chay song song

Sau khi cho xong, workflow tang gia tri `CheckpointCount` va di vao **Parallel** state.

Muc dich cua Parallel state:

- Chay nhieu nhanh cung luc
- Phu hop voi cac cong viec doc lap

### Buoc 5. Cap nhat checkpoint va tong ket

Workflow tiep tuc tang checkpoint va ket thuc bang mot ban tong ket.

Ket qua cuoi cung trong vi du:

- Workflow thanh cong
- Tong thoi gian chay la ba giay
- Da di qua hai checkpoint

## Co the xem gi khi workflow dang chay

Step Functions cung cap kha nang theo doi rat tot trong luc thuc thi.

Ban co the xem:

- Graph view cua duong di workflow
- Input va output cua tung state
- Cac bien duoc gan trong qua trinh chay
- Event history
- Chi tiet giai thich vi sao mot nhanh thanh cong hoac that bai

Dieu nay rat huu ich khi debug workflow phuc tap.

## Nhanh thanh cong va nhanh that bai

Vi du cung cho thay cach thu nghiem nhanh that bai.

Neu ban doi gia tri hello-world flag tu `true` sang `false`, workflow se khong di theo nhanh thanh cong nua ma di vao failure state.

Dieu nay the hien mot nguyen tac quan trong:

- Workflow nen dinh nghia ro ca nhanh thanh cong lan nhanh that bai

## Tai sao Step Functions huu ich

Tu vi du nay, co the thay Step Functions huu ich vi no cho phep:

- Thiet ke workflow bang giao dien truc quan
- Tu dong tao workflow definition
- Mo hinh hoa logic dieu kien
- Chay cong viec song song
- Theo doi lich su thuc thi chi tiet
- Tich hop voi nhieu dich vu AWS

## Ghi nho cho hoc tap va phong van

Can nho cac diem sau:

- Step Functions la dich vu orchestration, khong phai compute service
- Workflow duoc dinh nghia duoi dang state machine
- Workflow Studio la cong cu thiet ke truc quan
- ASL la ngon ngu JSON dung de mo ta workflow
- Choice state dung cho logic re nhanh
- Parallel state dung de chay nhieu nhanh dong thoi
- Execution history ho tro giam sat va debug
- Quyen IAM rat quan trong khi Step Functions goi cac dich vu AWS khac

## Cau hoi tu luyen

1. AWS Step Functions dung de lam gi?
2. Amazon States Language la gi?
3. Khi nao nen dung Choice state?
4. Khi nao nen dung Parallel state?
5. Co the xem nhung thong tin nao trong luc workflow chay?
6. Dieu gi xay ra neu dieu kien trong Choice state la false?

## Tom tat ngan

AWS Step Functions cho phep ban xay dung workflow duoi dang state machine. Trong vi du, workflow khoi tao bien, kiem tra dieu kien, cho trong mot khoang thoi gian, chay mot so buoc song song, cap nhat checkpoint, va ket thuc voi trang thai thanh cong hoac that bai. Nhung y chinh can nho la Workflow Studio, ASL, Choice state, Parallel state, va kha nang theo doi qua trinh thuc thi.