## Customizable Load-Balancer

1. Run `make build` to build the docker images. This calls docker compose to build the server and load-balancer images.
2. Run `make run_lb` to run the load balancer. This starts up a load balancer instance at http://localhost:5000
    1. Supported endpoints: `/home, /heartbeat, /rep, /add, /rm`.
3. To stop all running containers, run `make stop`.
4. To remove all images and networks, run `make rm`.