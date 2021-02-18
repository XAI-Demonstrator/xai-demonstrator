#!/usr/bin/env bash

GCP_PROJECT="${1}"
IMAGE="${2}"
KEEP="${3}"

FULL_PATH="gcr.io/${GCP_PROJECT}/${IMAGE}"

echo "## Current container images in ${FULL_PATH}"
gcloud container images list-tags "${FULL_PATH}" --sort-by=TIMESTAMP

ALL_DIGESTS=$(gcloud container images list-tags "${FULL_PATH}" --sort-by=TIMESTAMP --format="get(digest)")

echo "There are $(echo "${ALL_DIGESTS}" | wc -l) images in total."

if [ "$(echo "${ALL_DIGESTS}" | wc -l)" -le "${KEEP}" ]; then
  echo "That's fewer than or equal to the ${KEEP} images we intend to keep. Exiting."
  exit 0
fi

TO_DELETE=$(echo "${ALL_DIGESTS}" | head -n -"${KEEP}")

echo "We want to keep ${KEEP}."
echo "Thus, we're going to delete the $(echo "${TO_DELETE}" | wc -l) oldest image(s)."

COUNTER=0

for digest in ${TO_DELETE}; do
  (
    set -x
    gcloud container images delete -q --force-delete-tags "${FULL_PATH}@$(echo "${digest}" | xargs)"
  )
  ((COUNTER++))
done

echo "We have deleted ${COUNTER} image(s)."
