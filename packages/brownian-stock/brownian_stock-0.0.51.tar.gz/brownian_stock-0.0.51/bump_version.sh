
if git show-ref --quiet refs/heads/release_branch; then
    git branch -d "release_branch"
    echo "Delete release_branch"
fi

# Create new release branch and push
echo "Create new release_branch"
BRANCH_NAME="release_branch_$(date +"%Y%m%d-%H%M%S")"
git stash
git fetch
git checkout -b $BRANCH_NAME "main"
rye run bumpversion patch
git push -u origin $BRANCH_NAME

# Create PR
gh pr create \
    --title "release: $(date +"%Y%m%d")"\
    --body "release pr on $(date +"%Y%m%d")"\
    --base main\
    --head $BRANCH_NAME\


# Post processing
git switch "main"
echo "Done"