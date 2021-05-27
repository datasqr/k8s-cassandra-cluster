K8S_NAMESPACE=cassandra-cluster
KUBECTL ?= kubectl
HELM ?= helm

k3d-create:
	k3d cluster create --config k3d.yaml

k3d-delete:
	k3d cluster delete rc

namespace-create:
	${KUBECTL} apply -f ./cassandra/cassandra-namespace.yaml
	
namespace-delete:
	${KUBECTL} delete -f ./cassandra/cassandra-namespace.yaml

cassandra-create:
	${KUBECTL} apply -f ./cassandra/cassandra-cluster.yaml
	
cassandra-delete:
	${KUBECTL} delete -f ./cassandra/cassandra-cluster.yaml

cassandra-port-forward:
	${KUBECTL} --namespace ${K8S_NAMESPACE} port-forward svc/cassandra --address 0.0.0.0 9042:9042
	
getpods:
	${KUBECTL} get pods -n ${K8S_NAMESPACE}

getall:
	${KUBECTL} describe pods ${podname} -n ${K8S_NAMESPACE}

cassandra-cqlsh:
	${KUBECTL} --namespace  ${K8S_NAMESPACE} run --rm -it cassandra-client \
		--restart='Never' \
		--image bitnami/cassandra:3.11.10-debian-10-r78 \
		-- cqlsh -u cassandra -p cassandra cassandra
