include config.mk

.PHONY :
default:

.PHONY :
do-everything: 
	make replace-bucket-name
	make install-kaggle-data
	make install-dataproc-python-demo
	make install-dataproc-java-demo
	make create-large-dataproc-cluster
	make create-small-dataproc-cluster
	make list-dataproc-clusters
	make submit-dataproc-java-job
	make submit-dataproc-python-job
	make list-dataproc-jobs

.PHONY :
submit-dataproc-python-job:
	gcloud dataproc jobs submit pyspark gs://$(BUCKET)/international_loans_dataproc_large.py --region $(REGION) --cluster $(CLUSTER2_NAME) --async

.PHONY :
list-dataproc-jobs:
	gcloud dataproc jobs list --region $(REGION)

.PHONY :
submit-dataproc-java-job:
	gcloud dataproc jobs submit spark --region $(REGION) --cluster $(CLUSTER2_NAME) --class org.example.dataproc.InternationalLoansAppDataprocLarge --jars gs://$(BUCKET)/dataprocJavaDemo-1.0-SNAPSHOT.jar --async

.PHONY : 
list-dataproc-clusters:
	gcloud dataproc clusters list --region $(REGION)

.PHONY : 
create-small-dataproc-cluster:
	gcloud dataproc clusters create $(CLUSTER1_NAME) --region $(REGION) --zone $(ZONE) --single-node --master-machine-type n1-standard-1 --master-boot-disk-size 500 --image-version 1.3-deb9 --project $(PROJECT_ID)

.PHONY : 
create-large-dataproc-cluster:
	gcloud dataproc clusters create $(CLUSTER2_NAME) --region $(REGION) --zone $(ZONE) --num-workers 2 --worker-machine-type n1-standard-4  --master-machine-type n1-standard-4 --master-boot-disk-size 500 --image-version 1.3-deb9 --project $(PROJECT_ID)

.PHONY : replace-bucket-name
replace-bucket-name:
	@echo config.mk should have proper variables, not XXX
	sed -i "s/XXXbucket/$(BUCKET)/g" dataproc-java-demo/src/main/java/org/example/dataproc/InternationalLoansAppDataprocLarge.java
	sed -i "s/XXXbucket/$(BUCKET)/g" dataproc-java-demo/src/main/java/org/example/dataproc/InternationalLoansAppDataprocSmall.java
	sed -i "s/XXXbucket/$(BUCKET)/g" dataproc-python-demo/international_loans_dataproc_large.py

.PHONY : install-dataproc-java-demo
install-dataproc-java-demo:
	cd dataproc-java-demo; gradle build --console plain
	cp build/libs/dataprocJavaDemo-1.0-SNAPSHOT.jar gs://$(BUCKET)

.PHONY : install-dataproc-python-demo
install-dataproc-python-demo:
	cp dataproc-python-demo/international_loans_dataproc_large.py gs://$(BUCKET)

.PHONY : install-kaggle-data
install-kaggle-data:
	gzip -d kaggle-data/*.gz
	cp kaggle-data/* gs://$(BUCKET)
