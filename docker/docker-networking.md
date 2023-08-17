---
title: Docker Networking and Advanced Routing
---

## Introduction to Docker Networking and Custom Networks

In Docker, containers by default join the 'bridge' network, but for better control and security, it's recommended to create custom networks. This guide explores the creation, management, and benefits of custom networks in Docker.

## Benefits of Isolated Networks

Using isolated networks in Docker offers several advantages:

-   **Isolation and Security**: Enhances security by containing breaches and unauthorized access.
-   **Controlled Communication**: Regulates service-to-service communication, avoiding undesired interactions.
-   **Microservices Architecture**: Streamlines management and scalability in line with microservices.
-   **Load Balancing**: Centralizes load balancers in unique networks for simplified traffic management.
-   **Operational Efficiency**: Network-specific management aids in troubleshooting and configuration.
-   **Resource Optimization**: Optimizes performance by preventing resource clashes.

## Creating Custom Networks

To create custom networks in Docker:

1. **Create Custom Networks:**

    Open a terminal and execute the following commands to create custom networks with specific IP address ranges:

    ```bash
    docker network create backend --subnet 10.0.0.0/24
    docker network create frontend --subnet 10.0.1.0/24
    docker network create loadbalancer --subnet 10.0.2.0/24
    ```

    This establishes three isolated networks: `backend`, `frontend`, and `loadbalancer`, each with its own IP address range.

2. **Inspect Network Properties:**

    You can inspect the properties of the created networks to ensure their configuration meets your requirements. Run the following commands to see detailed information about each network:

    ```bash
    docker network inspect backend
    docker network inspect frontend
    docker network inspect loadbalancer
    ```

    This command provides insights into network settings such as IP ranges, connected containers, and more.

## Creating Containers

Before connecting containers to networks or adding custom routes, create the necessary containers:

1. **Create the `nhttpd` Image:**

   Create a Dockerfile with the following content and save it in a directory:

    ```dockerfile
    FROM httpd

    RUN apt-get update
    RUN apt-get install -y iputils-ping
    RUN apt-get install -y inetutils-traceroute
    RUN apt-get install -y iproute2
    RUN apt-get install -y curl telnet dnsutils vim
    ```

   Build the image with the name `nhttpd`:

    ```bash
    docker build -t nhttpd /path/to/dockerfile_directory
    ```

2. **Create Containers with Network Administrative Capabilities:**

   Launch containers named `s1`, `s2`, and `lb1` using the `nhttpd` image and with network administrative capabilities:

    ```bash
    docker run -d --name s1 --cap-add=NET_ADMIN nhttpd
    docker run -d --name s2 --cap-add=NET_ADMIN nhttpd
    docker run -d --name lb1 --cap-add=NET_ADMIN nhttpd
    ```

   These containers are now equipped with the ability to perform advanced networking operations.

3. **Create the Gateway Container:**

   Launch a container named `gateway` using the `nhttpd` image, with network administrative capabilities:

    ```bash
    docker run -d --name gateway --cap-add=NET_ADMIN nhttpd
    ```

   This container will act as a central hub for connecting and routing traffic between networks.

## Connecting Containers to Networks

Now that the containers are created, connect them to the appropriate custom networks:

```bash
docker network connect backend s1
docker network connect frontend s2
docker network connect loadbalancer lb1
docker network connect backend gateway
docker network connect frontend gateway
```

These commands establish connections between containers and networks, enabling isolated communication.

## Advanced Routing and Communication Between Isolated Networks

For advanced routing and communication between isolated networks:

1. **Add Custom Routes to the Gateway Container:**

   Once you've set up your `gateway` container, you need to configure custom routes within this container to enable communication between the isolated networks.

   - **Step 1:** Access the `gateway` container's command line by running:

     ```bash
     docker exec -it gateway bash
     ```

   - **Step 2:** Inside the container, use the `ip route add` command to add custom routes. These routes will instruct the container's networking stack how to forward traffic between networks. For example, if you want to enable communication between the `frontend` network (10.0.1.0/24) and the `backend` network (10.0.0.0/24), run:

     ```bash
     ip route add 10.0.1.0/24 via 10.0.0.3
     ```

     Here, `10.0.1.0/24` is the destination subnet (for the `frontend` network), and `10.0.0.3` is the IP address of a container within the `backend` network that serves as a gateway. This route tells the `gateway` container how to forward traffic to the `frontend` network.

   - **Step 3:** Similarly, add a route for the `loadbalancer` network (if needed):

     ```bash
     ip route add 10.0.2.0/24 via 10.0.0.4
     ```

     Here, `10.0.2.0/24` is the destination subnet (for the `loadbalancer` network), and `10.0.0.4` is the IP address of a container within the `backend` network that serves as a gateway.

   - **Step 4:** Exit the container's command line:

     ```bash
     exit
     ```

   With these custom routes configured within the `gateway` container, it can now effectively route traffic between the isolated networks. This advanced routing enables seamless communication while maintaining the isolation and security of the networks.

## Centralized Networking and Custom Setups

The `gateway` container serves as a central point for connecting separate networks, enabling communication through advanced routing. Docker's flexibility in networking allows tailored setups to meet application requirements, ensuring security, performance, and communication needs are met.
