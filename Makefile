K8S_NAMESPACE=cassandra-cluster
KUBECTL ?= kubectl
HELM ?= helm

k3d-create:
	sudo k3d cluster create --config k3d.yaml

k3d-delete:
	sudo k3d cluster delete rc

namespace-create:
	sudo ${KUBECTL} apply -f ./cassandra/cassandra-namespace.yaml
	
namespace-delete:
	sudo ${KUBECTL} delete -f ./cassandra/cassandra-namespace.yaml

cassandra-create:
	sudo ${KUBECTL} apply -f ./cassandra/cassandra-cluster.yaml
	
cassandra-delete:
	sudo ${KUBECTL} delete -f ./cassandra/cassandra-cluster.yaml

cassandra-port-forward:
	sudo ${KUBECTL} --namespace ${K8S_NAMESPACE} port-forward svc/cassandra --address 0.0.0.0 9042:9042
	
getpods:
	sudo ${KUBECTL} get pods -n ${K8S_NAMESPACE}

getall:
	sudo ${KUBECTL} describe pods ${podname} -n ${K8S_NAMESPACE}


