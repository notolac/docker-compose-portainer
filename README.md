# docker-compose-notolac

# Introduction to Docker using Portainer and Docker Compose

Docker is an open-source platform that allows you to automate the deployment, scaling, and management of applications using containerization. Containers are lightweight, isolated environments that package everything needed to run an application, including the code, runtime, system tools, and libraries.

Portainer is a web-based user interface that simplifies the management of Docker environments. It provides a graphical interface to manage containers, images, networks, and volumes, making it easier to deploy and monitor applications.

Docker Compose is a tool that allows you to define and run multi-container Docker applications. It uses a YAML file to specify the services, networks, and volumes required for your application. With Docker Compose, you can easily define complex application architectures and manage them as a single unit.

## Prerequisites

Before getting started, make sure you have the following prerequisites:

- Docker installed on your machine. You can download and install Docker from the official website: [https://www.docker.com/get-started](https://www.docker.com/get-started)

## Getting Started

To get started with Docker using Portainer and Docker Compose, follow these steps:

1. install the necessary dependencies to install the latest version of docker:

   ```bash
   sudo apt install lsb-release gnupg2 apt-transport-https ca-certificates curl software-properties-common -y
   ```

2. Download GPG certificate and repositories to run via APT, use `debian` or `ubuntu` for the appropriate OS:

   ```bash
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/ubuntu.gpg
   ```

3. Add the downloaded repository to the system,use `debian` or `ubuntu` for the appropriate OS:

   ```bash
   sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   ```

4. Update the repositories:

   ```bash
   sudo apt update
   ```

5. Install docker:

   ```bash
   sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```

6. Install portainer node (Web interface from where you manage your nodes or agents) :

   ```bash
   sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_stuff:/data portainer/portainer-ce:2.21.0
   ```

7. Install portainer agent (each agent that you will manage from the node, does not run web interface):

   ```bash
   sudo docker run -d   -p 9001:9001   --name portainer_agent   --restart=always   -v /var/run/docker.sock:/var/run/docker.sock   -v /var/lib/docker/volumes:/var/lib/docker/volumes   portainer/agent:2.21.0
   ```

8. Access the Portainer web interface by opening the following URL in your web browser: [https://localhost:9443](https://localhost:9443)

   - If you are running Docker on a remote machine, replace `localhost` with the IP address or hostname of the machine.

9. Follow the on-screen instructions to set up an admin user and connect Portainer to your Docker environment.

10. Once logged in, you can start managing your Docker environment using the Portainer web interface.

## Conclusion

In this tutorial, we introduced Docker and demonstrated how to use Portainer and Docker Compose to simplify the management of Docker environments. With Portainer, you can easily deploy, monitor, and scale your applications, while Docker Compose allows you to define and run multi-container applications with ease.

For more information on Docker, Portainer, and Docker Compose, refer to the official documentation:

- Docker: [https://docs.docker.com](https://docs.docker.com)
- Portainer: [https://www.portainer.io](https://www.portainer.io)
