# EKS Cluster Upgrade Guide

## Step 1: Check Existing Version

```bash
aws eks describe-cluster \
--name project-eks \
--region us-east-1 \
--query "cluster.version"
```

Before going to upgrade we have to enable cordon to nodes to not deploy any pods on old node while doing version upgrade

```bash
kubectl cordon <old node>
kubectl cordon ip-10-0-3-8.ec2.internal
kubectl cordon ip-10-0-4-252.ec2.internal
```

## Step 2: Upgrade EKS Control Plane

Run:

```bash
aws eks update-cluster-version \
--region us-east-1 \
--name project-eks \
--kubernetes-version 1.32
```

## Step 3: Upgrade Node Groups

Once control plane upgrade completes, update worker nodes.

Option A — Rolling upgrade (recommended)

```bash
aws eks update-nodegroup-version \
  --cluster-name project-eks \
  --nodegroup-name eks-node-group \
  --kubernetes-version 1.32 \
  --region us-east-1
```

## Upgrade EKS Add-ons

Upgrade important components:

- CoreDNS
- kube-proxy
- VPC CNI

## Step 4: Upgrade Addons

Update each addon:

Example VPC CNI

```bash
aws eks update-addon \
--cluster-name project-eks \
--addon-name vpc-cni
```

Example CoreDNS

```bash
aws eks update-addon \
--cluster-name project-eks \
--addon-name coredns
```

Example kube-proxy

```bash
aws eks update-addon \
--cluster-name project-eks \
--addon-name kube-proxy
```

Example EBS CSI

```bash
aws eks update-addon \
--cluster-name project-eks \
--addon-name aws-ebs-csi-driver
```

Old node  
↓  
Drain  
↓  
Replace with new node  
↓  
Reschedule pods




## Resume Points – EKS Cluster Upgrade

- Planned and executed AWS EKS cluster version upgrades while minimizing downtime for production workloads.
- Managed node group upgrades using Terraform, ensuring worker nodes remained compatible with upgraded cluster versions.
- Implemented default EKS addons (CoreDNS, kube-proxy, VPC CNI, EBS CSI driver, pod identity) with automated upgrade paths using Terraform.
- Applied sequential addon deployment (depends_on) to reduce provisioning time and avoid AWS API throttling during upgrades.
- Leveraged Terraform variables and version control to dynamically manage cluster, node group, and addon versions for repeatable deployments.
- Ensured zero-impact upgrades by using rolling node updates, maintaining service availability during cluster version changes.
- Automated cluster and addon upgrades using Terraform best practices, including force_update_version and version pinning when needed.
- Monitored and validated post-upgrade cluster health, addon readiness, and application stability using AWS console and kubectl.


## Interview Explanation

"I have experience performing EKS cluster upgrades through multiple approaches. Manually, I've used the AWS console to upgrade the control plane and worker nodes while monitoring system components to ensure stability and zero downtime. Using the AWS CLI, I scripted cluster and node upgrades, validating addon and pod health to maintain operational reliability. With Terraform, I automated the entire upgrade process, managing cluster versions, node groups, and default addons like CoreDNS, kube-proxy, VPC CNI, and EBS CSI sequentially to avoid throttling. I also implemented best practices such as version pinning for critical addons, rolling updates for node groups, and health checks for system pods, ensuring upgrades are predictable and low-risk. By combining automation, monitoring, and sequential deployment, I was able to minimize downtime, maintain application availability, and deliver a fully auditable, repeatable process across multiple environments. This approach also improved team efficiency, reduced manual intervention, and allowed seamless scaling of the infrastructure."
