#!/usr/bin/env bash

set -eou pipefail

remote_repo=${REMOTE_REPO?Variable REMOTE_REPO is required}
docker_username=${DOCKER_USERNAME?Variable DOCKER_USERNAME is required}
docker_password=${DOCKER_PASSWORD?Variable DOCKER_PASSWORD is required}
git_tag=$GITHUB_REF_NAME
model_name="all-MiniLM-L6-v2"

function main() {
  init
  echo "git ref type is: $GITHUB_REF_TYPE"
  echo "git tag is: $git_tag"
  push_tag
}

function init() {
  docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
  docker buildx create --use
  echo "$docker_password" | docker login -u "$docker_username" --password-stdin
}

function push_tag() {
  if [ ! -z "$git_tag" ] && [ "$GITHUB_REF_TYPE" == "tag" ]; then
    tag_git="$remote_repo:$model_name-$git_tag"
    tag_latest="$remote_repo:$model_name-latest"
    tag="$remote_repo:$model_name"

    echo "Tag & Push $tag, $tag_latest, $tag_git"

    echo "Build linux/amd64 docker image"
    docker buildx build --platform=linux/amd64 \
      --push \
      --tag "$tag_git" \
      --tag "$tag_latest" \
      --tag "$tag" \
      .

    echo "Build windows/amd64 docker image"
    docker buildx build --platform=windows/amd64 -f windows.Dockerfile \
      --push \
      --tag "$tag_git" \
      --tag "$tag_latest" \
      --tag "$tag" \
      .
  fi
}

main "${@}"
