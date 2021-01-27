# kubernetes-keydb-active-replica
Setup active-replica KeyDB on Kubernetes cluster and demonstrate KeyDB streams with python producer/consumer scripts.


### Running on your existing kubernetes cluster with at least two nodes:  
```
> kubectl apply -f ./k8resources.yaml
service/keydb created
statefulset.apps/keydb created
deployment.apps/keydb-producer created
deployment.apps/keydb-consumer created
```
### Check keydb pods are up and running:  
```
> kubectl get pods -l app=keydb  
NAME                             READY   STATUS    RESTARTS   AGE  
keydb-0                          1/1     Running   0          28m  
keydb-1                          1/1     Running   0          28m  
```
### Check the active replication works
```
> kubectl exec keydb-0 -- keydb-cli set key1 value1
OK
>  kubectl exec keydb-1 -- keydb-cli get key1 
value1
> kubectl exec keydb-1 -- keydb-cli set key2 value2
OK
>  kubectl exec keydb-0 -- keydb-cli get key2 
value2
```
### check the log of producer and consumer to see how they work
find pod names by `kubectl get pods`  
```
 > kubectl logs -f keydb-producer-974fbbb48-krbdg
 > kubectl logs -f keydb-consumer-974fbbb48-krbdg
```
