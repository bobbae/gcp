include config.mk

.PHONY : default replace-bucket-name install-kaggle-data install-dataproc-python-demo install-dataproc-java-demo create-large-dataproc-cluster create-small-dataproc-cluster list-dataproc-clusters submit-dataproc-java-job submit-dataproc-python-job list-dataproc-jobs

default:  submit-dataproc-java-job

submit-dataproc-python-job: create-large-dataproc-cluster
	gcloud dataproc jobs submit pyspark gs://$(BUCKET)/international_loans_dataproc_large.py --region $(REGION) --cluster $(CLUSTER2_NAME) --async

list-dataproc-jobs:
	gcloud dataproc jobs list --region $(REGION)

submit-dataproc-java-job: submit-dataproc-python-job
	gcloud dataproc jobs submit spark --region $(REGION) --cluster $(CLUSTER2_NAME) --class org.example.dataproc.InternationalLoansAppDataprocLarge --jars gs://$(BUCKET)/dataprocJavaDemo-1.0-SNAPSHOT.jar --async

list-dataproc-clusters: 
	gcloud dataproc clusters list --region $(REGION)

create-small-dataproc-cluster: install-dataproc-java-demo
	gcloud dataproc clusters create $(CLUSTER1_NAME) --region $(REGION) --zone $(ZONE) --single-node --master-machine-type n1-standard-1 --master-boot-disk-size 500 --image-version 1.3-deb9 --project $(PROJECT_ID)

create-large-dataproc-cluster: create-small-dataproc-cluster
	gcloud dataproc clusters create $(CLUSTER2_NAME) --region $(REGION) --zone $(ZONE) --num-workers 2 --worker-machine-type n1-standard-4  --master-machine-type n1-standard-4 --master-boot-disk-size 500 --image-version 1.3-deb9 --project $(PROJECT_ID)

replace-bucket-name: 
	sed -i "s/XXXbucket/$(BUCKET)/g" dataproc-java-demo/src/main/java/org/example/dataproc/InternationalLoansAppDataprocLarge.java
	sed -i "s/XXXbucket/$(BUCKET)/g" dataproc-java-demo/src/main/java/org/example/dataproc/InternationalLoansAppDataprocSmall.java
	sed -i "s/XXXbucket/$(BUCKET)/g" dataproc-python-demo/international_loans_dataproc_large.py

install-dataproc-java-demo: install-dataproc-python-demo
	cd dataproc-java-demo; gradle build --console plain
	cp build/libs/dataprocJavaDemo-1.0-SNAPSHOT.jar gs://$(BUCKET)

install-dataproc-python-demo: install-kaggle-data
	cp dataproc-python-demo/international_loans_dataproc_large.py gs://$(BUCKET)

install-kaggle-data: replace-bucket-name
	gzip -d kaggle-data/*.gz
	cp kaggle-data/* gs://$(BUCKET)
