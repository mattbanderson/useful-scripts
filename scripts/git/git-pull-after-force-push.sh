#!/bin/sh

git stash
git pull # quit/exit merge commit message
git reset --hard origin/develop # or other branch
git stash pop