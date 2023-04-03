# lava

## Installation

### Docker
Run the docker build to create the image 
```bash
docker build . 
```
once done to push to local registry or remote one ( ECR , ACR ) change the deployment files under lava/lava/templates/ accordingly to take the image from it.

### Helm
Run the following to install the chart
```bash
helm upgrade --install  lava .\lava\ -n lava
```


you will create:

2 deployments

2 dedicated services for them based on selectors

1 general service to catch both services

1 TrafficSplit (CRD from nginx based on NGINX Service Mesh )

-------
### Code 
once you run the above and expose the canary service the UI will show:

```html
Hello, you are currently working with 10.244.0.21

Your Computer Name is: lava2-68bd47f75f-pzq9v
```

splitting intermidiatlly between lava1 and lava2 with:

60% of the calls will go to lava1, 40% of the calls will go to lava2
