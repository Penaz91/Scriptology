def splithalfh(inputfilename):
    from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
    from tempfile import mkdtemp
    from os.path import join, isfile, splitext
    from os import listdir
    output = PdfFileWriter()
    input1 = PdfFileReader(open(inputfilename+".pdf", "rb"))
    count = 0
    numpg = input1.getNumPages()
    tempdir = mkdtemp()
# codice per lo splitting
# ricavo la pagina
    for i in range(0, numpg):
        pg = input1.getPage(i)
        # Prima Pagina (alto)
        pg.mediaBox.setLowerRight((595, 421))
        outputstream = open(tempdir + "/" + str(count)+".pdf", "wb")
        output.addPage(pg)
        output.write(outputstream)
        pg.mediaBox.setLowerRight((595, 0))
        outputstream.close()
        del output, outputstream
        count += 1
        # Reset Dell'output
        output = PdfFileWriter()
        # Seconda Pagina (Basso)
        pg.mediaBox.setUpperRight((595, 421))
        outputstream = open(tempdir + "/" + str(count)+".pdf", "wb")
        output.addPage(pg)
        output.write(outputstream)
        outputstream.close()
        pg.mediaBox.setUpperRight((595, 842))
        count += 1
        del output, outputstream
        # Reset Dell'output
        output = PdfFileWriter()

# Giunzione delle pagine
    filelist = [splitext(file)[0] for file in listdir(tempdir) if isfile(join(tempdir, file))]
    filelist.sort(key=int)

    output = PdfFileMerger()
    for file in filelist:
        input = open(join(tempdir, file + ".pdf"), "rb")
        output.append(input)

    os = open(inputfilename+"_splitted.pdf", "wb")
    output.write(os)
    os.close()
