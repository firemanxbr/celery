# Introduction

Challenge proposed by Veriff to Senior Python Engineer position to calculate the value of the average face embedding vector across a large dataset of faces/photos.

## Master Node

The master node is a concept, in this challenge, that will be a container to orchestrate everything necessary to set up the tools, queue tasks, etc.. to other containers that will process the face embedding vector across a large dataset of faces.

**Note:** Regarding the size of this challenge, only one container as a master node will be necessary to process in a reasonable time. For bigger environments with a huge dataset will be necessary parallelization in the methods to acquire the dataset.


## REQUIREMENST

The environment used in this challenge was Mac Book Pro running macOS Mojave. To run and test the project will need:

* VirtualBox
* Minikube
* Docker


## VirtualBox
Necessary to run the minikube. Please download the MacOs version and install without any special configuration.

# Minikube
Necessary to run the kubernetes. Please download the MacOs version and install without any special configuration.
To run the minuke:

```
$ minikube start --vm-driver virtualbox --disk-size 50G --cpus 4 --memory 10000 -v=10
```

I used this configuration because my resources are so limited.

After started with success, please run:

```
🚜  Pulling images ...
🚀  Launching Kubernetes ... 
⌛  Verifying: apiserver proxy etcd scheduler controller dns
🏄  Done! kubectl is now configured to use "minikube"

$ minikube status
host: Running
kubelet: Running
apiserver: Running
kubectl: Correctly Configured: pointing to minikube-vm at 192.168.99.103
```

The ip used by minikube-vm will be used to access the web interfaces in this project.

We can use the minikube dashboard to analyze the use of our resources by kubernetes:

```
$ minikube dashboard
🔌  Enabling dashboard ...
🤔  Verifying dashboard health ...
🚀  Launching proxy ...
🤔  Verifying proxy health ...
🎉  Opening http://127.0.0.1:49926/api/v1/namespaces/kube-system/services/http:kubernetes-dashboard:/proxy/ in your default browser...
```

## Deployment

* GIT CLONE HERE

```
$ kubectl -f infra.yaml apply
service/rabbitmq created
deployment.extensions/rabbitmq created
persistentvolume/task-pv-volume created
persistentvolumeclaim/task-pv-claim created
```
Please wait the RabbitMQ will be running to continue deployment the other containers. How to check the RabbitMQ container?

```
 kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
rabbitmq-7d4bff7b86-vscjw   1/1     Running   0          95s
```

```
$ kubectl -f master.yaml apply
deployment.extensions/master created
service/master created

$ kubectl -f flower.yaml apply
deployment.extensions/celery-flower created
service/celery-flower created

$ kubectl -f worker.yaml apply
deployment.extensions/worker created
```

After everything it is running properly you can check the open the new tabs in your browser to load the Flower and the Master API, created to this project.

```
$ kubectl get pods
NAME                             READY   STATUS    RESTARTS   AGE
celery-flower-569dc4dd87-9flbt   1/1     Running   0          8m30s
master-f7cff7b59-ldj94           1/1     Running   0          8m37s
rabbitmq-7d4bff7b86-vscjw        1/1     Running   0          10m
worker-666b89856c-8tw8b          1/1     Running   0          6m56s
worker-666b89856c-qz2dv          1/1     Running   0          6m56s
```


