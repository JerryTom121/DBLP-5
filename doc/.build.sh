NAME=report

files=( "aux" "bbl" "blg" "fdb_latexmk" "fls" "log" "synctex.gz" "pdf" "dvi" )

for file in "${files[@]}"
do
    find . -name "*.$file" -exec rm -rf '{}' \;
done

pdflatex ${NAME}.tex
bibtex ${NAME}
pdflatex ${NAME}.tex
pdflatex ${NAME}.tex
