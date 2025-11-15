# docker-compose-notolac

# Introduction to Docker using Portainer and Docker Compose

Docker is an open-source platform that allows you to automate the deployment, scaling, and management of applications using containerization. Containers are lightweight, isolated environments that package everything needed to run an application, including the code, runtime, system tools, and libraries.

Portainer is a web-based user interface that simplifies the management of Docker environments. It provides a graphical interface to manage containers, images, networks, and volumes, making it easier to deploy and monitor applications.

Docker Compose is a tool that allows you to define and run multi-container Docker applications. It uses a YAML file to specify the services, networks, and volumes required for your application. With Docker Compose, you can easily define complex application architectures and manage them as a single unit.

## Prerequisites

Before getting started, make sure you have the following prerequisites:

- Docker installed on your machine. You can download and install Docker from the official website: [https://www.docker.com/get-started](https://www.docker.com/get-started)

## Getting Started

To get started with Docker using Portainer and Docker Compose, you need to install Docker first and then deploy Portainer. Choose your operating system below for detailed instructions.

### Installing Docker

#### For Ubuntu

1. **Install required dependencies:**
   These packages are necessary for adding the Docker repository and installing Docker properly.

   ```bash
   sudo apt update
   sudo apt install lsb-release gnupg2 apt-transport-https ca-certificates curl software-properties-common -y
   ```

2. **Add Docker's official GPG key:**
   This key verifies the authenticity of the Docker packages.

   ```bash
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg
   ```

3. **Add the Docker repository:**
   This adds the official Docker repository to your system's package sources.

   ```bash
   sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   ```

4. **Update package index:**
   Refresh the package list to include the new Docker repository.

   ```bash
   sudo apt update
   ```

5. **Install Docker:**
   Install Docker Engine, CLI, containerd, and the Docker Compose plugin.

   ```bash
   sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
   ```

#### For Debian

1. **Install required dependencies:**
   These packages are necessary for adding the Docker repository and installing Docker properly.

   ```bash
   sudo apt update
   sudo apt install lsb-release gnupg2 apt-transport-https ca-certificates curl software-properties-common -y
   ```

2. **Add Docker's official GPG key:**
   This key verifies the authenticity of the Docker packages.

   ```bash
   sudo curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg
   ```

3. **Add the Docker repository:**
   This adds the official Docker repository to your system's package sources.

   ```bash
   sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
   ```

4. **Update package index:**
   Refresh the package list to include the new Docker repository.

   ```bash
   sudo apt update
   ```

5. **Install Docker:**
   Install Docker Engine, CLI, containerd, and the Docker Compose plugin.

   ```bash
   sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
   ```

### Installing Portainer

Portainer consists of two main components: the Portainer Server (web interface) and the Portainer Agent (for managing remote Docker instances).

6. **Install Portainer Server (Web Interface):**
   The Portainer Server provides the web-based management interface. We're using the LTS version for stability.

   ```bash
   sudo docker run -d \
     -p 8000:8000 \
     -p 9443:9443 \
     --name portainer \
     --restart=always \
     -v /var/run/docker.sock:/var/run/docker.sock \
     -v portainer_data:/data \
     portainer/portainer-ce:lts
   ```

7. **(Optional) Install Portainer Agent:**
   The Portainer Agent allows you to manage this Docker instance from a remote Portainer Server. Only install this if you plan to manage multiple Docker hosts from a central Portainer instance.

   ```bash
   sudo docker run -d \
     -p 9001:9001 \
     --name portainer_agent \
     --restart=always \
     -v /var/run/docker.sock:/var/run/docker.sock \
     -v /var/lib/docker/volumes:/var/lib/docker/volumes \
     portainer/agent:lts
   ```

### Accessing Portainer

8. **Access the Portainer web interface:**
   Open your web browser and navigate to: [https://localhost:9443](https://localhost:9443)

   - If you're accessing from a remote machine, replace `localhost` with the server's IP address or hostname.
   - Accept the security warning for the self-signed certificate (this is normal for initial setup).

9. **Initial Setup:**
   - Create an admin user account
   - Connect Portainer to your local Docker environment
   - You can now manage containers, images, networks, and volumes through the web interface

10. **Start using Portainer:**
    Once logged in, you can:
    - Deploy containerized applications
    - Monitor running containers
    - Manage Docker images and volumes
    - Create and manage networks
    - Use Docker Compose to deploy multi-container applications

## Conclusion

In this tutorial, we introduced Docker and demonstrated how to use Portainer and Docker Compose to simplify the management of Docker environments. With Portainer, you can easily deploy, monitor, and scale your applications, while Docker Compose allows you to define and run multi-container applications with ease.

For more information on Docker, Portainer, and Docker Compose, refer to the official documentation:

- Docker: [https://docs.docker.com](https://docs.docker.com)
- Portainer: [https://www.portainer.io](https://www.portainer.io)
