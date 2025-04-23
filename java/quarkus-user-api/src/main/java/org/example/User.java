package org.example;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;

@Entity
public class User {
    @Id
    @GeneratedValue
    public Long id;

    public String name;
    public String email;

    // Construtores
    public User() {}
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
}
