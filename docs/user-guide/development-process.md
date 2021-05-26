# Development process 

This is a short guide to push locally developed code to the GitHub repository. 

## Pull the current master branch 

Switch to master:

```
git branch master
```

Pull master branch 

```
git pull 
```

## Create new branch 

Create a branch named new-branch 

```
git branch new-branch 
```

## Switch to the new branch 

```
git switch new-branch 
```

## Check the changes 

```
git status
```

## Add file 

Add file which is located under path-to-file

```
git add path-to-file/file 
```

OR add all changes with:

```
git add .
```

## Now commit the changes 

Commit the changes and add a short message, which explains your changes. 

```
git commit -m "message"
```

## Push to Github 

```
git push 
```