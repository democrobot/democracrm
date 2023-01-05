# Documentation

## Best Practices

https://diataxis.fr/how-to-use-diataxis/

## Building The Docs

From the DemocraCRM repo, assuming the docs website repo is in the same root directory, run: 

    mkdocs build -d ../democracrm.github.io/
    cd ../democracrm.github.io/
    git add .
    git commit - "Updated docs"
    git push
