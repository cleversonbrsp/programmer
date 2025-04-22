package org.example;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.transaction.Transactional;
import java.util.List;

@ApplicationScoped
public class UserService {

    @Transactional
    public void create(User user) {
        user.persist();
    }

    public List<User> listAll() {
        return User.listAll();
    }

    public User findById(Long id) {
        return User.findById(id);
    }

    @Transactional
    public void update(Long id, User data) {
        User user = User.findById(id);
        if (user != null) {
            user.name = data.name;
            user.email = data.email;
        }
    }

    @Transactional
    public void delete(Long id) {
        User.deleteById(id);
    }
}
