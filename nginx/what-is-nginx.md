---
title: What Is Nginx
subtitle:
author: Labin Ojha
keywords:
csl: https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl
fontsize: 11.5pt
mainfont: Arial, Palatino, Georgia, Times
---

## Nginx Usecases

-   Web Server
    -   Serves web content
-   Reverse Proxy
    -   Load Balancing
    -   Backend Routing
    -   Caching
    -   API Gateway (rate limiting, API versioning, authentication)

## Nginx Implementation Example

| Before Nginx                                                                                                           | After Nginx                                                              |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| ![Before Nginx](what-is-nginx/before-nginx.png)                                                                        | ![After Nginx](what-is-nginx/after-nginx.png)                            |
|                                                                                                                        |                                                                          |
| - The server can get overloaded as number of connections increase                                                      | Load balanced with Nginx, backend can scale independently                |
| - We can spin up multiple servers running on several ports but now the clients have to be aware of them too.           | Backend routing with Nginx                                               |
| - The endpoints are not secured, and with multiple servers multiple certificates need to be issued (or copied to each) | Can issue one certificate with Nginx, multiple certificates not required |
|                                                                                                                        |                                                                          |

_Nginx benefits don't come for free as it is an extra layer and there is some overhead, that is why Nginx or any reverse proxy has to be as efficient as possible._

## Nginx Layer 4 vs Layer 7 proxying

-   Layer 4/7 refers to OSI model layers.
-   In Layer 4 we see TCP/IP stack only nothing about the app, we have access to
    -   Source IP, Source Port
    -   Destination IP, Destination Port
    -   Simple packet inspection (SYN/TLS hello)
-   In Layer 7 we see the application, HTTP/ gRPC etc..
    -   We have access to more context
    -   I know where the client is going, which page they are visiting
    -   Require decryption
-   See [networking notes](../networking/) for more.
-   NGINX can operate in Layer 7 (e.g. http) or Layer 4 (tcp)
-   Layer 4 proxying is useful when NGINX doesn’t
    understand the protocol (MySQL database protocol)
-   Layer 7 proxying is useful when NGINX want to share
    backend connections and cache results
-   Using `stream` context it becomes a layer 4 proxy
-   Using `http` context it becomes a layer 7 proxy

## TLS Termination and TLS Passthrough

-   TLS stands for Transport Layer Security
-   It is a way to establish end-to-end encryption between one another
-   Symmetric encryption is used for communication (client/server has the
    same key)
-   Asymmetric encryption is used initially to exchange the symmetric key
    (diffie hellman)
-   Encryption alone, whether symmetric or asymmetric, doesn't guarantee the identity of communication parties. A middleman can pose as an authority, so Certificate Authorities (CAs) and verification methods are crucial for distinguishing between authorized and non-authorized entities, as encryption's primary role is content protection, not identity validation.
-   See [networking notes](../networking/) for more.

### TLS Termination

-   Even if NGINX has TLS (e.g. HTTPS) backend may or may not. For private server environment HTTP is fine if shielded by TLs at Nginx's layer. In this case NGINX terminates TLS, decrypts and sends unencrypted.
-   If NGINX is TLS and backend is also TLS ( HTTPS ). NGINX terminates TLS, decrypts, optionally rewrite headers and then re-encrypt the content to the backend. This introduces latency so the ciphers have to be fast and performant.
-   While NGINX can inspect Layer 7 (L7) data, rewrite headers, and cache content, it either needs to have its own SSL/TLS certificate or share the certificate used by the backend server. This certificate is essential for encrypting and decrypting data between NGINX and the backend.
-   Suitable for Load Balancing and Content Modification.
-   Shared Certificates for a Single Domain.

### TLS Passthrough

-   If the Backend has TLS, NGINX can be used to just to proxy/stream the packets directly to the backend. In this case Nginx doesn't respond to the 'TLS Hello' as it is not authorized to terminate TLS. The TLS handshake is forwarded all the way to the backend just like a tunnel and back.
-   There is no caching
-   There are L4 check only, but more secure as NGINX doesn’t need
    the backend certificate.
-   Preferred for End-to-End Encryption and Enhanced Security.
-   Appropriate When Content Inspection or Modification Is Not Required.
-   One disadvantage is that Nginx cannot share backend connections, every request will have a new connection and that can be costly.

## Nginx Internal Architecture

-   Nginx has a 'master process' that coordinates all other Nginx processes. It also manages caching, reading it from disk, and refreshing caches.
-   The primary focus is on 'worker processes', responsible for most of the work. Worker processes handle connections and requests.

    ![Nginx Master and Worker Processes](what-is-nginx/nginx-master-worker-proceses.png)

-   When Nginx is in 'auto' mode, worker processes are spawned based on the number of hardware threads on the server. Hardware threads can simulate multiple cores (with [hyper-threading](https://www.intel.com/content/www/us/en/gaming/resources/hyper-threading.html)), e.g., 4 cores can simulate 8 hardware threads.

-   **NGINX Threading Architecture**

    -   When NGINX reverse proxy starts it creates one thread per CPU core and these worker threads do the heavy lifting. The number of worker threads are configurable but NGINX recommends one thread per CPU core to avoid context switching and cache thrashing. In older versions of NGINX all threads accept connections by competing on the shared listener socket (by default only one process can listen on IP/port pair). In recent versions of NGINX this was changed to use socket sharding (through SO_REUSEPORT socket option) which allows multiple threads to listen on the same port and the OS will load balance connections on each accept queue.

    | Multiple Threads Single Acceptor Architecture                                                     | Multiple Threads with Socket Sharding (SO_REUSEPORT)                                                          |
    | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
    | ![Nginx Multiple Thread Single Acceptor](what-is-nginx/nginx-multiple-thread-single-acceptor.png) | ![Nginx Multiple Threads with Socket Sharding](what-is-nginx/nginx-multiple-threads-with-socket-sharding.png) |

    See more at [Threads And Connections In The Backend](../networking/threads-and-connections-in-the-backend.html)

-   When a client establishes a TCP connection to Nginx, connections are initially placed in a Syn queue and then moved to an accept queue. The kernel manages the queue but it's allocated by Nginx.

-   Worker processes retrieve connections from the accept queue. Worker processes are responsible for request handling. Each worker process is pinned to a CPU core to minimize context switches as Request handling involves CPU-intensive tasks.

-   Some requests are IO bound, requiring reading content from disk, making upstream network requests or writing to sockets(i.e writing a response which may also involve encryption). These IO-bound operations can be slow and cause waits, hence Nginx performs event-driven IO, allowing the process to perform other tasks during IO wait.

-   Nginx scales by adding more worker processes to handle incoming connections. Each worker process can manage multiple connections simultaneously. Load balancing distributes connections among worker processes. The number of worker processes depends on server hardware and usage patterns.

See also [How Nginx is Designed for Performance and Scale](https://www.nginx.com/blog/inside-nginx-how-we-designed-for-performance-scale/)
