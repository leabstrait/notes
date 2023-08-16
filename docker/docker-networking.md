---
title: Docker Networking and Advanced Routing
---

NEEDS TESTING

In Docker, default containers join the 'bridge' network, but for more control and security, custom networks are preferable. The 'bridge' network has limitations for production, making tailored networks necessary.

Creating custom networks:

```bash
docker network create backend --subnet 10.0.0.0/24
docker network create frontend --subnet 10.0.1.0/24
docker network create loadbalancer --subnet 10.0.2.0/24
```

Adding the `--internal` flag ensures internal-only networks.

Inspecting networks:

```bash
docker network inspect backend
docker network inspect frontend
docker network inspect loadbalancer
```

To connect a container to a network:

```bash
docker network connect backend s1
docker network connect frontend s2
docker network connect loadbalancer lb1
```

For detaching from the default 'bridge' network:

```bash
docker network disconnect bridge s1
docker network disconnect bridge s2
docker network disconnect bridge lb1
```

Benefits of using isolated networks:

- **Isolation and Security**: Enhances security by containing breaches and unauthorized access.
- **Controlled Communication**: Regulates service-to-service communication, avoiding undesired interactions.
- **Microservices Architecture**: Streamlines management and scalability in line with microservices.
- **Load Balancing**: Centralizes load balancers in unique networks for simplified traffic management.
- **Operational Efficiency**: Network-specific management aids in troubleshooting and configuration.
- **Resource Optimization**: Optimizes performance by preventing resource clashes.

To achieve advanced routing and allow communication between isolated networks, you can add custom routes within a container:

docker run -d --name gateway --network backend --network frontend  your_gateway_image

gateway can be connected to teh intenet and other networks connected to it, so hat we can do logging and centralize conenctio nfrom here.

```bash
ip route add 10.0.1.0/24 via 10.0.0.3
ip route add 10.0.2.0/24 via 10.0.0.4
```

Here, `10.0.1.0/24` is the destination subnet (for the `frontend` network), and `10.0.0.3` is the IP address of the gateway within the `backend` network. Similarly, `10.0.2.0/24` is the destination subnet for the `loadbalancer` network, and `10.0.0.4` is the corresponding gateway IP.

Additionally, you can enable network administrative capabilities using:

```bash
docker run -d --name s1 --network backend --cap-add=NET_ADMIN your_image
docker run -d --name s2 --network frontend --cap-add=NET_ADMIN your_image
docker run -d --name lb1 --network loadbalancer --cap-add=NET_ADMIN your_image
```

The `gateway` container serves as a central point for connecting separate networks. It is given administrative privileges through the `--cap-add=NET_ADMIN` flag, enabling it to perform advanced routing tasks. By connecting the `gateway` container to different networks (`backend` and `frontend` in this example), you enable communication between isolated networks.

This setup allows advanced routing and fine-grained control over container networking. If you need more networks, you can create them using similar commands. Docker's flexibility in networking enables tailored setups to meet application requirements, ensuring security, performance, and communication needs are met.

Remember to replace placeholders like `backend`, `frontend`, `loadbalancer`, `10.0.0.0/24`, `10.0.1.3`, `10.0.0.4`, `your_gateway_image`, and `your_image` with the appropriate values for your specific setup.