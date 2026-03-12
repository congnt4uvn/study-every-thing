# Lesson 12 — SQL + JPA + transactions

## Goal

Connect a Spring Boot service to a SQL database, model entities with JPA, and understand transactions.

## Key concepts

- SQL is the source of truth for many backend systems.
- JPA maps Java objects to database tables.
- Transactions provide atomicity and consistency.
- Schema migrations should be automated (Flyway/Liquibase).

## Hands-on

### 1) Add dependencies

Typically:

- Spring Data JPA
- PostgreSQL driver (or H2 for learning)
- Flyway

### 2) Define an entity

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

### 4) Transactional service

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

- You can store and retrieve data from a SQL DB.
- You can explain what a transaction is.
- You can keep controllers thin and logic in services.

## Common pitfalls

- Using lazy-loaded entities outside transactions without understanding.
- Not using migrations (leading to “works on my machine” schema drift).
- N+1 query issues (learn to detect later with SQL logs).

## Next

Capstone: combine everything into a small production-style service.
