#build the html files from the source folder
make html
#sync the build folder and the docs folder for github page
rsync -av --delete build/html/ docs/