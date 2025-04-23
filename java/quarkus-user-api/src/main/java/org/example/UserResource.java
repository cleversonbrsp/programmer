package org.example;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import java.util.List;

@Path("/users")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class UserResource {

    @Inject
    UserService service;

    @POST
    public void create(User user) {
        service.create(user);
    }

    @GET
    public List<User> list() {
        return service.listAll();
    }

    @GET
    @Path("/{id}")
    public User get(@PathParam("id") Long id) {
        return service.findById(id);
    }

    @PUT
    @Path("/{id}")
    public void update(@PathParam("id") Long id, User user) {
        service.update(id, user);
    }

    @DELETE
    @Path("/{id}")
    public void delete(@PathParam("id") Long id) {
        service.delete(id);
    }
}
