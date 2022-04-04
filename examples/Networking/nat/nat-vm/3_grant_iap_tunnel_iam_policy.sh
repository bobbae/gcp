# PROJECT_ID
# MEMBER_INFO     user:username@example.com    group:admins@example.com    serviceAccount:test123@example.domain.com
gcloud projects add-iam-policy-binding my-project-1 \
    --member=user:bob@example.com \
    --role=roles/iap.tunnelResourceAccessor
