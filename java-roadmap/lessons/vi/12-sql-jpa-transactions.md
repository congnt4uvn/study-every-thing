# Bài 12 — SQL + JPA + transaction

## Mục tiêu

Kết nối Spring Boot với SQL DB, model entity bằng JPA, và hiểu transaction.

## Khái niệm chính

- SQL là nguồn sự thật (source of truth) của nhiều hệ thống backend.
- JPA map object Java sang bảng DB.
- Transaction đảm bảo tính atomicity và consistency.
- Migration schema nên tự động (Flyway/Liquibase).

## Thực hành

### 1) Thêm dependencies

Thường gồm:

- Spring Data JPA
- PostgreSQL driver (hoặc H2 để học)
- Flyway

### 2) Entity

```java
import jakarta.persistence.*;

@Entity
@Table(name = "users")
public class UserEntity {
  @Id
  private String id;

  @Column(nullable = false, unique = true)
  private String email;

  protected UserEntity() {}

  public UserEntity(String id, String email) {
    this.id = id;
    this.email = email;
  }

  public String getId() { return id; }
  public String getEmail() { return email; }
}
```

### 3) Repository

```java
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<UserEntity, String> {
  Optional<UserEntity> findByEmail(String email);
}
```

### 4) Service có @Transactional

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserService {
  private final UserRepository repo;

  public UserService(UserRepository repo) {
    this.repo = repo;
  }

  @Transactional
  public UserEntity create(String id, String email) {
    repo.findByEmail(email).ifPresent(u -> {
      throw new IllegalArgumentException("email already used");
    });
    return repo.save(new UserEntity(id, email));
  }
}
```

## Checklist

- Lưu và đọc dữ liệu từ SQL DB.
- Giải thích được transaction là gì.
- Giữ controller mỏng, logic nằm ở service.

## Lỗi thường gặp

- Dùng entity lazy-load ngoài transaction mà không hiểu.
- Không dùng migration dẫn đến lệch schema.
- N+1 query (về sau học cách phát hiện bằng SQL log).

## Tiếp theo

Capstone: ghép tất cả thành service nhỏ kiểu production.
