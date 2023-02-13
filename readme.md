
**This repository is made by Marc Blomvliet (Aurai), and is for learning purpose only.** </br>
</br> 
In this tutorial you will learn how to create an Docker image of your fastAPI application. </br>
This application includes the following: </br>
* Takes two questions as input</br>
* Returns a prediction whether the two questions are similar or not similar</br>
* Saves the raw user input data in your mongoDB database </br>
* Saves the predictions in your mongoDB database </br></br>

*The application uses my own pre-trained model (with the use of MLFlow), the model is not very accurate but this is not the purpose of this training, neither to bother you with training your own model.* </br>

Furthermore, you will be introduced to MongoDB to create your own FREE database. </br>
Test your Docker image with Docker.</br>
Create a Kubernetes cluster with the same Docker image. </br>
The Kubernetes cluster contains the following: </br>
* Deployment </br>
* Load balancer </br>
* Auto scaler (Horizontal Pod Auto scaler)</br>

After you created your kubernetes cluster, you will perform a stress/load test on your API and therfore on your Kubernetes cluster. </br>

*The pink sections (3.8, 3.9 and 3.10) are optional and just for information.* </br>

# 1. Create your own MongoDB Database
## 1.1 
Make sure to create your own account on the mongoDB website: </br>
https://account.mongodb.com/account/login?signedOut=true </br>

### 1.1.1
After you created your account and succesfully logged in. </br>
You should add your current IP Address, and then Build a Database
<img align="left" src="https://github.com/MarcB77/kubernetes_tutorial/blob/main/images/mongoDB_step_1.png" width="200"/> </br>

### 1.1.2
Create a Free 'Shared' cluster, and leave it on the default settings. </br>
You can add your own cluster name if you like.
<img align="left" src="https://github.com/MarcB77/kubernetes_tutorial/blob/main/images/mongoDB_step_2.png" width="200"/> 
<img align="left" src="https://github.com/MarcB77/kubernetes_tutorial/blob/main/images/mongoDB_step_3.png" width="200"/> </br>

### 1.1.3
After you created your cluster. You are prompted to create a database user. </br>
Create one with a username and password.
<img align="left" src="https://github.com/MarcB77/kubernetes_tutorial/blob/main/images/mongoDB_step_4.png" width="200"/> </br>

## 1.1.4 Update the .env 
Update the file with your own credentials. </br>
MONGODB_PASSWORD: Is the password that you created for your database user in step 1.1.3 </br>
MONGODB_SHARED_CLUSTER_NAME: Is the name of your cluster (step 1.1.2), by default it is 'Cluster0'. </br>

# 2. Docker commands

## 2.1 Install Docker
https://docs.docker.com/get-docker/ </br>

## 2.2 Build the docker image </br> (run to make sure your image is working as expected).
> docker build -t <span style="color: orange"> image-name</span> .</br>
> docker run -dp 8020:8020 <span style="color: orange"> image-name</span> </br>

*<span style="color: orange">-image-name-</span> = tutorial-classifier </br>*

***Make sure to be in the root folder API_kubernetes/fastAPI/***  </br>

Go to http://0.0.0.0:8020/docs </br>
<img align="left" src="https://github.com/MarcB77/kubernetes_tutorial/blob/main/images/Docker_step_1.png" width="200"/> </br>

And test your API, Click on: POST /predict/  and select 'Try it out'</br>
Paste two questions inside "string", and predict the similarity. </br>
And execute the command. </br>
<img align="left" src="https://github.com/MarcB77/kubernetes_tutorial/blob/main/images/fastAPI_step_1.png" width="200"/> </br>

I you got a response, then there should also be data inside your mongoDB Database now. </br>
Go to your mongoDB and click 'Browse Collections', there should be two tables: Raw_input and Predictions. </br>
<img align="left" src="https://github.com/MarcB77/kubernetes_tutorial/blob/main/images/mongoDB_step_5.png" width="200"/> 
<img align="left" src="https://github.com/MarcB77/kubernetes_tutorial/blob/main/images/mongoDB_step_6.png" width="200"/> </br>

# 3. Kubernetes - Minikube commands
*minikube is local Kubernetes, focusing on making it easy to learn and develop for Kubernetes.* </br>

## 3.1 Install minikube
MacOS with homebrew: 
> brew install minikube </br>

Other OS: </br>
https://minikube.sigs.k8s.io/docs/start/ </br>

## 3.2 Start minikube
> minikube start </br>

## 3.3 Load Docker image to kubernetes / minikube
> minikube image load <span style="color: orange">-docker image name-</span> </br>

***<span style="color: orange">-docker image name-</span> = tutorial-classifier***

## 3.4 Apply the metrics server, in order to perform auto-scaling
> kubectl -n kube-system apply -f <span style="color: orange">metricserver-0.6.2.yaml</span> </br>

***Make sure to be in the root folder API_kubernetes/kubernetes/***  </br>
</br>

Check if the metric server is working: </br>
> kubectl get pods -n kube-system | grep metrics-server </br>

## 3.5 Deploy with your cluster_config.yml (config file)
> kubectl apply -f <span style="color: orange">cluster_config.yml</span> </br>

***Make sure to be in the root folder API_kubernetes/kubernetes/***  </br>

## 3.6 Get the URL of the Load-balancer service, this is the post.request url to all pods
> minikube service --all </br>

If you add '/docs' to the url of the load-balancer, then you should get the fastAPI page. </br>
Something like: http://127.0.0.1:49700/docs </br> 
The port number will probably be different. </br>

## 3.7 Kubernetes Dashboard UI
> minikube dashboard


## <span style="color: pink">3.8 Basic commands <span>
> kubectl get pods</br>
> kubectl get deployments</br>
> kubectl get services</br>
> kubectl get hpa // (Get the horizontal pod autoscalers (HPA))</br>

> kubectl describe svc <span style="color: orange">-service name-</span> </br>

*<span style="color: orange">-service name-</span> = loadbalancer-tutorial </br>*
> kubectl describe deployment <span style="color: orange">-deployment name-</span> </br>

*<span style="color: orange">-deployment name-</span> = tutorial-aurai-classifier </br>*

## <span style="color: pink">3.9 Basic delete commands <span>
> kubectl delete service <span style="color: orange">-service name-</span> </br>

*<span style="color: orange">-service name-</span> = loadbalancer-tutorial </br>*
> kubectl delete deployments <span style="color: orange">-deployment name-</span> </br>

*<span style="color: orange">-deployment name-</span> = tutorial-aurai-classifier </br>*
> kubectl delete hpa <span style="color: orange">-hpa name-</span> </br>

*<span style="color: orange">-hpa name-</span> autoscaler-tutorial </br>*


## <span style="color: pink"> 3.10 Get metrics commands <span>
> kubectl top pods </br>
> kubectl top nodes </br>

# 4. Locust stress testing API
## 4.1 Perfrom the stress/load testing on the kubernetes cluster/pods
> locust -f <span style="color: orange">./kubernetes/locust_test.py</span> </br>

***Make sure to be in the root folder API_kubernetes***  </br>

</br>
If you are interested you can extend the application with your snowflake database instead of a MongoDB. </br>
The project is already prepared for this. </br>

<style>H1{background:grey;}</style>
<style>H2{color:green;}</style>
