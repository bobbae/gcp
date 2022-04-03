# PROJECT_ID
# MEMBER_INFO     user:bob.bae@sada.com    group:admins@example.com    serviceAccount:test123@example.domain.com
gcloud projects add-iam-policy-binding acto-su-1 \
    --member=user:bob.bae@sada.com \
    --role=roles/iap.tunnelResourceAccessor
